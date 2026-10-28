import argparse
import csv
import json  # [PHASE2]
import math
import statistics
import time
from collections import defaultdict, deque

import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX

LEVELS = [
    (0.33, "LOW", (0, 200, 0)),
    (0.66, "MEDIUM", (0, 215, 255)),
    (1.0, "HIGH", (0, 120, 255)),
    (float("inf"), "CRITICAL", (0, 0, 255)),
]


def risk_level(peak, sat):
    ratio = peak / sat
    for limit, name, color in LEVELS:
        if ratio < limit:
            return name, color


def density_map(people, shape, alpha, scale=4):
    h, w = shape
    sh, sw = max(h // scale, 1), max(w // scale, 1)
    grid = np.zeros((sh, sw), np.float32)
    for cx, cy, bh in people:
        s = max(alpha * bh / scale, 1.0)
        r = int(3 * s)
        gx, gy = cx / scale, cy / scale
        x0, x1 = max(int(gx) - r, 0), min(int(gx) + r + 1, sw)
        y0, y1 = max(int(gy) - r, 0), min(int(gy) + r + 1, sh)
        if x0 >= x1 or y0 >= y1:
            continue
        xs = np.arange(x0, x1) - gx
        ys = np.arange(y0, y1) - gy
        grid[y0:y1, x0:x1] += np.exp(-(xs[None, :] ** 2 + ys[:, None] ** 2) / (2 * s * s))
    return cv2.resize(grid, (w, h), interpolation=cv2.INTER_LINEAR)


def overlay_heatmap(frame, density, sat, alpha=0.55):
    norm = np.clip(density / sat, 0, 1)
    color = cv2.applyColorMap((norm * 255).astype(np.uint8), cv2.COLORMAP_JET)
    blended = cv2.addWeighted(frame, 1 - alpha, color, alpha, 0)
    mask = (norm > 0.08)[..., None]
    return np.where(mask, blended, frame)


def draw_hud(frame, count, total, peak, fps, sat, k, med_speed, capacity=None):
    name, color = risk_level(peak, sat)
    t = max(int(k), 1)
    speed_text = "--" if med_speed is None else f"{med_speed:.2f} bh/s"
    cv2.rectangle(frame, (int(10 * k), int(10 * k)), (int(300 * k), int(150 * k)), (0, 0, 0), -1)
    cv2.rectangle(frame, (int(10 * k), int(10 * k)), (int(300 * k), int(150 * k)), color, t + 1)
    cap_txt = f"/{capacity}" if capacity is not None else ""
    lines = [
        (f"People now: {count}{cap_txt}", 0.65, (255, 255, 255), 2),
        (f"Total IDs seen: {total}", 0.55, (200, 200, 200), 1),
        (f"Peak density: {peak:.1f}", 0.55, (200, 200, 200), 1),
        (f"Median speed: {speed_text}", 0.55, (200, 200, 200), 1),
        (f"Risk: {name}", 0.65, color, 2),
    ]
    y = 38
    for text, size, col, th in lines:
        cv2.putText(frame, text, (int(20 * k), int(y * k)), FONT, size * k, col, th * t)
        y += 24
    cv2.putText(frame, f"{fps:.1f} FPS", (frame.shape[1] - int(120 * k), int(28 * k)), FONT, 0.6 * k, (255, 255, 255), 2 * t)


def draw_alerts(frame, active, k, blink):
    if not active:
        return
    h, w = frame.shape[:2]
    t = max(int(k), 1)
    if blink:
        cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 0, 255), 6 * t)
    bar = int(44 * k)
    cv2.rectangle(frame, (0, h - bar), (w, h), (0, 0, 160), -1)
    cv2.putText(frame, "ALERT: " + " | ".join(active), (int(20 * k), h - int(14 * k)), FONT, 0.8 * k, (255, 255, 255), 2 * t)


def draw_capacity_breach(frame, count, capacity, k):
    if count <= capacity:
        return
    h, w = frame.shape[:2]
    t = max(int(k), 1)
    cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 0, 255), 12 * t)
    
    # Scale down font size if text does not fit within narrow frames
    font_scale = 1.4 * k
    text = f"CAPACITY EXCEEDED  {count}/{capacity}"
    (tw, th), _ = cv2.getTextSize(text, FONT, font_scale, 4 * t)
    if tw > w - 40:
        font_scale = 1.0 * k
        (tw, th), _ = cv2.getTextSize(text, FONT, font_scale, 4 * t)
    if tw > w - 40:
        font_scale = 0.8 * k
        (tw, th), _ = cv2.getTextSize(text, FONT, font_scale, 4 * t)

    x = max((w - tw) // 2, 10)
    y = min(max(h // 2, th + 40), h - 30)
    x2 = min(x + tw + 20, w - 5)
    y2 = min(y + 20, h - 5)
    
    cv2.rectangle(frame, (max(x - 20, 0), max(y - th - 20, 0)), (x2, y2), (0, 0, 160), -1)
    cv2.putText(frame, text, (x, y), FONT, font_scale, (255, 255, 255), 4 * t)


def track_speed(trail, fps, gap=5):
    if len(trail) <= gap:
        return None
    p_now = trail[-1]
    p_old = trail[-1 - gap]
    d = math.dist(p_now, p_old)
    return d * fps / gap


class Alert:
    def __init__(self, name, frames):
        self.name = name
        self.frames = max(int(frames), 1)
        self.on = False
        self.streak = 0

    def update(self, cond):
        if cond == self.on:
            self.streak = 0
            return False
        self.streak += 1
        if self.streak >= self.frames:
            self.on = cond
            self.streak = 0
            return True
        return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="0")
    p.add_argument("--model", default="yolov8m.pt")
    p.add_argument("--out", default="crowd_output.mp4")
    p.add_argument("--conf", type=float, default=0.15)
    p.add_argument("--imgsz", type=int, default=1280)
    p.add_argument("--alpha", type=float, default=0.35)
    p.add_argument("--sat", type=float, default=4.0)
    p.add_argument("--trail", type=int, default=30)
    p.add_argument("--gap", type=int, default=8)
    p.add_argument("--anchor", choices=["center", "foot"], default="center")
    p.add_argument("--speed-unit", choices=["bh", "px"], default="bh")
    p.add_argument("--density-alert", type=float, default=0.66)
    p.add_argument("--hot", type=float, default=0.5)
    p.add_argument("--min-hot", type=int, default=4)
    p.add_argument("--stall", type=float, default=0.15)
    p.add_argument("--run", type=float, default=1.5)
    p.add_argument("--alert-secs", type=float, default=1.0)
    p.add_argument("--alert-log", default="alerts.csv")
    p.add_argument("--capacity", type=int, default=500,
                   help="Venue max occupancy; alert fires when count exceeds this")
    p.add_argument("--capacity-log", default="capacity_alerts.csv",
                   help="CSV log for capacity-limit violations")
    p.add_argument("--trails", action="store_true")
    p.add_argument("--no-show", action="store_true")
    p.add_argument("--progress-file", default=None, help="Path to write progress JSON")  # [PHASE2]
    p.add_argument("--summary", default=None, help="Path to write summary JSON")  # [PHASE2]
    args = p.parse_args()

    from ultralytics import YOLO

    model = YOLO(args.model)
    src = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise SystemExit(f"Cannot open source: {args.source}")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 25
    writer = cv2.VideoWriter(args.out, cv2.VideoWriter_fourcc(*"mp4v"), src_fps, (w, h))

    k = max(w / 960, 1.0)
    t = max(int(k), 1)
    history = defaultdict(lambda: deque(maxlen=max(args.trail, args.gap + 2)))
    last_seen = {}
    seen_ids = set()
    frame_no = 0
    fps = 0.0
    peak_s = 0.0
    persist = args.alert_secs * src_fps
    alerts = {name: Alert(name, persist) for name in
              ("HIGH DENSITY", "CROWD STALLED", "RUNNING", "OVER CAPACITY")}
    events = []
    cap_breach_events = []
    blink_period = max(int(src_fps / 2), 1)
    below_capacity_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0  # [PHASE2]
    max_people_count = 0  # [PHASE2]
    max_peak_s = 0.0  # [PHASE2]
    all_median_speeds = []  # [PHASE2]
    highest_risk_rank = 0  # [PHASE2]
    risk_rank_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}  # [PHASE2]
    highest_risk_name = "LOW"  # [PHASE2]

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t0 = time.time()
        frame_no += 1

        res = model.track(
            frame,
            persist=True,
            classes=[0],
            conf=args.conf,
            imgsz=args.imgsz,
            tracker="bytetrack.yaml",
            verbose=False,
        )[0]

        people, boxes_out = [], []
        boxes = res.boxes
        if boxes is not None and len(boxes):
            xyxy = boxes.xyxy.cpu().numpy()
            ids = boxes.id.int().cpu().tolist() if boxes.id is not None else [None] * len(xyxy)
            for (x1, y1, x2, y2), tid in zip(xyxy, ids):
                cx = (x1 + x2) / 2
                cy = y2 if args.anchor == "foot" else (y1 + y2) / 2
                people.append((cx, cy, y2 - y1))
                boxes_out.append((int(x1), int(y1), int(x2), int(y2), tid))
                if tid is not None:
                    history[tid].append((int(cx), int(cy)))
                    last_seen[tid] = frame_no
                    seen_ids.add(tid)

        for tid in [i for i, f in last_seen.items() if frame_no - f > 60]:
            history.pop(tid, None)
            last_seen.pop(tid, None)

        density = density_map(people, (h, w), args.alpha)
        peak = float(density.max()) if people else 0.0
        peak_s = peak if frame_no == 1 else 0.8 * peak_s + 0.2 * peak
        out = overlay_heatmap(frame, density, args.sat)

        # [PHASE2] Track metrics for summary
        if len(people) > max_people_count:  # [PHASE2]
            max_people_count = len(people)  # [PHASE2]
        if peak_s > max_peak_s:  # [PHASE2]
            max_peak_s = peak_s  # [PHASE2]
        current_risk_name, _ = risk_level(peak_s, args.sat)  # [PHASE2]
        if risk_rank_map.get(current_risk_name, 0) > highest_risk_rank:  # [PHASE2]
            highest_risk_rank = risk_rank_map.get(current_risk_name, 0)  # [PHASE2]
            highest_risk_name = current_risk_name  # [PHASE2]

        speeds, hot_speeds = [], []
        for i, (x1, y1, x2, y2, tid) in enumerate(boxes_out):
            cx, cy, bh = people[i]
            cv2.rectangle(out, (x1, y1), (x2, y2), (255, 255, 255), t)
            if tid is None:
                continue
            speed_px = track_speed(history[tid], src_fps, args.gap)
            if speed_px is None:
                continue
            spd = speed_px / max(bh, 1)
            gx = min(max(int(cx), 0), w - 1)
            gy = min(max(int(cy), 0), h - 1)
            speeds.append(spd)
            if density[gy, gx] >= args.hot * args.sat:
                hot_speeds.append(spd)
            label = f"{spd:.1f}" if args.speed_unit == "bh" else f"{speed_px:.0f}"
            cv2.putText(out, label, (x1, max(y1 - 5, int(14 * k))), FONT, 0.5 * k, (0, 255, 255), t)

        med = statistics.median(speeds) if len(speeds) >= 3 else None
        if med is not None:  # [PHASE2]
            all_median_speeds.append(med)  # [PHASE2]
        hot_med = statistics.median(hot_speeds) if len(hot_speeds) >= args.min_hot else None

        current_count = len(people)
        over_capacity = current_count > args.capacity

        if over_capacity:
            below_capacity_count = 0
        else:
            below_capacity_count += 1

        conds = {
            "HIGH DENSITY": peak_s >= args.density_alert * args.sat,
            "CROWD STALLED": hot_med is not None and hot_med < args.stall,
            "RUNNING": med is not None and med > args.run,
            "OVER CAPACITY": over_capacity,
        }
        for name, cond in conds.items():
            if name == "OVER CAPACITY":
                continue  # handled with custom debounce logic below
            a = alerts[name]
            if a.update(cond):
                state = "START" if a.on else "END"
                t_sec = frame_no / src_fps
                print(f"[{t_sec:6.2f}s] {name}: {state}")
                events.append((round(t_sec, 2), name, state, round(peak_s, 2), len(hot_speeds), None if med is None else round(med, 2)))

        cap_alert = alerts["OVER CAPACITY"]
        if over_capacity and not cap_alert.on:
            cap_alert.on = True
            cap_alert.streak = 0
            t_sec = frame_no / src_fps
            msg = (f"OVER CAPACITY: {current_count}/{args.capacity} "
                   f"(limit exceeded by {current_count - args.capacity})")
            print(f"[{t_sec:6.2f}s] {msg}")
            events.append((round(t_sec, 2), "OVER CAPACITY", "START", round(peak_s, 2),
                           current_count, None if med is None else round(med, 2)))
            cap_breach_events.append((round(t_sec, 2), msg, "START", current_count, args.capacity))
        elif cap_alert.on and below_capacity_count >= max(int(1.0 * src_fps), 5):
            cap_alert.on = False
            cap_alert.streak = 0
            t_sec = frame_no / src_fps
            msg = f"OVER CAPACITY cleared (now {current_count}/{args.capacity})"
            print(f"[{t_sec:6.2f}s] {msg}")
            events.append((round(t_sec, 2), "OVER CAPACITY", "END", round(peak_s, 2),
                           current_count, None if med is None else round(med, 2)))
            cap_breach_events.append((round(t_sec, 2), msg, "END", current_count, args.capacity))

        for trail in history.values() if args.trails else []:
            if len(trail) > 1:
                cv2.polylines(out, [np.array(trail, np.int32)], False, (255, 255, 0), t)

        dt = time.time() - t0
        fps = 0.9 * fps + 0.1 / dt if fps else 1 / dt
        draw_hud(out, len(people), len(seen_ids), peak_s, fps, args.sat, k, med, args.capacity)
        active = [n for n, a in alerts.items() if a.on]
        draw_alerts(out, active, k, (frame_no // blink_period) % 2 == 0)
        draw_capacity_breach(out, len(people), args.capacity, k)

        # [PHASE2] Periodic progress update to file
        if args.progress_file and (frame_no % 10 == 0 or frame_no == 1):
            try:
                with open(args.progress_file, "w") as pf:
                    json.dump({"frame": frame_no, "total": total_frames, "fps": round(fps, 1)}, pf)
            except Exception:
                pass

        writer.write(out)
        if not args.no_show:
            cv2.imshow("Crowd Density", out)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    writer.release()
    if not args.no_show:
        cv2.destroyAllWindows()

    with open(args.alert_log, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["time_s", "alert", "state", "peak_density", "hotspot_people", "median_speed_bh"])
        wr.writerows(events)
    print(f"Saved: {args.out}")
    print(f"Alert events: {len(events)} -> {args.alert_log}")

    with open(args.capacity_log, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["time_s", "event", "state", "people_count", "capacity"])
        wr.writerows(cap_breach_events)
    print(f"Capacity log: {args.capacity_log}")

    # [PHASE2] Final progress update (complete)
    if args.progress_file:
        try:
            with open(args.progress_file, "w") as pf:
                json.dump({"frame": frame_no, "total": total_frames or frame_no, "fps": round(fps, 1)}, pf)
        except Exception:
            pass

    # [PHASE2] Summary metrics export
    if args.summary:
        overall_med_speed = round(statistics.median(all_median_speeds), 2) if all_median_speeds else None
        summary_data = {
            "max_people": max_people_count,
            "peak_density": round(max_peak_s, 2),
            "median_speed": overall_med_speed,
            "risk_level": highest_risk_name,
            "total_ids": len(seen_ids),
        }
        with open(args.summary, "w") as sf:
            json.dump(summary_data, sf, indent=2)
        print(f"Summary saved: {args.summary}")


if __name__ == "__main__":
    main()
# Neural Topology Mapping for Early-Stage Crowd Surge and Compression Mitigation
### Real-Time Edge CCTV Telemetry, Spatial Density Estimation & Autonomous Alerting (Phase 2)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![YOLOv8](https://img.shields.io/badge/Computer%20Vision-YOLOv8m-00FFFF.svg?style=flat&logo=yolo)](https://github.com/ultralytics/ultralytics)
[![ByteTrack](https://img.shields.io/badge/Tracking-ByteTrack-orange.svg?style=flat)](https://github.com/ifzhang/ByteTrack)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57.svg?style=flat&logo=sqlite)](https://www.sqlite.org/)
[![Cloudflare](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick%20Tunnel-F38020.svg?style=flat&logo=cloudflare)](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
[![License](https://img.shields.io/badge/License-Academic%20Evaluation-lightgrey.svg?style=flat)](#)

---

## 1. Executive Summary & Problem Formulation

In high-density gatherings—such as transit hubs, religious pilgrimages, concerts, and stadium exits—crowd disasters (e.g., Itaewon 2022, Mina 2015, Hillsborough 1989) are rarely caused by wild trampling. Instead, they result from **compressive asphyxiation** caused by crowd turbulence and shockwaves propagating through physical density bottlenecks.

Traditional CCTV surveillance fails to prevent these catastrophes because:
1. **Simple Headcounting is Insufficient:** 100 people spread across a football pitch is completely safe; 100 people jammed into an 8-meter corridor represents an imminent lethal crush hazard.
2. **Perspective Foreshortening:** In standard monocular CCTV cameras, people closer to the lens appear large and fast in raw pixel measurements, while people further back appear tiny and artificially slow.
3. **Late Anomaly Detection:** By the time a crowd falls, shockwaves have already compressed victims with pressures exceeding 4,000 Newtons (~900 lbs).

**Our Solution:** 
**Neural Topology Mapping** is an end-to-end computer-vision telemetry platform that transforms ordinary monocular CCTV video feeds into real-time spatial density topology maps and velocity vectors. By combining deep-learning pedestrian detection (**YOLOv8**), multi-object trajectory association (**ByteTrack**), adaptive Gaussian spatial kernel smoothing, and perspective-normalized velocity tracking (**Body Heights per Second - `bh/s`**), the system detects early markers of crowd turbulence and stagnation up to tens of seconds before dangerous physical compression occurs.

---

## 2. End-to-End System Architecture

The project is structured as a decoupled, multi-tier edge architecture connecting an asynchronous **FastAPI** web server, a high-performance **OpenCV/YOLOv8** computer vision pipeline, an **SQLite** audit trail database, and an institutional dashboard frontend:

```
┌────────────────────────────────────────────────────────────────────────┐
│             WEB DASHBOARD FRONTEND (Mocha Light & Cream UI)             │
│  - Chunked Video Upload & Native HTML5 H.264 Playback                  │
│  - In-Monitor Progress Overlay (SHA-256 Check -> Detection -> Encode)  │
│  - Live Telemetry HUD: Peak Count, Spatial Density, Flow Velocity (bh/s)│
│  - Chronological Incident Queue & Evidentiary Archive Log              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST API (Port 8000)
┌───────────────────────────────────▼────────────────────────────────────┐
│                  FASTAPI APPLICATION SERVER (server.py)                │
│  - Single-Origin Static Asset Delivery                                 │
│  - SHA-256 Payload Hash Caching (Instant Zero-Compute Presentation)    │
│  - Thread-Safe FIFO Queue Worker (Non-blocking Subprocess Execution)   │
│  - Bundled imageio-ffmpeg Transcoder (H.264 Baseline, +faststart)     │
│  - RFC 7233 HTTP 206 Partial Content Range Streaming                   │
└─────────────────────┬───────────────────────────────┬──────────────────┘
                      │                               │
         (Inference / Evaluation)          (Persistence / Audit)
                      ▼                               ▼
┌──────────────────────────────────────────┐   ┌─────────────────────────┐
│     COMPUTER VISION ENGINE               │   │      SQLITE3 DATABASE   │
│     (crowd_density.py)                   │   │      (data/crowd.db)    │
│  - YOLOv8m Person Detection (Class 0)    │   │  - Table: jobs          │
│  - ByteTrack Trajectory Association      │   │  - Table: alert_events  │
│  - Adaptive 2D Gaussian Kernel Topology  │   │  - Index: SHA-256 Cache │
│  - Normalized Velocity Tracking (bh/s)   │   └─────────────────────────┘
│  - Dual Debounced Alert State Machine    │
└──────────────────────────────────────────┘
```

---

## 3. Database Architecture, Schema & ER Model

### 3.1 Database Location & Storage Engine
- **Engine:** SQLite 3 (ACID compliant, zero-configuration, serverless single-file database).
- **Physical Path:** [`data/crowd.db`](file:///c:/Users/USER/OneDrive/Desktop/MINI/data/crowd.db) (created automatically on server startup).
- **Concurrency & Locking:** Python `threading.Lock()` serializes database writes across the background worker and HTTP request handlers.

### 3.2 SQL Schema Definition (DDL)

```sql
-- Table: jobs
-- Stores top-level analysis runs, hardware execution telemetry, and summary statistics.
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    filename TEXT,
    sha256 TEXT,
    status TEXT,
    created_at TEXT,
    finished_at TEXT,
    max_people INTEGER,
    peak_density REAL,
    median_speed REAL,
    risk_level TEXT,
    model TEXT,
    device TEXT,
    mock INTEGER DEFAULT 0
);

-- Index for instant sub-millisecond cache lookups by video payload hash
CREATE INDEX IF NOT EXISTS idx_jobs_sha256 ON jobs (sha256);

-- Table: alert_events
-- Chronological event log of crowd anomalies detected during video analysis.
CREATE TABLE IF NOT EXISTS alert_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT,
    time_s REAL,
    alert TEXT,
    state TEXT,
    peak_density REAL,
    hotspot_people INTEGER,
    median_speed_bh REAL,
    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE
);
```

### 3.3 Entity-Relationship (ER) Diagram
<div align="center">

<table>
  <tr>
    <td align="center" style="border: 2px solid black; padding: 10px;">
      <img
        width="800"
        alt="ER Diagram"
        src="https://github.com/user-attachments/assets/fb9fb0ec-8458-41e2-b9a7-808c9c21a9fd"
      />
      <br/>
      <strong>ER Diagram</strong>
    </td>
  </tr>
</table>

</div>

### 3.4 Column Field Breakdown

| Table | Column | Type | Constraints | Description |
|---|---|---|---|---|
| `jobs` | `id` | `TEXT` | `PRIMARY KEY` | 12-character hex UUID uniquely identifying the analysis run. |
| `jobs` | `filename` | `TEXT` | `NOT NULL` | Sanitized original filename of the ingested CCTV clip. |
| `jobs` | `sha256` | `TEXT` | `INDEXED` | 64-character SHA-256 checksum for instant duplicate detection & caching. |
| `jobs` | `status` | `TEXT` | `NOT NULL` | Lifecycle state: `queued`, `running`, `done`, or `error`. |
| `jobs` | `created_at` | `TEXT` | `NOT NULL` | UTC ISO-8601 timestamp when job was ingested. |
| `jobs` | `finished_at`| `TEXT` | `NULLABLE` | UTC ISO-8601 timestamp when inference & transcoding completed. |
| `jobs` | `max_people` | `INTEGER` | `DEFAULT 0` | Peak instantaneous headcount across all frames. |
| `jobs` | `peak_density`| `REAL` | `DEFAULT 0.0` | Maximum spatial density recorded across the entire video. |
| `jobs` | `median_speed`| `REAL` | `NULLABLE` | Median velocity of tracked individuals in normalized body-heights/second. |
| `jobs` | `risk_level` | `TEXT` | `DEFAULT 'LOW'` | Peak risk classification: `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`. |
| `jobs` | `model` | `TEXT` | `NOT NULL` | Exact neural network weight name used (`yolov8m.pt`). |
| `jobs` | `device` | `TEXT` | `NOT NULL` | Hardware device string (`CUDA:0 (Tesla T4)` or `CPU`). |
| `jobs` | `mock` | `INTEGER` | `DEFAULT 0` | `1` if generated via mock simulation, `0` if real YOLO inference. |
| `alert_events` | `id` | `INTEGER` | `PK AUTOINCREMENT` | Unique event sequence number. |
| `alert_events` | `job_id` | `TEXT` | `FOREIGN KEY` | Foreign key referencing `jobs(id)` with cascading relationship. |
| `alert_events` | `time_s` | `REAL` | `NOT NULL` | Video timeline offset (in seconds) where anomaly began or resolved. |
| `alert_events` | `alert` | `TEXT` | `NOT NULL` | Type of hazard: `HIGH DENSITY`, `CROWD STALLED`, `RUNNING`, or `OVER CAPACITY`. |
| `alert_events` | `state` | `TEXT` | `NOT NULL` | `START` (anomaly entered active condition) or `END` (anomaly resolved). |
| `alert_events` | `peak_density` | `REAL` | `NOT NULL` | Gaussian peak density metric at the moment of the event. |
| `alert_events` | `hotspot_people` | `INTEGER` | `NOT NULL` | Number of detected individuals within the localized high-density cluster. |
| `alert_events` | `median_speed_bh` | `REAL` | `NULLABLE` | Instantaneous median speed of tracked persons in body heights per second. |

---

## 4. Comprehensive File-by-File & Function-by-Function Reference

### 4.1 Server Engine: [`server.py`](file:///c:/Users/USER/OneDrive/Desktop/MINI/server.py)

`server.py` implements the FastAPI web application, handles video file ingestion, manages SQLite persistence, coordinates asynchronous background job execution, and delivers transcoded H.264 streams with byte-range seeking.

| Function / Component | Description |
|---|---|
| `get_db_connection()` | Opens an SQLite connection to `data/crowd.db` with `sqlite3.Row` factory for dict-like column access. |
| `init_db()` | Initializes database schema, creates `jobs` and `alert_events` tables if missing, and builds the `idx_jobs_sha256` index. |
| `compute_sha256(filepath)` | Streams video file in 64 KB chunks to compute SHA-256 fingerprint for deduplication. |
| `db_find_cached_job(sha256)` | Queries SQLite for an existing successful job with identical SHA-256. If present and video file exists, returns cached payload immediately. |
| `db_insert_job(job)` | Writes a newly queued job record to SQLite. |
| `db_update_job_done(job_id, results, model_str, device_str)` | Commits final inference metrics, peak headcount, speed, risk level, and all generated alert events into SQLite upon pipeline completion. |
| `db_update_job_error(job_id, message)` | Updates job status to `error` and records the diagnostic failure trace. |
| `db_get_history(limit=10)` | Retrieves the most recent completed analysis jobs for display in the frontend evidentiary archive table. |
| `cleanup_old_jobs(keep=5)` | Prunes old video artifacts from `outputs/` while preserving the 5 most recent runs to prevent disk exhaustion. |
| `get_ffmpeg_executable()` | Locates FFmpeg binary: checks bundled `imageio_ffmpeg` first, falling back to system PATH. |
| `transcode_to_h264(input_path, output_path)` | Transcodes raw OpenCV `mp4v` output into web-standard H.264 (`yuv420p`) and relocates the MP4 `moov` atom to the front of the file (`+faststart`) to enable instantaneous browser video playback and scrub-seeking. |
| `background_worker()` | Thread daemon continuously polling an in-memory `queue.Queue`. Ensures only one video is processed at a time without blocking the HTTP server. |
| `run_mock_job(job, params)` | Simulation engine: generates synthetic crowd telemetry, heatmaps, and alerts for zero-GPU laptop testing without PyTorch or YOLO installed. |
| `run_real_job(job, params)` | Launches `crowd_density.py` as an isolated subprocess with arguments for source, model, confidence threshold, and IPC JSON paths. Reads real-time progress from `--progress-file`. |
| `GET /api/info` | Returns system metadata, active model (`yolov8m.pt`), compute device (`CUDA:0 (Tesla T4)` or `CPU`), and mock mode flag. |
| `POST /api/upload` | Validates and saves uploaded video file, computes SHA-256, checks cache, and enqueues job into background worker. |
| `POST /api/sample` | One-click demonstration endpoint: copies bundled `test.mp4` to uploads and queues it for analysis. |
| `GET /api/jobs/{job_id}` | Polling endpoint returning job status (`queued`, `running`, `done`, `error`), processed frame count, total frames, and ETA. |
| `GET /api/jobs/{job_id}/video` | Streams H.264 processed video with full RFC 7233 HTTP 206 Partial Content Range support for timeline scrubbing. |
| `GET /api/jobs/{job_id}/results` | Returns final diagnostic metrics, peak density, median speed, and chronological alert list. |
| `GET /api/jobs/{job_id}/alerts.csv`| Generates and downloads evidentiary CSV containing all timestamped alert transitions. |
| `GET /api/history` | Fetches historical runs from SQLite. |
| `GET /` | Serves the single-page application dashboard (`static/index.html`). |

---

### 4.2 Computer Vision Engine: [`crowd_density.py`](file:///c:/Users/USER/OneDrive/Desktop/MINI/crowd_density.py)

`crowd_density.py` is the core computer-vision analytics pipeline. It executes YOLOv8 object detection, ByteTrack tracking, Gaussian spatial topology mapping, perspective-invariant velocity calculation, and multi-condition alert debouncing.

| Function / Class | Mathematical / Algorithmic Role |
|---|---|
| `risk_level(peak, sat)` | Computes saturation ratio $R = \frac{\text{peak}}{\text{sat}}$. Categorizes risk level into: `LOW` ($R < 0.33$), `MEDIUM` ($0.33 \le R < 0.66$), `HIGH` ($0.66 \le R < 1.0$), and `CRITICAL` ($R \ge 1.0$). |
| `density_map(people, shape, alpha, scale=4)` | **Spatial Gaussian Density Kernel:** Downsamples grid by `scale=4` for high FPS. For each detected person $(c_x, c_y)$ with bounding-box height $h$, evaluates 2D Gaussian distribution:$$\sigma = \max\left(\frac{\alpha \cdot h}{\text{scale}}, 1.0\right)$$$$G(x,y) = \exp\left(-\frac{(x - g_x)^2 + (y - g_y)^2}{2\sigma^2}\right)$$Upsamples back to frame resolution via bilinear interpolation (`cv2.INTER_LINEAR`). Because $\sigma \propto h$, persons further from the camera naturally contribute tighter, narrower kernels, compensating for perspective scale! |
| `overlay_heatmap(frame, density, sat, alpha=0.55)` | Normalizes density map against saturation threshold: $\text{norm} = \text{clip}\left(\frac{\text{density}}{\text{sat}}, 0, 1\right)$. Maps to 8-bit Jet colormap (`cv2.COLORMAP_JET`), and alpha-blends onto video frame where $\text{norm} > 0.08$. |
| `draw_hud(frame, count, total, peak, fps, sat, k, med_speed, capacity)` | Overlays an on-video Heads-Up Display (HUD) displaying instantaneous headcount, total seen IDs, smoothed peak density index, median speed in `bh/s`, live FPS, and risk badge. |
| `draw_alerts(frame, active, k, blink)` | Renders flashing bottom alert banner if active safety violations exist (`HIGH DENSITY`, `CROWD STALLED`, `RUNNING`). |
| `draw_capacity_breach(frame, count, capacity, k)` | Overlays a bold red venue capacity breach alert if headcount exceeds preset limit ($N > N_{\text{capacity}}$). |
| `track_speed(trail, fps, gap=8)` | Calculates Euclidean pixel displacement of track history over a rolling gap of 8 frames:$$v_{\text{px}} = \frac{\sqrt{(x_{\text{now}} - x_{\text{old}})^2 + (y_{\text{now}} - y_{\text{old}})^2}}{\text{gap}} \cdot \text{FPS}$$ |
| **Speed Normalization (`bh/s`)** | **Perspective Invariance:** Divides raw pixel velocity $v_{\text{px}}$ by bounding box height $h$ (body height):$$v_{\text{normalized}} = \frac{v_{\text{px}}}{\max(h, 1)} \quad [\text{body-heights / second}]$$**Why this matters:** A person walking near the camera might move 80 px/s with a height of 160 px ($0.5\text{ bh/s}$). A person in the background might move 20 px/s with a height of 40 px ($0.5\text{ bh/s}$). In raw pixels, they look 4x different; in `bh/s`, both are recognized as normal walking speed! |
| `class Alert` | **Debounce State Machine:** Maintains rolling streak counters over a persistence window ($T = \text{alert\_secs} \times \text{FPS}$) to eliminate false alarms and rapid flickering. |
| `main()` | CLI entry point: loads YOLOv8, runs ByteTrack inference on each frame, accumulates metrics, updates `--progress-file` every 10 frames, and exports `--summary` and CSV logs on exit. |

---

### 4.3 Google Colab GPU Deployment: [`colab_run.ipynb`](file:///c:/Users/USER/OneDrive/Desktop/MINI/colab_run.ipynb)

A 5-step interactive Jupyter notebook designed for 1-click cloud execution on an NVIDIA Tesla T4 GPU in Google Colab:

- **Step 1 (`!nvidia-smi`):** Verifies hardware accelerator allocation and CUDA compute capability.
- **Step 2 (Clone & Dependencies):** Clones the repository (or pulls latest commits) and installs `requirements.txt`, `ultralytics`, and the `lapx` Linear Assignment Problem solver required by ByteTrack.
- **Step 3 (Background Server with Socket Recovery):** Cleans up port 8000 using `fuser -k 8000/tcp` to prevent `[Errno 98] address already in use`, starts `server.py` as a background process, and polls `/api/info` until the server reports online.
- **Step 4 (Cloudflare Quick Tunnel):** Downloads the official `cloudflared` binary and creates an encrypted HTTPS tunnel (`https://*.trycloudflare.com`) pointing to port 8000. Provides a live public URL to open the dashboard from any browser or smartphone.
- **Step 5 (Telemetry Log Stream):** Executes `!tail -n 40 server.log` to inspect live server output and YOLO inference diagnostics.

---

### 4.4 Web Dashboard Frontend: [`static/index.html`](file:///c:/Users/USER/OneDrive/Desktop/MINI/static/index.html)

The frontend is built with clean semantic HTML5, Vanilla JavaScript, and Tailwind CSS configured in a **Mocha Light & Light Beach Sand Cream** editorial aesthetic (`#faf5eb` canvas, `#2c2420` roasted bean typography, `#8c5338` terracotta accents, with zero gradients).

#### Frontend Architecture & Key JavaScript Functions:
- `bootServerInfo()`: Queries `GET /api/info` on page load to dynamically update the hardware compute badge (`CUDA:0 (Tesla T4)` or `CPU`), model weight badge, and pipeline engine status.
- `setPipelineBusy(busy)`: Toggles button disabled states, input states, and cursor styles to prevent conflicting concurrent submissions.
- `showProcessingUI(stage, percent, message, frameText, etaText, fpsText)`: Controls the in-monitor processing overlay (`#processingPanel`), animating the progress bar and active step indicators.
- `startPolling(jobId)`: Polls `GET /api/jobs/{job_id}` every 1,000 ms to update live progress, processed frame counters, and estimated completion time.
- `uploadVideoFile(file)`: Sends video payload via `XMLHttpRequest` with real-time byte upload progress tracking before entering the inference phase.
- `loadSampleFeed()`: Calls `POST /api/sample` to instantly ingest and analyze the demonstration test video.
- `onJobCompleted(jobId, isCached)`: Handles transition to completion: switches in-monitor view to `<video id="resultVideo">`, loads the transcoded H.264 stream via `GET /api/jobs/{jobId}/video`, fetches metric data, and displays the `CACHED RESULT` badge if SHA-256 matched.
- `fillTelemetryMetrics(results)`: Populates the live telemetry HUD cards:
  - **Peak Headcount:** Maximum simultaneous persons detected.
  - **Peak Spatial Density:** Peak Gaussian saturation index with risk badge (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
  - **Median Flow Velocity:** Crowd movement speed in body heights/sec (`bh/s`).
  - **Compression Hazard Status:** Real-time crowd dynamics evaluation (`SAFE`, `MODERATE`, `SURGE RISK`, `COMPRESSION EMERGENCY`).
  - **Incident Audit Log:** Dynamically renders chronological event cards with timecode, event name, state transition, and severity colors.
- `flushPipeline()`: Resets dashboard state back to idle video input view.
- `fetchHistory()`: Fetches recent runs from `GET /api/history` and renders the SQLite history table with click-to-load playback.

---

## 5. Mathematical Formulations & Scientific Principles

### 5.1 Spatial Gaussian Density Kernel Estimation
Rather than representing people as zero-dimensional points, each individual exerts a spatial physical footprint. For $N$ people at coordinates $(c_{x,i}, c_{y,i})$ with bounding box height $h_i$, the continuous density field $D(x, y)$ is:

$$D(x, y) = \sum_{i=1}^{N} \exp\left( -\frac{(x - c_{x,i})^2 + (y - c_{y,i})^2}{2\sigma_i^2} \right)$$

where the adaptive kernel variance is dynamically scaled by perspective body height:

$$\sigma_i = \alpha \cdot h_i$$

### 5.2 Perspective-Invariant Flow Velocity ($v_{\text{bh}}$)
To eliminate perspective distortion where near subjects appear faster than distant subjects:

$$v_{\text{bh}} = \frac{\|\mathbf{p}_t - \mathbf{p}_{t-\Delta t}\|_2}{\Delta t \cdot h_t} \quad \left[\frac{\text{body heights}}{\text{second}}\right]$$

- **Normal Walking:** $0.3 - 0.8\text{ bh/s}$
- **Stalled / Compression Hazard:** $< 0.15\text{ bh/s}$ (in high-density regions indicates dangerous physical crush/blockage)
- **Running / Panic Surge:** $> 1.5\text{ bh/s}$ (indicates stampede or sudden panic egress)

### 5.3 Exponential Moving Average (EMA) Density Smoothing
To prevent transient frame-to-frame bounding-box jitter from triggering false alarms, the peak density metric is smoothed via an exponential moving average:

$$\bar{S}_t = 0.8 \cdot \bar{S}_{t-1} + 0.2 \cdot \max_{(x,y)} D_t(x, y)$$

---

## 6. How to Run

### Mode A: Google Colab GPU Deployment (Recommended for Presentations)
1. Open Google Colab and upload [`colab_run.ipynb`](file:///c:/Users/USER/OneDrive/Desktop/MINI/colab_run.ipynb).
2. Set runtime accelerator to **GPU** (`Runtime > Change runtime type > T4 GPU`).
3. Run **Steps 1 through 4**.
4. Click the generated **Cloudflare Public Access URL** (`https://*.trycloudflare.com`) to open the live web interface.

### Mode B: Local Mock Mode (Zero-GPU Laptop Development)
Runs the entire web dashboard, SQLite database, and video playback on weak CPUs (e.g., Core i3) without needing PyTorch or YOLO:
```bash
# Windows
run.bat --mock

# Linux / macOS
python server.py --mock
```
Open **`http://localhost:8000`** in any browser.

### Mode C: Local GPU Inference Mode
Runs full YOLOv8m detection and ByteTrack tracking locally:
```bash
# Install GPU dependencies
pip install -r requirements.txt ultralytics lapx

# Launch server
python server.py --port 8000
```
Open **`http://localhost:8000`** in any browser.

---

## 7. REST API Reference

| Method | Endpoint | Request Payload | Response Schema | Description |
|---|---|---|---|---|
| `GET` | `/api/info` | None | `{status, model, device, mock}` | Hardware compute device and active model metadata. |
| `POST` | `/api/upload` | `multipart/form-data` (`video`) | `{job_id, status, cached}` | Ingests video file, checks SHA-256 cache, enqueues job. |
| `POST` | `/api/sample` | None | `{job_id, status, cached}` | Enqueues bundled demonstration video (`test.mp4`). |
| `GET` | `/api/jobs/{id}` | None | `{id, status, progress, frame, total, eta}` | Real-time job execution progress polling. |
| `GET` | `/api/jobs/{id}/video` | `Range: bytes=start-end` | Binary H.264 MP4 Stream | HTTP 206 partial content stream for video scrubbing. |
| `GET` | `/api/jobs/{id}/results`| None | `{job_id, max_people, peak_density, median_speed, risk_level, events}` | Final diagnostic analysis results and alert logs. |
| `GET` | `/api/jobs/{id}/alerts.csv`| None | CSV File Attachment | Downloads evidentiary alert log CSV. |
| `GET` | `/api/history` | None | `[{id, filename, created_at, max_people, peak_density, risk_level}, ...]` | Fetches recent analysis runs from SQLite. |
| `GET` | `/` | None | HTML Document | Delivers the Mocha Light web application. |

---

## 8. Academic Evaluation & Presentation Viva Guide

### Top 5 Viva Questions & Defenses:

1. **Why use Body Heights per Second (`bh/s`) instead of pixels per second (`px/s`)?**
   *Answer:* In standard monocular CCTV cameras without multi-camera calibration or ground-plane homography matrices, pixel speed varies drastically with distance from the lens. By dividing pixel displacement by bounding-box height ($h$), we normalize by the subject's physical scale. A person moving $0.5\text{ bh/s}$ travels half their body height per second regardless of whether they are 5 meters or 50 meters away.

2. **Why YOLOv8 over older architectures like Faster R-CNN or SSD?**
   *Answer:* YOLOv8 uses an anchor-free split head with decoupled classification and regression branches. It achieves high mean Average Precision (mAP) while delivering real-time frame rates (>30 FPS on an NVIDIA T4 GPU), which is critical for edge-deployed early-warning safety systems.

3. **Why ByteTrack instead of DeepSORT?**
   *Answer:* DeepSORT discards low-confidence bounding boxes and relies heavily on deep appearance feature re-ID extractors, which become computationally expensive and fail under severe occlusion. ByteTrack associates almost every detection box (high and low confidence) using Kalman filtering and Hungarian matching, maintaining consistent track IDs even when people momentarily occlude one another in dense crowds.

4. **Why SQLite rather than PostgreSQL or MySQL?**
   *Answer:* The edge surveillance unit is designed as a self-contained autonomous appliance. SQLite requires zero configuration, zero daemon overhead, supports full ACID transactions, and persists evidentiary records cleanly in a single portable file (`data/crowd.db`).

5. **How does the SHA-256 caching mechanism work?**
   *Answer:* When a video is submitted, the server calculates its SHA-256 cryptographic digest before running inference. If the identical video was previously processed, the system retrieves the existing results and transcoded H.264 stream from SQLite in under 5 milliseconds, enabling instant zero-compute playback during demonstrations.

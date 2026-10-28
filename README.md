# Neural Topology Mapping for Early-Stage Crowd Surge and Compression Mitigation
### Optical Telemetry & Edge CCTV Analysis Platform (Phase 2)

A real-time edge computer-vision platform for autonomous crowd monitoring, localized spatial density estimation, and compression risk alert dispatching.

---

## 1. System Overview & Architecture

The system connects an institutional CCTV surveillance front-end to a Python computer-vision backend via an asynchronous REST API:

```
┌────────────────────────────────────────────────────────┐
│             Web Browser Interface (HTML5/JS)           │
│  - XHR upload progress bar                             │
│  - In-monitor processing stages (upload/detect/encode) │
│  - Native H.264 video playback with Range seeking      │
│  - Real-time telemetry metrics & alert queue           │
│  - SQLite evidentiary archive with reload support      │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP REST API (port 8000)
┌───────────────────────────▼────────────────────────────┐
│                  FastAPI Backend Server                │
│  - Single origin static file hosting                   │
│  - SHA-256 result cache (instant presentation reload)  │
│  - Single-job FIFO background worker thread            │
│  - SQLite database: data/crowd.db                      │
│  - Automatic H.264 (+faststart) ffmpeg transcoder      │
└─────────────┬────────────────────────────┬─────────────┘
              │ (Mock Mode)                │ (Real Inference)
              ▼                            ▼
   ┌───────────────────────┐   ┌─────────────────────────┐
   │ Simulated Ingestion   │   │ Python Subprocess       │
   │ - Progress simulation │   │ - crowd_density.py      │
   │ - Zero GPU / No YOLO  │   │ - YOLOv8 + ByteTrack    │
   │ - Tested on weak CPUs │   │ - Heatmap + Speed HUD   │
   └───────────────────────┘   └─────────────────────────┘
```

---

## 2. Quick Start

### Prerequisites
- Python 3.9, 3.10, 3.11, 3.12, or 3.13
- Git

### Installation
Clone the repository and install core dependencies:
```bash
git clone https://github.com/rrohancodes/mini_project.git
cd mini_project
pip install -r requirements.txt
```

> **Note on FFmpeg:** Video transcoding uses the bundled `imageio-ffmpeg` binary automatically. No external FFmpeg install is required on Windows or Linux.

---

## 3. Running the Server

### A. Mock Mode (Recommended for development on laptops without GPU)
Skips PyTorch and YOLOv8 completely, allowing full UI workflow testing on low-power CPUs (e.g., Core i3):
```bash
# Windows
run.bat --mock

# Linux / Mac / Terminal
python server.py --mock
```
Open **http://localhost:8000** in your browser.

### B. Real Inference Mode (With YOLOv8 Detection & Tracking)
To run real inference, install `ultralytics`:
```bash
pip install ultralytics
```
Then start the server:
```bash
# Windows
run.bat

# Linux / Terminal
python server.py
```
Open **http://localhost:8000** in your browser.

---

## 4. Hardware Acceleration (GPU vs. CPU)

The server automatically probes for NVIDIA CUDA support on startup:
- **With NVIDIA GPU:** PyTorch will automatically use CUDA acceleration (`CUDA:0 (NVIDIA GeForce ...)`).
- **Without GPU:** The server smoothly falls back to multi-threaded CPU inference.

To run with PyTorch CUDA acceleration on Windows:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## 5. Speed vs. Accuracy Tradeoffs

When running on resource-constrained devices, you can adjust inference parameters directly:

| Setting | Default | High Speed (Low Compute) | High Accuracy (High Compute) |
|---|---|---|---|
| **Model Weight** | `yolov8m.pt` (Medium) | `yolov8n.pt` (Nano) | `yolov8x.pt` (Extra Large) |
| **Inference Resolution** | `--imgsz 1280` | `--imgsz 640` | `--imgsz 1280` |
| **Confidence Threshold** | `0.15` | `0.25` | `0.10` |

### Running with lightweight configuration:
```bash
python server.py --model yolov8n.pt --imgsz 640
```

---

## 6. Presentation & Demo Features

1. **SHA-256 Result Cache:**
   When presenting, processing the same video twice will immediately return cached results without re-running the model. The UI displays an amber badge: `CACHED RESULT (SHA-256)`.
   *Tip for presentation:* Click **"Load Demonstration Test Sample Feed"** once before the presentation to prime the cache.
2. **Instant Sample Feed:**
   The **"Load Demonstration Test Sample Feed"** button automatically loads and analyzes the bundled `test.mp4`.
3. **Evidentiary Archive:**
   The **Recent Analyses & Historical Evidence Log** displays past jobs stored in `data/crowd.db`. Clicking any row immediately reloads its video stream and metric diagnostics.

---

## 7. Cloud Deployment via Google Colab

To run in Google Colab on a cloud NVIDIA T4/A100 GPU:
1. Open Google Colab and upload `colab_run.ipynb`.
2. Select **Runtime > Change runtime type > T4 GPU**.
3. Run the notebook cells sequentially:
   - Cell 1 verifies the GPU.
   - Cell 2 clones the repository.
   - Cell 3 launches the FastAPI backend.
   - Cell 4 establishes a free **Cloudflare Quick Tunnel** and outputs a public `https://*.trycloudflare.com` URL.
4. Click the Cloudflare URL to use the portal from any device or phone without port forwarding.

---

## 8. API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web interface (`static/index.html`) |
| `GET` | `/api/info` | Returns runtime metadata, active model name, and device status |
| `POST` | `/api/upload` | Multipart upload for `.mp4`, `.mov`, `.avi` files (max 100MB) |
| `POST` | `/api/sample` | Enqueues analysis for bundled `test.mp4` |
| `GET` | `/api/jobs/{id}` | Returns execution status, frame counter, and ETA |
| `GET` | `/api/jobs/{id}/video` | Streams the H.264 video with HTTP Range request support |
| `GET` | `/api/jobs/{id}/results` | Returns metrics, peak headcount, density index, and alert log |
| `GET` | `/api/jobs/{id}/alerts.csv`| Downloads evidentiary alert log CSV |
| `GET` | `/api/history` | Returns recent analysis records from SQLite |

---

## 9. Troubleshooting FAQ

**Q: Video does not play in the browser after processing finishes.**
- *Cause:* Browsers cannot decode raw OpenCV `mp4v` codec streams.
- *Fix:* The server automatically transcodes to standard H.264 (`libx264`, `yuv420p`, `+faststart`) via `imageio-ffmpeg`. If missing, verify `pip install imageio-ffmpeg`.

**Q: Port 8000 is already in use.**
- *Fix:* Start on an alternative port: `python server.py --port 8080`.

**Q: Out of Memory (OOM) error on CUDA.**
- *Fix:* Lower the resolution: `python server.py --imgsz 640 --model yolov8n.pt`.

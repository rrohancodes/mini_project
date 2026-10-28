import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
src_html_path = BASE_DIR / "frontend_demo" / "code.html"
dst_html_path = BASE_DIR / "static" / "index.html"

with open(src_html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update title
content = content.replace(
    "<title>Civic Surveillance &amp; Optical Telemetry Portal</title>",
    "<title>Neural Topology Mapping • Crowd Surge &amp; Compression Mitigation</title>"
)

# 2. Update Live Metadata Grid Bar
old_meta = """<div class="border-l-2 border-emerald-600 pl-3 bg-surface-container-low/50 py-1.5">
<span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-sans font-semibold">Inference Model Engine</span>
<span class="text-emerald-800 font-bold text-xs mt-0.5 flex items-center gap-1.5">
<span class="w-1.5 h-1.5 bg-emerald-600"></span>
            YOLOv8 Edge Engine v1.0.4 Online
          </span>
</div>
<div class="border-l-2 border-secondary pl-3 bg-surface-container-low/50 py-1.5">
<span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-sans font-semibold">Optical Feed Input</span>
<span class="text-on-surface font-semibold text-xs mt-0.5 flex items-center gap-1.5">
<span class="w-1.5 h-1.5 bg-secondary"></span>
            Awaiting Frame Ingestion (Ready)
          </span>
</div>
<div class="border-l-2 border-outline pl-3 bg-surface-container-low/50 py-1.5">
<span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-sans font-semibold">Throughput &amp; Latency</span>
<span class="text-on-surface font-semibold text-xs mt-0.5">
            1080p @ 30 FPS / &lt;24ms inference
          </span>
</div>"""

new_meta = """<div class="border-l-2 border-emerald-600 pl-3 bg-surface-container-low/50 py-1.5">
<span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-sans font-semibold">Inference Model Engine</span>
<span class="text-emerald-800 font-bold text-xs mt-0.5 flex items-center gap-1.5">
<span class="w-1.5 h-1.5 bg-emerald-600"></span>
            <span id="metaModelText">YOLOv8m Crowd Tracking</span>
          </span>
</div>
<div class="border-l-2 border-secondary pl-3 bg-surface-container-low/50 py-1.5">
<span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-sans font-semibold">Optical Feed Input</span>
<span class="text-on-surface font-semibold text-xs mt-0.5 flex items-center gap-1.5">
<span class="w-1.5 h-1.5 bg-secondary" id="metaInputDot"></span>
            <span id="metaInputText">Awaiting Frame Ingestion (Ready)</span>
          </span>
</div>
<div class="border-l-2 border-outline pl-3 bg-surface-container-low/50 py-1.5">
<span class="text-[10px] text-on-surface-variant uppercase tracking-wider block font-sans font-semibold">Compute Device / FPS</span>
<span class="text-on-surface font-semibold text-xs mt-0.5 flex items-center gap-1.5 truncate" id="metaDeviceText">
            Detecting hardware...
          </span>
</div>"""

if old_meta in content:
    content = content.replace(old_meta, new_meta)
else:
    print("Warning: old_meta not found exactly, attempting regex")

# 3. Monitor container enhancements:
# Inside #monitorContainer:
# Add #processingPanel, #errorPanel, replace <img> with <video>, add id to simulatedControlsBar
old_monitor_body = """<!-- Live Loaded Mock Stream (Hidden initially) -->
<div class="absolute inset-0 hidden z-10" id="activeStreamState">
<img alt="Operational CCTV Feed Telemetry Console Reference View" class="w-full h-full object-cover object-center filter contrast-105" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBkZr1IbCWoMGtthotCzIEQwzB3psJpyJNAdEjosTZDGKxs1gKYYNSDHxAImrlY2bHsGClN7vRVnwWukKcJJmK9PpYCdCmdQEFSfVDDyVV01JF2k06IXGAaesmAc83ea-Dezow7bytyiBj5jDCnx2vahNF-cpPf74nK9_VVuh6yYZ-TPnPYs26vDuNDZJRVdUfiwWpUJuXO3o0O2yws_ULZr3ONh1tvVmYW57JCqiBE7ZfhvR9FXNtw"/>
<div class="absolute top-3 left-3 bg-black/80 text-white font-mono text-[10px] px-2 py-1 border border-outline-variant flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
<span>TEST FEED: SIMULATED_STATION_CONCOURSE_PEAK.MP4</span>
<span class="text-outline-variant">|</span>
<span class="text-primary-fixed">REC 00:03:42</span>
</div>
</div>
<!-- Bottom Video Player Controls Bar (Simulated) -->
<div class="absolute bottom-0 left-0 right-0 h-10 bg-black/85 backdrop-blur-sm border-t border-outline-variant/30 px-4 flex items-center justify-between text-xs text-outline-variant z-20">"""

new_monitor_body = """<!-- Dynamic In-Monitor Processing Panel (Hidden by default) -->
<div id="processingPanel" class="relative z-30 flex flex-col items-center text-center max-w-md w-full px-6 py-6 bg-surface-container-lowest/95 border border-outline-variant shadow-2xl hidden">
  <div class="w-full flex items-center justify-between pb-3 border-b border-outline-variant/30 text-xs font-mono">
    <span class="font-bold text-on-surface flex items-center gap-2">
      <span class="w-2 h-2 rounded-none bg-primary animate-ping"></span>
      <span id="procStageBadge" class="uppercase">STAGE: UPLOADING</span>
    </span>
    <span class="px-2 py-0.5 text-[10px] font-bold bg-primary-fixed text-on-primary-fixed border border-primary/20" id="procStatusBadge">STATUS: PROCESSING</span>
  </div>
  <div class="w-full my-4 space-y-2">
    <div class="flex justify-between items-center text-xs font-mono">
      <span id="procMessage" class="text-on-surface font-semibold text-left truncate max-w-[260px]">Ingesting optical telemetry stream...</span>
      <span id="procPercent" class="font-bold text-primary text-sm">0%</span>
    </div>
    <div class="w-full h-2.5 bg-surface-container-high border border-outline-variant/50 overflow-hidden">
      <div id="procProgressBar" class="h-full bg-primary transition-all duration-200" style="width: 0%"></div>
    </div>
    <div class="flex justify-between text-[11px] font-mono text-on-surface-variant pt-1">
      <span id="procFrameText">FRAME: 0 / 0</span>
      <span id="procEtaText">ETA: --</span>
      <span id="procFpsText">FPS: --</span>
    </div>
  </div>
</div>

<!-- Dynamic In-Monitor Error Panel (Hidden by default) -->
<div id="errorPanel" class="relative z-30 flex flex-col items-center text-center max-w-md w-full px-6 py-6 bg-surface-container-lowest border-2 border-error shadow-2xl hidden">
  <div class="w-12 h-12 bg-error/10 border border-error/30 text-error flex items-center justify-center mb-3">
    <span class="material-symbols-outlined text-3xl">warning</span>
  </div>
  <h3 class="text-sm font-bold uppercase tracking-wider text-error font-headline" id="errorTitle">Telemetry Pipeline Anomaly</h3>
  <p class="text-xs text-on-surface-variant mt-2 mb-4 leading-relaxed font-mono" id="errorMessage">An unexpected anomaly interrupted the pipeline.</p>
  <button id="errorRetryBtn" type="button" class="px-4 py-2 bg-error hover:bg-red-800 text-white font-label text-xs font-bold tracking-wider uppercase transition-colors border border-red-900 focus:outline focus:outline-2 focus:outline-error">
    Dismiss &amp; Retry
  </button>
</div>

<!-- Live Loaded Stream with Native Video Player -->
<div class="absolute inset-0 hidden z-10" id="activeStreamState">
  <video id="resultVideo" controls playsinline class="w-full h-full object-contain bg-black"></video>
  <div id="videoOverlayBadge" class="absolute top-3 left-3 bg-black/85 text-white font-mono text-[10px] px-2 py-1 border border-outline-variant flex items-center gap-2 pointer-events-none z-10">
    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
    <span id="activeStreamLabel">CCTV TELEMETRY: PROCESSED FEED</span>
    <span class="text-outline-variant">|</span>
    <span id="cachedResultTag" class="hidden text-amber-300 font-bold bg-amber-950/80 px-1 border border-amber-600/50">CACHED RESULT (SHA-256)</span>
  </div>
</div>
<!-- Bottom Video Player Controls Bar (Simulated - shown only on idle) -->
<div class="absolute bottom-0 left-0 right-0 h-10 bg-black/85 backdrop-blur-sm border-t border-outline-variant/30 px-4 flex items-center justify-between text-xs text-outline-variant z-20" id="simulatedControlsBar">"""

if old_monitor_body in content:
    content = content.replace(old_monitor_body, new_monitor_body)
else:
    print("Warning: old_monitor_body not found exactly")

# 4. Ingestion Action Ribbon (Add Download Links & Cache Badge)
old_ingestion_end = """<div class="flex items-center gap-2 text-xs text-on-surface-variant font-mono">
<span class="material-symbols-outlined text-base text-secondary">info</span>
<span>Max Payload: 100MB (Local processing)</span>
</div>
</div>
</div>
</div>"""

new_ingestion_end = """<div class="flex items-center gap-2 text-xs text-on-surface-variant font-mono">
<span class="material-symbols-outlined text-base text-secondary">info</span>
<span>Max Payload: 100MB (Local processing)</span>
</div>
</div>
</div>
<!-- Post-Analysis Evidentiary Actions Ribbon -->
<div id="downloadActionPanel" class="p-3 bg-surface-container border-t border-outline-variant/40 flex flex-wrap items-center justify-between gap-3 text-xs hidden">
  <div class="flex flex-wrap items-center gap-2">
    <a id="downloadVideoBtn" href="#" download class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-surface-container-lowest hover:bg-surface-container-high text-on-surface border border-outline-variant font-semibold transition-colors">
      <span class="material-symbols-outlined text-sm text-primary">download</span>
      Download Processed Video (H.264)
    </a>
    <a id="downloadCsvBtn" href="#" download class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-surface-container-lowest hover:bg-surface-container-high text-on-surface border border-outline-variant font-semibold transition-colors">
      <span class="material-symbols-outlined text-sm text-secondary">table_chart</span>
      Download Evidentiary Alerts CSV
    </a>
  </div>
  <div id="cachedIndicatorBanner" class="hidden items-center gap-1.5 text-amber-800 bg-amber-50 px-2.5 py-1 border border-amber-300 font-mono text-[11px]">
    <span class="material-symbols-outlined text-xs text-amber-600">verified</span>
    <span>Verified Telemetry SHA-256 Cache Hit</span>
  </div>
</div>
</div>"""

if old_ingestion_end in content:
    content = content.replace(old_ingestion_end, new_ingestion_end)
else:
    print("Warning: old_ingestion_end not found exactly")

# 5. Metric Cards Honesty & Units
# Headcount
content = content.replace(
    '<span class="text-[10px] text-tertiary font-mono block">OCCUPANCY IN BOUNDING BOX</span>',
    '<span class="text-[10px] text-tertiary font-mono block">MAX OCCUPANCY (PEAK)</span>'
)
# Density
content = content.replace(
    '<span>Density: <strong class="text-on-surface" id="metricDensity">0.0 persons / m²</strong></span>',
    '<span>Density: <strong class="text-on-surface" id="metricDensity">0.0 (sat=4.0)</strong></span>'
)
content = content.replace(
    '<span class="text-emerald-700 font-semibold font-sans">NORMAL</span>',
    '<span class="text-emerald-700 font-semibold font-sans" id="metricDensityStatus">NORMAL</span>'
)
# Velocity unit BH / S
content = content.replace(
    '<span class="text-xs font-mono text-tertiary">M / SEC</span>',
    '<span class="text-xs font-mono text-tertiary">BH / S</span>'
)
content = content.replace(
    '<span class="font-mono">Motion: <strong class="text-on-surface font-semibold">Stationary / Normal</strong></span>',
    '<span class="font-mono">Metric: <strong class="text-on-surface font-semibold">Body-Heights / sec</strong></span>'
)
content = content.replace(
    '<span class="px-1.5 py-0.2 bg-surface-container text-on-surface-variant text-[10px] font-mono">LAMBDA: 1.0</span>',
    '<span class="px-1.5 py-0.2 bg-surface-container text-on-surface-variant text-[10px] font-mono" id="velocityFpsTag">FPS: 0.0</span>'
)
content = content.replace(
    '<span>0.0 m/s</span>\\n<span>1.2 m/s (NOMINAL FLOW)</span>\\n<span>&gt;2.5 m/s</span>',
    '<span>0.0 bh/s</span>\\n<span>0.8 bh/s (NOMINAL)</span>\\n<span>&gt;1.5 bh/s (RUNNING)</span>'
)
# Risk Index & Falls Planned Phase 3
content = content.replace(
    '<span class="text-xs font-mono text-emerald-700">INDEX: 0.04</span>',
    '<span class="text-xs font-mono text-emerald-700" id="metricRiskIndex">INDEX: 0.04</span>'
)
content = content.replace(
    '<span>Fallen / Motionless: <strong class="text-on-surface" id="metricFalls">0 detected</strong></span>',
    '<span>Fallen / Motionless: <strong class="text-on-surface" id="metricFalls">Planned (Phase 3)</strong></span>'
)

# Button onclick attribute for immediate reactivity
content = content.replace(
    'id="loadSampleFeedBtn" type="button"',
    'id="loadSampleFeedBtn" onclick="window.loadSampleFeed &amp;&amp; window.loadSampleFeed()" type="button"'
)
content = content.replace(
    'id="systemRefreshBtn" type="button"',
    'id="systemRefreshBtn" onclick="window.flushPipeline &amp;&amp; window.flushPipeline()" type="button"'
)

# 6. Panel 2: Model Specifications Honesty
old_specs = """<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Detection Engine</span>
<span class="font-bold text-on-surface flex items-center gap-1">
                  YOLOv8n Crowd
                  <span class="text-emerald-700 text-[10px] px-1 bg-emerald-50 border border-emerald-300">Ready</span>
</span>
</div>
<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Pose &amp; Fall Classifier</span>
<span class="font-semibold text-on-surface">YOLOv8-Pose Anomaly</span>
</div>
<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Temporal Buffer</span>
<span class="font-semibold text-on-surface">15-minute sliding window</span>
</div>
<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Inference Latency</span>
<span class="font-bold text-emerald-800">≤ 24ms (TensorRT FP16)</span>
</div>"""

new_specs = """<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Detection Engine</span>
<span class="font-bold text-on-surface flex items-center gap-1">
                  <span id="specModelName">YOLOv8m Edge</span>
                  <span class="text-emerald-700 text-[10px] px-1 bg-emerald-50 border border-emerald-300">Ready</span>
</span>
</div>
<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Pose &amp; Fall Classifier</span>
<span class="font-semibold text-on-surface-variant">Planned (Phase 3) / N/A</span>
</div>
<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Spatial Tracking</span>
<span class="font-semibold text-on-surface">ByteTrack Trajectory Filter</span>
</div>
<div class="py-2 flex items-center justify-between">
<span class="text-on-surface-variant font-sans text-[11px]">Throughput &amp; Latency</span>
<span class="font-bold text-emerald-800" id="specThroughputText">Dynamic Edge Ingestion</span>
</div>"""

if old_specs in content:
    content = content.replace(old_specs, new_specs)
else:
    print("Warning: old_specs not found exactly")

# 7. Settings modal additions (density alert and capacity)
old_slider1 = """<!-- Slider 1: Localized Density Trigger -->
<div class="space-y-2">
<div class="flex justify-between items-center">
<label class="font-bold text-on-surface uppercase tracking-wide text-[11px]" for="densityThresholdSlider">Crowd Density Alert Trigger (p/m²)</label>
<span class="font-mono font-bold text-primary bg-primary-fixed/40 px-2 py-0.5 border border-primary/20" id="densitySliderVal">4.0 persons / m²</span>
</div>
<input class="w-full accent-primary h-2 bg-surface-container-high rounded-none cursor-pointer" id="densityThresholdSlider" max="6.0" min="1.0" step="0.1" type="range" value="4.0"/>
<div class="flex justify-between text-[10px] font-mono text-tertiary">
<span>1.0 (Sparse)</span>
<span>3.5 (Normal Commuter Transit)</span>
<span>6.0 (Severe Crush)</span>
</div>
</div>"""

new_slider1 = """<!-- Slider 1: Localized Density Trigger -->
<div class="space-y-2">
<div class="flex justify-between items-center">
<label class="font-bold text-on-surface uppercase tracking-wide text-[11px]" for="densityThresholdSlider">Crowd Density Alert Ratio (--density-alert)</label>
<span class="font-mono font-bold text-primary bg-primary-fixed/40 px-2 py-0.5 border border-primary/20" id="densitySliderVal">0.66</span>
</div>
<input class="w-full accent-primary h-2 bg-surface-container-high rounded-none cursor-pointer" id="densityThresholdSlider" max="1.0" min="0.2" step="0.05" type="range" value="0.66"/>
<div class="flex justify-between text-[10px] font-mono text-tertiary">
<span>0.20 (Sensitive)</span>
<span>0.66 (Standard Threshold)</span>
<span>1.00 (Critical Surge)</span>
</div>
</div>
<!-- Input 2: Capacity Limit Setting -->
<div class="space-y-2">
<div class="flex justify-between items-center">
<label class="font-bold text-on-surface uppercase tracking-wide text-[11px]" for="capacityInput">Venue Occupancy Limit (--capacity)</label>
<span class="font-mono font-bold text-primary bg-primary-fixed/40 px-2 py-0.5 border border-primary/20" id="capacityVal">500 Persons</span>
</div>
<input class="w-full bg-surface-container-lowest border border-outline-variant px-3 py-2 text-xs font-mono font-bold text-on-surface focus:outline focus:outline-2 focus:outline-primary" id="capacityInput" min="10" max="5000" step="10" type="number" value="500"/>
<div class="flex justify-between text-[10px] font-mono text-tertiary">
<span>Min: 10</span>
<span>Default: 500</span>
<span>Max: 5000</span>
</div>
</div>"""

if old_slider1 in content:
    content = content.replace(old_slider1, new_slider1)
else:
    print("Warning: old_slider1 not found exactly")

# 8. Add Recent Analyses & Evidentiary Archive Table
archive_section = """<!-- Recent Analyses & Evidentiary Archive Table -->
<div class="bg-surface-container-lowest border border-outline-variant p-6 shadow-sm space-y-4" id="recentAnalysesContainer">
  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-outline-variant/40">
    <div>
      <span class="text-[10px] font-bold uppercase tracking-widest text-primary font-mono block">EVIDENTIARY ARCHIVE // SQLITE REGISTRY</span>
      <h2 class="text-sm font-bold font-headline text-on-surface uppercase tracking-wider">Recent Telemetry Analyses &amp; Historical Evidence Log</h2>
    </div>
    <button id="refreshHistoryBtn" type="button" class="px-3 py-1.5 text-xs font-semibold bg-surface-container hover:bg-surface-container-high border border-outline-variant flex items-center gap-1.5 transition-colors">
      <span class="material-symbols-outlined text-sm text-primary">sync</span>
      Refresh Archive
    </button>
  </div>
  <div class="overflow-x-auto border border-outline-variant/40">
    <table class="w-full text-left text-xs font-mono">
      <thead class="bg-inverse-surface text-inverse-on-surface border-b-2 border-primary uppercase text-[10px] tracking-wider font-sans">
        <tr>
          <th class="py-2.5 px-3">Job ID</th>
          <th class="py-2.5 px-3">Source Payload</th>
          <th class="py-2.5 px-3">Timestamp (UTC)</th>
          <th class="py-2.5 px-3">Peak Headcount</th>
          <th class="py-2.5 px-3">Peak Density</th>
          <th class="py-2.5 px-3">Risk Level</th>
          <th class="py-2.5 px-3">Alerts Raised</th>
          <th class="py-2.5 px-3">Status</th>
          <th class="py-2.5 px-3 text-right">Inspect</th>
        </tr>
      </thead>
      <tbody id="historyTableBody" class="divide-y divide-outline-variant/20 bg-surface-container-lowest">
        <tr>
          <td colspan="9" class="py-6 text-center text-on-surface-variant font-sans">Loading historical records from SQLite...</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""

roadmap_header = '<!-- Institutional Roadmap Ribbon: Upcoming Modules & Phases -->'
if roadmap_header in content:
    content = content.replace(roadmap_header, archive_section + "\n" + roadmap_header)
else:
    print("Warning: roadmap_header not found")

# 9. Replace the <script> block completely
js_code = """<script>
(function initCivicOpticalTelemetry() {
  // Elements
  const cctvFileInput = document.getElementById('cctvFileInput');
  const loadSampleFeedBtn = document.getElementById('loadSampleFeedBtn');
  const systemRefreshBtn = document.getElementById('systemRefreshBtn');
  const simulateIncidentBtn = document.getElementById('simulateIncidentBtn');

  const monitorContainer = document.getElementById('monitorContainer');
  const noStreamState = document.getElementById('noStreamState');
  const activeStreamState = document.getElementById('activeStreamState');
  const processingPanel = document.getElementById('processingPanel');
  const errorPanel = document.getElementById('errorPanel');
  const resultVideo = document.getElementById('resultVideo');
  const simulatedControlsBar = document.getElementById('simulatedControlsBar');

  const procStageBadge = document.getElementById('procStageBadge');
  const procStatusBadge = document.getElementById('procStatusBadge');
  const procMessage = document.getElementById('procMessage');
  const procPercent = document.getElementById('procPercent');
  const procProgressBar = document.getElementById('procProgressBar');
  const procFrameText = document.getElementById('procFrameText');
  const procEtaText = document.getElementById('procEtaText');
  const procFpsText = document.getElementById('procFpsText');

  const errorTitle = document.getElementById('errorTitle');
  const errorMessage = document.getElementById('errorMessage');
  const errorRetryBtn = document.getElementById('errorRetryBtn');

  const metricHeadcount = document.getElementById('metricHeadcount');
  const metricDensity = document.getElementById('metricDensity');
  const metricDensityStatus = document.getElementById('metricDensityStatus');
  const densityBar = document.getElementById('densityBar');
  const metricVelocity = document.getElementById('metricVelocity');
  const velocityFpsTag = document.getElementById('velocityFpsTag');
  const metricRisk = document.getElementById('metricRisk');
  const metricRiskIndex = document.getElementById('metricRiskIndex');
  const metricFalls = document.getElementById('metricFalls');

  const eventQueueCount = document.getElementById('eventQueueCount');
  const alertStatusBox = document.getElementById('alertStatusBox');
  const eventLogContainer = document.getElementById('eventLogContainer');

  const downloadActionPanel = document.getElementById('downloadActionPanel');
  const downloadVideoBtn = document.getElementById('downloadVideoBtn');
  const downloadCsvBtn = document.getElementById('downloadCsvBtn');
  const cachedIndicatorBanner = document.getElementById('cachedIndicatorBanner');
  const cachedResultTag = document.getElementById('cachedResultTag');

  const metaModelText = document.getElementById('metaModelText');
  const metaInputText = document.getElementById('metaInputText');
  const metaDeviceText = document.getElementById('metaDeviceText');
  const specModelName = document.getElementById('specModelName');
  const specThroughputText = document.getElementById('specThroughputText');

  const configModal = document.getElementById('configModal');
  const openConfigModalBtn = document.getElementById('openConfigModalBtn');
  const closeConfigModalBtn = document.getElementById('closeConfigModalBtn');
  const cancelModalBtn = document.getElementById('cancelModalBtn');
  const saveModalBtn = document.getElementById('saveModalBtn');
  const densityThresholdSlider = document.getElementById('densityThresholdSlider');
  const densitySliderVal = document.getElementById('densitySliderVal');
  const capacityInput = document.getElementById('capacityInput');
  const capacityVal = document.getElementById('capacityVal');

  const historyTableBody = document.getElementById('historyTableBody');
  const refreshHistoryBtn = document.getElementById('refreshHistoryBtn');

  // Application State
  let currentJobId = null;
  let pollTimer = null;
  let isJobRunning = false;
  let runtimeInfo = { mock: false, model: '', device: '' };
  let configSettings = {
    densityAlert: 0.66,
    capacity: 500
  };

  // Boot & Initialization
  async function bootServerInfo() {
    try {
      const res = await fetch('/api/info');
      if (!res.ok) throw new Error('API Info unreachable');
      runtimeInfo = await res.json();
      
      if (metaModelText) metaModelText.textContent = runtimeInfo.model || 'YOLOv8 Edge Engine';
      if (specModelName) specModelName.innerHTML = `${runtimeInfo.model || 'YOLOv8m'} <span class="text-emerald-700 text-[10px] px-1 bg-emerald-50 border border-emerald-300">Ready</span>`;
      if (metaDeviceText) metaDeviceText.textContent = runtimeInfo.device || 'CPU Inference';
      if (specThroughputText) specThroughputText.textContent = runtimeInfo.mock ? 'Simulated 26.5 FPS' : 'Measured Edge Latency';
      
      // Honesty: Hide simulate anomaly unless in mock mode
      if (simulateIncidentBtn) {
        if (runtimeInfo.mock) {
          simulateIncidentBtn.style.display = 'inline-block';
        } else {
          simulateIncidentBtn.style.display = 'none';
        }
      }
    } catch (err) {
      console.warn('Server info fetch error:', err);
      if (metaDeviceText) metaDeviceText.textContent = 'Server Offline (Check port 8000)';
    }
    fetchHistory();
  }

  // Set Controls Disabled/Enabled
  function setPipelineBusy(busy) {
    isJobRunning = busy;
    if (cctvFileInput) cctvFileInput.disabled = busy;
    if (loadSampleFeedBtn) {
      loadSampleFeedBtn.disabled = busy;
      if (busy) {
        loadSampleFeedBtn.classList.add('opacity-50', 'cursor-not-allowed');
      } else {
        loadSampleFeedBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }
    const fileLabel = document.querySelector('label[for="cctvFileInput"]');
    if (fileLabel) {
      if (busy) {
        fileLabel.classList.add('opacity-50', 'cursor-not-allowed');
      } else {
        fileLabel.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }
  }

  // Show Processing Stage in Monitor
  function showProcessingUI(stage, percent, message, frameText, etaText, fpsText) {
    if (noStreamState) noStreamState.classList.add('hidden');
    if (activeStreamState) activeStreamState.classList.add('hidden');
    if (errorPanel) errorPanel.classList.add('hidden');
    if (processingPanel) processingPanel.classList.remove('hidden');

    if (procStageBadge) procStageBadge.textContent = `STAGE: ${stage.toUpperCase()}`;
    if (procMessage) procMessage.textContent = message || 'Processing stream...';
    if (procPercent) procPercent.textContent = `${percent}%`;
    if (procProgressBar) procProgressBar.style.width = `${percent}%`;
    if (procFrameText) procFrameText.textContent = frameText || 'FRAME: --';
    if (procEtaText) procEtaText.textContent = etaText || 'ETA: --';
    if (procFpsText) procFpsText.textContent = fpsText || 'FPS: --';
  }

  // Display In-Monitor Error
  function showPipelineError(title, msg) {
    stopPolling();
    setPipelineBusy(false);
    if (processingPanel) processingPanel.classList.add('hidden');
    if (activeStreamState) activeStreamState.classList.add('hidden');
    if (noStreamState) noStreamState.classList.add('hidden');
    if (errorPanel) {
      errorPanel.classList.remove('hidden');
      if (errorTitle) errorTitle.textContent = title;
      if (errorMessage) errorMessage.textContent = msg;
    }
  }

  // Polling Job Status
  function startPolling(jobId) {
    stopPolling();
    currentJobId = jobId;
    setPipelineBusy(true);

    pollTimer = setInterval(async () => {
      try {
        const res = await fetch(`/api/jobs/${jobId}`);
        if (!res.ok) {
          throw new Error(`Job status returned ${res.status}`);
        }
        const data = await res.json();

        if (data.status === 'queued') {
          showProcessingUI('Queued', 5, data.message || 'Queued in pipeline buffer...', 'WAITING', 'ETA: --', 'FPS: --');
        } else if (data.status === 'processing') {
          const pct = Math.max(data.progress || 0, 8);
          const fText = data.total_frames ? `FRAME: ${data.frame} / ${data.total_frames}` : `FRAME: ${data.frame}`;
          const eta = data.eta_s ? `ETA: ${data.eta_s}s` : 'ETA: --';
          const fps = data.fps ? `FPS: ${data.fps}` : 'FPS: --';
          showProcessingUI('Detecting & Tracking', pct, data.message || 'Extracting optical tensor vectors...', fText, eta, fps);
        } else if (data.status === 'encoding') {
          showProcessingUI('Encoding', 95, data.message || 'Transcoding H.264 (+faststart) stream for browser...', 'COMPLETE', 'ETA: <1s', 'H.264');
        } else if (data.status === 'done') {
          stopPolling();
          onJobCompleted(jobId, data.cached);
        } else if (data.status === 'error') {
          showPipelineError('Inference Pipeline Failure', data.message || 'The neural execution encountered a critical error.');
        }
      } catch (err) {
        console.error('Job polling error:', err);
        showPipelineError('Network / Server Unreachable', 'Could not establish connection to FastAPI telemetry endpoint.');
      }
    }, 1000);
  }

  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  }

  // Upload Video File via XMLHttpRequest (Upload Progress tracking)
  function uploadVideoFile(file) {
    // Client-side validations
    const allowed = ['.mp4', '.mov', '.avi'];
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!allowed.includes(ext)) {
      showPipelineError('Unsupported Format', `Invalid video format "${ext}". Supported codecs: .mp4, .mov, .avi`);
      return;
    }
    const maxBytes = 100 * 1024 * 1024;
    if (file.size > maxBytes) {
      showPipelineError('Payload Exceeded', `File size (${(file.size / 1024 / 1024).toFixed(1)}MB) exceeds statutory maximum of 100MB.`);
      return;
    }

    setPipelineBusy(true);
    showProcessingUI('Uploading', 0, `Uploading ${file.name} to server...`, 'PAYLOAD', 'Calculating...', '--');

    const formData = new FormData();
    formData.append('video', file);
    if (configSettings.capacity) formData.append('capacity', configSettings.capacity);
    if (configSettings.densityAlert) formData.append('density_alert', configSettings.densityAlert);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/upload', true);

    xhr.upload.onprogress = function(e) {
      if (e.lengthComputable) {
        const pct = Math.round((e.loaded / e.total) * 100);
        showProcessingUI('Uploading', pct, `Streaming payload: ${pct}% uploaded...`, `${(e.loaded/1024/1024).toFixed(1)}MB / ${(e.total/1024/1024).toFixed(1)}MB`, 'In Progress', '--');
      }
    };

    xhr.onload = function() {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const resp = JSON.parse(xhr.responseText);
          currentJobId = resp.job_id;
          if (metaInputText) metaInputText.textContent = `${file.name} (${(file.size/1024/1024).toFixed(1)}MB)`;
          
          if (resp.cached) {
            onJobCompleted(resp.job_id, true);
          } else {
            showProcessingUI('Ingested', 10, 'Payload verified. Queuing neural model...', 'READY', 'ETA: Estimating', '--');
            startPolling(resp.job_id);
          }
        } catch (e) {
          showPipelineError('Response Error', 'Failed to parse telemetry server response.');
        }
      } else {
        let msg = `HTTP ${xhr.status}`;
        try {
          const d = JSON.parse(xhr.responseText);
          if (d.detail) msg = d.detail;
        } catch (_) {}
        showPipelineError('Upload Rejection', msg);
      }
    };

    xhr.onerror = function() {
      showPipelineError('Connection Severed', 'Failed connecting to server during telemetry upload.');
    };

    xhr.send(formData);
  }

  // Load Sample Feed
  async function loadSampleFeed() {
    setPipelineBusy(true);
    showProcessingUI('Ingesting Sample', 15, 'Requesting test.mp4 demonstration feed from server...', 'SAMPLE', 'Initializing', '--');
    try {
      const res = await fetch('/api/sample', { method: 'POST' });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Sample feed request failed');
      }
      const data = await res.json();
      currentJobId = data.job_id;
      if (metaInputText) metaInputText.textContent = 'Demonstration Feed: test.mp4';

      if (data.cached) {
        onJobCompleted(data.job_id, true);
      } else {
        startPolling(data.job_id);
      }
    } catch (err) {
      showPipelineError('Sample Feed Error', err.message);
    }
  }

  // On Job Completed: Play Video & Populate Metrics
  async function onJobCompleted(jobId, isCached) {
    setPipelineBusy(false);
    currentJobId = jobId;

    // Switch Monitor Screen
    if (processingPanel) processingPanel.classList.add('hidden');
    if (errorPanel) errorPanel.classList.add('hidden');
    if (noStreamState) noStreamState.classList.add('hidden');
    if (activeStreamState) activeStreamState.classList.remove('hidden');
    if (simulatedControlsBar) simulatedControlsBar.classList.add('hidden');

    // Video stream playback with HTTP Range seeking
    if (resultVideo) {
      resultVideo.src = `/api/jobs/${jobId}/video?t=${Date.now()}`;
      resultVideo.muted = true;
      resultVideo.play().catch(e => console.log('Autoplay policy caught:', e));
    }

    // Cache Indicators
    if (cachedResultTag) {
      if (isCached) cachedResultTag.classList.remove('hidden');
      else cachedResultTag.classList.add('hidden');
    }
    if (cachedIndicatorBanner) {
      if (isCached) {
        cachedIndicatorBanner.classList.remove('hidden');
        cachedIndicatorBanner.classList.add('flex');
      } else {
        cachedIndicatorBanner.classList.add('hidden');
        cachedIndicatorBanner.classList.remove('flex');
      }
    }

    // Enable Download Action Links
    if (downloadActionPanel) downloadActionPanel.classList.remove('hidden');
    if (downloadVideoBtn) downloadVideoBtn.href = `/api/jobs/${jobId}/video`;
    if (downloadCsvBtn) downloadCsvBtn.href = `/api/jobs/${jobId}/alerts.csv`;

    // Fetch and populate telemetry results
    try {
      const res = await fetch(`/api/jobs/${jobId}/results`);
      if (res.ok) {
        const results = await res.json();
        fillTelemetryMetrics(results);
      }
    } catch (err) {
      console.error('Error fetching job results:', err);
    }

    // Refresh history registry
    fetchHistory();
  }

  // Fill Telemetry Metrics and Event Queue
  function fillTelemetryMetrics(results) {
    const maxPeople = results.max_people !== undefined ? results.max_people : 0;
    const peakDensity = results.peak_density !== undefined ? results.peak_density : 0.0;
    const medSpeed = results.median_speed !== null && results.median_speed !== undefined ? Number(results.median_speed).toFixed(2) : '--';
    const risk = results.risk_level || 'LOW';
    const events = results.events || [];

    // Tile 1: Headcount & Localized Packing
    if (metricHeadcount) metricHeadcount.textContent = maxPeople;
    if (metricDensity) metricDensity.textContent = `${peakDensity.toFixed(2)} (sat=4.0)`;
    
    // Density bar: sat default is 4.0
    const densityPct = Math.min(Math.round((peakDensity / 4.0) * 100), 100);
    if (densityBar) {
      densityBar.style.width = `${densityPct}%`;
      if (densityPct > 75) densityBar.className = 'h-full bg-error';
      else if (densityPct > 45) densityBar.className = 'h-full bg-amber-500';
      else densityBar.className = 'h-full bg-primary';
    }
    if (metricDensityStatus) {
      if (densityPct > 75) {
        metricDensityStatus.textContent = 'CRITICAL';
        metricDensityStatus.className = 'text-error font-semibold font-sans';
      } else if (densityPct > 45) {
        metricDensityStatus.textContent = 'MODERATE';
        metricDensityStatus.className = 'text-amber-700 font-semibold font-sans';
      } else {
        metricDensityStatus.textContent = 'NORMAL';
        metricDensityStatus.className = 'text-emerald-700 font-semibold font-sans';
      }
    }

    // Tile 2: Velocity & Vector Displacement
    if (metricVelocity) metricVelocity.textContent = medSpeed;
    if (velocityFpsTag) velocityFpsTag.textContent = results.fps ? `FPS: ${results.fps}` : 'FPS: ACTIVE';

    // Tile 3: Risk Level
    if (metricRisk) {
      metricRisk.textContent = risk;
      if (risk === 'CRITICAL') {
        metricRisk.className = 'text-4xl font-extrabold font-headline text-error tracking-tight';
      } else if (risk === 'HIGH') {
        metricRisk.className = 'text-4xl font-extrabold font-headline text-orange-600 tracking-tight';
      } else if (risk === 'MEDIUM') {
        metricRisk.className = 'text-4xl font-extrabold font-headline text-amber-700 tracking-tight';
      } else {
        metricRisk.className = 'text-4xl font-extrabold font-headline text-emerald-800 tracking-tight';
      }
    }
    if (metricRiskIndex) {
      metricRiskIndex.textContent = `RATIO: ${(peakDensity / 4.0).toFixed(2)}`;
    }
    if (metricFalls) {
      metricFalls.textContent = 'Planned (Phase 3)';
    }

    // Event Queue Count & Alert Status Box
    const startEvents = events.filter(e => e.state === 'START');
    const totalStartCount = startEvents.length;

    if (eventQueueCount) {
      eventQueueCount.textContent = `${totalStartCount} EVENT${totalStartCount === 1 ? '' : 'S'}`;
      if (totalStartCount > 0) {
        eventQueueCount.className = 'px-2 py-0.5 text-[10px] font-bold font-mono bg-error text-white border border-error';
      } else {
        eventQueueCount.className = 'px-2 py-0.5 text-[10px] font-bold font-mono bg-surface-container-lowest text-on-surface border border-outline-variant';
      }
    }

    if (alertStatusBox) {
      if (totalStartCount > 0) {
        const lastAlert = startEvents[startEvents.length - 1];
        alertStatusBox.className = 'p-3 bg-error-container/40 border-l-4 border-error flex items-start gap-3';
        alertStatusBox.innerHTML = `
          <div class="w-6 h-6 rounded-none bg-error text-white flex items-center justify-center shrink-0 mt-0.5">
            <span class="material-symbols-outlined text-sm">warning</span>
          </div>
          <div class="space-y-1">
            <span class="text-xs font-bold text-error block leading-tight">ACTIVE ALERT: ${lastAlert.alert} (${lastAlert.time_s}s)</span>
            <span class="text-[11px] text-on-surface-variant block font-mono">OPTICAL SWEEP RAISED ${totalStartCount} RESTRAINT INCIDENT(S)</span>
          </div>
        `;
      } else {
        alertStatusBox.className = 'p-3 bg-surface-container border border-outline-variant/60 flex items-start gap-3';
        alertStatusBox.innerHTML = `
          <div class="w-6 h-6 rounded-none bg-emerald-100 border border-emerald-300 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
            <span class="material-symbols-outlined text-sm">check</span>
          </div>
          <div class="space-y-1">
            <span class="text-xs font-bold text-emerald-900 block leading-tight">No anomalous crowd compression or stalls detected.</span>
            <span class="text-[11px] text-tertiary block font-mono">NOMINAL SENSOR SWEEP • VERIFIED</span>
          </div>
        `;
      }
    }

    // Populate Event Log Feed
    if (eventLogContainer) {
      if (events.length === 0) {
        eventLogContainer.innerHTML = `
          <span class="material-symbols-outlined text-2xl text-outline-variant block mx-auto">playlist_add_check</span>
          <p class="font-medium text-xs text-on-surface">Queue is clear</p>
          <p class="text-[11px] text-tertiary">No incident markers triggered during optical ingestion.</p>
        `;
      } else {
        let html = '<div class="text-left space-y-2 text-xs">';
        events.forEach((ev, idx) => {
          const isStart = ev.state === 'START';
          const bgClass = isStart ? 'bg-error-container/20 border-error/40' : 'bg-surface-container-low border-outline-variant/40';
          const textClass = isStart ? 'text-error font-bold' : 'text-on-surface font-semibold';
          const speedTxt = ev.median_speed_bh !== null && ev.median_speed_bh !== undefined ? ` • Speed: ${ev.median_speed_bh} bh/s` : '';
          
          html += `
            <div class="p-2 border ${bgClass} flex items-start justify-between">
              <div>
                <span class="${textClass} font-mono block text-[11px]">[T+${ev.time_s}s] ${ev.alert} &mdash; ${ev.state}</span>
                <span class="text-on-surface-variant text-[11px]">Peak Density: ${ev.peak_density || 0}${speedTxt}</span>
              </div>
              <span class="font-mono text-[10px] px-1 py-0.2 ${isStart ? 'bg-error text-white' : 'bg-surface-container text-on-surface'}">${ev.state}</span>
            </div>
          `;
        });
        html += '</div>';
        eventLogContainer.innerHTML = html;
      }
    }
  }

  // Flush Pipeline / Reset UI to Idle
  function flushPipeline() {
    stopPolling();
    setPipelineBusy(false);
    currentJobId = null;

    if (resultVideo) {
      resultVideo.pause();
      resultVideo.removeAttribute('src');
      resultVideo.load();
    }

    if (noStreamState) noStreamState.classList.remove('hidden');
    if (activeStreamState) activeStreamState.classList.add('hidden');
    if (processingPanel) processingPanel.classList.add('hidden');
    if (errorPanel) errorPanel.classList.add('hidden');
    if (simulatedControlsBar) simulatedControlsBar.classList.remove('hidden');
    if (downloadActionPanel) downloadActionPanel.classList.add('hidden');

    if (metricHeadcount) metricHeadcount.textContent = '0';
    if (metricDensity) metricDensity.textContent = '0.0 (sat=4.0)';
    if (densityBar) {
      densityBar.style.width = '4%';
      densityBar.className = 'h-full bg-primary';
    }
    if (metricDensityStatus) {
      metricDensityStatus.textContent = 'NORMAL';
      metricDensityStatus.className = 'text-emerald-700 font-semibold font-sans';
    }
    if (metricVelocity) metricVelocity.textContent = '0.00';
    if (velocityFpsTag) velocityFpsTag.textContent = 'FPS: --';
    if (metricRisk) {
      metricRisk.textContent = 'LOW';
      metricRisk.className = 'text-4xl font-extrabold font-headline text-emerald-800 tracking-tight';
    }
    if (metricRiskIndex) metricRiskIndex.textContent = 'INDEX: 0.00';
    if (metricFalls) metricFalls.textContent = 'Planned (Phase 3)';

    if (eventQueueCount) {
      eventQueueCount.textContent = '0 EVENTS';
      eventQueueCount.className = 'px-2 py-0.5 text-[10px] font-bold font-mono bg-surface-container-lowest text-on-surface border border-outline-variant';
    }
    if (alertStatusBox) {
      alertStatusBox.className = 'p-3 bg-surface-container border border-outline-variant/60 flex items-start gap-3';
      alertStatusBox.innerHTML = `
        <div class="w-6 h-6 rounded-none bg-emerald-100 border border-emerald-300 text-emerald-800 flex items-center justify-center shrink-0 mt-0.5">
          <span class="material-symbols-outlined text-sm">check</span>
        </div>
        <div class="space-y-1">
          <span class="text-xs font-bold text-emerald-900 block leading-tight">No anomalous crowd compression or falls detected.</span>
          <span class="text-[11px] text-tertiary block font-mono">NOMINAL SENSOR SWEEP • T-00:00:00</span>
        </div>
      `;
    }
    if (eventLogContainer) {
      eventLogContainer.innerHTML = `
        <span class="material-symbols-outlined text-2xl text-outline-variant block mx-auto">playlist_add_check</span>
        <p class="font-medium text-xs text-on-surface">Queue is clear</p>
        <p class="text-[11px] text-tertiary">Incident markers will appear here automatically when triggered.</p>
      `;
    }
    if (metaInputText) metaInputText.textContent = 'Awaiting Frame Ingestion (Ready)';
  }

  // Historical Records Retrieval
  async function fetchHistory() {
    if (!historyTableBody) return;
    try {
      const res = await fetch('/api/history');
      if (!res.ok) throw new Error('History query failed');
      const jobs = await res.json();

      if (!jobs || jobs.length === 0) {
        historyTableBody.innerHTML = `
          <tr>
            <td colspan="9" class="py-6 text-center text-on-surface-variant font-sans">No analyses recorded in SQLite registry yet.</td>
          </tr>
        `;
        return;
      }

      let html = '';
      jobs.forEach((j, index) => {
        const isZebra = index % 2 === 1 ? 'bg-surface-container-low/40' : 'bg-surface-container-lowest';
        const formattedDate = j.created_at ? new Date(j.created_at).toLocaleTimeString() : '--:--:--';
        const riskColor = j.risk_level === 'CRITICAL' ? 'text-error font-bold' : j.risk_level === 'HIGH' ? 'text-orange-600 font-bold' : j.risk_level === 'MEDIUM' ? 'text-amber-700 font-bold' : 'text-emerald-700';

        html += `
          <tr class="${isZebra} hover:bg-surface-container transition-colors cursor-pointer" data-job-id="${j.id}">
            <td class="py-2.5 px-3 font-mono font-bold text-primary">${j.id}</td>
            <td class="py-2.5 px-3 text-on-surface max-w-[140px] truncate" title="${j.filename}">${j.filename}</td>
            <td class="py-2.5 px-3 text-on-surface-variant">${formattedDate}</td>
            <td class="py-2.5 px-3 font-bold">${j.max_people !== null ? j.max_people : '--'}</td>
            <td class="py-2.5 px-3 font-mono">${j.peak_density !== null ? Number(j.peak_density).toFixed(2) : '--'}</td>
            <td class="py-2.5 px-3 ${riskColor}">${j.risk_level || '--'}</td>
            <td class="py-2.5 px-3">
              <span class="px-1.5 py-0.5 text-[10px] ${j.alert_count > 0 ? 'bg-error text-white font-bold' : 'bg-surface-container-high text-on-surface'}">${j.alert_count || 0}</span>
            </td>
            <td class="py-2.5 px-3">
              <span class="px-1.5 py-0.5 text-[10px] ${j.status === 'done' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'} uppercase font-bold">${j.status}</span>
            </td>
            <td class="py-2.5 px-3 text-right">
              <button class="px-2 py-1 text-[11px] bg-primary text-on-primary hover:bg-primary-container transition-colors view-history-btn" data-job-id="${j.id}" type="button">
                Load
              </button>
            </td>
          </tr>
        `;
      });
      historyTableBody.innerHTML = html;

      // Attach click listeners to rows
      historyTableBody.querySelectorAll('tr[data-job-id]').forEach(row => {
        row.addEventListener('click', function() {
          const jid = this.getAttribute('data-job-id');
          if (jid) onJobCompleted(jid, true);
        });
      });
    } catch (err) {
      console.warn('History table fetch error:', err);
    }
  }

  // Event Listeners Setup
  if (loadSampleFeedBtn) loadSampleFeedBtn.addEventListener('click', loadSampleFeed);
  if (systemRefreshBtn) systemRefreshBtn.addEventListener('click', flushPipeline);
  if (refreshHistoryBtn) refreshHistoryBtn.addEventListener('click', fetchHistory);

  if (cctvFileInput) {
    cctvFileInput.addEventListener('change', function(e) {
      if (e.target.files && e.target.files[0]) {
        uploadVideoFile(e.target.files[0]);
      }
    });
  }

  // Drag and Drop on Monitor Container
  if (monitorContainer) {
    ['dragenter', 'dragover'].forEach(eventName => {
      monitorContainer.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
        monitorContainer.classList.add('ring-2', 'ring-primary');
      }, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
      monitorContainer.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
        monitorContainer.classList.remove('ring-2', 'ring-primary');
      }, false);
    });
    monitorContainer.addEventListener('drop', function(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        uploadVideoFile(files[0]);
      }
    }, false);
  }

  if (errorRetryBtn) {
    errorRetryBtn.addEventListener('click', flushPipeline);
  }

  // Configuration Modal Triggers
  function openModal() {
    if (configModal) {
      configModal.classList.remove('hidden');
      configModal.classList.add('flex');
    }
  }
  function closeModal() {
    if (configModal) {
      configModal.classList.add('hidden');
      configModal.classList.remove('flex');
    }
  }

  if (openConfigModalBtn) openConfigModalBtn.addEventListener('click', openModal);
  if (closeConfigModalBtn) closeConfigModalBtn.addEventListener('click', closeModal);
  if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);
  if (saveModalBtn) {
    saveModalBtn.addEventListener('click', function() {
      if (densityThresholdSlider) {
        configSettings.densityAlert = parseFloat(densityThresholdSlider.value);
      }
      if (capacityInput) {
        configSettings.capacity = parseInt(capacityInput.value) || 500;
      }
      closeModal();
    });
  }

  // Slider & Input Bindings
  if (densityThresholdSlider && densitySliderVal) {
    densityThresholdSlider.addEventListener('input', function(e) {
      densitySliderVal.textContent = parseFloat(e.target.value).toFixed(2);
    });
  }
  if (capacityInput && capacityVal) {
    capacityInput.addEventListener('input', function(e) {
      capacityVal.textContent = `${e.target.value || 500} Persons`;
    });
  }

  // Anomaly Simulation (Mock Mode Only)
  if (simulateIncidentBtn) {
    simulateIncidentBtn.addEventListener('click', function() {
      if (!runtimeInfo.mock) return;
      metricHeadcount.textContent = '84';
      metricDensity.textContent = '3.85 (CRITICAL)';
      metricVelocity.textContent = '1.82';
      metricRisk.textContent = 'CRITICAL';
      metricRisk.className = 'text-4xl font-extrabold font-headline text-error tracking-tight';
      if (densityBar) {
        densityBar.style.width = '96%';
        densityBar.className = 'h-full bg-error';
      }
      if (eventQueueCount) {
        eventQueueCount.textContent = '2 EVENTS';
        eventQueueCount.className = 'px-2 py-0.5 text-[10px] font-bold font-mono bg-error text-white border border-error';
      }
      if (alertStatusBox) {
        alertStatusBox.className = 'p-3 bg-error-container/40 border-l-4 border-error flex items-start gap-3';
        alertStatusBox.innerHTML = `
          <div class="w-6 h-6 rounded-none bg-error text-white flex items-center justify-center shrink-0 mt-0.5">
            <span class="material-symbols-outlined text-sm">warning</span>
          </div>
          <div class="space-y-1">
            <span class="text-xs font-bold text-error block leading-tight">CRITICAL SURGE DETECTED (p=3.85 / sat=4.0)</span>
            <span class="text-[11px] text-on-surface-variant block font-mono">SIMULATION INJECTION • HIGH TURBULENCE</span>
          </div>
        `;
      }
    });
  }

  // Expose global controller methods on window
  window.loadSampleFeed = loadSampleFeed;
  window.flushPipeline = flushPipeline;
  window.onJobCompleted = onJobCompleted;

  // Boot server info
  bootServerInfo();
})();
</script>"""

# Replace script tag and contents
content = re.sub(r'<script>\s*\(function initConsoleTelemetry\(\)[\s\S]*?</script>', js_code, content)

with open(dst_html_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully generated {dst_html_path} ({len(content)} bytes)")

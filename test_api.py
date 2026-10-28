import time
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000"

print("--- 1. Testing /api/info ---")
res = requests.get(f"{BASE_URL}/api/info")
print("Status:", res.status_code)
info = res.json()
print("Info response:", info)
assert res.status_code == 200
assert info["mock"] is True

print("\n--- 2. Testing Frontend root / ---")
res = requests.get(f"{BASE_URL}/")
print("Status:", res.status_code)
assert res.status_code == 200
assert "Neural Topology Mapping" in res.text

print("\n--- 3. Testing POST /api/sample ---")
res = requests.post(f"{BASE_URL}/api/sample")
print("Status:", res.status_code)
sample_data = res.json()
print("Sample response:", sample_data)
assert res.status_code == 200
job_id = sample_data["job_id"]

print(f"\n--- 4. Polling Job {job_id} to completion ---")
while True:
    res = requests.get(f"{BASE_URL}/api/jobs/{job_id}")
    assert res.status_code == 200
    st = res.json()
    print(f"Status: {st['status']}, Progress: {st.get('progress')}%, Msg: {st.get('message')}")
    if st["status"] in ("done", "error"):
        break
    time.sleep(1.5)

assert st["status"] == "done"
print("Job completed successfully!")

print("\n--- 5. Testing HTTP Range request on /api/jobs/{id}/video ---")
headers = {"Range": "bytes=0-1023"}
v_res = requests.get(f"{BASE_URL}/api/jobs/{job_id}/video", headers=headers)
print("Video status with Range header:", v_res.status_code)
print("Content-Range header:", v_res.headers.get("content-range"))
assert v_res.status_code == 206
assert len(v_res.content) == 1024

print("\n--- 6. Testing /api/jobs/{id}/results ---")
r_res = requests.get(f"{BASE_URL}/api/jobs/{job_id}/results")
print("Results status:", r_res.status_code)
results = r_res.json()
print("Results:", results)
assert r_res.status_code == 200
assert "max_people" in results
assert "peak_density" in results
assert "events" in results

print("\n--- 7. Testing /api/jobs/{id}/alerts.csv ---")
c_res = requests.get(f"{BASE_URL}/api/jobs/{job_id}/alerts.csv")
print("CSV status:", c_res.status_code)
print("CSV sample line:", c_res.text.splitlines()[0] if c_res.text else "Empty")
assert c_res.status_code == 200
assert "time_s" in c_res.text

print("\n--- 8. Testing SHA-256 Cache: Calling /api/sample again ---")
sample_res2 = requests.post(f"{BASE_URL}/api/sample")
sample_data2 = sample_res2.json()
print("Second sample call response:", sample_data2)
assert sample_data2["cached"] is True
print("SHA-256 Cache hit verified!")

print("\n--- 9. Testing /api/history ---")
h_res = requests.get(f"{BASE_URL}/api/history")
print("History status:", h_res.status_code)
history = h_res.json()
print(f"History records found: {len(history)}")
for h in history[:3]:
    print(f" - Job {h['id']}: {h['filename']}, Status: {h['status']}, Alerts: {h.get('alert_count')}")
assert len(history) > 0

print("\n==========================================")
print("ALL BACKEND ENDPOINTS TESTED & PASSED!")
print("==========================================")

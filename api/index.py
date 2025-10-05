from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/")
@app.post("/")
async def analyze_latency(request: Request):
    if request.method == "POST":
        body = await request.json()
        regions = body.get("regions", [])
        threshold = body.get("threshold_ms", 180)
        
        with open("telemetry.json") as f:
            telemetry = json.load(f)

        results = {}
        for region in regions:
            records = telemetry.get(region, [])
            if not records:
                continue
            latencies = [r["latency_ms"] for r in records]
            uptimes = [r["uptime"] for r in records]

            avg_latency = float(np.mean(latencies))
            p95_latency = float(np.percentile(latencies, 95))
            avg_uptime = float(np.mean(uptimes))
            breaches = int(sum(1 for x in latencies if x > threshold))

            results[region] = {
                "avg_latency": round(avg_latency, 2),
                "p95_latency": round(p95_latency, 2),
                "avg_uptime": round(avg_uptime, 3),
                "breaches": breaches,
            }

        return results
    return {"message": "Serverless function is alive, send a POST request with JSON."}

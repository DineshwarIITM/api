import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from pydantic import BaseModel
from typing import List

# Define the request body model
class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

# Load the telemetry data
with open("telemetry.json", "r") as f:
    telemetry_data = json.load(f)

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def analyze_telemetry(request: TelemetryRequest):
    """
    Analyzes telemetry data for given regions and returns metrics.
    """
    response = {}
    for region in request.regions:
        region_data = [d for d in telemetry_data if d["region"] == region]

        if not region_data:
            continue

        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]

        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        avg_uptime = np.mean(uptimes)
        breaches = sum(1 for latency in latencies if latency > request.threshold_ms)

        response[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches,
        }
    return response

@app.get("/")
def read_root():
    return {"message": "Telemetry API is running."}
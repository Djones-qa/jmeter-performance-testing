"""
JMeter results analyzer — parses JTL output and calculates metrics.
"""
import pandas as pd
import os


def parse_jtl(jtl_path: str) -> pd.DataFrame:
    """Parse JMeter JTL results file."""
    df = pd.read_csv(jtl_path)
    df.columns = [c.strip() for c in df.columns]
    return df


def calculate_metrics(df: pd.DataFrame) -> dict:
    """Calculate key performance metrics from JMeter results."""
    total = len(df)
    passed = df[df["success"] == True] if "success" in df.columns else df
    failed = total - len(passed)

    return {
        "total_requests": total,
        "passed": len(passed),
        "failed": failed,
        "error_rate": round(failed / total * 100, 2) if total > 0 else 0,
        "avg_response_ms": round(df["elapsed"].mean(), 2) if "elapsed" in df.columns else 0,
        "min_response_ms": int(df["elapsed"].min()) if "elapsed" in df.columns else 0,
        "max_response_ms": int(df["elapsed"].max()) if "elapsed" in df.columns else 0,
        "p90_response_ms": round(df["elapsed"].quantile(0.90), 2) if "elapsed" in df.columns else 0,
        "p95_response_ms": round(df["elapsed"].quantile(0.95), 2) if "elapsed" in df.columns else 0,
        "throughput_rps": round(total / (df["elapsed"].sum() / 1000), 2) if "elapsed" in df.columns else 0,
    }


def generate_sample_results(num_requests: int = 100) -> pd.DataFrame:
    """Generate sample JTL-like results for testing."""
    import numpy as np
    import random
    np.random.seed(42)
    random.seed(42)

    labels = ["GET Homepage", "GET API Status", "POST Request",
              "GET User Agent", "GET Headers"]
    records = []
    base_time = 1700000000000

    for i in range(num_requests):
        elapsed = int(np.random.normal(250, 80))
        elapsed = max(50, elapsed)
        success = random.random() > 0.02
        records.append({
            "timeStamp": base_time + (i * 1000),
            "elapsed": elapsed,
            "label": random.choice(labels),
            "responseCode": "200" if success else "500",
            "responseMessage": "OK" if success else "Server Error",
            "threadName": f"Thread Group 1-{random.randint(1,50)}",
            "dataType": "text",
            "success": success,
            "bytes": random.randint(500, 5000),
            "sentBytes": random.randint(100, 500),
            "grpThreads": random.randint(1, 50),
            "allThreads": random.randint(1, 50),
            "Latency": int(elapsed * 0.8),
            "IdleTime": 0,
            "Connect": random.randint(10, 100),
        })
    return pd.DataFrame(records)

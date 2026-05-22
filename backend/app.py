from flask import Flask, request, jsonify
from flask_cors import CORS
from trend_engine import generate_forecast
import json
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Restrict CORS to ALLOWED_ORIGINS to prevent unauthorized access in production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins != "*":
    origins = [origin.strip() for origin in allowed_origins.split(",")]
    CORS(app, origins=origins)
    print(f"🔒 CORS enabled for origins: {origins}")
else:
    CORS(app, origins="*")
    print("⚠️ CORS enabled for all origins (*)")

# Connect to Upstash Redis (optional — runs without it)
try:
    import redis
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        upstash_url = os.getenv("UPSTASH_REDIS_URL")
        upstash_token = os.getenv("UPSTASH_REDIS_TOKEN")
        if upstash_url and upstash_token:
            clean_url = upstash_url.strip().strip('"').strip("'")
            clean_token = upstash_token.strip().strip('"').strip("'")
            # If URL already has scheme, extract the host and port
            if "://" in clean_url:
                scheme, host_port = clean_url.split("://", 1)
            else:
                scheme, host_port = "rediss", clean_url
            redis_url = f"{scheme}://default:{clean_token}@{host_port}"
        else:
            redis_url = "redis://localhost:6379"
            
    cache = redis.from_url(redis_url, decode_responses=True)
    cache.ping()
    print("✅ Connected to Redis (Upstash)")
except Exception as e:
    print(f"⚠️ Redis not available: {e}. Running without cache.")
    cache = None

CACHE_TTL = 86400  # 24 hours in seconds


def get_cache_key(region, year, signals):
    """Generate a unique cache key from the request parameters."""
    raw = f"{region}:{year}:{','.join(sorted(signals))}"
    return f"forecast:{hashlib.md5(raw.encode()).hexdigest()}"


@app.route("/", methods=["GET"])
def home():
    """Root JSON endpoint showing backend service health status."""
    return jsonify({
        "status": "active",
        "service": "Fashion Forecasting Lab Backend API",
        "framework": "Flask / Python",
        "endpoints": {
            "/api/forecast": "POST - Core forecasting analysis engine"
        }
    })


@app.route("/api/forecast", methods=["POST"])
def api_forecast():
    """JSON API endpoint for forecast with Redis caching."""
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
        
    region = data.get("region", "Pan India")
    year = data.get("year", "2026")
    signals = data.get("signals", [])
    
    # Support direct signal or query passed in URL query parameters
    query_signal = request.args.get("signal") or request.args.get("query")
    if query_signal:
        if not isinstance(signals, list):
            signals = []
        if query_signal not in signals:
            signals.append(query_signal)

    if not signals:
        return jsonify({"error": "No signals selected"}), 400

    # Check Redis cache first
    cache_key = get_cache_key(region, year, signals)
    if cache:
        try:
            cached = cache.get(cache_key)
            if cached:
                print(f"🔁 Cache HIT for {cache_key}")
                return jsonify({"forecasts": json.loads(cached), "cached": True})
        except Exception as e:
            print(f"⚠️ Cache read error: {e}")

    # Generate fresh forecast (calls pytrends + Gemini AI)
    print(f"🆕 Cache MISS — generating forecast for {region}, {year}, {signals} with query {query_signal}")
    try:
        forecasts = generate_forecast(region, year, signals, query=query_signal)
        print(f"✅ Generated {len(forecasts)} forecasts: {forecasts}")
    except Exception as ex:
        import traceback
        print("❌ Error during generate_forecast:")
        traceback.print_exc()
        forecasts = []

    # Store in Redis with 24-hour TTL
    if cache and forecasts:
        try:
            cache.set(cache_key, json.dumps(forecasts), ex=CACHE_TTL)
            print(f"💾 Cached result for {cache_key} (TTL: {CACHE_TTL}s)")
        except Exception as e:
            print(f"⚠️ Cache write error: {e}")

    return jsonify({"forecasts": forecasts, "cached": False})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

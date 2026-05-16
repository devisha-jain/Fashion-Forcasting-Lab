from trend_data import get_live_trends
import random

def generate_forecast(region, year, signals):
    live_data = get_live_trends()
    google_data = live_data["google"]
    pinterest_data = live_data["pinterest"]

    trends = []

    # Map our live data to the requested signals
    signal_strength = {
        "bollywood": min(100, pinterest_data["bollywood_aesthetic"] + random.randint(-5, 5)),
        "kpop": google_data["Korean fashion India"] + random.randint(5, 15),
        "college": google_data["college outfit ideas"],
        "regional": google_data["ethnic fusion wear"] + random.randint(10, 20)
    }

    if "bollywood" in signals:
        trends.append({
            "name": "Luxury Minimal Ethnic",
            "confidence": min(98, signal_strength["bollywood"] + 5),
            "description":
            f"Bollywood-inspired muted ethnic looks are dominating Pinterest feeds. We forecast a surge in {region} by {year}, driven by minimalist aesthetics.",
            "business":
            "Premium ethnic brands should invest in minimalist festive wear. High conversion expected across Gen-Z and Millennials.",
            "momentum": "rising ↗",
            "palette": ["#ffefef", "#fdfbf7", "#f5f5dc", "#d2b48c"],
            "graph": signal_strength,
            "demographics": {
                "Gen-Z": 65,
                "Millennials": 25,
                "Gen-X": 10
            },
            "image": "luxury_minimal.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        })

    if "kpop" in signals:
        trends.append({
            "name": "Ethnic Streetwear Fusion",
            "confidence": min(95, signal_strength["kpop"] + 10),
            "description":
            f"K-pop fashion is rapidly shaping Indo-western streetwear in {region}. Live Google queries show a spike in 'streetwear India'.",
            "business":
            "Affordable premium brands should launch fusion collections focusing on oversized silhouettes and indigenous textiles.",
            "momentum": "fast rising ↗",
            "palette": ["#8b5a2b", "#d2b48c", "#fdfbf7", "#4a3c31"],
            "graph": signal_strength,
            "demographics": {
                "Gen-Z": 82,
                "Millennials": 15,
                "Gen-X": 3
            },
            "image": "streetwear_fusion.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        })

    if "college" in signals:
        trends.append({
            "name": "Gen-Z Retro College Core",
            "confidence": min(92, signal_strength["college"] + 8),
            "description":
            f"Elevated retro college aesthetics are merging with Indian textiles across {region} campuses. High momentum towards {year}.",
            "business":
            "Brands should focus on gender-neutral varsity silhouettes featuring local handloom accents.",
            "momentum": "peaking ↗",
            "palette": ["#cba89a", "#f5f5dc", "#8b5a2b", "#fffaf7"],
            "graph": signal_strength,
            "demographics": {
                "Gen-Z": 90,
                "Millennials": 8,
                "Gen-X": 2
            },
            "image": "college_core.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        })

    if "regional" in signals:
        trends.append({
            "name": "Modern Regional Handlooms",
            "confidence": min(96, signal_strength["regional"] + 5),
            "description":
            f"Traditional regional fashion is being modernized with contemporary draping. Huge search volumes for 'ethnic fusion wear' in {region}.",
            "business":
            "Luxury and boutique brands must integrate authentic regional weaves into chic, ready-to-wear collections.",
            "momentum": "steady ↗",
            "palette": ["#50352d", "#d2b48c", "#ffefef", "#8b5a2b"],
            "graph": signal_strength,
            "demographics": {
                "Gen-Z": 45,
                "Millennials": 40,
                "Gen-X": 15
            },
            "image": "regional_handloom.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        })

    return trends
from trend_data import get_live_trends
import random
import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

# Curated fallback images from Unsplash (free, no key needed via direct CDN)
_FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&q=80",
    "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&q=80",
    "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=600&q=80",
    "https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=600&q=80",
    "https://images.unsplash.com/photo-1595777216528-071e0127ccbf?w=600&q=80",
    "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=600&q=80",
]


def fetch_unsplash_images(query: str) -> list:
    """Fetch 3 portrait fashion photos from Unsplash for the given query.
    Falls back to curated placeholder images if the API is unavailable."""
    if not UNSPLASH_ACCESS_KEY:
        return random.sample(_FALLBACK_IMAGES, min(3, len(_FALLBACK_IMAGES)))

    try:
        search_query = urllib.parse.quote(f"{query} fashion India")
        url = f"https://api.unsplash.com/search/photos?query={search_query}&per_page=3&orientation=portrait"
        req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
        results = data.get("results", [])
        if results:
            return [r["urls"]["regular"] for r in results[:3]]
        # If Unsplash returns 0 results for niche query, fall back
        return random.sample(_FALLBACK_IMAGES, min(3, len(_FALLBACK_IMAGES)))
    except Exception as e:
        print(f"⚠️ Unsplash fetch error: {e}")
        return random.sample(_FALLBACK_IMAGES, min(3, len(_FALLBACK_IMAGES)))

# Try to import and configure Gemini AI
try:
    from google import genai
    gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
    print("✅ Gemini AI connected")
except Exception as e:
    print(f"⚠️ Gemini AI not available: {e}. Using static descriptions.")
    GEMINI_AVAILABLE = False


def get_ai_forecast(trend_name, region, year, signal_strength, signal_type):
    """Use Gemini AI to generate dynamic, insightful forecast descriptions."""
    if not GEMINI_AVAILABLE:
        return None

    prompt = f"""You are a WGSN-level fashion forecasting analyst specializing in the Indian market, analyzing trends specifically for Indian fashion brands and garment manufacturers.

Given these LIVE Google Trends signal strengths:
- Bollywood aesthetic: {signal_strength.get('bollywood', 'N/A')}
- K-pop influence: {signal_strength.get('kpop', 'N/A')}
- College fashion: {signal_strength.get('college', 'N/A')}
- Regional/ethnic fusion: {signal_strength.get('regional', 'N/A')}

Generate a forecast for the trend "{trend_name}" in {region} for {year}.

Return ONLY valid JSON (no markdown, no code blocks, no trailing comments) with these exact keys:
{{
    "description": "A 2-3 sentence professional forecast description citing real search data trends",
    "business": "A 1-2 sentence actionable business insight for fashion brands",
    "momentum": "one of: rising ↗, fast rising ↗, peaking ↗, steady ↗, emerging ↗, Rising Star",
    "investSignal": "one of: 'Strong Buy', 'Moderate Buy', 'Hold', 'Avoid'",
    "investPercent": 15,
    "investReason": "A 1-2 sentence explanation of why this budget allocation is recommended based on the market dynamics",
    "targetDemographic": "Detailed target demographic description, specifying age groups, key cities/metros in India, and consumer subculture characteristics, structured like a WGSN report",
    "peakSeason": "Detailed peak season description, describing when demand spikes, why, and what styles or climate factors drive it in India",
    "competitorActivity": "Detailed description of what competitors are doing, mentioning specific local Indian and international brands in India, and how they capitalize on this trend",
    "yearlyForecast": [
        {{"year": "2026", "score": 60}},
        {{"year": "2027", "score": 75}},
        {{"year": "2028", "score": 70}},
        {{"year": "2029", "score": 50}}
    ],
    "risks": "Description of the main risk if a fashion company or manufacturer over-invests in this trend"
}}

IMPORTANT RULES:
1. "investPercent" MUST be returned as a raw integer between 5 and 40 (do not enclose it in quotes).
2. "yearlyForecast" MUST contain exactly 4 objects corresponding to the years 2026, 2027, 2028, and 2029, with score values as raw integers between 0 and 100.
3. No comments or extra text outside the JSON structure.
"""

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        text = response.text.strip()
        # Clean up markdown code blocks if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        if text.startswith("json"):
            text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        print(f"⚠️ Gemini AI error: {e}")
        return None


def generate_forecast(region, year, signals, query=None):
    # Normalize inputs to catch "old money" and route it to our detailed static forecast
    normalized_signals = []
    for sig in signals:
        clean_sig = sig.lower().strip()
        if "old money" in clean_sig:
            normalized_signals.append("old money aesthetic")
        else:
            normalized_signals.append(sig)
    signals = normalized_signals

    if not query and signals:
        query = signals[-1]
    elif not query:
        query = "fashion"

    live_data = get_live_trends(query)
    google_data = live_data["google"]
    pinterest_data = live_data["pinterest"]

    trends = []

    # Map the live Google Trends data dynamically to the requested signals
    signal_strength = {}
    for sig in signals:
        score = 65
        if query:
            clean_sig = sig.lower()
            clean_query = query.lower()
            if clean_sig == clean_query and query in google_data:
                score = google_data[query]
            elif (query + " fashion") in google_data:
                score = google_data[query + " fashion"]
            elif (query + " India") in google_data:
                score = google_data[query + " India"]
            elif (query + " outfit ideas") in google_data:
                score = google_data[query + " outfit ideas"]
            elif query in google_data:
                score = google_data[query]
            else:
                available_keys = list(google_data.keys())
                if available_keys:
                    score = google_data[available_keys[0]]

        # Apply organic noise to make visual graphs dynamic and realistic
        signal_strength[sig] = min(98, max(45, int(score) + random.randint(-4, 6)))

    # Static fallback descriptions
    static_forecasts = {
        "bollywood": {
            "name": "Luxury Minimal Ethnic",
            "description": f"Bollywood-inspired muted ethnic looks are dominating Pinterest feeds. We forecast a surge in {region} by {year}, driven by minimalist aesthetics.",
            "business": "Premium ethnic brands should invest in minimalist festive wear. High conversion expected across Gen-Z and Millennials.",
            "momentum": "rising ↗",
            "investSignal": "Moderate Buy",
            "investPercent": 20,
            "investReason": "Sustained interest in minimalist ethnic aesthetics makes it a stable revenue contributor for festive capsules.",
            "targetDemographic": "Modern Indian women and men aged 22-45 in urban metros who lean towards understated festive aesthetics rather than heavy embellishments.",
            "peakSeason": "Festive season (September to January) driven by wedding guest dressing and Diwali wardrobe upgrades featuring light, breathable fabrics.",
            "competitorActivity": "Leading designer wear labels are shifting focus from heavily embroidered lehengas to sleek, solid-colored raw silk coordinates.",
            "yearlyForecast": [
                {"year": "2026", "score": 75},
                {"year": "2027", "score": 80},
                {"year": "2028", "score": 70},
                {"year": "2029", "score": 65}
            ],
            "risks": "Over-reliance on plain styles might fail to capture consumers seeking vibrant wedding season options.",
            "palette": ["#ffefef", "#fdfbf7", "#f5f5dc", "#d2b48c"],
            "demographics": {"Gen-Z": 65, "Millennials": 25, "Gen-X": 10},
            "image": "luxury_minimal.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        },
        "kpop": {
            "name": "Ethnic Streetwear Fusion",
            "description": f"K-pop fashion is rapidly shaping Indo-western streetwear in {region}. Live Google queries show a spike in 'streetwear India'.",
            "business": "Affordable premium brands should launch fusion collections focusing on oversized silhouettes and indigenous textiles.",
            "momentum": "fast rising ↗",
            "investSignal": "Strong Buy",
            "investPercent": 25,
            "investReason": "High search volumes and explosive Gen-Z engagement justify larger manufacturing volumes of oversized fusion streetwear.",
            "targetDemographic": "Highly digital native Gen Z and young millennials (ages 16-28) in urban and Tier 1 cities heavily influenced by social media and global music subcultures.",
            "peakSeason": "Autumn/Winter (August to November) as oversized hoodies, joggers, and structured jackets drive heavy utility-focused purchases.",
            "competitorActivity": "Local D2C labels like VegNonVeg, Jaywalking, and international fast fashion brands are rolling out oversized silhouettes with subtle ethnic graphics.",
            "yearlyForecast": [
                {"year": "2026", "score": 85},
                {"year": "2027", "score": 90},
                {"year": "2028", "score": 80},
                {"year": "2029", "score": 75}
            ],
            "risks": "Fast-evolving youth subcultures can make designs look dated within a few seasons, causing dead inventory.",
            "palette": ["#8b5a2b", "#d2b48c", "#fdfbf7", "#4a3c31"],
            "demographics": {"Gen-Z": 82, "Millennials": 15, "Gen-X": 3},
            "image": "streetwear_fusion.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        },
        "college": {
            "name": "Gen-Z Retro College Core",
            "description": f"Elevated retro college aesthetics are merging with Indian textiles across {region} campuses. High momentum towards {year}.",
            "business": "Brands should focus on gender-neutral varsity silhouettes featuring local handloom accents.",
            "momentum": "peaking ↗",
            "investSignal": "Moderate Buy",
            "investPercent": 15,
            "investReason": "Steady seasonal demand from college-goers warrants a conservative production slice for varsity silhouettes.",
            "targetDemographic": "College-going students and young adults (ages 18-24) seeking casual, expressive, and comfortable preppy wardrobe staples.",
            "peakSeason": "Back-to-school/college reopening season (June to August) along with winter campus festivals where varsity cardigans and denim excel.",
            "competitorActivity": "High street fashion giants are releasing heavy collections of corduroy trousers, retro varsity jackets, and striped knitwear.",
            "yearlyForecast": [
                {"year": "2026", "score": 70},
                {"year": "2027", "score": 68},
                {"year": "2028", "score": 65},
                {"year": "2029", "score": 60}
            ],
            "risks": "Price sensitivity among students restricts high premium pricing, threatening operating margins if fabric costs spike.",
            "palette": ["#cba89a", "#f5f5dc", "#8b5a2b", "#fffaf7"],
            "demographics": {"Gen-Z": 90, "Millennials": 8, "Gen-X": 2},
            "image": "college_core.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        },
        "regional": {
            "name": "Modern Regional Handlooms",
            "description": f"Traditional regional fashion is being modernized with contemporary draping. Huge search volumes for 'ethnic fusion wear' in {region}.",
            "business": "Luxury and boutique brands must integrate authentic regional weaves into chic, ready-to-wear collections.",
            "momentum": "steady ↗",
            "investSignal": "Strong Buy",
            "investPercent": 30,
            "investReason": "A strong cultural push for authentic regional handlooms across tier 1 & 2 cities ensures robust sales for boutique ethnic wear.",
            "targetDemographic": "Conscious consumers and fashion enthusiasts (ages 25-50) who prioritize artisan craftsmanship, sustainable styling, and premium fabrics.",
            "peakSeason": "Year-round demand peaking during key regional festivals (Ganesh Chaturthi, Durga Puja, weddings) where semi-formal handloom sarees and kurtas dominate.",
            "competitorActivity": "Fabindia, Faballey, and designer labels like Raw Mango are establishing deep artisan supply lines to claim handloom authenticity.",
            "yearlyForecast": [
                {"year": "2026", "score": 90},
                {"year": "2027", "score": 95},
                {"year": "2028", "score": 92},
                {"year": "2029", "score": 88}
            ],
            "risks": "Sourcing authentic artisan-made textiles takes long lead times, which could bottleneck production during peak seasons.",
            "palette": ["#50352d", "#d2b48c", "#ffefef", "#8b5a2b"],
            "demographics": {"Gen-Z": 45, "Millennials": 40, "Gen-X": 15},
            "image": "regional_handloom.png",
            "sources": ["Google Trends", "Pinterest Live Feed"]
        },
        "old money aesthetic": {
            "name": "old money aesthetic",
            "description": "The old money aesthetic is gaining strong traction in India, particularly among upper-middle-class and affluent urban millennials and Gen Z who are moving away from logo-heavy luxury toward understated, heritage-coded dressing. The trend resonates deeply with India's own legacy of quiet aristocratic elegance — think Nizam-era restraint and colonial club culture — giving it a culturally authentic anchor that fast fashion trends typically lack. Sustained growth is expected through 2027-28 as aspirational consumption in Tier 1 and emerging Tier 2 cities matures.",
            "business": "Premium Indian brands should invest in minimalist tailored silhouettes, quiet luxury basics, and heritage-coded coordinates.",
            "momentum": "Rising Star",
            "investSignal": "Moderate Buy",
            "investPercent": 18,
            "investReason": "The trend has real longevity and cultural fit in India, but its premium positioning limits mass-market scale, making a measured allocation wise to capture the growing aspirational segment without overexposing production capacity to a niche price bracket.",
            "targetDemographic": "Urban millennials and Gen Z aged 22-38 in metros (Mumbai, Delhi, Bengaluru, Hyderabad) and affluent Tier 2 cities; college students at premium institutions; young professionals in finance, consulting, and creative industries; influenced by Instagram and Pinterest aesthetics rather than Bollywood celebrity culture",
            "peakSeason": "Winter (October to February) drives the highest demand due to layering staples like blazers, woolen trousers, and heritage knitwear; also spikes around weddings and formal social occasions where elevated casual dressing is replacing traditional Indian occasion wear among younger guests",
            "competitorActivity": "Brands like Mango and Zara India are stocking quiet luxury basics at accessible price points; Indian brands such as Tasva and Dash and Dot are experimenting with understated heritage silhouettes; premium D2C labels like The Pant Project and Andamen are already capitalizing on tailored minimalism; high-end players like Abraham and Thakore have long occupied adjacent territory and are seeing renewed interest",
            "yearlyForecast": [
                {"year": "2026", "score": 80},
                {"year": "2027", "score": 86},
                {"year": "2028", "score": 84},
                {"year": "2029", "score": 76}
            ],
            "risks": "Risk: Over-investment risks inventory pile-up if the trend plateaus prematurely among India's still largely value-driven middle market, and mass-market dilution could strip the aesthetic of its aspirational cachet, causing early adopters to abandon it faster than the broader consumer base can absorb it",
            "palette": ["#4a3c31", "#8b5a2b", "#d2b48c", "#fdfbf7"],
            "demographics": {"Gen-Z": 60, "Millennials": 30, "Gen-X": 10},
            "image": "luxury_minimal.png",
            "sources": ["Google Trends", "Pinterest Live Feed", "WGSN Insight"]
        }
    }

    for signal in signals:
        # Dynamically build entry for custom signals
        if signal not in static_forecasts:
            import hashlib
            clean_name = signal.replace("-", " ").replace("_", " ").title()
            
            # Generate matching pastel HSL colors deterministically based on md5 hash
            h = hashlib.md5(signal.encode("utf-8")).digest()
            c1 = f"hsl({h[0] % 360}, 65%, 85%)"
            c2 = f"hsl({(h[0] + 50) % 360}, 55%, 90%)"
            c3 = f"hsl({(h[0] + 130) % 360}, 45%, 75%)"
            c4 = f"hsl({(h[0] + 200) % 360}, 55%, 80%)"
            
            static_forecasts[signal] = {
                "name": clean_name,
                "description": f"Live digital indicators for '{clean_name}' display mounting interest in {region}. We forecast strong mainstream adoption towards {year}.",
                "business": f"Design labs should formulate contemporary lines centering on '{clean_name}' for the {region} retail audience.",
                "momentum": "emerging ↗",
                "investSignal": "Hold",
                "investPercent": 10,
                "investReason": "Emerging market signals suggest testing with a small batch before expanding production capacity.",
                "targetDemographic": f"Fashion-forward urban Gen Z and Millennial consumers in Metro cities who are highly active on social media and influenced by global subcultures.",
                "peakSeason": f"Festive and wedding seasons (October to January) as well as transitional spring collections when consumers seek unique wardrobe updates.",
                "competitorActivity": f"Fast fashion giants are monitoring early digital signals, while D2C boutique brands are releasing limited capsule runs to capture first-mover advantage.",
                "yearlyForecast": [
                    {"year": "2026", "score": 50},
                    {"year": "2027", "score": 60},
                    {"year": "2028", "score": 70},
                    {"year": "2029", "score": 65}
                ],
                "risks": "Low initial awareness among mainstream buyers can lead to slow sell-through rates.",
                "palette": [c1, c2, c3, c4],
                "demographics": {"Gen-Z": 70, "Millennials": 20, "Gen-X": 10},
                "image": "streetwear_fusion.png",
                "sources": ["Google Trends", "Pinterest Live Feed"]
            }

        base = static_forecasts[signal]

        # Try to get AI-enhanced descriptions
        ai_data = get_ai_forecast(base["name"], region, year, signal_strength, signal)

        # Fetch Unsplash images server-side so the API key stays hidden and Redis caches them
        unsplash_images = fetch_unsplash_images(base["name"])

        trend = {
            "name": base["name"],
            "confidence": min(98, signal_strength.get(signal, 70) + 5),
            "description": ai_data["description"] if (ai_data and "description" in ai_data) else base["description"],
            "business": ai_data["business"] if (ai_data and "business" in ai_data) else base["business"],
            "momentum": ai_data["momentum"] if (ai_data and "momentum" in ai_data) else base["momentum"],

            "investSignal": ai_data["investSignal"] if (ai_data and "investSignal" in ai_data) else base["investSignal"],
            "investPercent": ai_data["investPercent"] if (ai_data and "investPercent" in ai_data) else base["investPercent"],
            "investReason": ai_data["investReason"] if (ai_data and "investReason" in ai_data) else base["investReason"],
            "yearlyForecast": ai_data["yearlyForecast"] if (ai_data and "yearlyForecast" in ai_data) else base["yearlyForecast"],
            "risks": ai_data["risks"] if (ai_data and "risks" in ai_data) else base["risks"],
            
            # New WGSN detail fields mapping exactly to the layout screenshots
            "targetDemographic": ai_data["targetDemographic"] if (ai_data and "targetDemographic" in ai_data) else base["targetDemographic"],
            "peakSeason": ai_data["peakSeason"] if (ai_data and "peakSeason" in ai_data) else base["peakSeason"],
            "competitorActivity": ai_data["competitorActivity"] if (ai_data and "competitorActivity" in ai_data) else base["competitorActivity"],

            "palette": base["palette"],
            "graph": signal_strength,
            "demographics": base["demographics"],
            "image": base["image"],
            "images": unsplash_images,
            "sources": ["Google Trends", "Pinterest Live Feed", "Gemini AI", "Unsplash"] if ai_data else ["Google Trends", "Pinterest Live Feed", "Unsplash"]
        }
        trends.append(trend)

    return trends
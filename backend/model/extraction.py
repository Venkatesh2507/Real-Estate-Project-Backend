import re
import emoji

def normalize_text(text: str) -> str:
    # 1. Convert emoji numbers (1️⃣2️⃣3️⃣ etc.) to digits
    text = re.sub(r"(\d)\uFE0F?\u20E3", r"\1", text)

    # 2. Remove emojis (keep text)
    text = emoji.replace_emoji(text, replace=" ")

    # 3. Lowercase
    text = text.lower()

    # 4. Normalize money formats: 42k, 42 k, ₹42k → 42000
    text = re.sub(
        r"(₹?\s*\d+)\s*k\b",
        lambda m: re.sub(r"\D", "", m.group(1)) + "000",
        text
    )

    # 5. Normalize area units
    text = re.sub(r"\bsq\s*ft\b|\bsqft\b|\bsq ft\b", "sqft", text)

    # 6. Remove non-informational symbols
    text = re.sub(r"[^a-z0-9₹.\s]", " ", text)

    # 7. Collapse spaces
    return re.sub(r"\s+", " ", text).strip()


def extract_fields(text: str) -> dict:
    original_text = text  # Keep original to extract location with emoji markers
    normalized_text = normalize_text(text)
    data = {}
    

    # BHK (works for 1–10 BHK)
    bhk = re.search(r"\b(\d{1,2})\s*bhk\b", normalized_text)
    if bhk:
        data["typeBHK"] = f"{bhk.group(1)}BHK"

    # Transaction
    if re.search(r"\b(rent|lease)\b", normalized_text):
        data["transaction"] = "rent"
    elif re.search(r"\b(sale|sell|buy|outright)\b", normalized_text):
        data["transaction"] = "sale"

    # Price - extract from normalized text first, or from original if not found
    # Try patterns: 42000, 42k, ₹42000, ₹42k
    price_match = re.search(r"₹?\s*(\d+)\s*k\b", original_text, re.IGNORECASE)
    if price_match:
        # Found "42k" format - convert to full amount
        data["price"] = int(price_match.group(1)) * 1000
    else:
        # Try to find any 4+ digit number in normalized text
        price_match = re.search(r"(\d{4,})", normalized_text)
        if price_match:
            price_val = int(price_match.group(1))
            # Only accept if it's a realistic price (1000 to 100M)
            if 1000 < price_val < 100000000:
                data["price"] = price_val

    # Area
    area = re.search(r"(\d{3,5})\s*sqft", normalized_text)
    if area:
        data["area_sqft"] = int(area.group(1))

    # Phone
    phone = re.search(r"\b([6-9]\d{9})\b", normalized_text)
    if phone:
        data["phone"] = phone.group(1)

    # Location - extract from ORIGINAL text to capture emoji markers like 📍
    location_match = re.search(r"(?:📍|in|at|near|opp|behind)\s+([a-zA-Z ]{3,30})", original_text)
    if location_match:
        data["location"] = location_match.group(1).strip()
    else:
        # Fallback to patterns on normalized text
        location_patterns = [
            r"\b(?:in|at|near|opp|behind)\s+([a-z][a-z ]{2,30})",
            r"\b([a-z][a-z ]{2,30})\s+(?:east|west|north|south)\b"
        ]

        for pattern in location_patterns:
            match = re.search(pattern, normalized_text)
            if match:
                data["location"] = match.group(1).strip()
                break

    return data


def extract_location(text: str):
    # Location must appear AFTER a location indicator
    pattern = r"(?:📍|in|at|near|opp|behind)\s+([a-z ]{3,30})(?:\b|$)"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None

import json
import csv

PRIMARY_SCORE = 95
STRONG_SECONDARY = 70
WEAK_SECONDARY = 45
LOW_SCORE = 5

BASE_COLORS = [
    "Violet", "Blue", "Green", "Red", "Yellow", "Orange",
    "Purple", "Pink", "White", "Black", "Grey", "Brown"
]

def clamp(val, lo=0, hi=100):
    return max(lo, min(hi, val))

def boost(scores, base, amount):
    scores[base] = clamp(scores[base] + amount)

def contains_any(text, keywords):
    text = text.lower()
    return any(k in text for k in keywords)

def apply_brightness(scores, brightness):
    if brightness == "high":
        boost(scores, "White", 5)
    elif brightness == "low":
        boost(scores, "Black", 5)
    elif brightness == "very-low":
        boost(scores, "Black", 10)

def apply_saturation(scores, saturation):
    if saturation == "very-high":
        boost(scores, "Red", 5)
        boost(scores, "Blue", 5)
        boost(scores, "Purple", 5)
    elif saturation == "low":
        boost(scores, "Grey", 5)
    elif saturation == "very-low":
        boost(scores, "Grey", 10)

def apply_temperature(scores, temperature):
    if temperature == "warm":
        boost(scores, "Red", 5)
        boost(scores, "Orange", 5)
        boost(scores, "Yellow", 5)
    elif temperature == "cool":
        boost(scores, "Blue", 5)
        boost(scores, "Violet", 5)
    elif temperature == "neutral":
        boost(scores, "Grey", 5)

def apply_semantic_boosts(scores, name, associations):
    text = f"{name} {' '.join(associations)}".lower()

    if contains_any(text, ["noir", "shadow", "ink", "eclipse", "void"]):
        boost(scores, "Black", 10)

    if contains_any(text, ["frost", "ice", "glacier", "snow"]):
        boost(scores, "White", 10)
        boost(scores, "Blue", 5)

    if contains_any(text, ["ember", "molten", "flame", "fire"]):
        boost(scores, "Red", 10)
        boost(scores, "Orange", 5)

    if contains_any(text, ["metal", "metallic", "chrome", "steel", "titanium"]):
        boost(scores, "Grey", 10)

    if contains_any(text, ["earth", "wood", "leather", "soil", "clay"]):
        boost(scores, "Brown", 10)

    if contains_any(text, ["pastel", "porcelain", "silk", "linen"]):
        boost(scores, "White", 10)

    if contains_any(text, ["gemstone", "jewel", "crystal", "opal"]):
        boost(scores, "Violet", 5)
        boost(scores, "Blue", 5)
        boost(scores, "Red", 5)

def apply_conflict_suppression(scores, color):
    associations = color.get("associations", [])

    if "pastel" in associations:
        scores["Black"] = min(scores["Black"], 10)

    if color["primary_base"] == "Brown":
        scores["Blue"] = min(scores["Blue"], 10)

def apply_neutral_support(scores, color):
    primary = color["primary_base"]

    if primary in ["Violet", "Purple", "Blue", "Red"]:
        scores["White"] = max(scores["White"], 20)

    if scores["Black"] >= 70:
        scores["Grey"] = max(scores["Grey"], 20)

    if scores["Grey"] >= 70:
        scores["White"] = max(scores["White"], 15)

    if primary in ["Green", "Brown"]:
        scores["Brown"] = max(scores["Brown"], 20)
        scores["Grey"] = max(scores["Grey"], 15)

def generate_scores(color):
    scores = {base: LOW_SCORE for base in BASE_COLORS}

    scores[color["primary_base"]] = PRIMARY_SCORE

    for idx, base in enumerate(color.get("secondary_bases", [])):
        if base not in scores:
            continue
        scores[base] = STRONG_SECONDARY if idx == 0 else WEAK_SECONDARY

    apply_brightness(scores, color.get("brightness"))
    apply_saturation(scores, color.get("saturation"))
    apply_temperature(scores, color.get("temperature"))
    apply_semantic_boosts(scores, color["name"], color.get("associations", []))
    apply_conflict_suppression(scores, color)
    apply_neutral_support(scores, color)

    for base in scores:
        scores[base] = clamp(scores[base])

    return scores
def main():
    with open("dataset/real_world_colors.json", "r", encoding="utf-8") as f:
        colors = json.load(f)

    with open("dataset/base_realworld_scores.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["real_world_color"] + BASE_COLORS)

        for color in colors:
            scores = generate_scores(color)
            writer.writerow(
                [color["name"]] + [scores[base] for base in BASE_COLORS]
            )

    print("base_realworld_scores.csv generated...finally---yeah")

if __name__ == "__main__":
    main()
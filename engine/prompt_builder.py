import random
import json

with open("dataset/enhancements.json", "r", encoding="utf-8") as f:
    enhancements = json.load(f)

ENH_BY_NAME = {e["name"]: e for e in enhancements}

def assemble_prompt(base_color, theme, recommendations, max_enhancements=2):
    if not recommendations:
        return "A stylized outfit with balanced color harmony."

    top = recommendations[0]
    color_name = top["color"]

    enhancement_phrases = []

    for enh in ["Electric", "Ghost", "Metallic", "Velvet", "Matte", "Gloss"]:
        if random.random() < 0.3:
            enhancement_phrases.append(enh.lower())

        if len(enhancement_phrases) >= max_enhancements:
            break

    enh_text = ""
    if enhancement_phrases:
        enh_text = " with " + " and ".join(enhancement_phrases) + " accents"

    prompt = (
        f"A {theme.lower()} outfit featuring {color_name} "
        f"{base_color.lower()} tones{enh_text}, "
        f"high detail, realistic fabric and materials, cinematic lighting."
    )

    return prompt
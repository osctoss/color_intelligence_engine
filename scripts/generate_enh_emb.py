import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler

TEXT_WEIGHT = 0.5
ATTRIBUTE_WEIGHT = 0.3
THEME_WEIGHT = 0.2

TEXT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

THEMES = [
    "Sci-Fi", "Dark", "Royal", "Fantasy", "Mythic",
    "Natural", "Cinematic", "Minimal", "Historic", "Luxury"
]

ATTRIBUTE_KEYS = [
    "brightness_shift",
    "saturation_shift",
    "temperature_shift",
    "texture",
    "energy_level"
]
with open("dataset/enhancements.json", "r", encoding="utf-8") as f:
    enhancements = json.load(f)

with open("dataset/theme_enhancement_weights.json", "r", encoding="utf-8") as f:
    theme_weights_raw = json.load(f)

theme_weight_map = {
    entry["theme"]: entry["enhancement_weights"]
    for entry in theme_weights_raw
}
texts = []
enhancement_names = []

for enh in enhancements:
    name = enh["name"]
    category = enh["category"]
    texture = enh.get("texture", "")
    energy = enh.get("energy_level", "")
    desc = f"{name} {category} {texture} {energy}"

    texts.append(desc)
    enhancement_names.append(name)

model = SentenceTransformer(TEXT_MODEL_NAME)
text_embeddings = model.encode(texts, show_progress_bar=True)

attribute_vectors = []

for enh in enhancements:
    vec = []
    for key in ATTRIBUTE_KEYS:
        val = enh.get(key, "neutral")
        vec.append(hash(val) % 1000) 
    attribute_vectors.append(vec)

attribute_vectors = np.array(attribute_vectors, dtype=float)

attribute_vectors = MinMaxScaler().fit_transform(attribute_vectors)

attr_embeddings = np.zeros_like(text_embeddings)
attr_embeddings[:, :attribute_vectors.shape[1]] = attribute_vectors

theme_vectors = []

for enh in enhancements:
    name = enh["name"]
    vec = []
    for theme in THEMES:
        weight = theme_weight_map.get(theme, {}).get(name, 0.5)
        vec.append(weight)
    theme_vectors.append(vec)

theme_vectors = np.array(theme_vectors)
theme_vectors = MinMaxScaler().fit_transform(theme_vectors)
theme_embeddings = np.zeros_like(text_embeddings)
theme_embeddings[:, :theme_vectors.shape[1]] = theme_vectors

final_embeddings = (
    TEXT_WEIGHT * text_embeddings +
    ATTRIBUTE_WEIGHT * attr_embeddings +
    THEME_WEIGHT * theme_embeddings
)

np.save("dataset/enhancement_embeddings.npy", final_embeddings)

json_out = []
for idx, name in enumerate(enhancement_names):
    json_out.append({
        "enhancement": name,
        "embedding": final_embeddings[idx].tolist()
    })

with open("dataset/enhancement_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(json_out, f, indent=2)

print("Enhancements generated...")
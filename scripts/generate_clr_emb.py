import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler

TEXT_WEIGHT = 0.7
SCORE_WEIGHT = 0.3

BASE_COLORS = [
    "Violet", "Blue", "Green", "Red", "Yellow", "Orange",
    "Purple", "Pink", "White", "Black", "Grey", "Brown"
]

TEXT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

with open("dataset/real_world_colors.json", "r", encoding="utf-8") as f:
    real_world_colors = json.load(f)

scores_df = pd.read_csv("dataset/base_realworld_scores.csv")

texts = []
color_names = []

for color in real_world_colors:
    name = color["name"]
    description = color.get("description", "")
    associations = " ".join(color.get("associations", []))

    text = f"{name} {description} {associations}"
    texts.append(text)
    color_names.append(name)

model = SentenceTransformer(TEXT_MODEL_NAME)
text_embeddings = model.encode(texts, show_progress_bar=True)

score_vectors = scores_df[BASE_COLORS].values.astype(float)

scaler = MinMaxScaler()
score_vectors = scaler.fit_transform(score_vectors)

score_embeddings = np.zeros_like(text_embeddings)
score_embeddings[:, :len(BASE_COLORS)] = score_vectors

final_embeddings = (
    TEXT_WEIGHT * text_embeddings +
    SCORE_WEIGHT * score_embeddings
)

np.save("dataset/color_embeddings.npy", final_embeddings)

embeddings_json = []

for idx, name in enumerate(color_names):
    embeddings_json.append({
        "color": name,
        "embedding": final_embeddings[idx].tolist()
    })

with open("dataset/color_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embeddings_json, f, indent=2)

print("Color embeddings generated ...Npy+ JSON")
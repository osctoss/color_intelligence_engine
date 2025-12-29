import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE_WEIGHT = 0.5
EMBEDDING_WEIGHT = 0.3
THEME_WEIGHT = 0.2

BASE_COLORS = [
    "Violet", "Blue", "Green", "Red", "Yellow", "Orange",
    "Purple", "Pink", "White", "Black", "Grey", "Brown"
]

THEMES = [
    "Sci-Fi", "Dark", "Royal", "Fantasy", "Mythic",
    "Natural", "Cinematic", "Minimal", "Historic", "Luxury"
]

scores_df = pd.read_csv("dataset/base_realworld_scores.csv")

with open("dataset/real_world_colors.json", "r", encoding="utf-8") as f:
    real_world_colors = json.load(f)

with open("dataset/theme_enhancement_weights.json", "r", encoding="utf-8") as f:
    theme_weights_raw = json.load(f)

theme_weights = {
    t["theme"]: t["enhancement_weights"]
    for t in theme_weights_raw
}

color_embeddings = np.load("dataset/color_embeddings.npy")
enhancement_embeddings = np.load("dataset/enhancement_embeddings.npy")

with open("dataset/enhancements.json", "r", encoding="utf-8") as f:
    enhancements = json.load(f)

enhancement_index = {
    e["name"]: idx for idx, e in enumerate(enhancements)
}

def recommend(base_color, theme, top_k=10):
    assert base_color in BASE_COLORS
    assert theme in THEMES

    candidates = scores_df[scores_df[base_color] >= 45].copy()
    candidates["base_norm"] = candidates[base_color] / 100.0

    enh_weights = theme_weights.get(theme, {})
    vectors = []
    weights = []

    for enh, w in enh_weights.items():
        if enh in enhancement_index:
            vectors.append(enhancement_embeddings[enhancement_index[enh]])
            weights.append(w)

    theme_vector = np.average(vectors, axis=0, weights=weights)

    color_idxs = candidates.index.tolist()
    color_vecs = color_embeddings[color_idxs]

    embed_sims = cosine_similarity(color_vecs, [theme_vector]).flatten()
    embed_sims = (embed_sims + 1)/2  

    candidates["final_score"] = (
        BASE_WEIGHT * candidates["base_norm"] +
        EMBEDDING_WEIGHT * embed_sims +
        THEME_WEIGHT * candidates["base_norm"] 
    )
    results = candidates.sort_values("final_score", ascending=False).head(top_k)

    output = []
    for _, row in results.iterrows():
        reasons = [
            f"Strong {base_color} base affinity ({int(row[base_color])})"
        ]
        if embed_sims[candidates.index.get_loc(row.name)] > 0.75:
            reasons.append("High semantic compatibility with theme")
        if row["base_norm"] > 0.8:
            reasons.append("Primary base color match")

        output.append({
            "color": row["real_world_color"],
            "score": round(float(row["final_score"]), 3),
            "reasons": reasons
        })

    return output
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request
from engine.recommender import recommend
from engine.prompt_builder import assemble_prompt

app = Flask(__name__)

BASE_COLORS = [
    "Violet", "Blue", "Green", "Red", "Yellow", "Orange",
    "Purple", "Pink", "White", "Black", "Grey", "Brown"
]

THEMES = [
    "Sci-Fi", "Dark", "Royal", "Fantasy", "Mythic",
    "Natural", "Cinematic", "Minimal", "Historic", "Luxury"
]

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    prompt = None

    if request.method == "POST":
        base_color = request.form["base_color"]
        theme = request.form["theme"]
        top_k = int(request.form.get("top_k", 5))

        results = recommend(base_color, theme, top_k)
        prompt = assemble_prompt(base_color, theme, results)

    return render_template(
        "index.html",
        base_colors=BASE_COLORS,
        themes=THEMES,
        results=results,
        prompt=prompt
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
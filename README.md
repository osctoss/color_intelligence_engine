🎨 Color Intelligence Engine

A hybrid rule-based + ML-assisted color recommendation system designed to generate high-quality, real-world color palettes and cinematic prompt descriptions for generative AI tools (Mainly for Gemini Ai Pro (Veo 3)).

This project bridges human color theory, real-world semantics, and machine-learned embeddings to produce visually coherent, explainable, and context-aware color recommendations.


---

🚀 What This Project Does

Given:

A base color (e.g. Blue, Purple)

A theme / genre (e.g. Sci-Fi, Mythic, Luxury)


The system:

1. Recommends the best real-world color variants


2. Ranks them using hybrid ML logic


3. Generates a cinematic, model-friendly natural language prompt


4. Displays everything through a modern Flask UI




---

🧠 Why This Project Exists

Generative AI models understand real-world concepts (e.g. Amethyst, Titanium Blue, Velvet Black) far better than abstract color names like “light purple” or “dark blue”.

This engine:

Translates simple user intent → semantically rich color language

Produces outputs that align better with AI visual reasoning

Remains explainable and controllable, not a black box



---

🏗️ System Architecture (High Level)

User Input
   ↓
Base Color + Theme
   ↓
Rule-Based Filtering (Ontology)
   ↓
ML Embedding Similarity (Soft Ranking)
   ↓
Final Ranking + Explanation
   ↓
Prompt Assembly
   ↓
Flask UI Output


---

📊 Datasets Overview

Core (The basic database is manually designed / The choice varies)

Dataset	Purpose

base_colours.json	User-facing base color anchors
real_world_colors.json	Grounded real-world color definitions
base_realworld_scores.csv	Base ↔ real-world compatibility scores
enhancements.json	Style & texture transformations
theme_enhancement_weights.json	Theme-context logic


Derived (ML-Generated, Reproducible)

Dataset	Purpose

Color Embeddings	Semantic similarity between colors
Enhancement Embeddings	Contextual similarity between enhancements


---

🤖 Where Machine Learning Is Used

This project uses ML correctly and intentionally, not everywhere.

✅ ML is used for:

Text embeddings using a pretrained transformer

Semantic similarity between colors

Soft ranking via cosine similarity

Contextual alignment between themes and enhancements


❌ ML is NOT used for:

Basic color theory rules

Ontology constraints

Hard business logic


This hybrid approach mirrors real-world production systems.


---

🧩 Recommendation Logic

Final score is a weighted combination of:

Final Score =
0.50 × Base Compatibility
0.30 × Embedding Similarity
0.20 × Theme Alignment

This ensures:

Strong base color consistency

Semantic richness

Context awareness


---

📁 Project Structure

color_intelligence_engine/
│
├── dataset/
│   ├── base_colours.json
│   ├── real_world_colors.json
│   ├── base_realworld_scores.csv
│   ├── enhancements.json
│   └── theme_enhancement_weights.json
│
├── engine/
│   ├── __init__.py
│   ├── recommender.py
│   └── prompt_builder.py
│
├── web/
│   ├── app.py
│   ├── templates/index.html
│   └── static/style.css
│
├── scripts/
│   ├── generate_csv.py
│   ├── generate_clr_emb.py
│   └── generate_enh_emb.py
│
├── requirements.txt
├── README.md
└── .gitignore


---

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone <https://github.com/osctoss/color_intelligence_engine>
cd color_intelligence_engine

2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt


---

▶️ Running the Application

python web/app.py

---

🧪 Reproducibility

To regenerate derived datasets:

python scripts/generate_csv.py
python scripts/generate_clr_emb.py
python scripts/generate_enh_emb.py


---

🧠 Example Output

Input

Base Color: Blue

Theme: Sci-Fi


Output

Titanium Blue

Cobalt Royale

Glacier Blue


Generated Prompt

A sci-fi outfit featuring Titanium Blue tones with electric and metallic accents, high detail, realistic fabric and cinematic lighting.


---

🎯 Future Enhancements

Auto-generate HEX values from dataset

User feedback → learning-to-rank

Public deployment (Render / Railway)

REST API endpoints

Visual enhancement previews



---

🧑‍💻 Author Notes

This project was designed to reflect how real ML systems are built:

Human intelligence + machine intelligence

Explainability over blind training

Reproducibility over static artifacts


---

👤 Author

Manish Patel (Osctoss)
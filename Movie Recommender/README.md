 🎬 Movie Recommender System

A content-based Movie Recommender System built with Python, Streamlit, and the TMDb API. The application uses Cosine Similarity on processed movie tags (genres, keywords, cast, and crew) to recommend top 5 similar movies complete with their official posters.

🚀 **Live Demo:** [Click here to launch the app](https://machinelearningprojects-626eztk3okegpgnjemvqdx.streamlit.app/)

---

## 🛠️ Features
- **Interactive UI:** Simple drop-down selection powered by Streamlit.
- **Content-Based Filtering:** Recommends 5 relevant movies based on vector similarity scores.
- **Dynamic Poster Fetching:** Fetches real-time movie posters directly from TMDb API.
- **Optimized Storage:** Uses Gzip compression (`cs.pkl.gz`) to store and load the similarity matrix efficiently without exceeding repository storage limits.

---

## 🧰 Tech Stack
- **Language:** Python
- **Frontend/Deployment:** Streamlit, Streamlit Community Cloud
- **Machine Learning:** Scikit-Learn (Cosine Similarity), Pandas, NumPy
- **APIs:** The Movie Database (TMDb) API
- **Version Control:** Git, GitHub

---

## 📁 Repository Structure
```text
├── app.py                         # Streamlit web application
├── Movie_Recommender_System.ipynb # Data preprocessing & model building notebook
├── movies_dict.pkl                # Pickled dictionary containing movie metadata
├── cs.pkl.gz                      # Compressed cosine similarity matrix
├── requirements.txt               # Dependencies for cloud deployment
└── README.md                      # Project documentation

import pickle
import gzip
import pandas as pd
import requests
import streamlit as st

# Configure wide layout and browser tab title
st.set_page_config(
    page_title="Movie Recommender", page_icon="🎬", layout="wide"
)

# Custom Cinema-Themed Dark UI CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b0c10 0%, #1f2833 50%, #0b0c10 100%);
        color: #ffffff;
    }
    h1 {
        color: #e50914 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-shadow: 0px 0px 20px rgba(229, 9, 20, 0.7);
        text-align: center;
        margin-bottom: 30px;
    }
    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 10px !important;
    }
    .stButton {
        width: 100%;
        margin-top: 0px !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #e50914 0%, #b20710 100%);
        color: white;
        border-radius: 8px;
        border: none;
        height: 42px;
        font-weight: 700;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff0a16 0%, #d60812 100%);
        box-shadow: 0 6px 18px rgba(229, 9, 20, 0.7);
        transform: translateY(-1px);
    }
    .movie-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
        margin-top: 10px;
        text-align: center;
        line-height: 1.3;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Fetch poster with fallback logic to prevent app crashes
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception:
        pass
    # Return placeholder image if fetch fails or poster is missing
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"


# Cache pickle loading to avoid memory lag
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # Load compressed similarity file
    with gzip.open('cs.pkl.gz', 'rb') as f:
        similarity = pickle.load(f)

    return movies, similarity

movies, similarity = load_data()


# Recommendation logic function (Handles 'movie_id' vs 'id' key mismatches)
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        row = movies.iloc[i[0]]

        # Safe key lookup regardless of exported dataframe column name
        if 'movie_id' in row:
            movie_id = row['movie_id']
        elif 'id' in row:
            movie_id = row['id']
        else:
            movie_id = row.name

        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(row['title'])

    return recommended_movie_names, recommended_movie_posters


# App Header
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Selection controls layout
col_select, col_btn = st.columns([4, 1])

with col_select:
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list,
        label_visibility="collapsed",
    )

with col_btn:
    recommend_clicked = st.button("Show Recommendation 🍿")

# Display Recommendations Grid
if recommend_clicked:
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie
    )

    st.markdown(
        "<h3 style='color: #ffffff; margin-top: 30px; margin-bottom: 20px;'>Recommended Movies:</h3>",
        unsafe_allow_html=True,
    )

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(
                recommended_movie_posters[idx], use_container_width=True
            )
            st.markdown(
                f'<div class="movie-title">{recommended_movie_names[idx]}</div>',
                unsafe_allow_html=True,
            )
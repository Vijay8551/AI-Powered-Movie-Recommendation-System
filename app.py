import streamlit as st 
import pickle
import pandas as pd
import urllib.parse
import json
import requests
import os

# 1. Page Configuration
st.set_page_config(
    page_title="PopcornPick - AI Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Cached Data Loading
@st.cache_data
def load_metadata():
    df = pd.read_csv('tmdb_5000_movies.csv')
    return df

@st.cache_resource
def load_similarity_data():
    with open('movies_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    return movies, similarity

metadata = load_metadata()
movies, similarity = load_similarity_data()

# 3. Helper Functions
def parse_genres(genres_str):
    try:
        genres = json.loads(genres_str)
        return [g['name'] for g in genres]
    except Exception:
        return []

def parse_year(release_date):
    if pd.isna(release_date):
        return "N/A"
    return str(release_date).split('-')[0]

def get_svg_poster(title, genre="Movie"):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 750" width="100%" height="100%">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FF6B35;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grad)" />
        <rect width="90%" height="93%" x="5%" y="3.5%" rx="20" fill="#090d16" opacity="0.9" />
        <text x="50%" y="32%" font-family="'Outfit', 'Inter', sans-serif" font-size="70" font-weight="bold" fill="#ffffff" opacity="0.12" text-anchor="middle">🍿</text>
        <text x="50%" y="48%" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="800" fill="#ffffff" text-anchor="middle">
            {title[:16] + '...' if len(title) > 16 else title}
        </text>
        <text x="50%" y="56%" font-family="'Outfit', 'Inter', sans-serif" font-size="16" font-weight="600" fill="#94a3b8" text-anchor="middle">
            {genre}
        </text>
        <rect width="60%" height="8%" x="20%" y="78%" rx="20" fill="url(#grad)" opacity="0.9" />
        <text x="50%" y="83%" font-family="'Outfit', 'Inter', sans-serif" font-size="14" font-weight="bold" fill="#ffffff" text-anchor="middle">POPCORNPICK AI</text>
    </svg>"""
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)

def fetch_poster(movie_id, title, genre="Movie"):
    url = f"https://api.tmdb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        pass
    return get_svg_poster(title, genre)


def recommend_movies_engine(movie_title, filter_genre="All"):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    sorted_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    
    recommend_list = []
    for i in sorted_indices:
        if i[0] == movie_index:
            continue
        
        m_id = movies.iloc[i[0]].movie_id
        meta_row = metadata[metadata['id'] == m_id]
        if not meta_row.empty:
            row = meta_row.iloc[0]
            genres = parse_genres(row['genres'])
            
            if filter_genre == "All" or filter_genre in genres:
                match_percentage = min(99, max(55, int(i[1] * 100) + 40))
                recommend_list.append((row, match_percentage))
                if len(recommend_list) == 6:
                    break
    return recommend_list

def generate_text_report(recommendations, selected_movie, selected_genre):
    report = "="*50 + "\n"
    report += "         POPCORNPICK AI RECOMMENDATION REPORT\n"
    report += "="*50 + "\n\n"
    report += f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Selected Movie: {selected_movie}\n"
    if selected_genre != "All":
        report += f"Genre Filter: {selected_genre}\n"
    report += "\n" + "-"*50 + "\n"
    report += f"{'Rank':<5} | {'Movie Title':<28} | {'Match %':<8}\n"
    report += "-"*50 + "\n"
    for idx, (row, match_pct) in enumerate(recommendations, 1):
        title = row['title']
        title_truncated = title[:26] + ".." if len(title) > 26 else title
        report += f"{idx:<5} | {title_truncated:<28} | {match_pct:>6}%\n"
    report += "-"*50 + "\n\n"
    report += "Thanks for using PopcornPick! 🍿\n"
    return report

# 4. Global Stylesheet (CSS Injection)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Main Styling */
.stApp {
    font-family: 'Outfit', sans-serif;
    background-color: #05050c !important;
    background-image: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #05050c 50%),
                      radial-gradient(circle at 80% 80%, #3b0764 0%, #05050c 50%) !important;
    color: #f8fafc;
}

/* Glowing Blob Elements */
.glowing-blob-1 {
    position: fixed;
    top: 10%;
    left: -5%;
    width: 450px;
    height: 450px;
    background: #8B5CF6;
    filter: blur(120px);
    opacity: 0.18;
    border-radius: 50%;
    z-index: -1;
    pointer-events: none;
}
.glowing-blob-2 {
    position: fixed;
    bottom: 10%;
    right: -5%;
    width: 500px;
    height: 500px;
    background: #FF6B35;
    filter: blur(140px);
    opacity: 0.15;
    border-radius: 50%;
    z-index: -1;
    pointer-events: none;
}

/* Adjust main layout padding */
.main .block-container {
    padding-top: 3rem !important;
}

/* Hide native streamlit components */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Premium Headers */
.logo-title {
    font-size: 3.8rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #FF6B35 0%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -1.5px;
    animation: slideUp 0.8s ease;
}

.logo-subtitle {
    font-size: 1.2rem;
    font-weight: 400;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 3rem;
    letter-spacing: 0.5px;
}

/* Recommendations Card styles */
.rec-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 1rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    height: 380px;
}

.rec-card:hover {
    transform: translateY(-8px) scale(1.03);
    border-color: rgba(255, 107, 53, 0.5);
    box-shadow: 0 15px 35px rgba(255, 107, 53, 0.18);
}

.rec-poster {
    height: 250px;
    width: 100%;
    background-size: cover;
    background-position: center;
    position: relative;
}

.rec-match-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: linear-gradient(135deg, #FF6B35 0%, #8B5CF6 100%);
    color: #ffffff;
    padding: 4px 10px;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.rec-content {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    justify-content: space-between;
}

.rec-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.rec-meta {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 0.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}


/* Form element controls styling override */
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

/* Custom styled Button */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #FF6B35 0%, #8B5CF6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.6rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
    width: 100% !important;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 107, 53, 0.6) !important;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>

<!-- Glowing Background Blobs -->
<div class="glowing-blob-1"></div>
<div class="glowing-blob-2"></div>
""", unsafe_allow_html=True)

# 5. Header Elements
st.markdown('<h1 class="logo-title">🍿 PopcornPick</h1>', unsafe_allow_html=True)
st.markdown('<p class="logo-subtitle">AI-powered recommendations based on your taste, mood, and interests.</p>', unsafe_allow_html=True)

# 6. Recommendation Layout Input
col_input_1, col_input_2 = st.columns([2, 1])
with col_input_1:
    selected_movie_name = st.selectbox('Select a Base Movie:', movies['title'].values, key="select_movie")
with col_input_2:
    selected_genre = st.selectbox('Filter by Genre (Optional):', ["All", "Action", "Comedy", "Sci-Fi", "Drama", "Horror", "Romance", "Adventure", "Thriller"], key="select_genre")

if st.button('🚀 Get Recommendations', key="btn_get_recs"):
    with st.spinner("AI Engine searching vector space..."):
        recommendations = recommend_movies_engine(selected_movie_name, selected_genre)
        
    if recommendations:
        st.markdown(f'<h3 style="color:#ffffff; margin-top:2rem; font-weight:700;">Top Recommendations for you:</h3>', unsafe_allow_html=True)
        
        # Download Report Options
        report_content = generate_text_report(recommendations, selected_movie_name, selected_genre)
        st.download_button(
            label="📥 Download recommendations report as PDF/Text",
            data=report_content,
            file_name=f"PopcornPick_{selected_movie_name.replace(' ', '_')}.txt",
            mime="text/plain"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display recommendations cards in a 5-column layout grid (Netflix style row)
        cols = st.columns(5)
        for idx in range(min(5, len(recommendations))):
            with cols[idx]:
                row, match_pct = recommendations[idx]
                poster_url = fetch_poster(row['id'], row['title'])
                year = parse_year(row['release_date'])
                rating = f"{row['vote_average']:.1f}" if not pd.isna(row['vote_average']) else "N/A"
                
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-poster" style="background-image: url('{poster_url}');">
                        <span class="rec-match-badge">{match_pct}% Match</span>
                    </div>
                    <div class="rec-content">
                        <div>
                            <div class="rec-title" title="{row['title']}">{row['title']}</div>
                            <div class="rec-meta">
                                <span>📅 {year}</span>
                                <span>⭐ {rating}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons under the card
                sub_col1, sub_col2 = st.columns(2)
                with sub_col1:
                    st.markdown(f'<a href="https://www.youtube.com/results?search_query={row["title"].replace(" ", "+")}+official+trailer" target="_blank" style="text-decoration:none;"><button style="width:100%; border:1px solid rgba(255,255,255,0.06); background:rgba(255,255,255,0.01); color:#cbd5e1; border-radius:8px; padding:5px 0px; font-size:0.75rem; font-weight:600; cursor:pointer;">🎬 Trailer</button></a>', unsafe_allow_html=True)
                with sub_col2:
                    st.markdown(f'<a href="https://www.themoviedb.org/movie/{row["id"]}" target="_blank" style="text-decoration:none;"><button style="width:100%; border:1px solid rgba(255,255,255,0.06); background:rgba(255,255,255,0.01); color:#cbd5e1; border-radius:8px; padding:5px 0px; font-size:0.75rem; font-weight:600; cursor:pointer;">ℹ️ Info</button></a>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.warning("No matches found for that combination. Try widening your filters!")
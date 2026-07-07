# 🍿 AI-Powered Movie Recommendation System

An intelligent movie recommendation system that leverages **Machine Learning**, **Natural Language Processing (NLP)**, and **Content-Based Filtering** to provide personalized movie suggestions. PopcornPick analyzes movie metadata such as genres, cast, crew, keywords, and overview to recommend movies with similar characteristics.

Designed with a modern Netflix-inspired interface, the application provides movie posters, ratings, release years, trailers, and detailed movie information through an intuitive and interactive user experience.

---

# 🚀 Features

* 🎬 AI-Powered Movie Recommendation Engine
* 🤖 Content-Based Recommendation System
* 🎭 Genre-Based Filtering
* 🖼️ Dynamic Movie Posters using TMDB API
* ⭐ IMDb-style Ratings Display
* 🎥 Direct YouTube Trailer Search
* 📖 Movie Information via TMDB
* 📄 Download Recommendation Report
* ⚡ High-Speed Recommendations using Cached Data
* 🎨 Modern Netflix-Inspired User Interface
* 📱 Responsive Layout
* 🔍 Fast Similarity Search
* 💾 Efficient Data Loading with Streamlit Cache
* 🧠 Machine Learning Based Recommendation Logic

---

# 🛠️ Technology Stack

### Programming Language

* Python

### Machine Learning

* Scikit-learn
* Cosine Similarity
* Count Vectorizer
* NLP Feature Engineering

### Framework

* Streamlit

### Libraries

* Pandas
* NumPy
* Pickle
* Requests
* JSON
* urllib

### API

* TMDB (The Movie Database API)

### Dataset

* TMDB 5000 Movies Dataset

---

# 🧠 Machine Learning Workflow

```
TMDB Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Combine Tags
      │
      ▼
Text Vectorization
      │
      ▼
Cosine Similarity Matrix
      │
      ▼
Movie Recommendation Engine
      │
      ▼
Interactive Streamlit Web Application
```

---

# ⚙️ Project Structure

```
PopcornPick/
│
├── app.py
├── main.ipynb
├── similarity.pkl
├── movies_dict.pkl
├── tmdb_5000_movies.csv
├── requirements.txt
├── README.md
└── assets/
```

---

# 🔍 Recommendation Process

1. Load the TMDB movie dataset.
2. Clean and preprocess the dataset.
3. Extract genres, cast, crew, keywords, and overview.
4. Merge important textual features.
5. Convert text into numerical vectors.
6. Compute cosine similarity between movies.
7. Recommend the most similar movies.
8. Display posters, ratings, trailers, and movie details.

---

# 📊 Dataset Information

The project uses the **TMDB 5000 Movies Dataset**, which contains:

* Movie Title
* Genres
* Keywords
* Cast
* Crew
* Overview
* Popularity
* Ratings
* Release Date
* Runtime
* Language

---

# 💡 Key Highlights

* AI-powered recommendation engine
* Real-time movie poster fetching
* Modern and attractive UI
* High recommendation accuracy
* Easy to use
* Lightweight and fast
* Beginner-friendly code structure
* Suitable for academic and portfolio projects

---

# 📈 Future Enhancements

* User Authentication
* Personalized User Profiles
* Watchlist & Favorites
* Movie Reviews
* Collaborative Filtering
* Hybrid Recommendation System
* Deep Learning Recommendation Model
* Sentiment Analysis
* Voice Search
* Recommendation History
* Movie Search Autocomplete
* Multi-language Support
* Dark/Light Theme
* Docker Deployment
* Cloud Deployment (AWS, Render, Azure)

---

# 📷 Screenshots

Add screenshots of the application here.

* Home Page
* Movie Selection
* Recommendation Results
* Download Report

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/your-username/PopcornPick.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🎯 Applications

* Entertainment Recommendation Systems
* Machine Learning Projects
* NLP Projects
* Data Science Portfolio
* Academic Mini Projects
* Final Year Projects
* AI Demonstrations

---

# 👨‍💻 Author

**Vijay Bhadane**

* 🎓 M.Sc. Computer Science
* 💻 Python Developer
* 🤖 AI & Machine Learning Enthusiast
* 📊 Data Science Learner

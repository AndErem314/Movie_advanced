# 🎬 My Movie App

This is a Python-based command-line application for managing a movie database with integrated OMDb API support. It allows you to:

- Add movies by fetching data from the OMDb API
- Store movie details in a SQLite database via SQLAlchemy
- View statistics like average and median ratings
- Generate a responsive static HTML page displaying your movie collection

## 📦 Features

- List, add, delete, and update movie and movie's rating
- Search movies case-insensitively
- Show best/worst rated movies and random recommendations
- Sort movies by rating
- Generate a static website using a template and style

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Movie_advanced.git
cd Movie_advanced
```

### 2. Set up your environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure the API key

Create a .env file in the root directory with your OMDb API key:
```
OMDB_KEY=your_api_key_here
```

You can get a free key from https://www.omdbapi.com/apikey.aspx.

### 4. Run the app
```
python run.py
```
## 📋 Requirements
	•	Python 3.7+
	•	Internet connection (for OMDb API)
	•	OMDb API key

## ✅ License

This project is open-source and free to use for educational and personal purposes.
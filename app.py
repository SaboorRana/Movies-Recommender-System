from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

def fetch_poster(movie_id):
    try:
        os.environ['NO_PROXY'] = 'api.themoviedb.org'
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=5bdfe9747226f07df7d034a1fb0689ea&language=en-US',
            timeout=(5, 14)
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

def recommend(movie):
    try:
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
        recommended_movies = []
        recommended_movies_posters = []
        for i in movie_indices:
            movie_id = movies_df.iloc[i[0]].movie_id
            recommended_movies.append(movies_df.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except IndexError:
        return [], []

# Load pickled data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_titles = movies_df['title'].values

@app.route('/')
def index():
    return render_template('index.html', movie_titles=movie_titles)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    selected_movie_name = request.form['movie']
    names, posters = recommend(selected_movie_name)
    combined = list(zip(names, posters))  # Combine names and posters into tuples
    return render_template('recommend.html', combined=combined)


if __name__ == '__main__':
    app.run(debug=True)

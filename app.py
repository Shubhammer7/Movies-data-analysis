from flask import Flask, render_template, request
import pandas as pd
from recommendations import get_recommendations, generate_similarity
app = Flask(__name__)

# Load your dataset
df_recommendation = pd.read_csv('tmdb_5000_movies.csv')

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = pd.DataFrame()  # Initialize as an empty DataFrame
    if request.method == 'POST':
        title = request.form['movie_title']
        recommendations = get_recommendations(title, df_recommendation, cosine_sim)  # Pass the DataFrame and cosine_sim
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
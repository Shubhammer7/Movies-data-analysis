from flask import Flask, request, render_template
import model  # Import model.py as a module

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Recommendations route
@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')  # Get the movie title from the form
    if title:
        recommendations = model.get_recommendations(title)  # Call the function from model.py
        return render_template('index.html', recommendations=recommendations)
    return render_template('index.html', recommendations=[])

if __name__ == "__main__":
    app.run(debug=True)


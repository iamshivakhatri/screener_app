from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load data
def load_data():
    # Replace with your actual data loading logic
    # For example:
    df_day_gainers = pd.read_csv('data/day_gainers.csv')
    df_day_losers = pd.read_csv('data/day_losers.csv')
    df_most_actives = pd.read_csv('data/most_actives.csv')
    df_trending = pd.read_csv('data/trending.csv')
    df_undervalued_large_caps = pd.read_csv('data/undervalued_large_caps.csv')
    
    return {
        'day_gainers': df_day_gainers,
        'day_losers': df_day_losers,
        'most_actives': df_most_actives,
        'trending': df_trending,
        'undervalued_large_caps': df_undervalued_large_caps
    }

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/day_gainers')
def day_gainers():
    data = load_data()['day_gainers']
    return render_template('day_gainers.html', table=data.to_html(classes='table table-striped'))

@app.route('/day_losers')
def day_losers():
    data = load_data()['day_losers']
    return render_template('day_losers.html', table=data.to_html(classes='table table-striped'))

@app.route('/most_actives')
def most_actives():
    data = load_data()['most_actives']
    return render_template('most_actives.html', table=data.to_html(classes='table table-striped'))

@app.route('/trending')
def trending():
    data = load_data()['trending']
    return render_template('trending.html', table=data.to_html(classes='table table-striped'))

@app.route('/undervalued_large_caps')
def undervalued_large_caps():
    data = load_data()['undervalued_large_caps']
    return render_template('undervalued_large_caps.html', table=data.to_html(classes='table table-striped'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

# Load data
def load_data():
    # Replace with your actual data loading logic
    # For example:
    df_day_gainers = pd.read_csv('data/day_gainers.csv')

    df_small_cap_gainers = pd.read_csv('data/small_cap_gainers.csv')
    df_most_actives = pd.read_csv('data/most_actives.csv')
    df_trending = pd.read_csv('data/trending.csv')
    df_undervalued_large_caps = pd.read_csv('data/undervalued_large_caps.csv')
    
    return {
        'day_gainers': df_day_gainers,
        'most_actives': df_most_actives,
        'trending': df_trending,
        'undervalued_large_caps': df_undervalued_large_caps,
        'small_cap_gainers': df_small_cap_gainers
    }

@app.route('/')
def index():
    # Load and process the first dataset
    with open("fmp_gainers.json", "r") as f:
        gainers_data = json.load(f)
    gainers_df = pd.DataFrame(gainers_data)
    gainers_filtered = gainers_df[(gainers_df['price'] > 1) & (gainers_df['price'] < 20)]
    gainers_filtered = gainers_filtered.reset_index(drop=True)
    gainers_filtered = gainers_filtered.head(10)
    gainers_filtered = gainers_filtered

    # Load and process the second dataset
    with open("fmp_active.json", "r") as f:
        active_data = json.load(f)
    active_df = pd.DataFrame(active_data)
    active_filtered = active_df[( active_df['price'] > 1) & ( active_df['price'] < 20) & ( active_df['changesPercentage'] > 0)]
    active_filtered = active_filtered.reset_index(drop=True)

    return render_template('index.html', gainers=gainers_filtered.to_dict(orient='records'), active=active_filtered.to_dict(orient='records'))

@app.route('/day_gainers')
def day_gainers():
    data = load_data()['day_gainers']
    return render_template('daily_gainers.html', table=data.to_html(classes='table table-striped'))

@app.route('/small_cap_gainers')
def small_cap_gainers():
    data = load_data()['small_cap_gainers']
    return render_template('small_cap_gainers.html', table=data.to_html(classes='table table-striped'))

@app.route('/most_actives')
def most_actives():
    data = load_data()['most_actives']
    return render_template('most_active.html', table=data.to_html(classes='table table-striped'))

@app.route('/trending')
def trending():
    data = load_data()['trending']
    return render_template('trending.html', table=data.to_html(classes='table table-striped'))

@app.route('/undervalued_large_caps')
def undervalued_large_caps():
    data = load_data()['undervalued_large_caps']
    return render_template('undervalued_large_caps.html', table=data.to_html(classes='table table-striped'))

@app.route('/try_page')
def try_page():
    return render_template('try.html')


if __name__ == '__main__':
    app.run(debug=True)

def load_data(filepath):
    import pandas as pd
    return pd.read_csv(filepath)

def preprocess_data(df):
    # Handle missing values
    df = df.dropna()
    # Convert ratings to numeric
    df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')
    return df

def get_user_preferences():
    import json
    with open('configs/qcm_questions.json') as f:
        questions = json.load(f)
    return questions

def filter_data_by_preferences(df, preferences):
    # Filter data based on user preferences
    if preferences.get('category'):
        df = df[df['category_name'] == preferences['category']]
    if preferences.get('ratings') == 'Yes':
        df = df[df['ratings'] >= 4.0]  # Example threshold
    return df

def recommend_attractions(df, user_input):
    # Example recommendation logic
    filtered_data = filter_data_by_preferences(df, user_input)
    return filtered_data.sort_values(by='ratings', ascending=False).head(5)
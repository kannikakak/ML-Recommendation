import pandas as pd

def load_data(filepath):
    """Load the dataset from a CSV file."""
    data = pd.read_csv(filepath)
    return data

def preprocess_data(data):
    """Preprocess the data for the recommendation system."""
    # Handle missing values
    data = data.dropna(subset=['name', 'category_name', 'ratings', 'reviews_count'])
    
    # Convert ratings and reviews_count to numeric
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
    data['reviews_count'] = pd.to_numeric(data['reviews_count'], errors='coerce')
    
    # Normalize the ratings
    data['ratings'] = (data['ratings'] - data['ratings'].min()) / (data['ratings'].max() - data['ratings'].min())
    
    return data

def save_processed_data(data, output_filepath):
    """Save the processed data to a new CSV file."""
    data.to_csv(output_filepath, index=False)

# Example usage
if __name__ == "__main__":
    raw_data_filepath = 'data/raw/dataset_with_descriptions_cleaned.csv'
    processed_data_filepath = 'data/processed/processed_data.csv'
    
    raw_data = load_data(raw_data_filepath)
    processed_data = preprocess_data(raw_data)
    save_processed_data(processed_data, processed_data_filepath)
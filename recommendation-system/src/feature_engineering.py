import pandas as pd

def load_data(file_path):
    """Load the dataset from a CSV file, handling encoding issues."""
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        print('UTF-8 failed, trying latin1 encoding...')
        data = pd.read_csv(file_path, encoding='latin1')
    return data

def feature_engineering(data):
    """Perform feature engineering on the dataset."""
    # Example: Create a new feature for the average rating
    # Ensure 'ratings' and 'reviews_count' are numeric before division
    data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
    data['reviews_count'] = pd.to_numeric(data['reviews_count'], errors='coerce')
    data['average_rating'] = data['ratings'] / data['reviews_count']
    
    # Example: Convert categorical features to numerical
    data = pd.get_dummies(data, columns=['category_name'], drop_first=True)
    
    return data

def main():
    # Load the dataset
    file_path = 'data/raw/dataset_with_descriptions_cleaned.csv'
    data = load_data(file_path)
    
    # Perform feature engineering
    engineered_data = feature_engineering(data)
    
    # Save the processed data
    engineered_data.to_csv('data/processed/engineered_data.csv', index=False)

if __name__ == "__main__":
    main()
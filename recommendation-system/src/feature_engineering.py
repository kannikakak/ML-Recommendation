import pandas as pd

def load_data(file_path):
    """Load the dataset from a CSV file."""
    data = pd.read_csv(file_path)
    return data

def feature_engineering(data):
    """Perform feature engineering on the dataset."""
    # Example: Create a new feature for the average rating
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
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

class RecommendationSystem:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.user_preferences = None

    def set_user_preferences(self, preferences):
        self.user_preferences = preferences

    def preprocess_data(self):
        # Example preprocessing steps
        self.data['ratings'] = self.data['ratings'].fillna(self.data['ratings'].mean())
        self.data['reviews_count'] = self.data['reviews_count'].fillna(0)

    def calculate_similarity(self):
        # Assuming we are using ratings and reviews_count for similarity
        features = self.data[['ratings', 'reviews_count']]
        self.similarity_matrix = cosine_similarity(features)

    def recommend(self, num_recommendations=5):
        if self.user_preferences is None:
            raise ValueError("User preferences not set.")

        # Example logic to find recommendations based on user preferences
        user_vector = np.array(self.user_preferences).reshape(1, -1)
        user_similarity = cosine_similarity(user_vector, self.similarity_matrix)
        recommended_indices = user_similarity.argsort()[0][-num_recommendations:][::-1]

        return self.data.iloc[recommended_indices]

# Example usage:
# recommender = RecommendationSystem('data/raw/dataset_with_descriptions_cleaned.csv')
# recommender.set_user_preferences([4.5, 100])  # Example user preferences
# recommender.preprocess_data()
# recommender.calculate_similarity()
# recommendations = recommender.recommend()
# print(recommendations)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import json

class RecommendationSystem:
    def __init__(self, data_path, questions_path):
        self.data = pd.read_csv(data_path)
        self.questions = self.load_questions(questions_path)
        self.model = None

    def load_questions(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def preprocess_data(self):
        # Example preprocessing steps
        self.data.fillna(0, inplace=True)
        self.data['ratings'] = self.data['ratings'].astype(float)
        self.data['reviews_count'] = self.data['reviews_count'].astype(int)

    def train_model(self):
        features = self.data[['latitude', 'longitude', 'ratings', 'reviews_count']]
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        self.model = NearestNeighbors(n_neighbors=5)
        self.model.fit(scaled_features)

    def recommend(self, user_input):
        user_data = pd.DataFrame([user_input])
        scaled_user_data = StandardScaler().fit_transform(user_data)
        distances, indices = self.model.kneighbors(scaled_user_data)
        return self.data.iloc[indices[0]]
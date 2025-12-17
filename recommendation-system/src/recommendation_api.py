import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

class RecommendationEngine:
    """
    Recommendation engine for filtering and finding similar places.
    """
    def __init__(self, data: pd.DataFrame, X_scaled: np.ndarray, n_neighbors: int = 5):
        self.data = data
        self.X_scaled = X_scaled
        self.knn = NearestNeighbors(n_neighbors=n_neighbors)
        self.knn.fit(self.X_scaled)

    def filter_places(self, user_answers: dict) -> pd.DataFrame:
        """
        Filter places based on user answers. Returns up to 5 recommendations.
        """
        filtered = self.data.copy()

        # Filter by province
        province = user_answers.get("province")
        if province:
            filtered = filtered[filtered['province_name'].astype(str) == str(province)]

        # Filter by category
        category = user_answers.get("category")
        if category:
            cat_col = f'category_name_{category}'
            if cat_col in filtered.columns:
                filtered = filtered[filtered[cat_col] == 1]

        # Filter by ratings (only if "Yes")
        if user_answers.get("ratings") == "Yes":
            filtered = filtered[filtered['ratings'] >= 4.0]

        # Filter by entry_free (only if "Yes")
        if user_answers.get("entry_free") == "Yes" and "entry_free" in filtered.columns:
            filtered = filtered[filtered['entry_free'] == 1]

        # Sort by popularity if important
        if user_answers.get("popularity") in ["Very important", "Somewhat important"]:
            filtered = filtered.sort_values(by='reviews_count', ascending=False)

        # If no results, try relaxing filters
        if filtered.empty:
            filtered = self._relaxed_filter(user_answers)

        return filtered.head(5)

    def _relaxed_filter(self, user_answers: dict) -> pd.DataFrame:
        """
        Apply more relaxed filtering when strict filters return no results.
        """
        filtered = self.data.copy()

        # Only apply province filter (most important)
        province = user_answers.get("province")
        if province:
            filtered = filtered[filtered['province_name'].astype(str) == str(province)]

        # Apply category if available
        category = user_answers.get("category")
        if category:
            cat_col = f'category_name_{category}'
            if cat_col in filtered.columns:
                filtered = filtered[filtered[cat_col] == 1]

        # Relax rating requirement to 3.0 instead of 4.0
        if user_answers.get("ratings") == "Yes":
            filtered = filtered[filtered['ratings'] >= 3.0]

        # Sort by ratings and reviews
        if 'ratings' in filtered.columns and 'reviews_count' in filtered.columns:
            filtered = filtered.sort_values(
                by=['ratings', 'reviews_count'],
                ascending=[False, False]
            )

        return filtered

    def get_similar_places(self, idx: int, n_neighbors: int = 5) -> pd.DataFrame:
        """
        Get similar places using KNN. Returns a DataFrame of similar places.
        """
        if idx not in self.data.index:
            # Index not found
            return pd.DataFrame()
        try:
            position = self.data.index.get_loc(idx)
            if n_neighbors != self.knn.n_neighbors:
                self.knn.set_params(n_neighbors=n_neighbors)
                self.knn.fit(self.X_scaled)
            distances, indices = self.knn.kneighbors([self.X_scaled[position]])
            return self.data.iloc[indices[0]]
        except Exception:
            return pd.DataFrame()

    def get_statistics(self) -> dict:
        """
        Get dataset statistics for debugging or display.
        """
        stats = {
            'total_places': len(self.data),
            'provinces': self.data['province_name'].nunique() if 'province_name' in self.data.columns else 0,
            'avg_rating': float(self.data['ratings'].mean()) if 'ratings' in self.data.columns else 0,
            'categories': []
        }
        for col in self.data.columns:
            if col.startswith('category_name_'):
                cat_name = col.replace('category_name_', '')
                count = self.data[col].sum()
                stats['categories'].append({cat_name: int(count)})
        return stats
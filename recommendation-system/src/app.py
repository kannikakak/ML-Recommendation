import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from feature_engineering import load_data, feature_engineering
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors

# Load and prepare data
data = load_data('../data/raw/dataset_with_descriptions_cleaned.csv')
engineered_data = feature_engineering(data)

# Ensure all categories are handled
all_categories = ['Hotel', 'Restaurant', 'Tourist Attraction', 'Transportation']
category_cols = [f'category_name_{cat}' for cat in all_categories]
for cat in category_cols:
    if cat not in engineered_data.columns:
        engineered_data[cat] = 0

# Encode features for KNN
le_province = LabelEncoder()
engineered_data['province_encoded'] = le_province.fit_transform(engineered_data['province_name'])
engineered_data['category_encoded'] = engineered_data[category_cols].idxmax(axis=1).apply(lambda x: x.replace('category_name_', ''))
le_category = LabelEncoder()
engineered_data['category_encoded'] = le_category.fit_transform(engineered_data['category_encoded'])
features = ['province_encoded', 'category_encoded', 'ratings', 'reviews_count', 'average_rating']

# Fill missing values in features to avoid NaN errors
engineered_data[features] = engineered_data[features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(engineered_data[features])
knn = NearestNeighbors(n_neighbors=5)
knn.fit(X_scaled)

# Streamlit UI
st.title("Tourist Attraction Recommendation System")

# QCM Questions
st.sidebar.header("Tell us about your preferences")
province = st.sidebar.selectbox(
    "Which province would you like to explore?",
    sorted(engineered_data['province_name'].unique())
)
category = st.sidebar.selectbox(
    "What type of attractions are you interested in?",
    all_categories
)
ratings = st.sidebar.radio(
    "Do you prefer attractions with higher ratings?",
    ["Yes", "No"]
)
entry_free = None
if 'entry_free' in engineered_data.columns:
    entry_free = st.sidebar.radio(
        "Do you prefer attractions with free entry?",
        ["Yes", "No"]
    )
popularity = st.sidebar.selectbox(
    "How important is the number of reviews for you when choosing an attraction?",
    ["Very important", "Somewhat important", "Not important"]
)

# Collect answers
user_answers = {
    "province": province,
    "category": category,
    "ratings": ratings,
    "popularity": popularity
}
if entry_free is not None:
    user_answers["entry_free"] = entry_free

# Recommendation logic
filtered = engineered_data.copy()
filtered = filtered[filtered['province_name'] == user_answers["province"]]
cat_col = f'category_name_{user_answers["category"]}'
if cat_col in filtered.columns:
    filtered = filtered[filtered[cat_col] == 1]
if user_answers.get("ratings") == "Yes":
    filtered = filtered[filtered['ratings'] >= 4.0]
if "entry_free" in user_answers and "entry_free" in filtered.columns:
    if user_answers["entry_free"] == "Yes":
        filtered = filtered[filtered['entry_free'] == 1]
if user_answers.get("popularity") == "Very important":
    filtered = filtered.sort_values(by='reviews_count', ascending=False)
elif user_answers.get("popularity") == "Somewhat important":
    filtered = filtered.sort_values(by='reviews_count', ascending=False)
recommendations = filtered.head(5)

# Show recommendations
st.header("Recommended places for you")
if not recommendations.empty:
    for _, row in recommendations.iterrows():
        st.subheader(row['name'])
        st.write(f"**Province:** {row['province_name']}")
        st.write(f"**Ratings:** {row['ratings']} stars")
        st.write(f"**Reviews:** {row['reviews_count']} reviews")
        if 'image_url' in row:
            st.image(row['image_url'], caption=row['name'], use_column_width=True)

        # Map visualization for each place
        if 'latitude' in row and 'longitude' in row:
            st.write("**Location:**")
            m = folium.Map(location=[row['latitude'], row['longitude']], zoom_start=15)
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['name']} ({row['ratings']} stars)"
            ).add_to(m)
            st_folium(m, width=700, height=500)

        # User reviews and ratings
        st.write("**User Reviews and Ratings:**")
        if 'user_reviews' in row:
            st.write(row['user_reviews'])
        else:
            st.write("No reviews available.")
        user_review = st.text_area(f"Write your review for {row['name']}")
        user_rating = st.slider(f"Rate {row['name']}", 1, 5, 3)
        if st.button(f"Submit review for {row['name']}"):
            st.write(f"Thank you for reviewing {row['name']}!")

    # Show similar places to top match
    idx = recommendations.index[0]
    distances, indices = knn.kneighbors([X_scaled[idx]])
    st.subheader("Places similar to your top match")
    similar_places = engineered_data.iloc[indices[0]]
    for _, row in similar_places.iterrows():
        st.write(f"**{row['name']}**")
        st.write(f"Province: {row['province_name']}, Ratings: {row['ratings']} stars")
else:
    st.write("No places found for your criteria.")
import ast

# Helper function to parse image URLs and append API key if needed
def parse_image_url(images_url_str):
    try:
        if pd.isna(images_url_str):
            return None
        if isinstance(images_url_str, str):
            # Try to parse as a list
            if images_url_str.strip().startswith('['):
                try:
                    urls = ast.literal_eval(images_url_str)
                    if isinstance(urls, list) and urls:
                        for url in urls:
                            if isinstance(url, str) and url.strip():
                                if "maps.googleapis.com" in url:
                                    # Append API key if not present
                                    if "key=" not in url:
                                        url += f"&key={GOOGLE_MAPS_API_KEY}"
                                return url.strip()
                except Exception:
                    pass
            # Otherwise, treat as a single URL
            if images_url_str.strip():
                url = images_url_str.strip()
                if "maps.googleapis.com" in url and "key=" not in url:
                    url += f"&key={GOOGLE_MAPS_API_KEY}"
                return url
        return None
    except Exception:
        return None

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from feature_engineering import load_data, feature_engineering
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
from recommendation_api import RecommendationEngine
import json
import ast

# Helper function to parse image URLs

def get_fallback_image(place_name, category):
    """Get a fallback image from Unsplash based on place name and category"""
    category_search = {
        'Hotel': 'hotel,resort,accommodation',
        'Restaurant': 'restaurant,food,dining',
        'Tourist Attraction': 'tourist,landmark,cambodia',
        'Transportation': 'transportation,travel,vehicle'
    }
    search_term = category_search.get(category, 'travel,cambodia')
    return f"https://source.unsplash.com/400x300/?{search_term}"

def get_placeholder_html(place_name, category='Tourist Attraction'):
    """Generate placeholder HTML for missing images"""
    placeholder_icons = {
        'Hotel': '🏨',
        'Restaurant': '🍽️',
        'Tourist Attraction': '🗿',
        'Transportation': '🚌'
    }
    icon = placeholder_icons.get(category, '📍')
    return f"""
    <div style="background-color: #f0f2f6; padding: 80px 20px; text-align: center; 
                border-radius: 10px; border: 2px dashed #ccc; min-height: 250px; 
                display: flex; flex-direction: column; justify-content: center;">
        <h1 style="font-size: 60px; margin: 0;">{icon}</h1>
        <p style="color: #666; margin: 15px 0; font-weight: 500;">{place_name}</p>
        <small style="color: #999;">No image available</small>
    </div>
    """

# Page configuration
st.set_page_config(
    page_title="Tourist Attraction Recommendations",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Website-like CSS
st.markdown("""
<style>
body {
    background: #f7fafd;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}
.navbar {
    width: 100vw;
    background: linear-gradient(90deg, #1f77b4 60%, #4CAF50 100%);
    color: #fff;
    padding: 1.2rem 2rem 1.2rem 2rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
}
.navbar-title {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: 1px;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.navbar-links {
    font-size: 1.1rem;
    display: flex;
    gap: 2rem;
}
.navbar-links a {
    color: #fff;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}
.navbar-links a:hover {
    color: #ffe082;
}
.hero-section {
    margin-top: 4.5rem;
    padding: 2.5rem 0 1.5rem 0;
    background: linear-gradient(90deg, #e3f2fd 60%, #e8f5e9 100%);
    border-radius: 0 0 32px 32px;
    box-shadow: 0 4px 24px rgba(31,119,180,0.07);
    text-align: center;
}
.hero-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: #1f77b4;
    margin-bottom: 0.5rem;
}
.hero-desc {
    font-size: 1.25rem;
    color: #333;
    margin-bottom: 1.2rem;
}
.filter-panel {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 2px 12px rgba(31,119,180,0.07);
    padding: 2rem 1.2rem 1.2rem 1.2rem;
    margin-bottom: 1.5rem;
}
.card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2.2rem;
    justify-content: center;
    margin-top: 1.5rem;
}
.card {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    width: 340px;
    margin: 1rem 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: box-shadow 0.2s;
    border: 1.5px solid #e3f2fd;
}
.card:hover {
    box-shadow: 0 8px 32px rgba(31,119,180,0.13);
    border: 1.5px solid #1f77b4;
}
.card-img {
    width: 100%;
    height: 190px;
    object-fit: cover;
    background: #e3f2fd;
}
.card-body {
    padding: 1.2rem 1.2rem 0.7rem 1.2rem;
}
.card-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: #1f77b4;
    margin-bottom: 0.3rem;
}
.card-province {
    color: #4CAF50;
    font-weight: 500;
    margin-bottom: 0.2rem;
}
.card-rating {
    color: #ff9800;
    margin-bottom: 0.2rem;
}
.card-category {
    color: #2196f3;
    margin-bottom: 0.2rem;
}
.card-description {
    color: #444;
    font-size: 1.01rem;
    margin-bottom: 0.2rem;
}
.stButton>button {
    width: 100%;
    background-color: #1f77b4;
    color: white;
    border-radius: 5px;
    font-weight: 600;
    font-size: 1.1rem;
    margin-top: 0.7rem;
    margin-bottom: 0.5rem;
    transition: background 0.2s;
}
.stButton>button:hover {
    background-color: #4CAF50;
}
.stSidebar {
    background: #e3f2fd;
}
.stExpanderHeader {
    font-weight: 600;
    color: #1f77b4;
}
.stTabs [data-baseweb="tab"] {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1f77b4;
}
.stTabs [aria-selected="true"] {
    background: #e3f2fd;
    border-radius: 12px 12px 0 0;
}
.stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# Navigation bar
st.markdown("""
<div class="navbar">
    <div class="navbar-title">🗺️ Tourist Recommendation</div>
    <div class="navbar-links">
        <a href="#" onclick="window.scrollTo(0,0)">Home</a>
        <a href="#" onclick="window.scrollTo(0,document.body.scrollHeight)">Contact</a>
        <a href="#" onclick="window.scrollTo(0,document.body.scrollHeight)">About</a>
    </div>
</div>
<div class="hero-section">
    <div class="hero-title">Discover Your Perfect Destination</div>
    <div class="hero-desc">Find the best places to visit, eat, and stay in Cambodia. Get personalized recommendations based on your travel style, budget, and interests!</div>
</div>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_and_prepare_data():
    data = load_data('../data/raw/dataset_with_descriptions_cleaned.csv')
    engineered_data = feature_engineering(data)
    all_categories = ['Hotel', 'Restaurant', 'Tourist Attraction', 'Transportation']
    category_cols = [f'category_name_{cat}' for cat in all_categories]
    for cat in category_cols:
        if cat not in engineered_data.columns:
            engineered_data[cat] = 0
    le_province = LabelEncoder()
    engineered_data['province_encoded'] = le_province.fit_transform(engineered_data['province_name'])
    engineered_data['category_encoded'] = engineered_data[category_cols].idxmax(axis=1).apply(
        lambda x: x.replace('category_name_', '')
    )
    le_category = LabelEncoder()
    engineered_data['category_encoded'] = le_category.fit_transform(engineered_data['category_encoded'])
    features = ['province_encoded', 'category_encoded', 'ratings', 'reviews_count', 'average_rating']
    engineered_data[features] = engineered_data[features].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(engineered_data[features])
    return engineered_data, X_scaled, all_categories

engineered_data, X_scaled, all_categories = load_and_prepare_data()

# Instantiate recommendation engine
rec_engine = RecommendationEngine(engineered_data, X_scaled, n_neighbors=5)

# Header
st.title("🗺️ Tourist Attraction Recommendation System")
st.markdown("### Discover your perfect travel destination based on your preferences!")
st.markdown("---")

# Sidebar for user preferences as a filter panel
with st.sidebar:
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.header("📋 Your Travel Preferences")
    st.markdown("Answer these questions to get personalized recommendations:")

    province_names = engineered_data['province_name'].dropna().unique()
    province_names = [p for p in province_names if isinstance(p, str) and not p.strip().replace(' ', '').replace('-', '').replace("'", '').replace('.', '').isdigit()]
    province_names = sorted(province_names)
    province = st.selectbox(
        "🌍 Which province would you like to explore?",
        province_names,
        help="Select the province you want to visit"
    )

    category = st.selectbox(
        "🏨 What type of attractions are you interested in?",
        all_categories,
        help="Choose the type of place you want to visit"
    )

    ratings = st.radio(
        "⭐ Do you prefer highly-rated attractions (4+ stars)?",
        ["Yes", "No"],
        help="Filter for top-rated places"
    )

    entry_free = None
    if 'entry_free' in engineered_data.columns:
        entry_free = st.radio(
            "💰 Do you prefer attractions with free entry?",
            ["Yes", "No"],
            help="Filter for free or paid attractions"
        )

    popularity = st.selectbox(
        "📊 How important is popularity (number of reviews)?",
        ["Very important", "Somewhat important", "Not important"],
        help="Places with more reviews are generally more popular"
    )

    budget = st.select_slider(
        "💵 What's your budget range?",
        options=["Budget-friendly", "Moderate", "Luxury", "Any"],
        value="Any",
        help="Your preferred spending level"
    )

    travel_style = st.multiselect(
        "🎒 What's your travel style?",
        ["Adventure", "Relaxation", "Cultural", "Family-friendly", "Romantic"],
        help="Select all that apply"
    )

    duration = st.slider(
        "⏰ How many days are you planning to stay?",
        min_value=1,
        max_value=14,
        value=3,
        help="Duration of your trip"
    )

    group_size = st.radio(
        "👥 Who are you traveling with?",
        ["Solo", "Couple", "Family", "Friends", "Group"],
        help="Your travel companions"
    )

    season = st.selectbox(
        "🌤️ Preferred season to visit?",
        ["Spring", "Summer", "Autumn", "Winter", "Any"],
        help="Best time to visit"
    )

    st.markdown("---")
    search_button = st.button("🔍 Find Recommendations", type="primary")

    if st.checkbox("🔧 Debug: Show dataset info"):
        st.write("**Dataset columns:**", engineered_data.columns.tolist())
        if 'images_url' in engineered_data.columns:
            st.write("**Sample image URLs:**")
            st.write(engineered_data['images_url'].head(3))
            st.write(f"**Non-null images:** {engineered_data['images_url'].notna().sum()} / {len(engineered_data)}")
        elif 'image_url' in engineered_data.columns:
            st.write("**Sample image URLs:**")
            st.write(engineered_data['image_url'].head(3))
            st.write(f"**Non-null images:** {engineered_data['image_url'].notna().sum()} / {len(engineered_data)}")
        else:
            st.warning("No image column found in dataset!")
    st.markdown('</div>', unsafe_allow_html=True)

# Collect user answers
user_answers = {
    "province": province,
    "category": category,
    "ratings": ratings,
    "popularity": popularity,
    "budget": budget,
    "travel_style": travel_style,
    "duration": duration,
    "group_size": group_size,
    "season": season
}
if entry_free is not None:
    user_answers["entry_free"] = entry_free

# Main content area
if search_button or 'recommendations' not in st.session_state:
    recommendations = rec_engine.filter_places(user_answers)
    st.session_state['recommendations'] = recommendations
    st.session_state['user_answers'] = user_answers
else:
    recommendations = st.session_state.get('recommendations', pd.DataFrame())

# Display recommendations as a modern card grid
if not recommendations.empty:
    st.markdown(f"<h2 style='margin-top:2rem;'>✨ Recommended Places for You</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#333;font-size:1.15rem;margin-bottom:1.2rem;'>Found <b>{len(recommendations)}</b> amazing places matching your preferences!</div>", unsafe_allow_html=True)

    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    for idx, row in recommendations.iterrows():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'''
        <div class="card-body">
            <div class="card-title">{row['name']}</div>
            <div class="card-province">{row['province_name']}</div>
            <div class="card-rating">⭐ {row['ratings']} ({row['reviews_count']} reviews)</div>
            <div class="card-category">{row['category_name'] if 'category_name' in row else ''}</div>
            <div class="card-description">{row['description'] if 'description' in row else ''}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🗺️ Map View", "📊 Comparison"])

    with tab1:
        st.markdown("### 🗺️ All Recommended Places on Map")
        if 'latitude' in recommendations.columns and 'longitude' in recommendations.columns:
            valid_coords = recommendations[['latitude', 'longitude']].dropna()
            if not valid_coords.empty:
                valid_coords['latitude'] = pd.to_numeric(valid_coords['latitude'], errors='coerce')
                valid_coords['longitude'] = pd.to_numeric(valid_coords['longitude'], errors='coerce')
                center_lat = valid_coords['latitude'].mean()
                center_lon = valid_coords['longitude'].mean()
                map_all = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=10,
                    tiles='OpenStreetMap'
                )
                for idx, row in recommendations.iterrows():
                    if pd.notna(row.get('latitude')) and pd.notna(row.get('longitude')):
                        folium.Marker(
                            location=[row['latitude'], row['longitude']],
                            popup=f"<b>{row['name']}</b><br>⭐ {row['ratings']}<br>💬 {int(row['reviews_count'])} reviews",
                            tooltip=row['name'],
                            icon=folium.Icon(color='blue', icon='star')
                        ).add_to(map_all)
                st_folium(map_all, width=1000, height=600)
            else:
                st.warning("⚠️ No location data available for map view")

    with tab2:
        st.markdown("### 📊 Compare All Recommendations")
        comparison_cols = ['name', 'province_name', 'ratings', 'reviews_count']
        if 'average_rating' in recommendations.columns:
            comparison_cols.append('average_rating')
        st.dataframe(
            recommendations[comparison_cols].style.highlight_max(
                subset=['ratings', 'reviews_count'],
                color='lightgreen'
            ),
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("<h3>🔍 Similar Places You Might Like</h3>", unsafe_allow_html=True)
    idx = recommendations.index[0]
    similar_places = rec_engine.get_similar_places(idx, n_neighbors=6)
    similar_places = similar_places[similar_places.index != idx]
    cols = st.columns(min(3, len(similar_places)))
    for i, (_, row) in enumerate(similar_places.head(3).iterrows()):
        with cols[i]:

            image_url = None
            if 'images_url' in row and pd.notna(row['images_url']):
                image_url = parse_image_url(row['images_url'])
            elif 'image_url' in row and pd.notna(row['image_url']):
                image_url = parse_image_url(row['image_url'])
            if not image_url or not image_url.strip():
                image_url = get_fallback_image(row['name'], user_answers.get('category', 'Tourist Attraction'))
            if image_url:
                st.image(image_url, use_column_width='always')
            else:
                st.info("📷")
            st.markdown(f"**{row['name']}**")
            st.write(f"📍 {row['province_name']}")
            st.write(f"⭐ {row['ratings']} stars | 💬 {int(row['reviews_count'])} reviews")

else:
    st.warning("⚠️ No places found matching your criteria. Try adjusting your preferences!")
    st.info("💡 Tip: Try selecting 'No' for some filters or choosing a different province.")
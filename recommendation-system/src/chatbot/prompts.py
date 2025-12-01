# Define chatbot prompt templates here.

# Prompt templates for the chatbot

def get_place_prompt(place_name, description, ratings, reviews_count, category_name):
    """
    Generate a prompt for the chatbot based on the place's data.

    Args:
        place_name (str): Name of the place.
        description (str): Description of the place.
        ratings (float): Average ratings of the place.
        reviews_count (int): Number of reviews for the place.
        category_name (str): Category of the place.

    Returns:
        str: A formatted prompt for the chatbot.
    """
    return (
        f"You are an AI assistant for the place '{place_name}'. "
        f"Here is some information about it: {description}. "
        f"It has an average rating of {ratings} based on {reviews_count} reviews. "
        f"This place belongs to the category: {category_name}. "
        f"Answer questions about this place in a helpful and friendly manner."
    )
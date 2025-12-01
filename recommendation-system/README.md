# Recommendation System

This project is a recommendation system designed to suggest attractions, hotels, and restaurants based on user preferences and input data. The system utilizes machine learning techniques to provide personalized recommendations to users.

## Project Structure

- **data/**: Contains the datasets used in the project.
  - **raw/**: Contains the raw dataset files.
    - `dataset_with_descriptions_cleaned.csv`: This file contains data about attractions, hotels, and restaurants, including their names, locations, ratings, reviews, and descriptions.
  - **processed/**: This directory will contain processed data files.

- **notebooks/**: Contains Jupyter Notebooks for exploratory data analysis and model training.
  - `Recommendation-System.ipynb`: This notebook includes code for data loading, preprocessing, model training, and evaluation.

- **src/**: Contains the source code for the recommendation system.
  - `__init__.py`: Initializes the source package.
  - `data_preprocessing.py`: Contains functions for data cleaning and preprocessing.
  - `feature_engineering.py`: Contains functions for feature extraction and transformation.
  - `model.py`: Contains the machine learning model implementation.
  - `recommend.py`: Contains functions for generating recommendations based on user input.
  - `utils.py`: Contains utility functions used throughout the project.

- **configs/**: Contains configuration files.
  - `qcm_questions.json`: Contains a set of questions and options related to user preferences for attractions, hotels, and restaurants.

- **requirements.txt**: Lists the dependencies required for the project, including libraries for data manipulation, machine learning, and web frameworks.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd recommendation-system
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Open the Jupyter Notebook:
   ```
   jupyter notebook notebooks/Recommendation-System.ipynb
   ```

## Usage Guidelines

- Run the Jupyter Notebook to load the dataset, preprocess the data, train the model, and generate recommendations.
- Use the `qcm_questions.json` file to gather user preferences for personalized recommendations.
- Modify the source code in the `src/` directory as needed to improve the recommendation algorithm or add new features.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.
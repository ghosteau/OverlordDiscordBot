# Import libraries and tools for the machine learning model
import pandas as pd  # This will be used for data management
import numpy as np
from sklearn.model_selection import train_test_split  # This will be used for splitting data
from sklearn.feature_extraction.text import TfidfVectorizer  # This is used to extract features from text
from sklearn.linear_model import LogisticRegression  # We will use logistic regression to classify something as "spam" or not

def log1_prediction(text):
    new_input = [text]
    input_data_features = feature_extraction.transform(new_input)
    new_prediction = model.predict(input_data_features)

    if new_prediction == "spam":
        return True
    else:
        return False

# Importing the data from CSV --> for open-source data used, check GitHub links in the repository
spamData = pd.read_csv(r"Data/spam.csv", encoding = "latin1")

X = spamData["v2"]
Y = spamData["v1"]

# Split the data into training and testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 1)

# Creating model and standardizing data
feature_extraction = TfidfVectorizer(min_df = 110, max_df = 3000, stop_words = "english", lowercase = True)
X_train_features = feature_extraction.fit_transform(X_train)
X_test_features = feature_extraction.transform(X_test)

model = LogisticRegression()

model.fit(X_train_features, Y_train)
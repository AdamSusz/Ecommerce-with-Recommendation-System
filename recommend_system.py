from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
import requests
import re
import numpy as np
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Get data from fakestoreAPI
def get_products():
    url = 'https://fakestoreapi.com/products'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_categories():
    categories = list(set(p['category'] for p in get_products()))
    return categories

def get_user_features(user_profile):
    # Encode gender
    gender_map = {'male': 0, 'female': 1, 'other': 2}
    gender_feature = np.array([gender_map.get(user_profile.get('gender', 'male'), 0)])
    gender_vector = np.zeros(3)
    gender_vector[gender_feature] = 1


    # Obtain info from past purchases
    past_purchases = user_profile.get('past_purchases', [])
    categories = get_categories()

    category_counts = defaultdict(int)
    total_spent = 0
    
    for purchase in past_purchases:
        category_counts[purchase['category']] += 1
        total_spent += purchase['price']
    
    # Create normalized category preference vector
    total_purchases = len(past_purchases) if past_purchases else 1
    category_vector = [category_counts[cat] / total_purchases for cat in categories]

    average_spend = total_spent / max(len(past_purchases), 1)

    user_vector = np.hstack([gender_vector, category_vector, average_spend])
    return user_vector

# Return the gender of the product based on name or category using regex
def get_product_gender(product):
    title = product.get('title', '').lower()
    category = product.get('category', '').lower()

    if re.search(r'\b(women|woman|female)\b', title) or re.search(r'\b(women|woman|female)\b', category):
        return 1
    elif re.search(r'\b(men|man|male)\b', title) or re.search(r'\b(men|man|male)\b', category):
        return 0
    else:
        return 2

def get_product_features(product):
    gender = get_product_gender(product)

    categories = get_categories()
    category_index = {category: index for index, category in enumerate(categories)}
    category_vector = np.zeros(len(categories))

    if product['category'] in category_index:
        category_vector[category_index[product['category']]] = 1
    
    price_vector = np.array([product['price']])

    num_genders = 3
    gender_vector = np.zeros(num_genders)
    gender_vector[gender] = 1
    
    product_features = np.concatenate([gender_vector, category_vector, price_vector])
    return product_features

def get_recommendations(user_profile, n=5):
    product_data = get_products()
    user_vector = get_user_features(user_profile)
    
    product_features = []

    for product in product_data:
        product_features.append(get_product_features(product))

    knn = NearestNeighbors(n_neighbors=n, metric='cosine')
    knn.fit(product_features)
    
    # Find nearest neighbors
    _, indices = knn.kneighbors([user_vector])
    
    # Get recommended products
    recommended_products = [product_data[i] for i in indices[0]]
    return recommended_products

# Load test user from JSON file
with open('src/testUser.json', 'r') as f:
    test_user = json.load(f)

# Reccomend based on current productID
@app.route('/recommend', methods=['GET'])
def recommend():

    user_profile = test_user
    recommendations = get_recommendations(user_profile, n=5)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
    with open('src/testUser.json', 'r') as f:
        test_user = json.load(f)

    # Get recommendations
    recommended_products = get_recommendations(test_user, n=5)

    # Print the recommendations
    print("Recommended Products:")
    for idx, product in enumerate(recommended_products, 1):
        print(f"{idx}. {product['title']} - ${product['price']}")


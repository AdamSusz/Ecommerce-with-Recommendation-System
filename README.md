# Ecommerce with User Based Recommendation System

## Running the App
To run the app, unzip it and head over to the ecommerce directory:

```bash
cd ecommerce
```

Then install the necessary Python requirements using:

```bash
pip install -r requirements.txt
```

Then install dependencies using:

```bash
npm install
```
or, if needed for compatibility:

```bash
npm install react-material-ui-carousel --save --legacy-peer-deps
```

Now you can start the frontend server using:

```bash
npm start
```

And start the Flask backend recommendation system using:

```bash
python recommend_system.py
```


## Recommendation System
I decided to go for the Recommendation system and implemented it using a K-Nearest Neighbours approach based on user data such as gender and past purchases. This way the product data from the page is clustered into its groups and shows similarity between categories as well as within categories which helps with less populated categories. Then it determines the gender of the product using normal regex so it recommends male items for men and female items for women with the rest being recommended to everyone. The users purchase history gives data on catoeries they frequently purchase from as well as a price range allowing to recommend items with a similar price to their average spend. 

This feature can be integrated with the blockchain by recommending certain cryptocurrencies to individuals based on their purchasing habits, for example if a user has a history of purchasing highly volatile and high risk crypto currencies, other high risk ones can be pushed to them.

## Tools & Libraries

- **Flask:** Used to connect with the frontend due to its simplicity and my experience, which made implementation smoother.
- **Scikit-Learn:** Used for the recommendation system because of the limited data size and its efficiency on standard hardware. The built-in KNN implementation is well-suited for this task.
- **NumPy:** Used to efficiently vectorize all necessary features and speed up execution.

---

## Assumptions
This code has only been tested on a Linux system and its functionality is only guaranteed on Linux. Frontend changes were made to be functional and not pretty. Flask API uses fetch requests to FakeStoreAPI and was not made to work with static JSON objects for recommendations. Currently implementation is hard coded to use the testUser.json for its recommendations.


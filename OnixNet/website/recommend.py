from .models import Reaction, Post
import pandas as pd

# Reccomendation
import pandas as pd
import numpy as np
import scipy.stats
from sklearn.metrics.pairwise import cosine_similarity


class Recommend():
    def Update(self):
        self.ratings = pd.DataFrame.from_records(Reaction.objects.all().values())
        self.ratings = self.ratings.rename(columns={"user_id": "userId", "parent_post_id": "postId", "vote": "rating"})
        self.ratings["rating"] = self.ratings["rating"].astype(int)
        # print(ratings.head())
        self.posts = pd.DataFrame.from_records(Post.objects.all().values("id", "title"))
        self.posts = self.posts.rename(
            columns={"id": "postId"}
        )

        # print(posts.head())
        self.df = pd.merge(self.ratings, self.posts, on="postId", how="inner")
        # print(df.head())

        # Aggregate by movie
        self.agg_ratings = (
            self.df.groupby("title")
            .agg(mean_rating=("rating", "mean"), number_of_ratings=("rating", "count"))
            .reset_index()
        )

        # Keep the movies with over 100 ratings
        self.agg_ratings_GT100 = self.agg_ratings[self.agg_ratings["number_of_ratings"] > 0]
        self.df_GT100 = pd.merge(self.df, self.agg_ratings_GT100[["title"]], on="title", how="inner")
        # Create user-item matrix
        self.matrix = self.df_GT100.pivot_table(index='userId', columns='postId', values='rating')
        self.matrix_norm = self.matrix.subtract(self.matrix.mean(axis=1), axis="rows")

        self.user_similarity = self.matrix_norm.T.corr()
        self.user_similarity_cosine = cosine_similarity(self.matrix_norm.fillna(0))
    def Recommend(self, picked_userid):
        self.user_similarity.drop(index=picked_userid, inplace=True)
        # Number of similar users
        n = 10

        # User similarity threashold
        user_similarity_threshold = 0.3

        # Get top n similar users
        similar_users = self.user_similarity[self.user_similarity[picked_userid] > user_similarity_threshold][picked_userid].sort_values(ascending=False)[:n]

        # Print out top n similar users
        print(f"The similar users for user {picked_userid} are", similar_users)
        picked_userid_watched = self.matrix_norm[self.matrix_norm.index == picked_userid].dropna(
            axis=1, how="all"
        )
        similar_user_movies = self.matrix_norm[self.matrix_norm.index.isin(similar_users.index)].dropna(axis=1, how='all')
        similar_user_movies.drop(
            picked_userid_watched.columns, axis=1, inplace=True, errors="ignore"
        )
        # A dictionary to store item scores
        item_score = {}

        # Loop through items
        for i in similar_user_movies.columns:
            # Get the ratings for movie i
            movie_rating = similar_user_movies[i]
            # Create a variable to store the score
            total = 0
            # Create a variable to store the number of scores
            count = 0
            # Loop through similar users
            for u in similar_users.index:
                # If the movie has rating
                if pd.isna(movie_rating[u]) == False:
                    # Score is the sum of user similarity score multiply by the movie rating
                    score = similar_users[u] * movie_rating[u]
                    # Add the score to the total score for the movie so far
                    total += score
                    # Add 1 to the count
                    count += 1
            # Get the average score for the item
            item_score[i] = total / count

        # Convert dictionary to pandas dataframe
        item_score = pd.DataFrame(item_score.items(), columns=["post", "post_score"])

        # Sort the movies by score
        ranked_item_score = item_score.sort_values(by="post_score", ascending=False)

        # Select top m movies
        m = 10
        self.user_similarity = self.matrix_norm.T.corr()

        return ranked_item_score
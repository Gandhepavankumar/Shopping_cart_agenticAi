"""Reviews API is used to read the reviews from the `reviews` table in the database (store_db)
and returns aggregated rating information for products ."""

import sqlite3
import os

DB_path = os.path.join(os.path.dirname(__file__), "store_db.db")

def get_reviews(product_id):
    """Fetches reviews for a given product_id from the database and returns aggregated rating information."""
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    
    # Fetch reviews for the specified product_id
    cursor.execute("SELECT rating FROM reviews WHERE product_id = ?", (product_id,))
    ratings = cursor.fetchall()
    
    conn.close()
    
    if not ratings:
        return {"product_id": product_id, "average_rating": None, "total_reviews": 0}
    
    # Calculate average rating and total number of reviews
    total_reviews = len(ratings)
    average_rating = sum(rating[0] for rating in ratings) / total_reviews
    
    return {
        "product_id": product_id,
        "average_rating": round(average_rating, 2),
        "total_reviews": total_reviews
    }  

if __name__ == "__main__":
    # Example usage
    product_id = 1  # Replace with actual product_id to test
    reviews_info = get_reviews(product_id)
    print(reviews_info)
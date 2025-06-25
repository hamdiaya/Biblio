from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent

# Instantiating a FastAPI object
app = FastAPI()

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_csv(filename: str):
    """Helper function to load CSV files from data directory"""
    file_path = BASE_DIR / "data" / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} not found")
    return pd.read_csv(file_path)

@app.get("/get10TopBooks")
async def get_top_10_books():
    try:
        # Load the data
        df = load_csv("final_rules2.csv")
        df_books = load_csv("books.csv")

        # Sort by antecedent support in descending order
        df_sorted = df.sort_values(by="antecedent support", ascending=False)

        # Drop duplicates based on antecedents
        df_distinct = df_sorted.drop_duplicates(subset="antecedents", keep="first")

        # Select the top 20 rows
        top_20_distinct = df_distinct.head(20)

        # Ensure proper data handling in the "antecedents" column
        top_20_distinct["antecedents"] = top_20_distinct["antecedents"].apply(
            lambda x: list(x) if isinstance(x, set) else x
        )

        # Merge with book details
        merged_df = pd.merge(
            top_20_distinct,
            df_books,
            left_on="antecedents",
            right_on="title",
            how="inner"
        )

        # Keep only the required columns
        filtered_df = merged_df[[
            "antecedents", "image_url_x", "image_url_y", 
            "small_image_url", "book_rating", "book_desc", "book_authors"
        ]]

        # Fill missing values
        filtered_df['book_desc'].fillna(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            inplace=True
        )
        filtered_df.fillna('', inplace=True)

        return filtered_df.to_dict(orient="records")

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing expected column in data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get('/get10TopAuthors')
async def get_top_10_authors():
    try:
        # Load the data
        df = load_csv("final_rules2.csv")
        df_books = load_csv("books.csv")

        # Sort by antecedent support
        df_sorted = df.sort_values(by="antecedent support", ascending=False)

        # Merge with book details
        new_df = pd.merge(
            df_sorted,
            df_books,
            left_on="antecedents",
            right_on="title",
            how="inner"
        )

        # Drop duplicates
        new_df = new_df.drop_duplicates(
            subset=["antecedents", "book_authors"],
            keep="first"
        )

        # Get top 10 authors
        top_10_authors = new_df['book_authors'].head(10).tolist()

        return {"top_10_authors": top_10_authors}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing expected column in data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/getBookInfo/{book_title}")
async def get_book_info(book_title: str):
    try:
        # Load the data
        df = load_csv("final_rules2.csv")
        df2 = load_csv("books.csv")

        # Merge to get the book's general info
        new_df = pd.merge(
            df[df['antecedents'] == book_title],
            df2,
            left_on="antecedents",
            right_on="title",
            how="inner"
        )

        if new_df.empty:
            raise HTTPException(
                status_code=404,
                detail="Book title not found in database."
            )

        # Fill missing values
        new_df['book_desc'].fillna(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            inplace=True
        )
        new_df.fillna('', inplace=True)

        # Create general info dictionary
        general_info = {
            'title': book_title,
            'desc': new_df['book_desc'].iloc[0],
            'book_author': new_df['book_authors'].iloc[0],
            'rating': new_df['book_rating'].iloc[0],
            'image_url_x': new_df['image_url_x'].iloc[0],
            'image_url_y': new_df['image_url_y'].iloc[0],
            'small_image_url': new_df['small_image_url'].iloc[0],
            'reads': new_df['book_rating_count'].iloc[0]
        }

        # Get recommended books
        recommended_books_details = pd.merge(
            new_df[['consequents']],
            df2,
            left_on="consequents",
            right_on="title",
            how="inner"
        )

        # Clean recommended books data
        recommended_books_details['book_desc'].fillna(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            inplace=True
        )
        recommended_books_details.fillna('', inplace=True)
        recommended_books_list = recommended_books_details.drop_duplicates('title')
        recommended_books_list = recommended_books_list[[
            'title', 'book_rating', 'book_desc',
            'image_url_x', 'image_url_y', 'small_image_url', 'book_authors'
        ]].to_dict(orient='records')

        # Get author's other books
        book_author = new_df['book_authors'].iloc[0]
        author_books = df2[df2['book_authors'] == book_author][[
            "title", "image_url_x", "image_url_y",
            "small_image_url", "book_rating", "book_desc"
        ]]

        # Filter out the current book and unavailable books
        author_books = author_books[author_books['title'] != book_title]
        available_books = df['antecedents'].unique()
        author_books = author_books[author_books['title'].isin(available_books)]
        
        # Clean author books data
        author_books['book_desc'].fillna(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            inplace=True
        )
        author_books.fillna('', inplace=True)
        author_books = author_books.drop_duplicates('title')
        author_books = author_books.to_dict(orient='records')

        return {
            'title': book_title,
            'general_info': general_info,
            'recommended_books': recommended_books_list,
            'author_books': author_books
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing expected column in data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
import os
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Get absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Endpoint 1: Get 10 Top Books ----------
@app.get("/get10TopBooks")
async def get_top_10_books():
    try:
        rules_path = os.path.join(BASE_DIR, "data", "final_rules2.csv")
        books_path = os.path.join(BASE_DIR, "data", "books.csv")

        df = pd.read_csv(rules_path)
        df_books = pd.read_csv(books_path)

        df_sorted = df.sort_values(by="antecedent support", ascending=False)
        df_distinct = df_sorted.drop_duplicates(subset="antecedents", keep="first")
        top_10_distinct = df_distinct.head(20)

        top_10_distinct["antecedents"] = top_10_distinct["antecedents"].apply(
            lambda x: list(x) if isinstance(x, set) else x
        )

        merged_df = pd.merge(
            top_10_distinct,
            df_books,
            left_on="antecedents",
            right_on="title",
            how="inner"
        )

        filtered_df = merged_df[[
            "antecedents", "image_url_x", "image_url_y", "small_image_url",
            "book_rating", "book_desc", "book_authors"
        ]]

        filtered_df['book_desc'].fillna('Lorem ipsum...', inplace=True)
        filtered_df.fillna('', inplace=True)

        return filtered_df.to_dict(orient="records")

    except FileNotFoundError as e:
        return {"error": "File not found", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}


# ---------- Endpoint 2: Get 10 Top Authors ----------
@app.get("/get10TopAuthors")
async def get_top_10_authors():
    try:
        rules_path = os.path.join(BASE_DIR, "data", "final_rules2.csv")
        books_path = os.path.join(BASE_DIR, "data", "books.csv")

        df = pd.read_csv(rules_path)
        df_books = pd.read_csv(books_path)

        df_sorted = df.sort_values(by="antecedent support", ascending=False)
        new_df = pd.merge(
            df_sorted,
            df_books,
            left_on="antecedents",
            right_on="title",
            how="inner"
        )

        new_df = new_df.drop_duplicates(subset=["antecedents", "book_authors"], keep="first")
        top_10_authors = new_df["book_authors"].head(10).tolist()

        return {"top_10_authors": top_10_authors}

    except FileNotFoundError as e:
        return {"error": "File not found", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}


# ---------- Endpoint 3: Get Book Info ----------
@app.get("/getBookInfo/{book_title}")
async def get_book_info(book_title: str):
    try:
        rules_path = os.path.join(BASE_DIR, "data", "final_rules2.csv")
        books_path = os.path.join(BASE_DIR, "data", "books.csv")

        df = pd.read_csv(rules_path)
        df_books = pd.read_csv(books_path)

        new_df = pd.merge(
            df[df['antecedents'] == book_title],
            df_books,
            left_on="antecedents",
            right_on="title",
            how="inner"
        )

        if new_df.empty:
            return {"error": "Book title not found in database."}

        new_df['book_desc'].fillna('Lorem ipsum...', inplace=True)
        new_df.fillna('', inplace=True)

        general_info = {
            'title': book_title,
            'desc': new_df['book_desc'][0],
            'book_author': new_df['book_authors'][0],
            'rating': new_df['book_rating'][0],
            'image_url_x': new_df['image_url_x'][0],
            'image_url_y': new_df['image_url_y'][0],
            'small_image_url': new_df['small_image_url'][0],
            'reads': new_df['book_rating_count'].tolist()[0]
        }

        recommended_books_details = pd.merge(
            new_df[['consequents']],
            df_books,
            left_on="consequents",
            right_on="title",
            how="inner"
        )
        recommended_books_details['book_desc'].fillna('Lorem ipsum...', inplace=True)
        recommended_books_details.fillna('', inplace=True)

        recommended_books_list = recommended_books_details.drop_duplicates('title')[[
            "title", "book_rating", "book_desc",
            "image_url_x", "image_url_y", "small_image_url", "book_authors"
        ]].to_dict(orient='records')

        book_author = new_df['book_authors'][0]
        author_books = df_books[df_books['book_authors'] == book_author][[
            "title", "image_url_x", "image_url_y", "small_image_url", "book_rating", "book_desc"
        ]]
        author_books = author_books[author_books['title'] != book_title]
        available_books = df['antecedents'].unique()
        author_books = author_books[author_books['title'].isin(available_books)]
        author_books['book_desc'].fillna('Lorem ipsum...', inplace=True)
        author_books.fillna('', inplace=True)
        author_books = author_books.drop_duplicates('title').to_dict(orient='records')

        return {
            'title': book_title,
            'general_info': general_info,
            'recommended_books': recommended_books_list,
            'author_books': author_books
        }

    except FileNotFoundError as e:
        return {"error": "File not found", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}

from fastapi import FastAPI
import pandas as pd
import numpy as np

from fastapi.middleware.cors import CORSMiddleware

# Instantiating a FastAPI object
app = FastAPI()
# CORS configuration
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Creating a GET endpoint
@app.get("/get10TopBooks")
async def get_top_10_books():
    try:
        # Load the rules DataFrame
        df = pd.read_csv('./data/final_rules2.csv')

        # Sort by antecedent support in descending order
        df_sorted = df.sort_values(by="antecedent support", ascending=False)

        # Drop duplicates based on antecedents
        df_distinct = df_sorted.drop_duplicates(subset="antecedents", keep="first")

        # Select the top 10 rows
        top_10_distinct = df_distinct.head(20)

        # Ensure proper data handling in the "antecedents" column
        top_10_distinct["antecedents"] = top_10_distinct["antecedents"].apply(
            lambda x: list(x) if isinstance(x, set) else x
        )

        # Load the book details DataFrame
        df_books = pd.read_csv('data/books.csv')

        # Merge with book details DataFrame on the specified columns
        merged_df = pd.merge(
            top_10_distinct,
            df_books,
            left_on="antecedents",  # Adjust this based on actual column names
            right_on="title",       # Adjust this based on actual column names
            how="inner"             # Perform an inner join
        )

        # Keep only the required columns
        filtered_df = merged_df[["antecedents", "image_url_x", "image_url_y", "small_image_url", "book_rating", "book_desc","book_authors"]]

        # Replace NaN and infinite values with empty strings
        
        filtered_df['book_desc'].fillna('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmodLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' , inplace=True)
        filtered_df.fillna('',inplace=True)
        # Convert the filtered DataFrame to a list of dictionaries and return as JSON
        return filtered_df.to_dict(orient="records")

    except FileNotFoundError as e:
        return {"error": "File not found. Ensure the file paths are correct.", "details": str(e)}
    except KeyError as e:
        return {"error": "Key error. Verify column names in the DataFrames.", "details": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred.", "details": str(e)}





@app.get('/get10TopAuthors')
async def get_top_10_authors():
    try:
        # Load the rules DataFrame
        df = pd.read_csv('./data/final_rules2.csv')

        # Sort by antecedent support in descending order
        df_sorted = df.sort_values(by="antecedent support", ascending=False)

        # Load the books DataFrame
        df_books = pd.read_csv('./data/books.csv')

        # Merge the two DataFrames based on the columns "antecedents" and "title"
        new_df = pd.merge(
            df_sorted,
            df_books,
            left_on="antecedents",  # Adjust based on your column names
            right_on="title",       # Adjust based on your column names
            how="inner"             # Perform an inner join
        )

        # Drop duplicates based on 'antecedents' and 'book_authors' columns
        new_df = new_df.drop_duplicates(subset=["antecedents", "book_authors"], keep="first")

        # Get the top 10 distinct authors
        top_10_authors = new_df['book_authors'].head(10).tolist()

        return {"top_10_authors": top_10_authors}

    except FileNotFoundError as e:
        return {"error": "File not found. Ensure the file paths are correct.", "details": str(e)}
    except KeyError as e:
        return {"error": "Key error. Verify column names in the DataFrames.", "details": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred.", "details": str(e)}





@app.get("/getBookInfo/{book_title}")
async def get_book_info(book_title: str):
    #Load data
   
    df = pd.read_csv('./data/final_rules2.csv')
    df2 = pd.read_csv('./data/books.csv')
    print(book_title)
    # Merge to get the book's general info
    new_df = pd.merge(
        df[df['antecedents'] == book_title],
        df2, 
        left_on="antecedents", 
        right_on="title",  
        how="inner"
    )

    if new_df.empty:
        return {"error": "Book title not found in database."}
    
    # Fill NaN values with empty string or appropriate value
    new_df['book_desc'].fillna('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmodLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' , inplace=True)
    new_df.fillna('', inplace=True)

    # Create general info dictionary
    general_info = {
        'title': book_title,
        'desc': new_df['book_desc'][0],
        'book_author': new_df['book_authors'][0],
        'rating': new_df['book_rating'][0],
        'image_url_x': new_df['image_url_x'][0],
        'image_url_y': new_df['image_url_y'][0],
        'small_image_url': new_df['small_image_url'][0],
        'reads':new_df['book_rating_count'].tolist()[0]
    }
    
    # Get recommended books based on the consequents
    recommended_books_details = pd.merge(
        new_df[['consequents']],  
        df2, 
        left_on="consequents", 
        right_on="title",  
        how="inner"
    )
    
    # Fill NaN values
    recommended_books_details['book_desc'].fillna('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmodLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' , inplace=True)
    recommended_books_details.fillna('', inplace=True)

    # Select relevant columns and convert to list of dictionaries
    recommended_books_list=recommended_books_details.drop_duplicates('title')
    recommended_books_list = recommended_books_list[['title', 'book_rating', 'book_desc', 'image_url_x', 'image_url_y', 'small_image_url', 'book_authors']].to_dict(orient='records')
   
    # # Get the author's books
    book_author = new_df['book_authors'][0]
    author_books = df2[df2['book_authors'] == book_author][["title", "image_url_x", "image_url_y", "small_image_url", "book_rating", "book_desc"]]

    # Drop rows where 'title' is equal to 'book_title'
    author_books = author_books[author_books['title'] != book_title]
    
    # Get available books from the DataFrame
    available_books = df['antecedents'].unique()

    # Filter the author_books DataFrame to include only books whose titles are in available_books
    author_books = author_books[author_books['title'].isin(available_books)]
    author_books['book_desc'].fillna('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmodLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' , inplace=True)
    author_books.fillna('', inplace=True)
    author_books=author_books.drop_duplicates('title')
    # Convert author books to list of dictionaries
    author_books = author_books.to_dict(orient='records')

    #Return the general info and recommended books as a response
    return {
        'title':book_title,
        'general_info': general_info,
        'recommended_books': recommended_books_list,
        'author_books': author_books
    }

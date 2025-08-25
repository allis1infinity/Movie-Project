from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("""SELECT title, year, rating, poster_url 
                                            FROM movies"""))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies}

print(list_movies())

def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""INSERT INTO movies (title, year, rating, poster_url) 
                                           VALUES (:title, :year, :rating, :poster_url)"""),
                               {"title": title, "year": year, "rating": rating, "poster_url": poster_url})
            connection.commit()
            return f"Movie '{title}' added successfully."
        except Exception as error:
            return f"Error: {error}"


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""DELETE FROM movies
                                    WHERE LOWER(title) = LOWER(:title) """),
                               {"title": title})
            connection.commit()
            return f"Movie '{title}' successfully deleted."
        except Exception as error:
            return f"Error: {error}"


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""UPDATE movies 
                                    SET rating = :rating
                                    WHERE title = :title """),
                               {"title": title, "rating": rating})
            connection.commit()
            return f"Movie '{title}' successfully updated."
        except Exception as error:
           return f"Error: {error}"




from movie_storage_sql import list_movies


def serialize_movie(title, movie_info):
    """
    Formats the movie data into an HTML string
    """

    # define an empty string
    output = ""

    year = movie_info.get('year')
    rating = movie_info.get('rating')
    poster = movie_info.get('poster_url')

    # append information to each string
    output += '\n\t<li>'
    output += '\n\t\t<div class="movie">'
    output += f'\n\t\t\t<img class="movie-poster" src="{poster}" alt="Movie poster {title}"/>'
    output += f'\n\t\t\t<div class="movie-title">{title}</div>'
    output += f'\n\t\t\t<div class="movie-title">{year}</div>'
    output += f'\n\t\t\t<div class="movie-title">{rating} &starf;</div>'
    output += '\n\t\t</div>'
    output += '\n\t</li>'
    return output


def display_movies_info(movies_dict):
    """
    Receives a list of dictionaries with movies data and
    returns an HTML string with formatted information
    for all movies.
    """
    output = ""
    for title, movie_info in movies_dict.items():
        output += serialize_movie(title, movie_info )
    return output



def create_movie_webpage():
    """
   Generates a full HTML page and writes the result to a new file.
    """
    movies = list_movies()
    movie_html_content = display_movies_info(movies)

    # Read the content of the template file
    with open("_static/index_template.html","r") as file:
        template_html = file.read()

    # Replace text in html with extracted info
    movie_html = template_html.replace("__TEMPLATE_MOVIE_GRID__", movie_html_content)

    # Write the new HTML content to a new file, animals.html
    with open("movies.html", "w") as final_file:
        final_file.write(movie_html)

    return "Web-page 'movies.html' successfully generated"



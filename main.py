from random import choice
from movie_storage.movie_fetching import fetch_data
from movie_storage.movie_storage_sql import add_movie, list_movies, delete_movie, update_movie
from movies_web_generator import create_movie_webpage

def menu_option():
    """
    Returns a string containing the text for the main menu options.
    """
    menu_text = """Menu:
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating
    9. Generate Web page
    10. Exit"""
    return menu_text


def user_menu_choice():
    """
    Prompts the user to enter a menu choice (1-10).
    """
    user_option = input("Enter choice (1-10): ")
    return user_option


def print_movies():
    """
    Prints a formatted list of all movies, including their title, rating, and year.
    """
    movies = list_movies()
    print(f" {len(movies)} movie(s) in total")
    for title, movie_info in movies.items():
        print(f" <{title}> 🎞  rating: 🏆{movie_info['rating']}, {movie_info['year']}, {movie_info['poster_url']}")


def add_new_movie():
    """Adds a new movie to the movie database.
    """
    movie_to_add = input("Enter a movie do you want to add: ").strip()
    movie_info = fetch_data(movie_to_add)

    if movie_info and "Title" in movie_info:
        try:
            title = movie_info['Title']
            year = movie_info['Year']
            rating_info = movie_info['Ratings'][0]['Value']
            rating = rating_info.split('/')[0]
            poster = movie_info['Poster']
            
            return add_movie(title, year, rating, poster)
        except KeyError as error:
            return f"Error processing data: {error}"

    else:
        return f"Movie with the title '{movie_to_add}' was not found."






def delete_specific_movie():
    """
    Deletes a movie from the database.
    """
    movie_to_delete = input("Enter the movie you want to delete: ").strip()
    movies = list_movies()

    if movie_to_delete in movies:
        return delete_movie(movie_to_delete)
    else:
        return f"Movie '{movie_to_delete}' was not found."


def update_specific_movie():
    """
    Updates the rating for a movie in the database.
    """
    movie_to_update = input("Enter a movie name: ").strip()
    try:
        rating_to_update = float(input("Enter new movie rating (0-10): "))
        if not (0 <= rating_to_update <= 10):
            return "Rating should be in range from 0 to 10."
    except ValueError:
        return "Error: Rating should be a number"

    return update_movie(movie_to_update, rating_to_update)


def sorted_movies_by_rating():
    """
    Returns a list of movies sorted by their rating in descending order.
    """
    movies = list_movies()
    sorted_movies = sorted(movies.items(), key = lambda x: x[1]["rating"], reverse=True)
    return sorted_movies

def get_best_movie():
    """
    Returns the movie with the highest rating from the list.
    """
    sorted_info = sorted_movies_by_rating()
    best_rating = sorted_info[0][1]["rating"]
    best_movies = ""
    for title, movie_info in sorted_info:
        if movie_info["rating"] == best_rating:
            best_movies += title
    return f"Best movie: {best_movies}🎞️ with rating 👍{best_rating}"


def get_worst_movie():
    """
    Returns the movie with the lowest rating from the list.
    """
    sorted_info = sorted_movies_by_rating()
    worst_rating = sorted_info[-1][1]["rating"]
    worst_movies = ""
    for title, movie_info in sorted_info:
        if movie_info["rating"] == worst_rating:
            worst_movies += title
    return f"Worst movie: {worst_movies}🎞️ with rating 👎{worst_rating}"


def get_average():
    """
    Returns the average rating of the movies.
    """
    movies = list_movies()
    rating_list = []
    for title, movie_info in movies.items():
        rating_list.append(movie_info["rating"])
    average = (sum(rating_list) / len(rating_list))
    average = round(average, 1)
    return f"The average rating is 📈 {average}"


def get_median():
    """
    Returns the median rating of the movies.
    """
    movies = list_movies()
    rating_list = []
    movies_amount = len(movies)
    for title, movie_info in movies.items():
        rating_list.append(movie_info["rating"])
    movies_rating_list = sorted(rating_list)
    is_odd = movies_amount % 2 != 0
    middle_num = movies_amount // 2
    if is_odd:
        median_rating = movies_rating_list[middle_num]
    else:
        median_rating = (movies_rating_list[middle_num] + movies_rating_list[middle_num - 1]) / 2
    return f"The median rating is 📊 {median_rating}."


def get_statistic():
    """
    Returns a summary of movie statistics.
    """
    best = get_best_movie()
    worst = get_worst_movie()
    average = get_average()
    median = get_median()
    return f"{best}\n{worst}\n{average}\n{median}"


def get_random_movie():
    """
    Selects a random movie from the list.
    """
    movies = list_movies()
    # Get a list of movies keys
    movies_titles = list(movies.keys())
    random_title = choice(movies_titles)
    random_movie = movies[random_title]

    return f"Your movie for tonight:  {random_title} 🎞️ - rating:  🏆 {random_movie['rating']}, date of release: {random_movie['year']}"


def show_sorted_movie_info():
    """
    Sorts the movies by rating in descending order
    """

    sorted_movies = sorted_movies_by_rating()
    display_sorted_movie = ""
    for title, movies_info in sorted_movies:
        display_sorted_movie += f" Rating: {movies_info['rating']} 🏆 - {title} 🎞️, Year: {movies_info['year']}\n"

    return display_sorted_movie


def search_movie():
    """
    Searches for movies by a partial title match
    """
    movies = list_movies()
    user_search = input("Enter part of movie name: ")
    found_movies = ""
    for title, movie_info in movies.items():
        if user_search.lower() in title.lower():
            found_movies += f"{title} 🎞️, rating:🏆 {movie_info['rating']}, year: {movie_info['year']}\n"

    if found_movies == "":
        return f"No movies found"
    else:
        return found_movies


def main():
    """
     Runs the main application loop for the movie database.
    """
    while True:
        print(f"  ***************  My Movies Database  *****************")
        print()
        print(menu_option())
        print()
        user_choice = user_menu_choice()

        if user_choice == "1":
            print_movies()
        elif user_choice == "2":
            print(add_new_movie())
        elif user_choice == "3":
            print(delete_specific_movie())
        elif user_choice == "4":
            print(update_specific_movie())
        elif user_choice == "5":
            print(get_statistic())
        elif user_choice == "6":
            print(get_random_movie())
        elif user_choice == "7":
            print(search_movie())
        elif user_choice == "8":
            print(show_sorted_movie_info())
        elif user_choice == "9":
            print(create_movie_webpage())
        elif user_choice == "10":
            print("exit menu")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 9.")
        print()
        input("Press enter to continue ")


if __name__ == "__main__":
    main()





import random
from data import movie_storage_sql as storage
import data_fetcher


# Color definitions
LIGHT_PURPLE = "\033[1;35m"
BLINK = "\033[5m"
RESET = "\033[0m"  # reset colors settings
MENU = "\033[0;32m"  # green color
ENT_TO_CONT = "\033[1;34m"  # light blue
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
HEADER = LIGHT_PURPLE + BLINK  # combination of the purple color and the blink effect


def print_menu_header():
    """The function to print the menu header only"""
    header_text = "*" * 15 + " My Movies Database " + "*" * 15
    print(f"{HEADER}{header_text}{RESET}")


def print_menu_interface():
    """The function to print the menu interface"""
    menu_text = """Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate webpage"""

    print()
    print(f"{MENU}{menu_text}{RESET}")


def enter_to_continue():
    """Wait for user input before returning to the menu interface"""
    input(f"{ENT_TO_CONT}\nPress Enter to continue...{RESET}")


def command_exit_program():
    """The function activate exit and break program"""
    print(f"{YELLOW}\nGoodbye! Exiting the program...{RESET}")
    return False


def command_list_movies():
    """Retrieve and display all movies from the database (choice 1)"""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']} {data['poster_url']}")
    enter_to_continue()


def command_add_movie():
    """Add a new movie by fetching data from OMDB API (choice 2)"""
    print("Cool, now we are talking")

    while True:  # Loop to avoid empty movie name
        movie = input("Enter movie name to add: ").strip()
        if movie:
            break
        print(f"{RED}Error: Movie name cannot be empty.{RESET}")

    # Fetch movie data from OMDB API
    movie_data = data_fetcher.fetch_data(movie)

    if not movie_data:
        print(f"{RED}Error: Movie {movie} not found on OMDB.{RESET}")
        enter_to_continue()
        return

    try:
        # Extract relevant data from API response
        title = movie_data["title"]
        year = int(movie_data["year"][:4])
        rating_str = movie_data["rating"].split("/")[0]
        rating = float(rating_str)
        poster_url = movie_data["poster_url"]

        # Add movie to database
        storage.add_movie(title, year, rating, poster_url)
        print(f"The movie {title} ({year}) was successfully added with rating {rating}")
        print(f"Poster URL: {poster_url}")

    except KeyError as e:
        print(f"{RED}Error: Missing data in API response - {e}{RESET}")
    except ValueError as e:
        print(f"{RED}Error: Invalid data format - {e}{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

    enter_to_continue()


def command_delete_movie():
    """The function to delete movie (choice 3)"""
    movie = input("Enter movie name to delete: ").strip()
    if not movie:
        print(f"{RED}Error: Movie name cannot be empty.{RESET}")
        enter_to_continue()

    else:
        storage.delete_movie(movie)

    enter_to_continue()


def command_update_movie():
    """The function to update movie (choice 4)"""
    movie = input("Enter movie's name: ").strip()
    if not movie:
        print(f"{RED}Error: Movie name cannot be empty.{RESET}")
        enter_to_continue()
        return

    try:
        rating = float(input("Enter new movie rating (0-10): "))
        if 0 <= rating <= 10:
            storage.update_movie(movie, rating)
        else:
            print(f"{RED}Error: Rating must be between 0 and 10.{RESET}")
    except ValueError:
        print(f"{RED}Please enter a valid number for the rating{RESET}")

    enter_to_continue()


def calculate_average(ratings):
    """Calculate average rating"""
    return sum(ratings) / len(ratings)


def calculate_median(ratings):
    """Calculate median rating"""
    sorted_ratings = sorted(ratings)
    n = len(sorted_ratings)
    if n % 2 == 1:
        return sorted_ratings[n // 2]
    return (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2


def get_best_movies(movies_data):
    """Return list of best movies (max rating) with their data"""
    max_rating = max(movie["rating"] for movie in movies_data.values())
    return [(title, data) for title, data in movies_data.items()
            if data["rating"] == max_rating]


def get_worst_movies(movies_data):
    """Return list of worst movies (min rating) with their data"""
    min_rating = min(movie["rating"] for movie in movies_data.values())
    return [(title, data) for title, data in movies_data.items()
            if data["rating"] == min_rating]


def display_movie_list(movies, title):
    """Helper function to display movie lists"""
    print(f"\n{title}:")
    for movie, data in movies:
        print(f"- {movie} ({data["rating"]}), {data["year"]}, {data["poster_url"]}")


def show_statistics():
    """The function to show the statistics (choice 5)"""
    movies = storage.list_movies()
    ratings = [movie["rating"] for movie in movies.values()]

    print(f"Average rating: {calculate_average(ratings):.2f}")
    print(f"Median rating: {calculate_median(ratings):.1f}")

    display_movie_list(get_best_movies(movies), "Best movie(s)")
    display_movie_list(get_worst_movies(movies), "Worst movie(s)")
    enter_to_continue()


def random_movie():
    """The function to suggest and print a random movie (choice 6)"""
    movies = storage.list_movies()
    random_key = random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {random_key}, it's rated {movies[random_key]['rating']} "
          f"from year {movies[random_key]['year']}, poster: {movies[random_key]['poster_url']}")
    enter_to_continue()


def search_movie():
    """The function for search case insensitive (choice 7)"""
    movies = storage.list_movies()
    search_movie_input = input("Enter part of movie name: ").lower()
    found = False
    for movie, data in movies.items():
        if search_movie_input in movie.lower():
            print(f"{movie}: Rating - {data['rating']} | Year - {data['year']}")
            found = True
    if not found:
        print(f"{RED}The movie {search_movie_input} not found{RESET}")

    enter_to_continue()


def sorting_movies_by_rating():
    """The function for sorting movies by rating (choice 8)"""
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
    for movie, data in sorted_movies:
        print(f"{movie}: Rating - {data['rating']} | Year - {data['year']}")

    enter_to_continue()


def generate_webpage():
    """Generates a static HTML page displaying all movies."""
    movies = storage.list_movies()

    try:
        with open("_static/index_template.html", "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError:
        print(f"{RED}Error: index_template.html not found.{RESET}")
        return

    movie_grid_items = []
    for title, data in movies.items():
        poster = data["poster_url"] if data["poster_url"] != "N/A" else ""
        movie_item = f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{poster}" alt="Poster for {title}">
                <div class="movie-title">{title}</div>
                <div class="movie-year">{data["year"]}</div>
                <div class="movie-rating">Rating: {data["rating"]}</div>
            </div>
        </li>"""
        movie_grid_items.append(movie_item.strip())

    filled_html = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    filled_html = filled_html.replace("__TEMPLATE_MOVIE_GRID__", "\n".join(movie_grid_items))

    with open("index.html", "w", encoding="utf-8") as output_file:
        output_file.write(filled_html)
    print()
    print("Website was generated successfully.")


def main():
    """The program to manage the database for movies json file storage.
    Use the dispatch function feature by user choice function."""

    dispatch_func = {
        "0": command_exit_program,
        "1": command_list_movies,
        "2": command_add_movie,
        "3": command_delete_movie,
        "4": command_update_movie,
        "5": show_statistics,
        "6": random_movie,
        "7": search_movie,
        "8": sorting_movies_by_rating,
        "9": generate_webpage
    }
    print_menu_header()

    while True:

        print_menu_interface()
        choice_directory = input("\nEnter choice (0-9): ")

        selected_function = dispatch_func.get(choice_directory)

        if selected_function:
            # Execute the function and check if it returns False for exit
            if selected_function() is False:
                break
        else:
            print(f"{RED}Invalid choice! Please enter a number between 0-8{RESET}")
            enter_to_continue()


if __name__ == "__main__":
    main()

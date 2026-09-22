class Movie:
    def __init__(self, title):
        self.title = title
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Rented"
        return f"{self.title} - {status}"


class Customer:
    def __init__(self, name):
        self.name = name
        self.rented_movies = []

    def rent_movie(self, movie):
        self.rented_movies.append(movie)

    def return_movie(self, movie):
        self.rented_movies.remove(movie)


class MovieRentalSystem:
    def __init__(self):
        self.movies = []
        self.customers = []

    def add_movie(self, title):
        movie = Movie(title)
        self.movies.append(movie)
        print(f"Movie '{title}' added successfully.")

    def register_customer(self, name):
        customer = Customer(name)
        self.customers.append(customer)
        print(f"Customer '{name}' registered successfully.")

    def rent_movie(self, customer_name, movie_title):
        customer = self.find_customer(customer_name)
        movie = self.find_movie(movie_title)

        if customer and movie:
            if movie.is_available:
                movie.is_available = False
                customer.rent_movie(movie)
                print(f"{customer_name} rented '{movie_title}'.")
            else:
                print("Movie is already rented.")
        else:
            print("Customer or Movie not found.")

    def return_movie(self, customer_name, movie_title):
        customer = self.find_customer(customer_name)
        movie = self.find_movie(movie_title)

        if customer and movie:
            if movie in customer.rented_movies:
                movie.is_available = True
                customer.return_movie(movie)
                print(f"{customer_name} returned '{movie_title}'.")
            else:
                print("This movie was not rented by the customer.")
        else:
            print("Customer or Movie not found.")

    def display_movies(self):
        print("\nAvailable Movies:")
        for movie in self.movies:
            print(movie)

    def find_movie(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie
        return None

    def find_customer(self, name):
        for customer in self.customers:
            if customer.name == name:
                return customer
        return None


# -------- MAIN PROGRAM --------
system = MovieRentalSystem()

while True:
    print("\n--- Movie Rental System ---")
    print("1. Add Movie")
    print("2. Register Customer")
    print("3. Rent Movie")
    print("4. Return Movie")
    print("5. Display Movies")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter movie title: ")
        system.add_movie(title)

    elif choice == "2":
        name = input("Enter customer name: ")
        system.register_customer(name)

    elif choice == "3":
        name = input("Enter customer name: ")
        title = input("Enter movie title: ")
        system.rent_movie(name, title)

    elif choice == "4":
        name = input("Enter customer name: ")
        title = input("Enter movie title: ")
        system.return_movie(name, title)

    elif choice == "5":
        system.display_movies()

    elif choice == "6":
        print("Exiting system...")
        break

    else:
        print("Invalid choice. Try again.")  
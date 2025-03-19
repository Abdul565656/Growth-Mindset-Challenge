import json
from typing import List, Dict, Union
import os

class LibraryManager:
    def __init__(self, filename: str = "library.txt"):
        """Initialize the library manager."""
        self.books: List[Dict[str, Union[str, int, bool]]] = []
        self.filename = filename
        self.load_library()
        if len(self.books) == 0:  # If library is empty after loading, add default books
            self._add_default_books()
            self.save_library()  # Save the default books to file

    def _add_default_books(self) -> None:
        """Add a default set of books to the library."""
        default_books = [
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "year": 1960,
                "genre": "Literary Fiction",
                "read": True
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "year": 1949,
                "genre": "Dystopian Fiction",
                "read": False
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "year": 1937,
                "genre": "Fantasy",
                "read": True
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "year": 1813,
                "genre": "Romance",
                "read": False
            },
            {
                "title": "The Da Vinci Code",
                "author": "Dan Brown",
                "year": 2003,
                "genre": "Mystery Thriller",
                "read": True
            },
            {
                "title": "The Hunger Games",
                "author": "Suzanne Collins",
                "year": 2008,
                "genre": "Young Adult",
                "read": False
            },
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "year": 1965,
                "genre": "Science Fiction",
                "read": True
            },
            {
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "year": 1988,
                "genre": "Philosophical Fiction",
                "read": False
            }
        ]
        
        self.books = default_books  # Replace any existing books with defaults
        print("Default books have been added to your library!")

    def load_library(self) -> None:
        """Load the library from a file if it exists."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    data = file.read().strip()
                    if data:  # Only try to load if file is not empty
                        self.books = json.loads(data)
                        print(f"Loaded {len(self.books)} books from {self.filename}")
                    else:
                        self.books = []
            else:
                self.books = []
                print("No existing library file found. Creating new library...")
        except Exception as e:
            print(f"Error loading library: {e}")
            self.books = []

    def save_library(self) -> None:
        """Save the library to a file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.books, file, indent=4)
            print("Library saved successfully!")
        except Exception as e:
            print(f"Error saving library: {e}")

    def add_book(self) -> None:
        """Add a new book to the library."""
        try:
            print("\nEnter book details:")
            title = input("Enter the book title: ").strip()
            author = input("Enter the author: ").strip()
            
            while True:
                try:
                    year = int(input("Enter the publication year: "))
                    if 0 <= year <= 2024:  # Basic validation
                        break
                    print("Please enter a valid year (0-2024)")
                except ValueError:
                    print("Please enter a valid number for the year")
            
            genre = input("Enter the genre: ").strip()
            read_status = input("Have you read this book? (yes/no): ").lower().strip()
            read = read_status in ['yes', 'y', 'true']

            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            
            self.books.append(book)
            print("\nBook added successfully!")
        except Exception as e:
            print(f"Error adding book: {e}")

    def remove_book(self) -> None:
        """Remove a book from the library."""
        title = input("\nEnter the title of the book to remove: ").strip()
        initial_length = len(self.books)
        self.books = [book for book in self.books if book["title"].lower() != title.lower()]
        
        if len(self.books) < initial_length:
            print("Book removed successfully!")
        else:
            print("Book not found in the library.")

    def search_book(self) -> None:
        """Search for a book by title or author."""
        print("\nSearch by:")
        print("1. Title")
        print("2. Author")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            search_term = input("Enter the title: ").lower().strip()
            results = [book for book in self.books if search_term in book["title"].lower()]
            search_type = "title"
        elif choice == "2":
            search_term = input("Enter the author: ").lower().strip()
            results = [book for book in self.books if search_term in book["author"].lower()]
            search_type = "author"
        else:
            print("Invalid choice!")
            return

        if results:
            print(f"\nMatching Books for {search_type} '{search_term}':")
            self._display_books(results)
        else:
            print(f"No books found matching the {search_type}.")

    def _display_books(self, books: List[Dict[str, Union[str, int, bool]]]) -> None:
        """Helper method to display a list of books."""
        if not books:
            print("No books to display!")
            return
            
        for i, book in enumerate(books, 1):
            read_status = "Read" if book["read"] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")

    def display_all_books(self) -> None:
        """Display all books in the library."""
        print("\nYour Library:")
        print("=" * 80)
        
        if len(self.books) == 0:
            print("Your library is empty!")
            return
        
        self._display_books(self.books)
        print("=" * 80)

    def display_statistics(self) -> None:
        """Display library stati4stics."""
        print("\nLibrary Statistics:")
        print("=" * 80)  # Add a separator line
        
        if not isinstance(self.books, list) or len(self.books) == 0:
            print("No books in the library!")
            return

        total_books = len(self.books)
        read_books = sum(1 for book in self.books if book.get("read", False))
        percent_read = (read_books / total_books) * 100 if total_books > 0 else 0

        print(f"Total number of books: {total_books}")
        print(f"Number of books read: {read_books}")
        print(f"Percentage of books read: {percent_read:.1f}%")
        
        # Add genre statistics
        genres = {}
        for book in self.books:
            genre = book.get("genre", "Unknown")
            genres[genre] = genres.get(genre, 0) + 1
        
        print("\nBooks by Genre:")
        for genre, count in genres.items():
            print(f"{genre}: {count} book(s)")
        print("=" * 80)  # Add a separator line

def display_menu() -> None:
    """Display the main menu."""
    print("\nWelcome to your Personal Library Manager!")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

def main():
    library = LibraryManager()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.remove_book()
        elif choice == "3":
            library.search_book()
        elif choice == "4":
            library.display_all_books()
        elif choice == "5":
            library.display_statistics()
        elif choice == "6":
            library.save_library()
            print("\nThank you for using Personal Library Manager. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main() 




# import json
# import os
# from typing import List, Dict

# class LibraryManager:
#     def __init__(self, filename: str = "library.txt"):
#         self.filename = filename
#         self.books: List[Dict] = self.load_library() or self._add_default_books()

#     def _add_default_books(self) -> List[Dict]:
#         books = [
#             {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "genre": "Fiction", "read": True},
#             {"title": "1984", "author": "George Orwell", "year": 1949, "genre": "Dystopian", "read": False},
#             {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937, "genre": "Fantasy", "read": True},
#         ]
#         self.save_library(books)
#         return books

#     def load_library(self) -> List[Dict]:
#         if os.path.exists(self.filename):
#             with open(self.filename, 'r') as file:
#                 return json.load(file) or []
#         return []

#     def save_library(self, books: List[Dict] = None) -> None:
#         with open(self.filename, 'w') as file:
#             json.dump(books or self.books, file, indent=4)

#     def add_book(self) -> None:
#         title = input("Title: ").strip()
#         author = input("Author: ").strip()
#         year = input("Year: ").strip()
#         genre = input("Genre: ").strip()
#         read = input("Read? (yes/no): ").strip().lower() in ["yes", "y"]
#         self.books.append({"title": title, "author": author, "year": int(year), "genre": genre, "read": read})
#         self.save_library()
#         print("Book added!")

#     def remove_book(self) -> None:
#         title = input("Title to remove: ").strip()
#         self.books = [book for book in self.books if book["title"].lower() != title.lower()]
#         self.save_library()
#         print("Book removed!" if self.books else "Book not found!")

#     def search_book(self) -> None:
#         term = input("Search by title or author: ").strip().lower()
#         results = [b for b in self.books if term in b["title"].lower() or term in b["author"].lower()]
#         self._display_books(results)

#     def display_all_books(self) -> None:
#         self._display_books(self.books)

#     def _display_books(self, books: List[Dict]) -> None:
#         if not books:
#             print("No books found!")
#         for i, book in enumerate(books, 1):
#             print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

#     def display_statistics(self) -> None:
#         total, read = len(self.books), sum(1 for b in self.books if b["read"])
#         print(f"Total books: {total}, Read: {read}, Unread: {total - read}")


# def main():
#     library = LibraryManager()
#     options = {"1": library.add_book, "2": library.remove_book, "3": library.search_book, "4": library.display_all_books, "5": library.display_statistics}
    
#     while (choice := input("1:Add 2:Remove 3:Search 4:Display 5:Stats 6:Exit\nChoose: ")) != "6":
#         options.get(choice, lambda: print("Invalid choice!"))()
    
#     library.save_library()
#     print("Goodbye!")

# if __name__ == "__main__":
#     main()

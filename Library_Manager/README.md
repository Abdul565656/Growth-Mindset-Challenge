# Personal Library Manager

A command-line application to manage your personal book collection. This program allows you to keep track of your books, including details like title, author, publication year, genre, and reading status.

## Features

- Add new books to your library
- Remove books from your library
- Search for books by title or author
- Display all books in your collection
- View library statistics (total books and reading progress)
- Automatic saving and loading of your library data

## Requirements

- Python 3.6 or higher
- No additional packages required (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Run the program using Python:
   ```
   python library_manager.py
   ```

## Usage

When you run the program, you'll be presented with a menu with the following options:

1. **Add a book**: Enter book details including title, author, publication year, genre, and read status
2. **Remove a book**: Remove a book by its title
3. **Search for a book**: Search by title or author
4. **Display all books**: View your entire library
5. **Display statistics**: See total books and percentage read
6. **Exit**: Save and quit the program

## Data Storage

Your library data is automatically saved to `library.txt` in JSON format when you exit the program and loaded when you start it again.

## Example Usage

```
Welcome to your Personal Library Manager!
1. Add a book
2. Remove a book
3. Search for a book
4. Display all books
5. Display statistics
6. Exit

Enter your choice (1-6): 1

Enter book details:
Enter the book title: The Great Gatsby
Enter the author: F. Scott Fitzgerald
Enter the publication year: 1925
Enter the genre: Fiction
Have you read this book? (yes/no): yes

Book added successfully!
```

## Error Handling

The program includes error handling for:
- Invalid menu choices
- Invalid year inputs
- File operations (saving/loading)
- General input validation

## Contributing

Feel free to fork this repository and submit pull requests with improvements! 
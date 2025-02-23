import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# JSON File Path
BOOKS_FILE = "books.json"

# Function to load books from JSON
def load_books():
    try:
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save books to JSON
def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)

# GET all books (with optional filtering by author or genre)
@app.route('/books', methods=['GET'])
def get_books():
    books = load_books()
    
    # Get query parameters
    author = request.args.get('author')
    genre = request.args.get('genre')

    # Apply filters if parameters are provided
    if author:
        books = [book for book in books if book["author"].lower() == author.lower()]
    if genre:
        books = [book for book in books if book["genre"].lower() == genre.lower()]

    return jsonify(books)

# POST: Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    books = load_books()
    data = request.get_json()
    
    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
        "genre": data["genre"]
    }
    books.append(new_book)
    save_books(books)
    
    return jsonify(new_book), 201

# ✅ GET a specific book by ID (Move this ABOVE `if __name__ == '__main__'`)
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    
    if book:
        return jsonify(book)
    
    return jsonify({"error": "Book not found"}), 404

# PUT: Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    # Update fields only if provided in the request
    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])
    book["genre"] = data.get("genre", book["genre"])

    # Save the updated list back to JSON
    save_books(books)

    return jsonify(book)

# DELETE: Remove a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Remove the book
    books = [b for b in books if b["id"] != book_id]

    # Save the updated list back to JSON
    save_books(books)

    return jsonify({"message": "Book deleted"}), 200

# ✅ Now move this block to the **very end** of the file
if __name__ == '__main__':
    app.run(debug=True)




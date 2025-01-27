from flask import Flask, request, jsonify

app = Flask(__name__)

authors = [
    {"id": "1", "name": "J.K. Rowling", "age": 59},
    {"id": "2", "name": "J.R.R. Tolkien", "age": 81},
]

books = [
    {"id": "1", "title": "Harry Potter and the Philosopher's Stone", "author_id": "1"},
    {"id": "2", "title": "Harry Potter and the Chamber of Secrets", "author_id": "1"},
    {"id": "3", "title": "Harry Potter and the Prisoner of Azkaban", "author_id": "1"},
    {"id": "4", "title": "The Hobbit", "author_id": "2"},
    {"id": "5", "title": "The Lord of the Rings: The Fellowship of the Ring",
        "author_id": "2"},
    {"id": "6", "title": "The Lord of the Rings: The Two Towers", "author_id": "2"},
    {"id": "7", "title": "The Lord of the Rings: The Return of the King", "author_id": "2"},
]


@app.route("/authors", methods=["GET"])
def get_authors():
    return jsonify(authors), 200


@app.route("/authors/<author_id>", methods=["GET"])
def get_author(author_id):
    author = next((a for a in authors if a["id"] == author_id), None)
    if author is None:
        return jsonify({"error": "Author not found"}), 404
    return jsonify(author), 200


@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing required field 'name'"}), 400

    new_author_id = str(len(authors) + 1)
    new_author = {
        "id": new_author_id,
        "name": data["name"],
        "age": data.get("age")
    }
    authors.append(new_author)

    return jsonify(new_author), 201


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200


@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    author = next((a for a in authors if a["id"] == book["author_id"]), None)
    book_with_author = {
        **book,
        "author": author
    }
    return jsonify(book_with_author), 200


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data or "title" not in data or "author_id" not in data:
        return jsonify({"error": "Missing required fields 'title' or 'author_id'"}), 400

    matching_author = next(
        (a for a in authors if a["id"] == data["author_id"]), None)
    if not matching_author:
        return jsonify({"error": f"No Author found with id={data['author_id']}"}), 400

    new_book_id = str(len(books) + 1)
    new_book = {
        "id": new_book_id,
        "title": data["title"],
        "author_id": data["author_id"]
    }
    books.append(new_book)

    return jsonify(new_book), 201


if __name__ == "__main__":
    app.run(debug=True)

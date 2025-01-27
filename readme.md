# Understanding gql: A Beginner's Guide with Examples
In an era where data is central to decision making and a key driver for many AI breakthroughs, 
data science relies heavily on efficient and flexible methods of accessing and combining information. 
gql is a query language released in 2015 by Meta that enhances this data access, making it more efficient. 
Its client-driven approach allows users to define exactly which data should be fetched from the server in a single query.
In contrast, the traditional REST API often suffers from under-fetching or over-fetching.   
Under-fetching occurs when too little information is retrieved from a REST API endpoint, necessitating multiple requests. 
Over-fetching, on the other hand, happens when too much information is retrieved, resulting in a waste of resources.
gql addresses these issues by providing a single endpoint that is located between the client and the backend service. 
Its schema-centric design and flexible querying model enable users to fetch exactly the required data at once.

## Structure of an gql Schema
The core concept of gql is the schema, which defines the shape of the data available on the server. 
It is typically defined using Schema Definition Language (SDL). 
The schema communicates to both the server and clients what operations are possible and what the responses should look like. 
It can be regarded as the map of the gql services.    
The schema consists of various types that describe the specific shape of the data. 
There are scalar types (e.g., Int, Float, String, Boolean, ID) and object types (e.g., Author, Book). 
These custom types are defined in your schema and can be considered blueprints of a data model in gql services, 
describing the structure of the data and its relationships to other types.  
Every schema has two required types: the `query` type, which is responsible for fetching (reading) data from the API, 
and the `mutation` type, which allows modifications of resources in the forms of creating, updating, and deleting data through the API. 
Additionally, the `subscription` type is an optional type that makes it possible to notify clients about changes in the data.  
If a schema contains both the query and mutation types, CRUD (Create, Read, Update, Delete) operations are possible, similar to REST APIs. 
Furthermore, each type has fields that clients can query or mutate, allowing them to specify exactly which properties to retrieve or update.
Although this may seem abstract at first, a small example can help make it more tangible.
```gql
schema {
  query: Query
  mutation: Mutation
}

type Query {
  author(id: ID!): Author
  allBooks: [Book]
}

type Mutation {
  createAuthor(name: String!, age: Int): Author
  createBook(title: String!, authorId: ID!): Book
}

type Author {
  id: ID!
  name: String!
  age: Int
  books: [Book]
}

type Book {
  id: ID!
  title: String!
  author: Author
}
```

In this example, there are two types Author and Book. Each type has different fields: ID, name and age for the Author and ID, title, and author for the book. But let's go through the schema step by step.
´´´gql
schema {
  query: Query
  mutation: Mutation
}
´´´
In the first part, the entry point of the gql API is defined. It specifies the Query and Mutation operation for the API.
```gql
type Query {
  author(id: ID!): Author
  allBooks: [Book]
}
```
The subsequent part defines the Query type, listing fields clients can request (read) from the API.
The first field takes an ID as an argument, where `!` means that the ID is required and returns the Autors object corresponding to this idea.
The second field returns a list of Book objects.
An example query for the first field would be:
```gql
query {
  author(id: "1") {
    id
    name
    age
  }
}
```
In the next part, the mutation type is defined for data modifications, allowing for changes in existing resources.
```gql
type Mutation {
  createAuthor(name: String!, age: Int): Author
  createBook(title: String!, authorId: ID!): Book
}
```
The first field allows you to create a new Author by providing a required name and an optional age. If the creation is successful, the newly created Author object is returned.
The second field functions similarly for Books; it enables you to create a new Book by providing a required title and an author ID.
For example, a query to create an author would look like this:
```gql
mutation {
  createAuthor(name: "George Orwell", age: 46) {
    id
    name
    age
  }
}
```
In the next part of the schema, the author entity is described and requires a unique identity and a name. The age and books are optional fields. The squared brackets define a list of Book objects associated with the author.
```gql
type Author {
  id: ID!
  name: String!
  age: Int
  books: [Book]
}
```
The referenced book entity is composed of a unique identity and a title. It also includes the unique identifier of the author, who wrote the book. 
```gql
type Book {
  id: ID!
  title: String!
  authorId: ID!
}
```
In a traditional REST setup, this implementation would likely have two main resources: `/authors` for handling author resources and `/books` for managing book resources. 
To be consistent with the example above, you can access the information of an author with a specific ID using the following GET command:
```
GET http://localhost:5000/authors/1
```
You can create an new author by using the `\authors` endpoint and the POST method sending an JSON file to the application, which could look like in the following way
```gql
{
  "name": "George Orwell",
  "age": 46
}
```
But if we want to get book information now, we have to access a different endpoint. 
```
GET http://localhost:5000/books/1
```
This highlights how dependent the client is on the implementation decision for the API developer and the multiple endpoints of REST APIs.


## Implementation of a GraphAPI and REST-API
To apply the knowledge gained in the previous sections, 
I want to create two simple web applications using Flask, each providing the same services but implemented with different APIs.
This approach will help deepen the understanding of both APIs.
Both web applications are developed with Flask, a lightweight and minimalistic Python-based web framework. 
In these examples, I will specifically utilize Flask's routing feature, which offers a straightforward way to define routes. 
These routes determine how URLs map to Python functions.

### REST-Application Implementation
Let's begin with the traditional approach: implementing a REST API for fetching and updating authors and their books.

First, create a new Python virtual environment and install the required packages.
```
python3 -m venv venv
source venv/bin/activate
pip install flask
```
Afterwards, the required components of the Flask library are imported.
```python
from flask import Flask, request, jsonify
```
Flask is the main class used to create Flask web applications. 
The request object contains information about the current HTTP request and allows access to data sent by the client, 
such as query parameters or JSON payloads in POST requests. 
The jsonify function converts Python dictionaries or lists into JSON-formatted responses. 
Using these objects, we can continue to build a RESTful API in Flask. In the next step, 
the Flask app can be initialized using the appropriate line of code.
```python
app = Flask(__name__)
```
In the next part of the code, we simulate a small database with two lists of dictionaries of authors and their books. 
```python
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
```
Then the routes can be implemented, which define the endpoints of the API, which the client can access. 
The first implemented route is `/authors` which responds to GET requests. When the client requests `/authors` the `get_authors()``is executed, returning all authors as a JSON response.
```python
@app.route("/authors", methods=["GET"])
def get_authors():
    return jsonify(authors), 200
```
The route `/authors/<author_id>` is designed for a GET request to retrieve a single author by their ID. 
This demonstrates the use of a dynamic parameter in the URL; for example, `/authors/1` would request the author with ID 1.
The function `get_author(author_id)` retrieves the first author from an iterator. 
In this function, there is a generator object, which acts as an iterator. 
This generator compares all IDs in the list with the provided ID from the client.
If there is a match, the function returns all the information about the author. 
If no match is found, it returns an error notification.
```python
@app.route("/authors/<author_id>", methods=["GET"])
def get_author(author_id):
    author = next((a for a in authors if a["id"] == author_id), None)
    if author is None:
        return jsonify({"error": "Author not found"}), 404
    return jsonify(author), 200
```
After fetching newly added data from the API, we also want to add new information (author) using a POST function. 
A POST request is used to send data to the server to create new resources.  
When the route `/authors` is called using the POST method, the `create_author` function is executed. 
This function first extracts the JSON payload sent by the client from the body of the POST request. 
It then converts the JSON data into a Python dictionary and stores it in the `data` variable using the `request.get_json()` function.  
Next, the function checks if the client has sent data by verifying the existence of the name field. 
A new author ID is generated by incrementing the length of the existing authors list by one. 
Then, a new dictionary is created to represent the new author, including the computed ID, the required name, and the age if provided by the client.  
Finally, the new author dictionary is added to the end of the authors list and returned in JSON format to the client.  
```python
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
```
After successfully implementing the author routes, we can proceed to do the same for the book routes.  
First, we will implement a route with a GET method that allows us to fetch all books from the API. 
The `/books` route will function similarly to the corresponding route for authors.  
```python
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), 200
```
Additionally, we want to provide the functionality to fetch specific books from the API using the `/books/<book_id>` endpoint. 
This represents a dynamic route where the `book_id` can be passed in the URL to retrieve details about a particular book.   
Based on this ID, a generator expression is executed to find the first book with the specified ID,
and it is stored in the `book` variable. 
If no match is found, `None` is assigned. In the following step, 
the author of the book is retrieved using the `author_id` from the book, following a similar approach. 
Finally, the book and author data are merged into a single dictionary using the unpacking operator (**book). 
This combined dictionary is then returned to the client.
```python
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
```
The final route involves creating new books using the POST method. 
When the `\books` route is accessed with a `POST` request, the `create_book()` function is executed. 
This function first extracts the JSON payload from the request body.  
Next, it checks whether both the title and the author_id are provided. If either one is missing, an error message is returned to the user. 
After that, the function verifies whether the provided author_id corresponds to an existing author.  
If the author_id is valid, the ID for the new book is generated by incrementing the current length of the book list by 1. 
Finally, a new book dictionary is created and added to the list of books. If everything is executed successfully, the newly created book is returned to the client in JSON format.
```python
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
```
A widely used tool for testing APIs is Postman. 
It assists developers in testing and debugging their APIs. To run the Python application, use the following command, where `rest_app.py` is the name of your Python file.
```python
if __name__ == "__main__":
    app.run(debug=True)
```
A widely used tool for testing APIs is Postman. 
It assists developers in testing and debugging their APIs. 
To run the Python application, use the following command, where `rest_app.py` is the name of your Python file.
```python
python3 rest_app.py
```
Next, open Postman and execute the example GET request to test your API.
```
http://127.0.0.1:5000/authors/1
```
If everything worked out successfully the following response should be returned from the server.
```gql
{
    "age": 59,
    "id": "1",
    "name": "J.K. Rowling"
}
```

### gql Application Implementation
In the next section, we will implement the same application using gql instead of REST. 
This implementation requires the additional library called Graphene, 
which provides a simple, powerful, and flexible way to define gql schemas and resolve queries.
Before we can start implementing the gql API, we need to install the required packages:
```
pip install Flask graphene "graphql-server[flask]"
```
In the first part of the code, we will import the Graphene module, 
which is used for building and managing gql schemas in Python. Additionally, 
we will import the Flask class to create the Flask web application. 
We will also import the gqlView class from the gql-server package, 
which will provide an endpoint (URL) where you can send gql queries.
```python
import graphene
from flask import Flask
from graphql_server.flask import GraphQLView
```
Afterwards, the simulated database, consisting of authors and books, is set up again.
```python
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
```
Then, we can begin implementing the two required gql object types: 
AuthorType and BookType. These types represent authors and books, as well as their relationship with each other.  
The AuthorType is composed of four fields: a unique identifier, which is always required; the name of the author; the author's age; and a list of books written by the author. 
The lambda function in the books field serves as a deferred reference to BookType. It passes a callable function instead of immediately referencing BookType, 
which may not yet be defined. Graphene will execute this callable later, when it needs to know the actual type. This approach is known as lazy evaluation.
The `resolver_books()` method retrieves all books written by the author by using the author's ID to filter the list of books.
```python
class AuthorType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    age = graphene.Int()
    books = graphene.List(lambda: BookType)

    def resolve_books(self, info):
        author_id = self.get("id")
        return [book for book in books if book["author_id"] == author_id]
```
The second class, BookType, represents a book in the gql schema. It consists of the fields: id, title, and author. This class is defined similarly to the Author class.
```python
class BookType(graphene.ObjectType):
    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    author = graphene.Field(lambda: AuthorType)

    def resolve_author(self, info):
        author_id = self.get("author_id")
        return next((author for author in authors if author["id"] == author_id), None)
```
In the next step, we will define the entry point for reading data from the gql API. Like all previously defined classes, this one inherits from the `graphene.ObjectType` class, which serves as the base class in Graphene for defining a gql query type.  
The first field in this class allows clients to query a single `AuthorType` object by its ID. It specifies that an object of type `AuthorType` is returned, and the ID is required for this query.  
The second field enables clients to query a list of all `BookType` objects. It indicates that this field will return a list of all books available in the dataset.  
These two fields are followed by their associated resolver methods. A resolver function in Graphene determines how to fetch or compute values for a specific field. Each resolver method starts with `resolve_`, followed by the name of the field it corresponds to.  
The `resolve_author(self, info, id)` method resolves the author field by locating the author with the given ID in the authors dataset. The `resolve_books(self, info)` method is even simpler, as it simply returns the previously defined list of books.
```python
class Query(graphene.ObjectType):
    author = graphene.Field(AuthorType, id=graphene.ID(required=True))
    all_books = graphene.List(BookType)

    def resolve_author(self, info, id):
        return next((author for author in authors if author["id"] == id), None)

    def resolve_all_books(self, info):
        return books
```
In the next step, we will define the gql mutations for adding new authors and books to the dataset. Mutations are used in gql for modifying and creating data, unlike queries, which are read-only.  
First, we need to define a mutation class that inherits from the Graphene mutation class. The inner `Argument` call specifies the arguments that the client must provide to the mutation, in this case, the name of the author and an optional age argument.  
The following line indicates what the mutation will return. In this case, it will return the newly created `AuthorType`.  
The `mutate()` method contains the logic for the mutation. It is called when the `create_author` mutation is invoked. Inside this method, the ID is computed, and a dictionary containing the relevant author information is created. Finally, the new author is appended to the global authors list, and an instance of `CreateAuthor` is returned, with the author field set to the newly created author.
```python
class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int()

    author = graphene.Field(lambda: AuthorType)

    def mutate(self, info, name, age=None):
        new_author_id = str(len(authors) + 1)
        new_author = {
            "id": new_author_id,
            "name": name,
            "age": age,
        }
        authors.append(new_author)
        return CreateAuthor(author=new_author)
```
Afterward, we create a similar mutation class for creating new books. The main difference lies in the `mutate` function, which uses a generator to find the author with the specified `author_id`. The remaining steps for creating a book are the same as those for creating a new author.
```python
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    book = graphene.Field(lambda: BookType)

    def mutate(self, info, title, author_id):
        matching_author = next(
            (author for author in authors if author["id"] == author_id), None)
        if not matching_author:
            raise Exception(f"No Author found with id={author_id}")

        new_book_id = str(len(books) + 1)
        new_book = {
            "id": new_book_id,
            "title": title,
            "author_id": author_id,
        }
        books.append(new_book)
        return CreateBook(book=new_book)
```
In the end, we define the class `Mutation`, which serves as the root mutation type for the gql schema. It groups all mutation classes into a single entry point for the gql schema.
```python
class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()
```
We are now prepared to define the gql schema by combining the `Query` and `Mutation` classes.
```python
schema = graphene.Schema(query=Query, mutation=Mutation)
```
In the final step, we set up a simple Flask application to create a gql API endpoint, which allows the client to send gql queries and mutations.    
The method `app.add_url_rule()` adds a URL route to the Flask application for handling requests to the gql endpoint. In this case, the API is accessible at `/gql`. Additionally, a view function is registered to handle requests to the `/gql` endpoint. The `gqlView` is a helper class provided by `gql_server` for integrating a gql schema with Flask.
```python
app = Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True
    ),
)

if __name__ == "__main__":
    app.run(debug=True)
```
You can run the application using the following command, where `gql_app.py` is the name of your file:
```bash
python3 gql_app.py
```
Next, open your web browser and navigate to the following URL:
```
http://127.0.0.1:5000/gql
```
Here, you can test the application by querying and mutating the API. For example, to retrieve all book titles from the API, use the following query:

```gql
{
  allBooks {
    id
    title
  }
}
```
If the application workes properly the following response should be returned:
```gql
{
  "data": {
    "allBooks": [
      {
        "id": "1",
        "title": "Harry Potter and the Philosopher's Stone"
      },
      {
        "id": "2",
        "title": "Harry Potter and the Chamber of Secrets"
      },
      {
        "id": "3",
        "title": "Harry Potter and the Prisoner of Azkaban"
      },
      {
        "id": "4",
        "title": "The Hobbit"
      },
      {
        "id": "5",
        "title": "The Lord of the Rings: The Fellowship of the Ring"
      },
      {
        "id": "6",
        "title": "The Lord of the Rings: The Two Towers"
      },
      {
        "id": "7",
        "title": "The Lord of the Rings: The Return of the King"
      }
    ]
  }
}
```
Additionally, you can add new authors with this mutation:
```gql
mutation {
  createAuthor(name: "William Shakespeare", age: 52) {
    author {
      id
      name
      age
    }
  }
}
```
If the author was successfully added via the API, the corresponding metadata will be returned.
```gql
{
  "data": {
    "createAuthor": {
      "author": {
        "id": "3",
        "name": "William Shakespeare",
        "age": 52
      }
    }
  }
}
```

## Comparison between REST and gql
Now that we have two simple applications for both API types. Let's make a comparison between the two APIs.

- **Data Fetching:** REST has multiple endpoints for different resources (e.g., /authors, /books). In contrast, gql uses a single endpoint (/gql) for all data fetching and mutations.
- **Flexibility:** REST has a fixed response structure defined by the API developers. gql follows a client-driven approach, allowing for queries that result in highly customizable responses.
- **Underfetching/Overfetching:** REST commonly faces issues with underfetching and overfetching due to its fixed endpoints. gql addresses this by allowing clients to specify exactly which data fields they need.
- **Versioning:** There is a significant difference in how the two API types handle versioning. REST requires new versions, such as `v1` or `v2`, for breaking changes. On the other hand, gql schemas can evolve without breaking compatibility.
- **Real-Time Updates:** Both REST and gql can retrieve real-time updates. However, REST often requires additional tools, like WebSockets, while gql has built-in subscriptions to manage real-time updates efficiently.
- **Performance:** REST necessitates multiple queries to request nested data. For example, if a client wants to fetch both authors and their books, they first need to fetch the authors (GET /authors) and then their books in a loop (GET /authors/{id}/books). This can lead to a large number of queries as the data grows. gql resolves this problem by allowing nested queries to fetch all the required data in one request, eliminating the need for multiple follow-up queries.
- **Use Cases:** REST is more suitable for simple applications with static requirements. Conversely, gql is better suited for complex, data-rich applications that require a higher level of flexibility and efficiency.

I hope this comparison and the simple implementation of both APIs make the differences clearer, highlight the advantages and disadvantages of both APIs and help you find the right solution for your personal project.

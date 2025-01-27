import graphene
from flask import Flask
from graphql_server.flask import GraphQLView


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


class AuthorType(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    age = graphene.Int()
    books = graphene.List(lambda: BookType)

    def resolve_books(self, info):
        author_id = self.get("id")
        return [book for book in books if book["author_id"] == author_id]


class BookType(graphene.ObjectType):
    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    author = graphene.Field(lambda: AuthorType)

    def resolve_author(self, info):
        author_id = self.get("author_id")
        return next((author for author in authors if author["id"] == author_id), None)


class Query(graphene.ObjectType):
    author = graphene.Field(AuthorType, id=graphene.ID(required=True))
    all_books = graphene.List(BookType)

    def resolve_author(self, info, id):
        return next((author for author in authors if author["id"] == id), None)

    def resolve_all_books(self, info):
        return books


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


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

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

import graphene
from graphene_django.types import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        field = ('id', 'title', 'author', 'descirption', 'publishedYear')

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.Int())

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_all_books(self, info):
        return Book.objects.all()

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        description = graphene.String(required=True)
        publishedYear = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, description, publishedYear):
        book = Book(
            title=title,
            author=author, 
            description=description,
            publishedYear=publishedYear
        )
        book.save()
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)  # Ensure this is defined
        title = graphene.String()
        author = graphene.String()
        description = graphene.String()  # Ensure this is defined
        publishedYear = graphene.Int()  # Ensure this is defined

    book = graphene.Field(BookType)

    def mutate(self, info, id, title=None, author=None, description=None, publishedYear=None):
        book = Book.objects.get(pk=id)
        if title:
            book.title = title
        if author:
            book.author = author
        if description is not None:
            book.description = description
        if publishedYear is not None:
            book.publishedYear = publishedYear
        book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBook(success=True)
        except Book.DoesNotExist:
            return DeleteBook(success=False)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
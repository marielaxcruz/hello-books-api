from app import db

from app.models.book import Book

# flask is the library -- methods/classes in flask
# flask is a class with helper methods 
from flask import request, Blueprint, Response, jsonify, make_response

books_bp = Blueprint("books", __name__, url_prefix="/books")

# you can look at the route path and what they will expect from the user 
# the decorator will determine which funtion will be called 
# for example when i go to this endpoint -- call this function
@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        # this code replaces the previous query all code and introduces the query parameter of filtering the results when a title query param is supplied 
        title_query = request.args.get("title")
        if title_query:
            # title = is specific to us bc this is an attribute we have already stated
            books = Book.query.filter_by(title=title_query)
        else:        
            books = Book.query.all()
        
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)
    elif request.method == "POST":
    # this will create a new insert request into our database 
        request_body = request.get_json()
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])
# # stagging the new book so it can be added to the new database 
# # you can stage several things
        db.session.add(new_book)
# commit is what actually executes the action         
        db.session.commit()
# # we can have differnet response structures here like dictionary 
        return make_response(f"Book {new_book.title} successfully created", 201)

# # the get command won't do something unless we make it aka with our python code since 
# # flask does not do that for us 
# #  when an web api gets a get request it will just get the data and give it back  
@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
# try to find the book with the given id in the path 
    book = Book.query.get(book_id)
    

    # if the book id for not exist this will execute 
    # we can apply this to all of our routes 
    # we could make this a helper function where it does its own thing 
    if book == None:
        return make_response("",404)

# method is static variable and request is a class 
    if request.method == "GET":
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }
    elif request.method == "PUT":
        # what is going on here ?????
        # converting postman json to a dict table
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()
# we know the default code is 200 
# documentation for make_response includes the default parameter is 200
        return make_response(f"Book #{book.id} successfully updated")
    
    elif request.method == "DELETE":
# DELETE requests do not generally include a request body, so 
#         # no additional planning around the request body is needed        
        db.session.delete(book)
        db.session.commit()
        # book_id will not go out of scope aka expire until the the function ends
        return make_response(f"Book #{book.id} successfully deleted")



# # a return message helps avoid any crashes bc it will give back a mssg        
#     # return {
#     #     "message" : (f"Book with id {book_id} was not found"),
#     #     "success": Flase,
#     # },404    

from app import db

# class is book and we are inheriting the class model from the module db 
# we are expecting this class book to line up with a table in our database 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

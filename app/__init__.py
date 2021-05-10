from flask import Flask

# SQLAlchemy is the the glue for our database and flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# library that communicates with our env. 
from dotenv import load_dotenv

# allows us to get the envir variables 
import os


db = SQLAlchemy()
migrate = Migrate()


# summary of create_app: if test_config flag is none or false it will connect to our development database 
# if it comes in as a true it will be a part of our test database so we can start creating tests to check  routes and how to store this test info for these tests 

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # if the flag is true then we want our code to be tested 
    if not test_config:
        # our program knows which database to call based on this path where I specify it at the end of the line here 
        # and now our connection string is here and hidden so no one has access to our database 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # new database created here for test
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    
    
    
    # Import models here
    from app.models.book import Book

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app

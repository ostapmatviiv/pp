from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

engine = create_engine("sqlite:///database.db")
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
session = Session()

from papa import urls
from papa import models
from papa import urlprovisor
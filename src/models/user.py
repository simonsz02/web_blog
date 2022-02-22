import uuid
from datetime import datetime

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        print("user is not found!")
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # User doesn't exists, so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()

            # Add user's email to the session
            session['email'] = email
            return True
        else:
            # User exists
            return False

    @staticmethod
    def login(user_email):
        # login-valid has already been called
        # Therefore, we know that the user has a valid email and password
        # we simply store their email in the session
        # Next time the user accesses that profile, for example, they will send us a unique identifier
        # in their cookie. This cookie will be able to identify this session
        # and this session will store their email because the session has the email stored.
        # We know this is a logged in user.
        # If the session does not have an email, it means the user has not yet logged in
        # because we're only storing the user email in the session when they log in.
        session['email'] = user_email

    @staticmethod
    def logout():
        # session only happens when they register or when they log in.
        # If we want them to log out.
        # The only thing we have to do is session email equals None
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # because the user has already logged-in, we know the author name
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.utcnow()):
        # title, content, date=datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
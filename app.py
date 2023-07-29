from flask import Flask
app=Flask(__name__)
from users import user

app.register_blueprint(user) 
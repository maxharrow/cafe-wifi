from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import sqlalchemy.exc
import random

#initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = '7471y2HGYTIbvcff(^bhbh%$67901255dfdfV'

# Config Flask-Login
login_manager = LoginManager()
# login_manager.init_app(app)


# Create DB
class Base(DeclarativeBase):
    pass

# connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# cafe table config
class Cafe(db.Model):
    __tablename__ = "cafe"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(250),unique=True,nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250),nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean,nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(20),nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(10),nullable=False)

    def to_dict(self):
        dictionary={}
        for column in self.__table__.columns:
            dictionary[column.name]=getattr(self,column.name)
        return dictionary


class User(UserMixin,db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    email: Mapped[int] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(250))



with app.app_context():
    db.create_all()


@app.route('/')
def origin():
    return render_template('origin.html')

@app.route('/login')
def login():
    return 'login'

@app.route('/register')
def register():
    return 'register'

@app.route('/home')
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.id))
    cafes = result.scalars().all()
    # for key,value in cafes[0].to_dict().items():
    #     print(value)
    # print(cafes[0].name)
    return render_template('index.html',all_cafes = cafes)


if __name__ == "__main__":
    app.run(debug=True)
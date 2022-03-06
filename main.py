from flask import Flask, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
#connect to databse
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

#cafe table configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dictionary(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self,column.name)
        return dictionary
class AddForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map = StringField('Map URL', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    toilet = BooleanField('Toilet')
    wifi = BooleanField('WiFi')
    sockets = BooleanField('Sockets')
    calls= BooleanField('Calls')
    price = StringField('Coffee price', validators=[DataRequired()])
    submit = SubmitField('Add')


cafes = db.session.query(Cafe).all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/view-all', )
def view_all_cafes():
    return render_template('all-cafes.html', all_cafes=cafes)

@app.route('/cafe-details/<int:cafe_id>', methods= ["GET", 'POST'])
def cafe_details(cafe_id):
    requested_cafe= Cafe.query.get(cafe_id)

    return render_template('details.html', cafe=requested_cafe)

@app.route('/add-cafe',  methods=['GET', 'POST'])
def  add_new_cafe():
    form = AddForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map.data,
            img_url = form.image.data,
            location = form.location.data,
            seats = form.seats.data,
            has_toilet = form.toilet.data,
            has_wifi = form.wifi.data,
            has_sockets = form.sockets.data,
            can_take_calls = form.calls.data,
            coffee_price = form.price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        updated = db.session.query(Cafe).all()
        return render_template('all-cafes.html', all_cafes=updated)

    return render_template('add-cafee.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

from flask import ( Flask,url_for,render_template,redirect,request,flash, get_flashed_messages)
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import forms
from forms import ReviewForm
app = Flask(__name__)
app.secret_key = 'development key'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///review.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Declare a model for customer reviews
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    product_name = db.Column(db.String(32))
    review = db.Column(db.String(32))

    def __init__(self, username, product_name, review):
        self.username = username
        self.product_name = product_name
        self.review=review

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'product_name', 'review')

user_schema = UserSchema()
users_schema = UserSchema(many=True)



'''@app.route('/', methods=['GET', 'POST'])
def cus_review():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_review = Review(form.username.data,form.product.data,form.review.data)
        db.session.add(new_review)
        db.session.commit()
        return 'We confirm your registration!'
    return render_template('index.html', form=form)'''


@app.route('/')
@app.route('/index')
def index():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.ReviewForm()
    if form.validate_on_submit():
        new_review = Review(form.username.data, form.product.data, form.review.data)
        db.session.add(new_review)
        db.session.commit()
        flash( 'Review added to the database!')
        return redirect(url_for('index'))

    return render_template('add.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    print("search entered")
    form = forms.SearchForm()
    print("line1")
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("product is "+form.product_name.data)
        reviews=Review.query.filter_by(product_name=form.product_name.data).all()
        print(reviews)
        return render_template('search.html', reviews=reviews)

    return render_template('productsearch.html', form=form)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    review = Review.query.get(task_id)
    form = forms.DeleteTaskForm()

    if review:
        if form.validate_on_submit():
            db.session.delete(review)
            db.session.commit()
            flash('Task has been deleted!')
            return redirect(url_for('index'))

        return render_template('delete.html', form=form, task_id=task_id, title=task.title)
    return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug = True)


from . import app, db, bcrypt
import secrets
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, PasswordChangeForm, RegistrationForm, UpdateAccountForm
from .models import User, ContactInformation
from main_utils import generate_id


#################################
#                               #
#           Site Stuff          #
#                               #
#################################

# this is only to be used on the production server for forcing the site to use https over http
# reference: https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
@app.before_request
def before_request():
    if not request.is_secure and app.config['HTTPS']:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'errors/404.html',
        title='404 error'
    )

# @app.errorhandler(500)
# def server_error(e):
#     return render_template(
#         'errors/500.html',
#         title='500 error'
#     )

@app.route('/')
def index():
    return render_template(
        'system/index.html',
        title='Home'
    )

# when '/home' or '/index' are typed in the URL or redirected, it will the redirect to the url without anything after the /
@app.route("/index")
@app.route("/home")
def home_redirect():
    return redirect(url_for('index'))


#################################
#                               #
#           User Stuff          #
#                               #
#################################

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == "POST":
        user = User(
            id = generate_id(User, 32),
            username = form.username.data,
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            email = form.email.data,
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )

        db.session.add(user)
        db.session.commit()
        flash('Account Created - You can now Login in')
        return redirect(url_for('login'))
    return render_template(
        'user/register.html',
        title='Register',
        form=form
    )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":
        # This allows the user to login with either their username or email
        user = ''
        if User.query.filter_by(username = form.username_email.data).first():
            user = User.query.filter_by(username = form.username_email.data).first()
        elif User.query.filter_by(email = form.username_email.data).first():
            user = User.query.filter_by(email = form.username_email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
        else:
            flash('Login Unsuccessful. Check username/email and Password')

    return render_template(
        'user/login.html',
        title = 'Login',
        form = form
    )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(request.referrer)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit() and request.method == "POST":

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        # current_user.email = form.email.data
        
        db.session.commit()
        flash('Your account was updated')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        # form.email.data = current_user.email

    return render_template(
        'user/account.html',
        title='Account',
        form=form
    )

@app.route("/password-reset", methods=['GET', 'POST'])
@login_required
def password_change():
    form = PasswordChangeForm()

    if form.validate_on_submit() and request.method == "POST":
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')

            current_user.password = hashed_password

            db.session.commit()

            flash('Your Password has been updated')
            return redirect(url_for('account'))
        else:
            flash("Couldn\'t change password")

    return render_template(
        'user/change_password.html',
        title='Reset Password',
        form=form
    )


#################################
#                               #
#          System Stuff         #
#                               #
#################################

@app.route("/about", methods=['GET'])
def about():
    return render_template(
        'system/about.html',
        title='about'
    )


@app.route("/contact", methods=['GET']) #, 'POST'])
def contact():
    return render_template(
        'system/contact.html',
        title='contact',
        # form=form
    )

#     form = ContactForm()
#     if form.validate_on_submit() and request.method == "POST":
#         contact_information = ContactInformation(
#             id = generate_id(ContactInformation),
#             title = form.title.data,
#             firstname = form.firstname.data,
#             lastname = form.lastname.data,
#             email = form.email.data,
#             phone_number = form.phone_number.data if form.phone_number.data else none,
#             description = form.description.data
#         )

#         db.session.add(contact_information)
#         db.session.commit()
#         flash('Contact information sent')
#         return redirect(url_for('contact'))
#     return render_template(
#         'system/contact.html',
#         title='contact',
#         form=form
#     )



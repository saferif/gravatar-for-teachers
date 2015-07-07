from handlers.web.base import BaseRequestHandler
from models import User
from utils import md5, csrf_protect


class SignUpHandler(BaseRequestHandler):
    def get(self):
        if self.user is not None:
            self.redirect_to('dashboard')
        else:
            self.render('signup.html')

    @csrf_protect
    def post(self):
        if self.user is not None:
            self.redirect_to('dashboard')

        first_name, last_name, email, password, password2 = \
            self.request.get('first_name').strip(), \
            self.request.get('last_name').strip(), \
            self.request.get('email').strip().lower(), \
            self.request.get('password'), \
            self.request.get('password2')

        error = None
        if not first_name:
            error = 'First name is not specified'
        elif not last_name:
            error = 'Last name is not specified'
        elif not email:
            error = 'E-mail is not specified'
        elif not password:
            error = 'Password is not specified'
        elif password != password2:
            error = 'Passwords do not match'
        else:
            user = User.get_by_id(email)
            if user:
                error = 'User with specified email already exists'
            else:
                user = User.create(email, first_name=first_name, last_name=last_name, password_hash=md5(password))
                user.put()
                self.session['user'] = user.key.urlsafe()

        if error:
            self.render('signup.html', error=error)
        else:
            self.redirect_to('dashboard')

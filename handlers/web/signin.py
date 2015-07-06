from handlers.web.base import BaseRequestHandler
from models import User
from utils import md5, csrf_protect


class SignInHandler(BaseRequestHandler):
    def get(self):
        if self.user is not None:
            self.redirect_to('dashboard')
        else:
            self.render('signin.html')

    @csrf_protect
    def post(self):
        if self.user is not None:
            self.redirect_to('dashboard')

        email, password = self.request.get('email').strip().lower(), self.request.get('password')

        error = None
        user = User.get_by_id(email)
        if not user:
            error = 'Invalid email/password'
        else:
            if user.password_hash != md5(password):
                error = 'Invalid email/password'
            else:
                self.session['user'] = user.key.urlsafe()

        if error:
            self.render('signin.html', error=error)
        else:
            self.redirect_to('dashboard')

import hashlib
from functools import wraps
import random
import string


def user_required(handler):
    @wraps(handler)
    def check_user(self, *args, **kwargs):
        if self.user is None:
            self.redirect_to('signin')
        else:
            return handler(self, *args, **kwargs)
    return check_user

def md5(string):
    return hashlib.md5(string).hexdigest()

def get_random_string(size=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in xrange(size))

def csrf_protect(handler):
    @wraps(handler)
    def check_csrf_token(self, *args, **kwargs):
        token = self.request.get('_csrf_token')
        s_token = self.session.get('_csrf_token')
        if (not token) or (token != s_token):
            self.session['_csrf_token'] = s_token
            self.abort(403)
        else:
            del self.session['_csrf_token']
        return handler(self, *args, **kwargs)
    return check_csrf_token

def generate_csrf_token(session):
    if not session.get('_csrf_token'):
        session['_csrf_token'] = get_random_string()
    return session['_csrf_token']

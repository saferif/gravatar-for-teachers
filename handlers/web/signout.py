from handlers.web.base import BaseRequestHandler
from utils import csrf_protect


class SignOutHandler(BaseRequestHandler):
    @csrf_protect
    def get(self):
        del self.session['user']
        self.redirect_to('main')

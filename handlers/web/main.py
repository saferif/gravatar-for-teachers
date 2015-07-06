from handlers.web.base import BaseRequestHandler


class MainPageHandler(BaseRequestHandler):
    def get(self):
        self.render('main.html')
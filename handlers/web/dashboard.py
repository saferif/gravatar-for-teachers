from google.appengine.ext import blobstore
from webapp2 import uri_for
from handlers.web.base import BaseRequestHandler
from utils import user_required


class DashboardHandler(BaseRequestHandler):
    @user_required
    def get(self):
        upload_url = blobstore.create_upload_url(uri_for('upload_avatar'))
        self.render('dashboard.html', upload_url=upload_url, error=self.request.get('error'))

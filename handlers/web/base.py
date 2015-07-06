from webapp2 import RequestHandler, cached_property
from webapp2_extras import sessions, jinja2
from google.appengine.ext import ndb
from google.appengine.ext.webapp.blobstore_handlers import BlobstoreUploadHandler
from utils import generate_csrf_token


def _get_base_handler(base_class):
    class BaseHandler(base_class):
        @cached_property
        def session_store(self):
            return sessions.get_store(request=self.request)

        @cached_property
        def session(self):
            return self.session_store.get_session()

        def dispatch(self):
            try:
                super(BaseHandler, self).dispatch()
            finally:
                self.session_store.save_sessions(self.response)

        @cached_property
        def user(self):
            user_key = self.session.get('user', None)
            if user_key is None:
                return None
            return ndb.Key(urlsafe=user_key).get()

        @cached_property
        def jinja2(self):
            return jinja2.get_jinja2(app=self.app)

        def render(self, template_name, **template_values):
            template_values.update({
                'url': self.request.path_qs,
                'current_user': self.user,
                '_csrf_token': generate_csrf_token(self.session),
            })
            rendered = self.jinja2.render_template(template_name, **template_values)
            self.response.write(rendered)
    return BaseHandler

BaseRequestHandler = _get_base_handler(RequestHandler)
BaseBlobstoreUploadHandler = _get_base_handler(BlobstoreUploadHandler)

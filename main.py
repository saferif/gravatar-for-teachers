from handlers import web, api
import secrets
from webapp2 import uri_for, Route, WSGIApplication
from webapp2_extras import jinja2
from utils import md5

config = {
    'webapp2_extras.sessions': {
        'secret_key': secrets.SESSION_KEY
    }
}


application = WSGIApplication([
    Route('/', web.MainPageHandler, 'main'),

    Route('/signup', web.SignUpHandler, 'signup'),
    Route('/signin', web.SignInHandler, 'signin'),
    Route('/signout', web.SignOutHandler, 'signout'),

    Route('/dashboard', web.DashboardHandler, 'dashboard'),
    Route('/upload_avatar', web.UploadAvatarHandler, 'upload_avatar'),

    #Route(r'/a/([^/]+)?', api.AvatarDownloadHandler, 'avatar')
    Route(r'/a/<email_hash>', api.AvatarDownloadHandler, 'avatar')
], debug=True, config=config)

jinja2.set_jinja2(jinja2.Jinja2(application, {
    'globals': {'uri_for': uri_for, 'md5': md5, 'site_name': 'My Gravatar'}
}), app=application)

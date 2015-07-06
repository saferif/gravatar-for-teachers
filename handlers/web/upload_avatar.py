from handlers.web.base import BaseBlobstoreUploadHandler
from models import Avatar
from utils import csrf_protect, user_required, md5


class UploadAvatarHandler(BaseBlobstoreUploadHandler):
    @csrf_protect
    @user_required
    def post(self):
        error = None
        try:
            upload = self.get_uploads()[0]
            email_hash = md5(self.user.email)
            avatar = Avatar.get_by_id(email_hash)
            if not avatar:
                avatar = Avatar.create(email_hash, avatar=upload.key())
            else:
                avatar.avatar = upload.key()
            avatar.put()
        except:
            error = 'Error occurred during file upload'
        finally:
            self.redirect_to('dashboard', **({'error': error} if error else {}))
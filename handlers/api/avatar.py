from google.appengine.ext import blobstore
from google.appengine.ext.webapp.blobstore_handlers import BlobstoreDownloadHandler
from models import Avatar


class AvatarDownloadHandler(BlobstoreDownloadHandler):
    def get(self, email_hash):
        avatar = Avatar.get_by_id(email_hash)
        if (not avatar) or (not blobstore.get(avatar.avatar)):
            self.abort(404)
        else:
            self.send_blob(avatar.avatar)

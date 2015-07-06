from google.appengine.ext import ndb


class User(ndb.Model):
    password_hash = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)

    @property
    def email(self):
        return self.key.id()

    @classmethod
    def create(cls, email, **kwargs):
        return cls(id=email, **kwargs)


class Avatar(ndb.Model):
    avatar = ndb.BlobKeyProperty(indexed=False)

    @property
    def email_hash(self):
        return self.key.id()

    @classmethod
    def create(cls, email_hash, **kwargs):
        return cls(id=email_hash, **kwargs)

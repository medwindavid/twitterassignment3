from google.appengine.ext import ndb
from posts import Posts

class MyUser(ndb.Model):
    email_address = ndb.StringProperty()
    user_id = ndb.StringProperty()
    user_name = ndb.StringProperty()
    about_me = ndb.StringProperty()

    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    dob = ndb.DateProperty()

    posts_ids = ndb.IntegerProperty(repeated=True)
    user_following = ndb.StringProperty(repeated=True)

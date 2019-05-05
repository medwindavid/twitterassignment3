

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

import  datetime

from methods import Methods
from posts import Posts

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):

    def post(self):

        blobinfo = None
        if len(self.get_uploads()) > 0:
            upload_file = self.get_uploads()[0]
            blobinfo = blobstore.BlobInfo(upload_file.key())

        share_text = self.request.get("share_text")
        share_type = self.request.get("share_type")

        if share_type == "Update":

            edit_posts_id = self.request.get("edit_posts_id")
            edit_posts = Methods().get_posts(posts_id=edit_posts_id)
            edit_posts.share_text = share_text
            edit_posts.time = datetime.datetime.now()
            if blobinfo != None:
                edit_posts.avatar = upload_file.key()
            edit_posts.put()

        else:

            myuser = Methods().get_login_user()
            posts = Posts(share_text=share_text,
                          user_id=myuser.key.id(),
                          user_name=myuser.user_name,
                          time=datetime.datetime.now())

            if blobinfo != None:
                posts.avatar = upload_file.key()
            posts.put()

            myuser.posts_ids.append(posts.key.id())
            myuser.put()

        self.redirect("/")

from google.appengine.api import users
from google.appengine.ext import ndb

from posts import Posts
from myuser import MyUser

class Methods(object):

    def create_user(self,user_id):

        myuser = MyUser(id=user_id, user_id=str(user_id))
        myuser.user_name = ""
        myuser.user_following = []
        myuser.put()
        return myuser

    def get_current_user(self):
        return users.get_current_user()


    def get_current_user_id(self):
        return users.get_current_user().user_id()


    def get_login_user(self):
        myuser_key = ndb.Key("MyUser", Methods().get_current_user_id())
        return  myuser_key.get()

    def search_by_posts(self, text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return Posts.query(Posts.share_text >= text, Posts.share_text < limit)

    def search_by_user(self,text):
        limit = text[:-1] + chr(ord(text[-1]) + 1)
        return Posts.query(Posts.user_name >= text, Posts.user_name < limit)

    def delete_posts(self, posts_id):

        myuser = Methods().get_login_user()
        posts_ids = myuser.posts_ids
        posts_ids.remove(int(posts_id))
        myuser.posts_ids = posts_ids
        myuser.put()

        posts_key = ndb.Key("Posts", int(posts_id))
        posts = posts_key.get()
        posts.key.delete()


    def get_posts(self, posts_id):

        posts_key = ndb.Key("Posts", int(posts_id))
        posts = posts_key.get()
        return posts

    def get_all_user_postss(self):

        myuser = Methods().get_login_user()
        postss = []
        for posts in Posts.query().order(-Posts.time).fetch():
            if posts.user_id in myuser.user_following or posts.user_id == myuser.key.id():
                postss.append(posts)
        return postss



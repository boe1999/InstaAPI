from flask import Flask,request
import instaloader

app = Flask(__name__)

followersSet = set()
followeesSet = set()
unfollowersSet = set()
whiteList = set()

class Insta_info:

    def __init__(self, username):

        self.username = username
        self.loader = instaloader.Instaloader()
        self.profile = instaloader.Profile.from_username(self.loader.context,self.username)


    def Login(self, username, password):

        login = self.loader.login(username, password)
        return login

    def get_my_followers(self):

        for followers in self.profile.get_followers():
            followersSet.add(followers.username)

    def get_my_followees(self):

        for followees in self.profile.get_followees():
            followeesSet.add(followees.username)

    def get_my_unfollowers(self):
        followers = set(followersSet)
        followees = set(followeesSet)
        return str(followees.difference(followers))

@app.route('/')
def main():
    username = request.args.get('user')
    password = request.args.get('passw')
    insta_info = Insta_info(username)
    try:
        try:
            insta_info.loader.load_session_from_file(username,"session")
        except:
            insta_info.Login(username, password)
            insta_info.loader.save_session_to_file("session")
        insta_info.get_my_followers()
        insta_info.get_my_followees()
        return (insta_info.get_my_unfollowers())
    except Exception as err:
        return (err)


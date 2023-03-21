from flask import Flask,request
import instaloader

app = Flask(__name__)

#use Set to not permit to use ripetitive data
followersSet = set()
followeesSet = set()

class Insta_info:

    #initialize class instaloader with username, loader and profile
    def __init__(self, username):

        self.username = username
        self.loader = instaloader.Instaloader()
        

    #define the function login to Log in with username and password
    def Login(self, username, password):

        login = self.loader.login(username, password)
        return login
    
    #define the function to update Set of followers
    def get_my_followers(self):
        self.profile = instaloader.Profile.from_username(self.loader.context,self.username)
        for followers in self.profile.get_followers():
            followersSet.add(followers.username)

    #define the function to upadate Set of followees
    def get_my_followees(self):
        self.profile = instaloader.Profile.from_username(self.loader.context,self.username)
        for followees in self.profile.get_followees():
            followeesSet.add(followees.username)

    #define the function that return Set of unFollowers
    def get_my_unfollowers(self):
        followers = set(followersSet)
        followees = set(followeesSet)
        return list(followees.difference(followers))

@app.route('/')
def main():
    #retrieve username and password from url (GET)
    username = request.args.get('user')
    password = request.args.get('passw')
    #try to login and call functions otherwise call exception
    try:
        #initialize class insta_info
        insta_info = Insta_info(username)
        insta_info.Login(username, password)
        insta_info.get_my_followers()
        insta_info.get_my_followees()
        return (insta_info.get_my_unfollowers())
    except Exception as err:
        return str(err)

if __name__ == "__main__":
    # Development only: run "python main.py" and open http://localhost:8080
    # When deploying to Cloud Run, a production-grade WSGI HTTP server,
    # such as Gunicorn, will serve the app.
    app.run(host="localhost", port=8080, debug=True)


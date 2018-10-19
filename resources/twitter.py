from flask import Flask, jsonify, Blueprint, request
from flask_restful import Resource, Api, reqparse, abort, inputs
from datetime import datetime                                       #fungsi untuk meambah date time
import json  #untuk memindahkan format json ke file

# user =[{
#     "username": "John",
#     "email": "john@haha.com",
#     "password": "Hahaha123",
#     "fullname": "John rukmana"
# },
# {
#    "username": "jeff",
#     "email": "jeff@haha.com",
#     "password": "Hahaha123",
#     "fullname": "Jeff rukmana" 
# }] 

# tweets = [{
#     "email": "john@haha.com",
#     "tweet": "Ini ceritanya tweet Twitter yah"
# },
# {
#     "email": "jeff@haha.com",
#     "tweet": "Ini ceritanya tweet Twitter yah"
# }]

#############################################
#langkah 1
#dibuat update data ke file

# with open('user.json', 'w') as outfile:
#     json.dump(user, outfile)

# with open('tweets.json', 'w') as outfile:
#     json.dump(tweets, outfile)    

# jalankan
# jika sudah maka di ganti kata dump dengan load

################################################
#langkah 2
#memanggil data dari file yang sudah si simpan

user = []
tweets = []
with open('user.json') as outfile:
    user = json.load(outfile)
    outfile.close()

with open('tweets.json') as outfile:
    tweets = json.load(outfile)
    outfile.close()

################################################
#langkah 3
#berfungsi untuk mengupdate file jika ada perubahan

def updateDataUser(user):
    with open('user.json','w') as file:
        file.write(json.dumps(user))
        file.close()

def updateDataTweets(tweets):
    with open('tweets.json', 'w') as file:
        file.write(json.dumps(tweets))
        file.close()

#################################################
class readAllUserTwitter(Resource):
    def get(self):
        return user

class readAllTwit(Resource):
    def get(self):
        return tweets

def userNameEmailAlreadyExist(username, email):
    exist = ""
    for data in user:
        if data["username"] == username or data["email"] == email:
            if data['username'] == username:
                exist += "username, "
            if data['email'] == email:
                exist += "email, "
            exist += "already exist"
            abort (400, message= exist )


class signUpTwitter(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "Entry email",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "username",
            help = "Entry username",
            required = True,
            location = ["json"]
        )
        
    def post(self):
        req = request.json
        self.reqparse.parse_args()
        userNameEmailAlreadyExist(req["username"],req["email"])
        user.append(req)
        updateDataUser(user)
        
        return {'Message' :'Sign up sucess'}, 201
         
class loginTwitter(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "Entry email",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "password",
            help = "Entry password",
            required = True,
            location = ["json"]
        )
    def post(self):
        self.reqparse.parse_args()
        req = request.json
        index = 0
        for data in user:
            if data['email'] == req['email'] and data['password'] == req['password']:
                return user[index], 200
            index += 1

        return abort (400, message = 'Email, Password incorrect')
        
        
def emailChecking(email):
    for data in user:
        if data ["email"] == email:
            return email

    abort(400, message="please sign up")

def checkingEmailInTweet(req):
    for data in tweets:
        if data['email'] == req['email']:
            data['tweet'].append(req['tweet'])
            data['date'].append(req['date'])

            return

    req['tweet'] = [req['tweet']]
    req['date'] = [req['date']]
    tweets.append(req)
    return


def emailCheckingAndTweets(email,tweet):
    indexEmail = 0
    for data in tweets:
        if data['email'] == email and data['tweet'] == tweet:
            return indexEmail
        indexEmail += 1

    abort (400, message="cannot delete")
        

class twitUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self):
        return tweets

    def post(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "entry email",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "tweet",
            help = "entry tweet",
            required = True,
            location = ["json"]
        )
        req = request.json
        date = datetime.now()                 #waktu sekarang
        req['date'] = str(date)
        args = self.reqparse.parse_args()
        emailChecking(req["email"])

        checkingEmailInTweet(req)

        updateDataTweets(tweets)

        return (req)

    def delete(self):
        self.reqparse =reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "entry email",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "tweet",
            help = "entry tweet",
            required = True,
            location = ["json"]
        )
        req = request.json
        args = self.reqparse.parse_args()
        indexEmail = emailCheckingAndTweets(req['email'],req['tweet'])
        tweets.pop(indexEmail)
        updateDataTweets(tweets)
        return {'message ':'tweet delete'}, 200
        
    def put(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            help = "entry email",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "tweet",
            help = "entry tweet",
            required = True,
            location = ["json"]
        )
        self.reqparse.add_argument(
            "tweetbaru",
            help = "entry new tweet",
            required = True,
            location = ["json"]
        )
        req = request.json
        self.reqparse.parse_args()
        index = 0 
        for data in tweets:
            if data["email"] == req["email"]:
                tweets[index]['tweet'] = req["tweetbaru"]
                updateDataTweets(tweets)
                return tweets[index]
            index += 1

        abort(400, message = "email incorrect")


        
twitter_api = Blueprint('resources/twitter',__name__)
api = Api(twitter_api)
api.add_resource(signUpTwitter,'signUpTwitter')
api.add_resource(readAllUserTwitter,'readAllUserTwitter')
api.add_resource(loginTwitter,'loginTwitter')
api.add_resource(twitUser,'twitUser')
api.add_resource(readAllTwit,'readAllTwit')
    


from flask import Flask, jsonify, Blueprint, request
from flask_restful import Resource, Api, reqparse, abort
import json
import datetime

with open('user.json') as user_file:
    user = json.load(user_file)

with open('tweet.json') as tweet_file:
    tweet = json.load(tweet_file)
    
def addUser():
    with open('user.json', 'w') as outfileuser:
            json.dump(user, outfileuser)
            outfileuser.close()

def addTweet():
    with open('tweet.json', 'w') as outfiletweet:
            json.dump(tweet, outfiletweet)
            outfiletweet.close()


class allUser(Resource):
    def get(self):
        return user

class allTweet(Resource):
    def get(self):
        return tweet

class login(Resource):
    def post(self):
        email = request.json["email"]
        password = request.json["password"]

        for data in user:
            if data['email'] == email and data['password'] == password:
                return data, 200
            elif data['email'] == email and data['password'] != password:
                return "Password Salah!", 400
        return "Email tidak ditemukan!", 404
        

def listEmail(mail):
    for data in user:
        if data['email'] == mail:
            abort(400, message = "email telah terdaftar")

def listUser(name):
    for data in user:
        if data['username'] == name:
            abort(400, message = "username telah terdaftar")

class Signup(Resource):
    def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                "email",
                help = "Email wajib diisi",
                required = True,
                location = ["json"]
            )
            self.reqparse.add_argument(
                "username",
                help = "username wajib diisi",
                required = True,
                location = ["json"]
            )
            self.reqparse.add_argument(
                "password",
                help = "password wajib diisi",
                required = True,
                location = ["json"]
            )
            self.reqparse.add_argument(
                "fullname",
                help = "fullname wajib diisi",
                required = True,
                location = ["json"]
            )
            super().__init__()

    def post(self):
        self.reqparse.parse_args()
        listEmail(request.json['email'])
        listUser(request.json['username'])
        user.append(request.json)
        addUser()        
        return "Akun Berhasil di Buat", 201

class Tweet(Resource):
     def __init__(self):
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                "email",
                help = "Email wajib diisi",
                required = True,
                location = ["json"]
            )
            
            self.reqparse.add_argument(
                "tweet",
                help = "tweet tidak boleh kosong",
                required = True,
                location = ["json"]
            )
            super().__init__()

     def post(self):
         data = request.json
         time = str(datetime.datetime.now())
         tmp = {}
         tmp["time"] = time
         req = data.copy()
         req.update(tmp)
         self.reqparse.parse_args()
         tweet.append(req)
         addTweet()
         return "tweet telah dibuat",201

     def delete(self):
        email = request.json["email"]
        twit = request.json["tweet"]

        for index in range(len(tweet)):
            if tweet[index]['email'] == email and tweet[index]['tweet'] == twit:
                tweet.pop(index)
                addTweet()
                return "Tweet telah terhapus", 200
        return "Tweet tidak ditemukan", 404

     def put(self):
         email = request.json["email"]
         oldTwit = request.json["old tweet"]
         newTwit = request.json["new tweet"]
         
         for index in range(len(tweet)):
             if tweet[index]['email'] == email and tweet[index]['tweet'] == oldTwit:
                 tweet[index]['tweet'] = newTwit
                 tweet[index]['time'] = str(datetime.datetime.now())
                 addTweet()
                 return "tweet telah diubah", 201
             return "tweet tidak ada", 400
    
     def get(self):
        tweetList = []
        email = request.json['email']
        for twits in tweet:
            if twits['email'] == email:
                tweetList.append(twits['tweet'])
        return tweetList, 200


twit_api = Blueprint('resources/tweeps', __name__)
api = Api(twit_api)
api.add_resource(allUser, 'allUser')
api.add_resource(allTweet,'allTweet')
api.add_resource(login, 'LogIn')
api.add_resource(Signup, 'SignUp')
api.add_resource(Tweet, 'Tweet')
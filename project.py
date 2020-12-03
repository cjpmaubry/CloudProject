import pymongo #pip install pymongo
import time  
from flask import Flask, render_template # pip install flask
from sshtunnel import SSHTunnelForwarder # pip install sshtunnel 



MONGO_HOST ="devicimongodb003.westeurope.cloudapp.azure.com"
MONGO_USER ="administrateur"
MONGO_PASS ="fcwP6h3H"
MONGO_DB ="cloud"
MONGO_COLLECTION_USERS ="users"
MONGO_COLLECTION_POSTS ="posts"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=(MONGO_DB, 22)
)

def launchQuery(resquestNumber):
    server.start()
    client = pymongo.MongoClient(MONGO_HOST, 30000)
    db = client[MONGO_DB]
    data = executeQueryNb(db,resquestNumber)
    server.stop()
    return data


#Define Timer 
class Timer(object):  
    def start(self):  
        if hasattr(self, 'interval'):  
            del self.interval  
        self.start_time = time.time()  
      
    def stop(self):  
        if hasattr(self, 'start_time'):  
            self.interval = time.time() - self.start_time  
            del self.start_time # Force timer reinit  

app = Flask(__name__)

def executeQueryNb(db,number):
    data =''
    if number == 1 :
        data = db.users.find({"Id": 7}, {"PostIds": 1,"CommentId": 1})
    if number == 2 :
        data =  db.users.find({"PostIds": {"$in": [X] }}, {"Badges": 1})
    if number == 3 :
        data =  db.posts.find({"Title": {"$regex":"X"}}, {"_id":0,"Title": 1}).sort({"CommentCount": -1})
    if number == 4 :
        postUsers = db.Users.find({"Id": X}, {"PostIds": 1,"CommentId.PostId": 1})
        C = postUsers.toArray()
        Tab = []
        C_len = len(C[0]["PostIds"])
        for i in range(0, C_len):
            Tab.push(NumberInt(C[0]["PostIds"][i]))
        C_len2 = len(C[0]["CommentId"])
        for i in range(0, C_len2):
            Tab.push(NumberInt(C[0]["CommentId"][i]["PostId"]))  
        data =  db.Posts.find({"Id": {"$in": Tab},"ClosedDate":""},{"Id":1,"Title":1,"Score":1}).sort({"Score": -1})
    if number == 5 :
        timeOpen = {"$addFields": { timeOpen: {"$switch": { branches: [ { case: {"ClosedDate":""}, then: {"$subtract": ["$$NOW", {"$convert": { input:"$CreaionDate", to:"date"} } ]}}, ], default: {"$subtract": [ {"$convert": { input:"$ClosedDate", to:"date"}}, {"$convert": { input:"$CreaionDate", to:"date"}}]}}} } }
        data =  db.Posts.aggregate([ {"$unwind":"$Tags"}, timeOpen, {"$group": {_id :"$Tags","maxTime": {"$max":"$timeOpen"} } }, {"$project": {"Tags": 1,"timeOpen": 1 ,"maxTime": 1 }} ])
    if number == 6 :
        data =  db.users.aggregate([{"$unwind":"$CommentId"}, {"$group": {"_id": {"Id":"$Id","DisplayName":"$DisplayName","UpVotes":"$UpVotes"} ,"totalComment": {"$sum": 1}  }  }, {"$project": {"Id":"$Id","DisplayName":"$DisplayName","note": {"$sum": ["$_id.UpVotes","totalComment"] }}}, {"$sort": {"note":-1}} ])
    if number == 7 :
        userscount = db.users.count()
        data =  db.users.aggregate([{"$unwind":"$Badges"}, {"$group": {"_id":"$Badges.Name","countBadge": {"$sum": 1}}}, {"$project": {"Badges.Name": 1,"pourcentage": {"$divide": ["$countBadge", userscount]}}}])
    if number == 8 :
        db.UsersAvg.drop()
        B = []
        db.Posts.find({"Tags":"prior"}, {"Comments.Id":1,"_id":0}).forEach(function(Comments){B.push(Comments)})
        C = []
        for i in range(0, len(B)):
            B_comments_len = len(B[i]["Comments"])
            for j in range(0, B_comments_len):
                C.push(NumberInt(B[i]["Comments"][j]["Id"]))
        Result = db.Users.find({"CommentId": {"$in":  C},"Age":{"$gt":0}}, {"Id": 1,"Age":1,"_id":0} )
        db.UsersAvg.insert(Result.toArray())
        data =  db.UsersAvg.aggregate([{"$group": {_id : null, ageAverage: {"$avg":"$Age"}}}])
    return data


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/adminView')
def adminView():
    return render_template('adminView.html')
    
@app.route('/analystView')
def analystView():
    return render_template('analystView.html')

@app.route('/userView')
def userView():
    return render_template('userView.html')


@app.route('/req1')
def req1():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(1)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)


@app.route('/req2')
def req2():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(2)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)



@app.route('/req3')
def req3():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(3)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)



@app.route('/req4')
def req4():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(4)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)

@app.route('/req5')
def req5():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(5)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)

@app.route('/req6')
def req6():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(6)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)


@app.route('/req7')
def req7():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(7)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)

@app.route('/req8')
def req8():
    query_description =""
    timer = Timer()  
    timer.start()
    data= launchQuery(8)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_decription= query_description)


if __name__ =="__main__":
    app.run()
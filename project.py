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
        data =  db.Users.find({"PostIds": {"$in": [X] }}, {"Badges": 1})
    if number == 3 :
        data =  db.Posts.find({"Title": {$regex :"X"}}, {"_id" :0,"Title": 1}).sort({"CommentCount": -1}).pretty()
    if number == 4 :
        data =  ''
    if number == 5 :
        data =  ''
    if number == 6 :
        data =  db.Users.aggregate([{"$unwind":"$CommentId"}, { $group : {"_id": {"Id":"$Id","DisplayName":"$DisplayName","UpVotes":"$UpVotes"} ,"totalComment": {$sum : 1}  }  }, {$project : {"Id":"$Id","DisplayName":"$DisplayName","note": {$sum : ["$_id.UpVotes","totalComment"] }}}, { $sort : {"note":-1}} ])
    if number == 7 :
        userscount = db.Users.count()
        data =  db.Users.aggregate([{"$unwind":"$Badges"}, { $group : {"_id":"$Badges.Name","countBadge": {$sum : 1}}}, { $project : {"Badges.Name": 1,"pourcentage": {$divide : ["$countBadge", userscount]}}}])
    if number == 8 :
        data =  ''
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
    timer = Timer()  
    timer.start()
    data= launchQuery(1)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )


@app.route('/req2')
def req2():
    timer = Timer()  
    timer.start()
    data= launchQuery(2)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )



@app.route('/req3')
def req3():
    timer = Timer()  
    timer.start()
    data= launchQuery(3)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )



@app.route('/req4')
def req4():
    timer = Timer()  
    timer.start()
    data= launchQuery(4)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )

@app.route('/req5')
def req5():
    timer = Timer()  
    timer.start()
    data= launchQuery(5)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )

@app.route('/req6')
def req6():
    timer = Timer()  
    timer.start()
    data= launchQuery(6)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )


@app.route('/req7')
def req7():
    timer = Timer()  
    timer.start()
    data= launchQuery(7)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )

@app.route('/req8')
def req8():
    timer = Timer()  
    timer.start()
    data= launchQuery(8)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )


if __name__ =="__main__":
    app.run()
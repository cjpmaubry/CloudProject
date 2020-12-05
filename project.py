import pymongo #pip install pymongo
import time  
from flask import Flask, render_template, request # pip install flask
from sshtunnel import SSHTunnelForwarder # pip install sshtunnel 



MONGO_HOST ="devicimongodb003.westeurope.cloudapp.azure.com"
MONGO_USER ="administrateur"
MONGO_PASS ="fcwP6h3H"
MONGO_DB ="cloud"
MONGO_COLLECTION_USERS ="users"
MONGO_COLLECTION_posts ="posts"

server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=(MONGO_DB, 22)
)

def launchQuery(resquestNumber,parametre):
    server.start()
    client = pymongo.MongoClient(MONGO_HOST, 30000)
    db = client[MONGO_DB]
    data = executeQueryNb(db,resquestNumber,parametre)
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

def executeQueryNb(db,number,parametre):
    data =''
    if number == 1 :
        data = db.users.find({"Id":int(parametre)}, {"PostIds": 1,"CommentId": 1})
    if number == 2 :
        data =  db.users.find({"PostIds": {"$in": [int(parametre)] }}, {"Badges": 1})
    if number == 3 :
        data =  db.posts.find({"Title": {"$regex": parametre }},{"_id":0,"Title": 1}).sort("CommentCount", -1)
    if number == 4 :
        postUsers = db.Users.find({"Id": int(parametre)}, {"PostIds": 1,"CommentId.PostId": 1})
        C = list(postUsers) # L'erreur est ici pas possible d'appliqué toArray à un cursor
        Tab = []
        C_len = len(C[0]["PostIds"])
        for i in range(0, C_len):
            Tab.append(int(C[0]["PostIds"][i]))
        C_len2 = len(C[0]["CommentId"])
        for i in range(0, C_len2):
            Tab.append(int(C[0]["CommentId"][i]["PostId"]))
        data =  db.posts.find({"Id": {"$in": Tab},"ClosedDate":""},{"Id":1,"Title":1,"Score":1}).sort({"Score": -1})
    if number == 5 :
        #on ne peut definir timeOpen par lui meme. Faut chercher la syntaxe avec python
        timeOpen = {"$addFields": { timeOpen: {"$switch": { "branches": [ { "case": {"ClosedDate":""}, "then": {"$subtract": ["$$NOW", {"$convert": { input:"$CreaionDate", "to":"date"} } ]}}, ], "default": {"$subtract": [ {"$convert": { input:"$ClosedDate", "to":"date"}}, {"$convert": { input:"$CreaionDate", "to":"date"}}]}}} } }
        data =  db.posts.aggregate([ {"$unwind":"$Tags"}, timeOpen, {"$group": {"_id" :"$Tags","maxTime": {"$max":"$timeOpen"} } }, {"$project": {"Tags": 1,"timeOpen": 1 ,"maxTime": 1 }} ])
    if number == 6 :
        data =  db.users.aggregate([{"$unwind":"$CommentId"}, {"$group": {"_id": {"Id":"$Id","DisplayName":"$DisplayName","UpVotes":"$UpVotes"} ,"totalComment": {"$sum": 1}  }  }, {"$project": {"Id":"$Id","DisplayName":"$DisplayName","note": {"$sum": ["$_id.UpVotes","totalComment"] }}}, {"$sort": {"note":-1}} ])
    if number == 7 :
        userscount = db.users.count()
        data =  db.users.aggregate([{"$unwind":"$Badges"}, {"$group": {"_id":"$Badges.Name","countBadge": {"$sum": 1}}}, {"$project": {"Badges.Name": 1,"pourcentage": {"$divide": ["$countBadge", userscount]}}}])
    if number == 8 :
        db.UsersAvg.drop()
        B = []
        _posts = db.posts.find({"Tags":parametre}, {"Comments.Id":1,"_id":0})
        for i in range(_posts.count()): # Un cursor n'est pas un tableau donc on peu pas utiliser len -> fix
            B.append(_posts[i]["Comments"])
        #.forEach(function(Comments){B.push(Comments)})
        C = []
        for i in range(0, len(B)):
            B_comments_len = len(B[i]["Comments"])
            for j in range(0, B_comments_len):
                C.append(int(B[i]["Comments"][j]["Id"]))
        Result = db.Users.find({"CommentId": {"$in":  C},"Age":{"$gt":0}}, {"Id": 1,"Age":1,"_id":0} )
        db.UsersAvg.insert(Result.toArray())
        data =  db.UsersAvg.aggregate([{"$group": {"_id" : "null", "ageAverage": {"$avg":"$Age"}}}])
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


@app.route('/req1',methods = ['POST'])
def req1():
    query_description ='L historique des commentaires et des posts pour un utilisateur donné'
    result = request.form
    id = result['id_user']
    timer = Timer()  
    timer.start()
    data= launchQuery(1,id)
    timer.stop()
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)


@app.route('/req2',methods = ['POST'])
def req2():
    query_description ="Les informations relatives aux badges de l'utilisateur d'un post donné"
    result = request.form
    id = result['id_post']
    timer = Timer()  
    timer.start()
    data= launchQuery(2,id)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)



@app.route('/req3',methods = ['POST'])
def req3():
    query_description =" La liste des posts dont le titre ou le corps contient un mot clef donné, trié par le nombre de commentaires associés.  "
    result = request.form
    mot_clef = result['mot_clef']
    timer = Timer()  
    timer.start()
    data= launchQuery(3,mot_clef)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)



@app.route('/req4',methods = ['POST'])
def req4():
    query_description ="La liste des posts actifs pour un utilisateur, trié par le score du post (c’est-à-dire les posts qu'il a créé ou commenté et qui n’ont pas encore été fermés.) "
    result = request.form
    id = result['id_user']
    timer = Timer()  
    timer.start()
    data= launchQuery(4,id)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)

@app.route('/req5',methods = ['POST'])
def req5():
    query_description ="Le post ayant la durée d'activité la plus longue par tag (pour le tag 1 c’est le post Y ; pour le tag 2 c’est le post X etc…)  "
    noparam=""
    timer = Timer()  
    timer.start()
    data= launchQuery(5,noparam)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)

@app.route('/req6',methods = ['POST'])
def req6():
    query_description ="L'utilisateur le plus actif en prenant en considération le nombre de votes positifs et le nombre de commentaires  "
    noparam=""
    timer = Timer()  
    timer.start()
    data= launchQuery(6,noparam)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)


@app.route('/req7',methods = ['POST'])
def req7():
    query_description ="Le pourcentage d’obtention de chaque badge"
    noparam=""
    timer = Timer()  
    timer.start()
    data= launchQuery(7,noparam)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)

@app.route('/req8',methods = ['POST'])
def req8():
    query_description ="L’âge moyen des utilisateurs commentant les posts d’un certain tag"
    result = request.form
    tag = result['tag']
    timer = Timer()  
    timer.start()
    data= launchQuery(8,tag)
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval, query_description= query_description)


if __name__ =="__main__":
    app.run(debug=True)
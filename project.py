import pymongo #pip install pymongo
import time  
from flask import Flask, render_template # pip install flask
from ssh_pymongo import MongoSession # pip install ssh-pymongo

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
    data= 'here it is the result of the request'
    #data= db.Users.find( {"Id" :X}, {"PostIds" :1, "CommentId" : 1} ).pretty() ; 
    timer.stop()  
    return render_template('req.html',data = data, time = timer.interval )


@app.route('/req2')
def req2():
    #db.Users.find( {"PostIds" : {"$in" : [X] }}, {"Badges" : 1} ).pretty() ; 
    return render_template('req.html')


@app.route('/req3')
def req3():
    #db.Posts.find({"Title" : {$regex : "X"}},  { "_id" :0, "Title" : 1}).sort({ "CommentCount" : -1}).pretty(); 
    #db.Posts.find({"Body" : {$regex : "X"}},  { "_id" :0, "Title" : 1}).sort({ "CommentCount" : -1}).pretty(); 
    return render_template('req.html')


@app.route('/req4')
def req4():
    #var postUsers = db.Users.find({"Id" : X}, {"PostIds" : 1, "CommentId.PostId" : 1}).pretty();  
    #var C = postUsers.toArray()  
    #var Tab = []  

# for (let i = 0; i< C[0]["PostIds"].length; i++) {   

#     Tab.push(NumberInt(C[0]["PostIds"][i]))   

# }  

# for (let i = 0; i< C[0]["CommentId"].length; i++) {   

#     Tab.push(NumberInt(C[0]["CommentId"][i]["PostId"]))   

# }  

#db.Posts.find({"Id" : {"$in": Tab}, "ClosedDate" : "" },{"Id":1,"Title":1,"Score":1}).sort({ "Score" : -1}).pretty(); 
    return render_template('req.html')


@app.route('/req5')
def req5():
    
#     timeOpen = {  

# $addFields: { timeOpen: {  

# $switch: {  

#         branches: [  

#           { case:  

#               { "ClosedDate" : "" },  

#               then:  

#           {$subtract :  

#               ["$$NOW", {$convert: 

#               { input : "$CreaionDate", to : "date"} } ]}},  

#         ],  

#         default:   

#             {$subtract :  

#                 [ {$convert:  

#                 { input : "$ClosedDate", to : "date"}} 

#             , {$convert: { input : "$CreaionDate", to : "date"}}]}   

#      }  

# } } };  

# db.Posts.aggregate([ {$unwind : "$Tags"},  timeOpen, {  $group :  {  _id : "$Tags", "maxTime" : {$max : "$timeOpen"}  
# }  },     

# { $project : { "Tags" : 1, 

#     "timeOpen" : 1 

#     ,"maxTime" : 1 

#     }}  

# ]); 

    return render_template('req.html')


@app.route('/req6')
def req6():
   
#     db.Users.aggregate( [  
# {"$unwind" : "$CommentId"},  
# { $group : {  
# "_id" : {"Id" : "$Id", "DisplayName" : "$DisplayName", "UpVotes" :  "$UpVotes"} , "totalComment" : {$sum : 1}  }  },  
# {$project : { 
# "Id" : "$Id", "DisplayName" : "$DisplayName", "note" : {$sum : ["$_id.UpVotes", "totalComment"] }}},  
# { $sort : {"note":-1}} ]) ; 

    return render_template('req.html')


@app.route('/req7')
def req7():
    #var userscount = db.Users.count(); 

# db.Users.aggregate( 
# [ 
# {"$unwind" : "$Badges"}, 
# { $group : { 
# "_id" : "$Badges.Name", 
# "countBadge" : {$sum : 1} 
# } 
# }, 
# { $project : { "Badges.Name" : 1, "pourcentage" : {$divide : ["$countBadge", userscount]}}} 
# ]) ; 
 
    return render_template('req.html')


@app.route('/req8')
def req8():
    
#     db.UsersAvg.drop() 
# var B = []  
# db.Posts.find(  
# {"Tags" :"prior"},  
# {"Comments.Id" :1, "_id":0}  
# ).forEach(function(Comments){B.push(Comments)});   
# var C = []  
# for (let i = 0; i< B.length; i++)  
# {  
#  for (let j = 0; j<B[i]["Comments"].length; j++) 
# {  
#  C.push(NumberInt(B[i]["Comments"][j]["Id"]))  
# } 
# }  
# var Result = db.Users.find( 
# {"CommentId" : {"$in" :  C},"Age":{"$gt":0}}, 
# {"Id" : 1,"Age" :1,"_id":0} 
# );   
# db.UsersAvg.insert(Result.toArray()) 
# db.UsersAvg.aggregate(  
# [ 
# {  $group :   
#  {   
#  _id : null, 
#  ageAverage : {$avg : "$Age"}   
#      }   
# }   
# ]) ; 
    
    return render_template('req.html')


if __name__ == "__main__":
    app.run()
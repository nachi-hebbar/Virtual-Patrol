from flask import Flask,request, url_for, redirect, render_template
import pickle
import pymongo
import numpy as np
from prettytable import PrettyTable
x = PrettyTable()

y=PrettyTable()
y.field_names=["Name", "Number", "Date", "Incident-Type","Description",'status']
reg_current=""
x.field_names = ["Name", "Number", "Date", "Incident-Type","Description",'status']

app = Flask(__name__)
uri = 'mongodb://nachi:nachoss1999@ds033579.mlab.com:33579/forest_safety'
client = pymongo.MongoClient(uri)
db = client.get_default_database()

pred = db['predictions']
reg=db['registered']
users = db['users']
#db=MongoAlchemy()
model=pickle.load(open('model.pkl','rb'))
model2=pickle.load(open('model2.pkl','rb'))

names=['Naman','Nachiketa','Ajay']
list1=[]
@app.route('/')
def hello_world():
    return render_template("login.html")
@app.route('/report',methods=['POST','GET'])
def report():
    x.clear_rows()
    for i in names:

        user_det=users.find_one({'name':i})
        list2=list(user_det.values())
        print(list2)
        x.add_row(list2[1:])





    #name,date,incident,status=list2[1],list2[3],list2[4],list2[5]
    x.sortby ="Incident-Type"
    print(x)
    return render_template('reports.html',name=x.get_html_string())

@app.route('/map',methods=['POST','GET'])
def map():
    return render_template("map.html")
@app.route('/forest',methods=['POST','GET'])
def forest_fire():
    return render_template('forest_fire.html')

@app.route('/login_now',methods=['POST','GET'])
def login_now():
    print("hello")
    print(request.form())
    name1=request.form['username']
    print(name1)
    if reg.find_one({"name": name1})=='None':
        return "User Does Not Exist"
    else:
        if request.form['user-type']==Authority:
            user_det=reg.find_one({'name':request.form['username']})
            if user_det['password']==request.form['password']:

                return render_template("authority.html",naam=name1)
            else:
                return render_template("login.html",naam="Invalid Password")
        else:
            user_det=reg.find_one({'name':request.form['username']})
            if user_det['password'] == request.form['password']:

                return render_template("index2.html", naam=name1)
            else:
                return render_template("login.html", naam="Invalid Password")


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)
    pred.insert({'prediction': output})
    if output>str(0.5):
        return render_template('forest_fire.html',pred='Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output),bhai="kuch karna hain iska ab?")
    else:
        return render_template('forest_fire.html',pred='Your Forest is safe.\n Probability of fire occuring is {}'.format(output),bhai="Your Forest is Safe for now")


@app.route('/crime',methods=['POST','GET'])
def crime():
    return render_template("crime_prediction.html")
@app.route('/crime-predict',methods=['POST','GET'])
def crime_pred():
    print(request.form)
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model2.predict(final)
    #output='{0:.{1}f}'.format(prediction[0][1], 2)
    #pred.insert({'prediction': output})

    return render_template('crime_prediction.html',prediction_text='Predicted Number of Crimes in this region is {}'.format(prediction[0]))
    #else:
     #   return render_template('crime_prediction.html',prediction_text='Number of Crimes tht take place normally {}'.format(output))


@app.route('/masti',methods=['POST','GET'])
def masti():
    return render_template('ml.html')
@app.route('/status',methods=['POST','GET'])
def status():

    user_det = users.find_one({'name': 'Nachiketa'})
    list2 = list(user_det.values())
    print(list2)
    y.add_row(list2[1:])
    return render_template("citizen_reports.html",name=y.get_html_string())
@app.route('/user-registration',methods=['POST','GET'])
def register():
    type=request.form['user-type']
    print(type)
    reg.insert({'usertype':request.form['user-type'],'name':request.form['username'],'password':request.form['password']})

    if type=="Authority":
        return render_template("authority.html",naam=request.form['username'])
    elif type=="Citizen":
        return render_template("index2.html",naam=request.form['username'])
    else:
        return render_template("login.html",naam="Invalid user type")
@app.route('/notice1',methods=['POST','GET'])
def notice1():
    return render_template("notice.html")
@app.route('/databasee',methods=['POST','GET'])
def database():

    print(request.form)
    names.append(request.form['username'])

    users.insert({'name':request.form['username'], 'number':request.form['number'],'Date':request.form['incident_type'],'incident-type':request.form['type-incident'],'Description':request.form['incident'],'status':'0'})
    print("Updated")
    return("Done")

if __name__ == '__main__':
    app.run(debug=True)

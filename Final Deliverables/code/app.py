from flask import Flask, render_template, request, redirect, url_for
import flask
import ibm_db
import requests
app = Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=szm60307;PWD=bLDLs25hvhcdv6gk",'','')
if conn:
    print("connected")
@app.route('/register')
def register():
    return render_template('register.html')
app.add_url_rule('/register','register',register)
@app.route("/register",methods = ['POST'])
def register_data():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    city = request.form['city']
    infect = request.form['infect']
    blood = request.form['blood']
    password = request.form['passw']

    # sql = "SELECT * FROM DONOR2 WHERE name =?"
    # stmt = ibm_db.prepare(conn, sql)
    # ibm_db.bind_param(stmt,1,name)
    # ibm_db.execute(stmt)
    # account = ibm_db.fetch_assoc(stmt)
    # if account:
    #     return render_template('donor.html', msg="You are already a member, please login using your details")
    # else:
    #     #mailtest_donor(email)
    insert_sql = "insert into donor2 (name , email ,phone,city,infect,blood,password) values ('"+name+"','"+email+"','"+phone+"','"+city+"','"+infect+"','"+blood+"','"+password+"');"
    isOk=ibm_db.exec_immediate(conn,insert_sql)
    if isOk:
        print('yesssss')
        return render_template ("success.html")
    else:
        return "success"
@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['GET','POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    sql = "SELECT * FROM donor2 WHERE email =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.bind_param(stmt,2,passw)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print (account)
    print(user,passw)
    if account:
            return redirect(url_for('stats'))
    else:
        return render_template('login.html', pred="Login unsuccessful. Incorrect username / password !") 
 
@app.route('/stats')
def stats():
    '''sql = "SELECT blood FROM donor2 group by blood"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    count = ibm_db.fetch_assoc(stmt)
    print(count)'''
    return render_template('stats.html',b=0,b1=0,b2=0,b3=0,b4=0,b5=0,b6=0,b7=0,b8=0)

@app.route('/requester')
def requester():
    return render_template('request.html')

@app.route('/requester',methods=['GET','POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    address = request.form['address']
    print(address)
    sql = "SELECT * FROM donor2 WHERE blood=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,bloodgrp)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)
    msg = "Need Plasma of your blood group for: "+address
    while data != False:
        print ("The Phone is : ", data["PHONE"])
        url="https://www.fast2sms.com/dev/bulk?authorization=xCXuwWTzyjOD2ARd1EngbH3a7tKIq5PklJ8YSf0Lh4FQZecs9iNI1dSvuqprxFwCKYJXA5amQkBE36Rl&sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers="+str(data["PHONE"])
        result=requests.request("GET",url)
        print(result)
        data = ibm_db.fetch_assoc(stmt)
    return render_template('request.html', pred="Your request is sent to the concerned people.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)
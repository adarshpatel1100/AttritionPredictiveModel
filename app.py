from flask import Flask,jsonify,render_template,request,redirect,url_for,make_response,session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
# import tablib
import os
import pandas as pd
import numpy as np
import pickle
import pdfkit
from numpy import array

import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score






path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.secret_key = "mylearninglens"


#dataconnection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='hrdb'

mysql = MySQL(app)

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')


@app.route('/log_in',methods=['GET','POST']) 
def log_in():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # cur = mysql.connection.cursor()
        # cur.execute("SELECT email,password FROM sign_up WHERE email = %s AND password = %s",(email,password))
        # result= cur.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM sign_up WHERE email = %s AND password = %s',(email,password))
        # Fetch one record and return result
        result = cursor.fetchone()
        print(type(result))
        
        
        if result is None:
            session.pop('user', None)
            session.pop('name', None)
            flash('Username or Password is wrong! Try Again', 'danger')
            return render_template('login.html')
        else:
            session['user'] = email
            session['name'] = result['fname']
            name = result['fname']
            flash('Login successful', 'success')
            return render_template('home.html')


@app.route('/logout')
def user_logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out,{user}","info")
    session.pop('user', None)
    session.pop('name', None)   
    return render_template("Login.html")       

@app.route('/signup',methods=['GET','POST'])
def signup():
    return render_template('signup.html')


@app.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == "POST":
        details = request.form
        fname= details['fname']
        lname= details['lname']
        email= details['email']
        password= details['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sign_up(fname,lname,email,password) values (%s,%s,%s,%s)",(fname,lname,email,password))
        mysql.connection.commit()
        cur.close()
        return render_template('login.html')
    return render_template('signup.html')





@app.route('/newindex')
def newindex():
    return render_template("newindex.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/individual')
def individual():
    return render_template("individual.html")

@app.route('/pdf')
def pdf():
   
    newheadernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition','Predicted']

    data_frame = pd.read_csv(os.path.abspath("export_dataframe.csv"),names=newheadernames)

    x=data_frame.iloc[1:,:-2].values
    y=data_frame.iloc[1:,-2:].values

    x = pd.DataFrame(x, columns = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager'])
    
    y = pd.DataFrame(y, columns=['Attrition','Predicted'])
    

    print(x)
    print(y)
    # yes=y['Predicted']=='Yes'
    # yes=len(yes)
    # no=y['Predicted']=='No'
    # no=len(no)
    total=(len(data_frame)-1)

    yes=y.loc[y.Predicted == 'Yes','Predicted'].count()
    no=y.loc[y.Predicted == 'No','Predicted'].count()
    predyes=round((yes/total)*100,2)
    predno=round((no/total)*100,2)
    prediction=[predyes,predno]

    pred=y['Predicted'] == 'Yes'

    # Age
    # age1 = (x['Age'] > str(35)).value_counts()
    # list1 = list(age1)


    age1 =  len(x[(x['Age']<'25')]) 
    age2 =  len(x[(x['Age']>='25') & (x['Age']<'30')])
    age3 =  len(x[(x['Age']>='30') & (x['Age']<'35')])
    age4 =  len(x[(x['Age']>='35') & (x['Age']<'40')])
    age5 =  len(x[(x['Age']>='40')]) 
    agelist = [age1,age2,age3,age4,age5]
    # age2=age2.count()
    # print(age1)
    # print(age2)
    # print(age3)
    # print(age4)
    # print(age5)
    # age2 = (x['Age'] between str(25,35)).value_counts()
    # list2 = list(age2)

    # print(list2[1])
    
    newage1 =  len(x[(x['Age']<'25') & (y['Predicted'] == 'Yes')])
    newage2 =  len(x[(x['Age']>='25') & (x['Age']<'30')  & (y['Predicted'] == 'Yes')])
    newage3 =  len(x[(x['Age']>='30') & (x['Age']<'35')  & (y['Predicted'] == 'Yes')])
    newage4 =  len(x[(x['Age']>='35') & (x['Age']<'40')  & (y['Predicted'] == 'Yes')])
    newage5 =  len(x[(x['Age']>='40')  & (y['Predicted'] == 'Yes')]) 
    newage = [newage1,newage2,newage3,newage4,newage5]

    perage1 = round((newage1/age1)*100,2)
    perage2 = round((newage2/age2)*100,2)
    perage3 = round((newage3/age3)*100,2)
    perage4 = round((newage4/age4)*100,2)
    perage5 = round((newage5/age5)*100,2)

    perage=[perage1,perage2,perage3,perage4,perage5]
    # count = len(agenew)
    # per = (count/int(age1))*100
    # print(count)
    # print(per)
    # print(newage1)
    # print(newage2)
    # print(newage3)
    # print(newage4)
    # print(newage5)


    # Business Travel

    # busi=x['BusinessTravel'].value_counts()
    busi1=len(x[(x['BusinessTravel']=='1')])
    busi2=len(x[(x['BusinessTravel']=='2')])
    busi3=len(x[(x['BusinessTravel']=='3')])
    businesslist = [busi1,busi2,busi3]

    newbusiness1 = len(x[(x['BusinessTravel']=='1') & pred])
    newbusiness2 = len(x[( x['BusinessTravel']=='2') & pred])
    newbusiness3 = len(x[( x['BusinessTravel']=='3') & pred])
    newbusiness = [newbusiness1,newbusiness2,newbusiness3]

    perbusiness1 = round((newbusiness1/businesslist[0])*100,2)
    perbusiness2 = round((newbusiness2/businesslist[1])*100,2)
    perbusiness3 = round((newbusiness3/businesslist[2])*100,2)
    perbusiness = [perbusiness1,perbusiness2,perbusiness3]

    # Department

    # dept=x['Department'].value_counts()
    depart1=len(x[(x['Department']=='1')])
    depart2=len(x[(x['Department']=='2')])
    depart3=len(x[(x['Department']=='3')])
    departmentlist = [depart1,depart2,depart3]

    department1 = x['Department']=='1'
    department2 = x['Department']=='2'
    department3 = x['Department']=='3'

    newdepartment1 = len(x[department1 & pred])
    newdepartment2 = len(x[department2 & pred])
    newdepartment3 = len(x[department3 & pred])
    newdepartment = [newdepartment1,newdepartment2,newdepartment3]

    perdepartment1 = round((newdepartment1/departmentlist[0])*100,2)
    perdepartment2 = round((newdepartment2/departmentlist[1])*100,2)
    perdepartment3 = round((newdepartment3/departmentlist[2])*100,2)
    perdepartment = [perdepartment1,perdepartment2,perdepartment3]

    # Distance From Home

    # distancefromhome1 = len(x[(x['DistanceFromHome']<'5')]) 
    # print(distancefromhome1)
    # distancefromhome2 = len(x[(x['DistanceFromHome']>='5') & (x['DistanceFromHome']<'10')])
    # print(distancefromhome2)
    # distancefromhome3 = len(x[(x['DistanceFromHome']>='10') & (x['DistanceFromHome']<'15')])
    # print(distancefromhome3)
    # distancefromhome4 = len(x[(x['DistanceFromHome']>='15')])
    # distancefromhomelist = [distancefromhome1,distancefromhome2,distancefromhome3,distancefromhome4]
    # print(distancefromhomelist)
    # newdistancefromhome1 = len(x[(x['DistanceFromHome']<'5') & pred]) 
    # newdistancefromhome2 = len(x[(x['DistanceFromHome']>='5') & (x['DistanceFromHome']<'10') & pred])
    # newdistancefromhome3 = len(x[(x['DistanceFromHome']>='10') & (x['DistanceFromHome']<'15') & pred])
    # newdistancefromhome4 = len(x[(x['DistanceFromHome']>='15')  & pred])
    # newdistancefromhome = [newdistancefromhome1,newdistancefromhome2,newdistancefromhome3,newdistancefromhome4]
    # print(newdistancefromhome)
    # perdistancefromhome1 = round((newdistancefromhome1/distancefromhome1)*100,2)
    # perdistancefromhome2 = round((newdistancefromhome2/distancefromhome2)*100,2)
    # perdistancefromhome3 = round((newdistancefromhome3/distancefromhome3)*100,2)
    # perdistancefromhome4 = round((newdistancefromhome4/distancefromhome4)*100,2)
    # perdistancefromhome=[perdistancefromhome1,perdistancefromhome2,perdistancefromhome3,perdistancefromhome4]
    # print(predistancefromhome)

    # Gender
    # gender=x['Gender'].value_counts()
    gender1=len(x[(x['Gender']=='1')])
    gender2=len(x[(x['Gender']=='2')])
    genderlist = [gender1,gender2]
    

    newgender1 = len(x[(x['Gender']=='1') & pred])
    newgender2 = len(x[(x['Gender']=='2') & pred])
    newgender = [newgender1,newgender2]
    

    pergender1 = round((newgender1/genderlist[0])*100,2)
    pergender2 = round((newgender2/genderlist[1])*100,2)
    pergender = [pergender1,pergender2]
    
    # Job JobInvolvement 
    jobinvolve1 = len(x[(x['JobInvolvement']=='1')])
    jobinvolve2 = len(x[(x['JobInvolvement']=='2')])
    jobinvolve3 = len(x[(x['JobInvolvement']=='3')])
    jobinvolve4 = len(x[(x['JobInvolvement']=='4')])
    jobinvolvelist = [jobinvolve1,jobinvolve2,jobinvolve3,jobinvolve4]

    

    newjobinvolve1 = len(x[(x['JobInvolvement']=='1') & pred])
    newjobinvolve2 = len(x[(x['JobInvolvement']=='2') & pred])
    newjobinvolve3 = len(x[(x['JobInvolvement']=='3') & pred])
    newjobinvolve4 = len(x[(x['JobInvolvement']=='4') & pred])
    newjobinvolve = [newjobinvolve1,newjobinvolve2,newjobinvolve3,newjobinvolve4]



    perjobinvolve1 = round((newjobinvolve1/jobinvolvelist[0])*100,2)
    perjobinvolve2 = round((newjobinvolve2/jobinvolvelist[1])*100,2)
    perjobinvolve3 = round((newjobinvolve3/jobinvolvelist[2])*100,2)
    perjobinvolve4 = round((newjobinvolve4/jobinvolvelist[3])*100,2)
    perjobinvolve = [perjobinvolve1,perjobinvolve2,perjobinvolve3,perjobinvolve4]


    # Job Role

    jobrole1 = len(x[(x['JobRole']=='1')])
    jobrole2 = len(x[(x['JobRole']=='2')])
    jobrole3 = len(x[(x['JobRole']=='3')])
    jobrole4 = len(x[(x['JobRole']=='4')])
    jobrole5 = len(x[(x['JobRole']=='5')])
    jobrole6 = len(x[(x['JobRole']=='6')])
    jobrole7 = len(x[(x['JobRole']=='7')])
    jobrole8 = len(x[(x['JobRole']=='8')])
    jobrole9 = len(x[(x['JobRole']=='9')])
    jobrolelist = [jobrole1,jobrole2,jobrole3,jobrole4,jobrole5,jobrole6,jobrole7,jobrole8,jobrole9]
    

    newjobrole1 = len(x[(x['JobRole']=='1') & pred])
    newjobrole2 = len(x[(x['JobRole']=='2') & pred])
    newjobrole3 = len(x[(x['JobRole']=='3') & pred])
    newjobrole4 = len(x[(x['JobRole']=='4') & pred])
    newjobrole5 = len(x[(x['JobRole']=='5') & pred])
    newjobrole6 = len(x[(x['JobRole']=='6') & pred])
    newjobrole7 = len(x[(x['JobRole']=='7') & pred])
    newjobrole8 = len(x[(x['JobRole']=='8') & pred])
    newjobrole9 = len(x[(x['JobRole']=='9') & pred])
    newjobrole = [newjobrole1,newjobrole2,newjobrole3,newjobrole4,newjobrole5,newjobrole6,newjobrole7,newjobrole8,newjobrole9]
    print(newjobrole)

    perjobrole1 = round((newjobrole1/jobrolelist[0])*100,2)
    perjobrole2 = round((newjobrole2/jobrolelist[1])*100,2)
    perjobrole3 = round((newjobrole3/jobrolelist[2])*100,2)
    perjobrole4 = round((newjobrole4/jobrolelist[3])*100,2)
    perjobrole5 = round((newjobrole5/jobrolelist[4])*100,2)
    perjobrole6 = round((newjobrole6/jobrolelist[5])*100,2)
    perjobrole7 = round((newjobrole7/jobrolelist[6])*100,2)
    perjobrole8 = round((newjobrole8/jobrolelist[7])*100,2)
    perjobrole9 = round((newjobrole9/jobrolelist[8])*100,2)
    perjobrole = [perjobrole1,perjobrole2,perjobrole3,perjobrole4,perjobrole5,perjobrole6,perjobrole7,perjobrole8,perjobrole9]
    

    # Job Satisfaction

    jobsatisfy1 = len(x[(x['JobSatisfaction']=='1')])
    jobsatisfy2 = len(x[(x['JobSatisfaction']=='2')])
    jobsatisfy3 = len(x[(x['JobSatisfaction']=='3')])
    jobsatisfy4 = len(x[(x['JobSatisfaction']=='4')])
    jobsatisfylist = [jobsatisfy1,jobsatisfy2,jobsatisfy3,jobsatisfy4]
    print(jobsatisfylist)

    newjobsatisfy1 = len(x[(x['JobSatisfaction']=='1') & pred])
    newjobsatisfy2 = len(x[(x['JobSatisfaction']=='2') & pred])
    newjobsatisfy3 = len(x[(x['JobSatisfaction']=='3') & pred])
    newjobsatisfy4 = len(x[(x['JobSatisfaction']=='4') & pred])
    newjobsatisfy = [newjobsatisfy1,newjobsatisfy2,newjobsatisfy3,newjobsatisfy4]
    print(newjobsatisfy)

    perjobsatisfy1 = round((newjobsatisfy1/jobsatisfylist[0])*100,2)
    perjobsatisfy2 = round((newjobsatisfy2/jobsatisfylist[1])*100,2)
    perjobsatisfy3 = round((newjobsatisfy3/jobsatisfylist[2])*100,2)
    perjobsatisfy4 = round((newjobsatisfy4/jobsatisfylist[3])*100,2)
    perjobsatisfy = [perjobsatisfy1,perjobsatisfy2,perjobsatisfy3,perjobsatisfy4]
    print(perjobsatisfy)


    # Over Time 
    over1=len(x[(x['OverTime']=='1')])
    over2=len(x[(x['OverTime']=='2')])
    overlist = [over1,over2]
    print(overlist)

    newover1 = len(x[(x['OverTime']=='1') & pred])
    newover2 = len(x[(x['OverTime']=='2') & pred])
    newover = [newover1,newover2]
    print(newover)
    

    perover1 = round((newover1/overlist[0])*100,2)
    perover2 = round((newover2/overlist[1])*100,2)
    perover = [perover1,perover2]
    print(perover)

    import base64

    with open(os.path.abspath("static/pdfheader.png"), "rb") as image_file:
        img = base64.b64encode(image_file.read())
    img = img.decode('utf-8')

    # with open(os.path.abspath("static/footer80per.png"), "rb") as image_file:
    #     imgfoot = base64.b64encode(image_file.read())
    # imgfoot = imgfoot.decode('utf-8')

    rendered = render_template("pdf.html",name=algorithm,accuracy=accuracy,yes=yes,no=no,total=total,prediction=prediction,newage=newage,agelist=agelist,perage=perage,businesslist=businesslist,
                                newbusiness=newbusiness,perbusiness=perbusiness,departmentlist=departmentlist,newdepartment=newdepartment,perdepartment=perdepartment,
                                genderlist=genderlist,newgender=newgender, pergender=pergender,img=img,jobinvolvelist=jobinvolvelist,newjobinvolve=newjobinvolve,perjobinvolve=perjobinvolve,
                                jobrolelist=jobrolelist,newjobrole=newjobrole,perjobrole=perjobrole,jobsatisfylist=jobsatisfylist,newjobsatisfy=newjobsatisfy,perjobsatisfy=perjobsatisfy,
                                overlist=overlist,newover=newover,perover=perover)



    pdf = pdfkit.from_string(rendered,False,configuration=config)
    # pdfkit.from_url('https://google.co.in','out_new.pdf',configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename = output.pdf'

    return response


# @app.route('/dataset_view')
# def dataset_view():
#     return render_template('file.html')



@app.route('/individual_predict',methods=['GET','POST'])
def individual_predict():
    age = request.form["age"]
    businesstravel =  request.form["businesstravel"]
    department = request.form["department"]
    distancefromhome = request.form["distancefromhome"]
    education = request.form["education"]
    educationfield = request.form["educationfield"]
    gender = request.form["gender"]
    jobinvolvment = request.form["jobinvolvment"]
    joblevel = request.form["joblevel"]
    jobrole = request.form["jobrole"]
    jobsatisfaction = request.form["jobsatisfaction"]
    monthlyincome = request.form["monthlyincome"]
    monthlyrate = request.form["monthlyrate"]
    overtime = request.form["overtime"]
    percentsalaryhike = request.form["percentsalaryhike"]
    performancerating = request.form["performancerating"]
    totalworkingyears = request.form["totalworkingyears"]
    yearsatcompany = request.form["yearsatcompany"]
    yearsincurrentrole = request.form["yearsincurrentrole"]
    yearssincelastpromotion = request.form["yearssincelastpromotion"]
    yearswithcurrmanager = request.form["yearswithcurrmanager"]

    
    newlist = array([age,businesstravel,department,distancefromhome,education,educationfield,gender,jobinvolvment,joblevel,jobrole,jobsatisfaction,monthlyincome,monthlyrate,overtime,percentsalaryhike,performancerating,totalworkingyears,yearsatcompany,yearsincurrentrole,yearssincelastpromotion,yearswithcurrmanager])
    global algorithm_individual
    algorithm_individual = request.form["algorithm"]
    
    if algorithm_individual == 'K-Nearest Neighbors Algorithm':
        with open('knnclass_new','rb') as fw:
            classifier = pickle.load(fw)
        pred = classifier.predict([newlist])
        print("KNN")
    elif algorithm_individual == 'Support Vector Machine': 
        with open('svmpickle','rb') as fw:
            classifier = pickle.load(fw)
        pred = classifier.predict([newlist])
        print("SVM")
    elif algorithm_individual == 'Random Forest': 
        with open('randomforestpickle','rb') as fw:
            rfc = pickle.load(fw)
        pred = rfc.predict([newlist])   
        print("Random Forest")   
    elif algorithm_individual == 'Decision Tree':
        with open('decisiontreepickle','rb') as fw:
            tree_results = pickle.load(fw)
        pred = tree_results.predict([newlist]) 
        print("Decision Tree")

    pred = pred[0]
    
    
    # with open('knnclass_new','rb') as fw:
    #         classifier = pickle.load(fw)
    # pred = classifier.predict([newlist])
  

    return render_template("individual_predict.html",age=age,businesstravel=businesstravel
                            ,department=department,distancefromhome=distancefromhome,education=education,
                            educationfield=educationfield,gender=gender,jobinvolvment=jobinvolvment,
                            joblevel=joblevel,jobrole=jobrole,jobsatisfaction=jobsatisfaction,monthlyincome=monthlyincome,
                            monthlyrate=monthlyrate,overtime=overtime,percentsalaryhike=percentsalaryhike,performancerating=performancerating,
                            totalworkingyears=totalworkingyears,yearsatcompany=yearsatcompany,yearsincurrentrole=yearsincurrentrole,
                            yearssincelastpromotion=yearssincelastpromotion,yearswithcurrmanager=yearswithcurrmanager,algorithm_individual=algorithm_individual,pred=pred)

@app.route('/model_predict',methods=['GET','POST'])
def model_predict():

    if request.method == 'POST': 
        path = request.files["file1"]
    headernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition']
    df = pd.read_csv(path, names=headernames)
    
    businessTravel = {'Travel_Rarely': 1,'Travel_Frequently': 2,'Non-Travel':3}
    df.BusinessTravel = [businessTravel[item] for item in df.BusinessTravel]

    gender= {"Male": 1,"Female": 2}
    df.Gender = [gender[item] for item in df.Gender]

    abc= {"Sales":1, "Research & Development":2, "Human Resources":3}
    df.Department= [abc[item] for item in df.Department]

    edu= {"Medical":1, "Life Sciences":2, "Other":3,"Marketing":4,"Technical Degree":5,"Human Resources":6}
    df.EducationField= [edu[item] for item in df.EducationField]

    job= {"Sales Executive":1, "Research Scientist":2, "Laboratory Technician":3,"Healthcare Representative":4,"Manager":5, "Sales Representative":6,"Research Director":7,"Manufacturing Director":8,"Human Resources":9}
    df.JobRole= [job[item] for item in df.JobRole]

    over = {"Yes":1, "No":2}
    df.OverTime= [over[item] for item in df.OverTime]

    x=df.iloc[:,:-1].values
    y=df.iloc[:,21].values

    global algorithm
    algorithm = request.form["algo"]

    if algorithm == 'K-Nearest Neighbors Algorithm':
        with open('knnclass_new','rb') as fw:
            classifier = pickle.load(fw)
        pred = classifier.predict(x)
        print("KNN")
    elif algorithm == 'Support Vector Machine': 
        with open('svmpickle','rb') as fw:
            classifier = pickle.load(fw)
        pred = classifier.predict(x)
        print("SVM")
    elif algorithm == 'Random Forest': 
        with open('randomforestpickle','rb') as fw:
            rfc = pickle.load(fw)
        pred = rfc.predict(x)   
        print("Random Forest")   
    elif algorithm == 'Decision Tree':
        with open('decisiontreepickle','rb') as fw:
            tree_results = pickle.load(fw)
        pred = tree_results.predict(x)   
        print("Decision Tree")





    
   # for i in pred:
   #     print(i)
    
    # pred = {"No":0, "Yes":1}
    # df.Pred = [pred[item] for item in df.Pred]

    list1 = list(pred)
    # print(list1)
    # # array(list1)
    # se = pd.Series(list1)
    # df['Pred'] = se.values
    df['Predicted'] = np.array(list1)
    # businessTravel = {1 : 'Travel_Rarely',2 : 'Travel_Frequently',3 : 'Non-Travel'}
    # df.BusinessTravel = [businessTravel[item] for item in df.BusinessTravel]
    csv_data = df.to_csv(os.path.abspath("export_dataframe.csv"), index = False, header=True)
    
    businessTravel = {1 : 'Travel_Rarely',2 : 'Travel_Frequently',3 : 'Non-Travel'}
    df.BusinessTravel = [businessTravel[item] for item in df.BusinessTravel]


    csv_data = df.to_csv(os.path.abspath("export_dataframe_withvariable.csv"), index = False, header=True)
    # Data Visualization
   

    # yes=df.loc[df.Attrition == 'Yes','Attrition'].count()
    # no=df.loc[df.Attrition == 'No','Attrition'].count()

    # y = pd.DataFrame(y, columns = ['Attrition'])
    
    # y_yes=y.loc[y.Attrition == 'Yes','Attrition'].count()
    # y_no=y.loc[y.Attrition == 'No','Attrition'].count()


    # pred = pd.DataFrame(pred, columns = ['Attrition_Pred']) #Thik Karna he Attrition_pred to Predicted
    # pred_no=pred.loc[pred.Attrition_Pred == 'No','Attrition_Pred'].count()
    # pred_yes=pred.loc[pred.Attrition_Pred == 'Yes','Attrition_Pred'].count()


    # prediction= 'Yes','No'
    # datasetviz=[yes,no]
    # testviz=[y_yes,y_no]
    # predviz=[pred_yes,pred_no]


    newheadernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition','Predicted']

    

    data_frame = pd.read_csv(os.path.abspath("export_dataframe.csv"),names=newheadernames)
   
   


    stocklist = list(data_frame.values)
    global accuracy
    accuracy = round((accuracy_score(y,pred))*100,2)
    return render_template("view_new.html",stocklist=stocklist,accuracy=accuracy,algorithm=algorithm)

@app.route("/diagrams",methods=['GET','POST'])
def diagrams():
    # newheadernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
    #            'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
    #            'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
    #            'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition','Predicted']

    data_frame = pd.read_csv(os.path.abspath("export_dataframe.csv"))

    diagram = request.form["diagrams"]
    title = diagram

    if diagram == 'Bar' or diagram =='Line' :
        pd.crosstab(data_frame.Age,data_frame.Attrition).plot(kind=title)
        plt.title("Age Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\age_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.Age,data_frame.Predicted).plot(kind=title)
        plt.title("Age Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\age_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.BusinessTravel,data_frame.Attrition).plot(kind=title)
        plt.title("BusinessTravel Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\business_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.BusinessTravel,data_frame.Predicted).plot(kind=title)
        plt.title("BusinessTravel Vs  Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\business_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.Department,data_frame.Attrition).plot(kind=title)
        plt.title("Department Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\depart_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.Department,data_frame.Predicted).plot(kind=title)
        plt.title("Department Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\depart_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.DistanceFromHome,data_frame.Attrition).plot(kind=title)
        plt.title("DistanceFromHome Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\dist_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.DistanceFromHome,data_frame.Predicted).plot(kind=title)
        plt.title("DistanceFromHome Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\dist_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.Education,data_frame.Attrition).plot(kind=title)
        plt.title("Education Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edu_vs_attriton.png"))
        plt.clf()
        pd.crosstab(data_frame.Education,data_frame.Predicted).plot(kind=title)
        plt.title("Education Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edu_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.EducationField,data_frame.Attrition).plot(kind=title)
        plt.title("EducationField Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edufield_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.EducationField,data_frame.Predicted).plot(kind=title)
        plt.title("EducationField Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edufield_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.Gender,data_frame.Attrition).plot(kind=title)
        plt.title("Gender Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\gender_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.Gender,data_frame.Predicted).plot(kind=title)
        plt.title("Gender Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\gender_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobInvolvement,data_frame.Attrition).plot(kind=title)
        plt.title("JobInvolvement Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobinvolve_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobInvolvement,data_frame.Predicted).plot(kind=title)
        plt.title("JobInvolvement Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobinvolve_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobLevel,data_frame.Attrition).plot(kind=title)
        plt.title("JobLevel Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\joblevel_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobLevel,data_frame.Predicted).plot(kind=title)
        plt.title("JobLevel Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\joblevel_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobRole,data_frame.Attrition).plot(kind=title)
        plt.title("JobRole Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobrole_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobRole,data_frame.Predicted).plot(kind=title)
        plt.title("JobRole Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobrole_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobSatisfaction,data_frame.Attrition).plot(kind=title)
        plt.title("JobSatisfaction Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobsatisfy_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobSatisfaction,data_frame.Predicted).plot(kind=title)
        plt.title("JobSatisfaction Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobsatisfy_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.OverTime,data_frame.Attrition).plot(kind=title)
        plt.title("OverTime Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\overtime_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.OverTime,data_frame.Predicted).plot(kind=title)
        plt.title("OverTime Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\overtime_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.PercentSalaryHike,data_frame.Attrition).plot(kind=title)
        plt.title("PercentSalaryHike  Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\percenthike_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.PercentSalaryHike,data_frame.Predicted).plot(kind=title)
        plt.title("PercentSalaryHike  Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\percenthike_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.PerformanceRating,data_frame.Attrition).plot(kind=title)
        plt.title("PerformanceRating Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\perform_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.PerformanceRating,data_frame.Predicted).plot(kind=title)
        plt.title("PerformanceRating Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\perform_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsInCurrentRole,data_frame.Attrition).plot(kind=title)
        plt.title("YearsInCurrentRole Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\yearsincurrrole_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsInCurrentRole,data_frame.Predicted).plot(kind=title)
        plt.title("YearsInCurrentRole Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\yearsincurrrole_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsSinceLastPromotion,data_frame.Attrition).plot(kind=title)
        plt.title("YearsSinceLastPromotion Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\lastpromotion_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsSinceLastPromotion,data_frame.Predicted).plot(kind=title)
        plt.title("YearsSinceLastPromotion Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\lastpromotion_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsWithCurrManager,data_frame.Attrition).plot(kind=title)
        plt.title("YearsWithCurrentManager Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\currmanager_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsWithCurrManager,data_frame.Predicted).plot(kind=title)
        plt.title("YearsWithCurrentManager Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\currmanager_vs_pred.png"))
        plt.clf()
        


        
    elif diagram == 'Stacked Bar':
        pd.crosstab(data_frame.Age,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("Age Vs Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\age_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.Age,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("Age Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\age_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.BusinessTravel,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("BusinessTravel Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\business_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.BusinessTravel,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("BusinessTravel Vs  Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\business_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.Department,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("Department Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\depart_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.Department,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("Department Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\depart_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.DistanceFromHome,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("DistanceFromHome Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\dist_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.DistanceFromHome,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("DistanceFromHome Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\dist_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.Education,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("Education Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edu_vs_attriton.png"))
        plt.clf()
        pd.crosstab(data_frame.Education,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("Education Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edu_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.EducationField,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("EducationField Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edufield_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.EducationField,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("EducationField Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\edufield_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.Gender,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("Gender Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\gender_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.Gender,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("Gender Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\gender_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobInvolvement,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("JobInvolvement Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobinvolve_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobInvolvement,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("JobInvolvement Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobinvolve_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobLevel,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("JobLevel Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\joblevel_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobLevel,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("JobLevel Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\joblevel_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobRole,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("JobRole Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobrole_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobRole,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("JobRole Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobrole_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.JobSatisfaction,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("JobSatisfaction Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobsatisfy_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.JobSatisfaction,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("JobSatisfaction Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\jobsatisfy_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.OverTime,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("OverTime Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\overtime_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.OverTime,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("OverTime Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\overtime_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.PercentSalaryHike,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("PercentSalaryHike  Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\percenthike_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.PercentSalaryHike,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("PercentSalaryHike  Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\percenthike_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.PerformanceRating,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("PerformanceRating Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\perform_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.PerformanceRating,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("PerformanceRating Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\perform_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsInCurrentRole,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("YearsInCurrentRole Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\yearsincurrrole_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsInCurrentRole,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("YearsInCurrentRole Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\yearsincurrrole_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsSinceLastPromotion,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("YearsSinceLastPromotion Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\lastpromotion_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsSinceLastPromotion,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("YearsSinceLastPromotion Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\lastpromotion_vs_pred.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsWithCurrManager,data_frame.Attrition).plot.bar(stacked=True)
        plt.title("YearsWithCurrentManager Vs Observed Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\currmanager_vs_attrition.png"))
        plt.clf()
        pd.crosstab(data_frame.YearsWithCurrManager,data_frame.Predicted).plot.bar(stacked=True)
        plt.title("YearsWithCurrentManager Vs Predicted Attrition",fontsize=16)
        plt.savefig(os.path.abspath("static\\currmanager_vs_pred.png"))
        plt.clf()



    return render_template("diagrams.html",diagram=diagram)



@app.route("/prediction",methods=['GET','POST'])
def prediction():
    newheadernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition','Predicted']

    data_frame = pd.read_csv(os.path.abspath("export_dataframe.csv"),names=newheadernames)

    x=data_frame.iloc[1:,:-2].values
    y=data_frame.iloc[1:,-2:].values
    abc=y

    

    x = pd.DataFrame(x, columns = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager'])
    
    y = pd.DataFrame(y, columns=['Attrition','Predicted'])
    
    predict = request.form["predicted"]

    if predict == 'Yes':
        x_new =x.loc[y.Predicted == 'Yes']
        pred=y.loc[y.Predicted == 'Yes','Predicted'].count()
        actual=y.loc[y.Attrition == 'Yes','Attrition'].count()
        print("Yes")
    elif predict == 'No':
        x_new =x.loc[y.Predicted == 'No']
        pred=y.loc[y.Predicted == 'No','Predicted'].count()
        actual=pred_yes=y.loc[y.Attrition == 'No','Attrition'].count()
        print("No")
    # elif predict == 'reason':
    #     age = x['Age'] > '30'
    #     depart=x['Department']== '2'
    #     pre=y['Predicted'] == 'Yes'
    #     over=x['OverTime']== '1'
    
    #     x_new=x[age & depart & pre & over]
    #     print(x_new)
    #     new=len(x_new)

    x_new = list(x_new.values)
    abc = list(abc)
   
    count = 0
    for i in abc:
        if i[0] == predict:
            if i[0] == i[1]:
                count+=1
    match=count
            
        
    return render_template("prediction.html",x_new=x_new,pred=pred,predict=predict,actual=actual,match=match)

@app.route("/reasons",methods=['GET','POST'])
def reasons():
    newheadernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition','Predicted']

    data_frame = pd.read_csv(os.path.abspath("export_dataframe.csv"))

    x=data_frame.iloc[0:,:-2].values
    y=data_frame.iloc[0:,-2:].values
    abc=y

    x = pd.DataFrame(x, columns = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager'])
    
    y = pd.DataFrame(y, columns=['Attrition','Predicted'])

    

    reason = request.form["reasons"]
    if reason == 'Over Time':
        pre=y['Predicted'] == 'Yes'
        over=x['OverTime']== 1
        x_new=x[ pre & over]
        x_new = list(x_new.values)
        count = len(x_new)
      
    
    elif reason == 'Distance From Home':
        dist = x['DistanceFromHome'] > 3
        pre = y['Predicted']=='Yes'
        x_new=x[ pre & dist]
        x_new = list(x_new.values)
        count = len(x_new)

    elif reason == 'Job Satisfaction':
        satisfy = x['JobSatisfaction'] <= 3
        pre = y['Predicted'] == 'Yes'
        x_new=x[pre & satisfy]
        x_new = list(x_new.values)
        count = len(x_new)

    elif reason == 'All':
        pre=y['Predicted'] == 'Yes'
        over=x['OverTime']== 1
        x1=x[ pre & over]
        dist = x['DistanceFromHome'] > 3
        x2=x[ pre & dist]
        satisfy = x['JobSatisfaction'] <= 3
        x3=x[pre & satisfy]
        x4=x[pre & dist & over | pre & satisfy & over | pre & dist & satisfy]
        print("ALL")
        count1 = len(x1)
        count2 = len(x2)
        count3=len(x3)
        count4=len(x4)
        x1 = list(x1.values)
        x2 = list(x2.values)
        x3 = list(x3.values)    
        x4 = list(x4.values)
        x_new = [x1,x2,x3,x4]
        count = [count1,count2,count3,count4]
        reason = ['Over Time','Distance From Home','Job Satisfaction','Two Or More Reasons']
        
    
   
    return render_template("reasons.html",x_new=x_new,count=count,reason=reason)

@app.route("/trail",methods=['GET','POST'])
def trail():
    newheadernames = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager','Attrition','Predicted']

    data_frame = pd.read_csv(os.path.abspath("export_dataframe.csv"))

    x=data_frame.iloc[0:,:-2].values
    y=data_frame.iloc[0:,-2:].values
   
    # abc=y

    x = pd.DataFrame(x, columns = ['Age','BusinessTravel','Department','DistanceFromHome','Education','EducationField',
               'Gender','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MonthlyIncome','MonthlyRate',
               'OverTime','PercentSalaryHike','PerformanceRating','TotalWorkingYears','YearsAtCompany',
               'YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager'])
    
    y = pd.DataFrame(y, columns=['Attrition','Predicted'])

    reason1 = request.form["trail"]
    compare1 = request.form["compare"]
    num = request.form["numbercount"]
    pred = y['Predicted'] == 'Yes'
    # pred = x.loc[y.Predicted == 'Yes']
    print(pred)
    print(reason1)
    print(num)
   

    if compare1 == 'Greater Than':
        print(type(num))
        individualreason = x[reason1] > int(num) 

    elif compare1 == 'Less Than':
        individualreason = x[reason1] < int(num) 
    
    elif compare1 == 'Equal to':
        individualreason = x[reason1] == int(num) 
    
    newabc = x[pred & individualreason]
    print(newabc)
    count = len(newabc)
    newabc = list(newabc.values)
    

    return render_template("trail.html",newabc=newabc,reason1=reason1,compare1=compare1,num=num,count=count)



if __name__ == '__main__':
    app.run(debug=True,threaded=False)
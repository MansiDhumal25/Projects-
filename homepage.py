from flask import Flask,render_template,request,session,redirect,url_for
from flask_mysqldb import MySQL 
from datetime import date
import string
import random
import pymsgbox

app = Flask(__name__,template_folder= "template")

app.secret_key="aniket123"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='aniket@123'
app.config['MYSQL_DB']='project'

mysql=MySQL(app)

@app.route('/')
def homepage():
   return render_template('homepage.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/addpsychologist',methods=['GET','POST'])
def addpsychologist():
	if request.method=='POST':
		fname=request.form['fname']
		lname=request.form['lname']
		email=request.form['email']
		phoneno=request.form['phoneno']
		pswd=request.form['pswd']
		gender=request.form['gender']
		qualification=request.form['qualification']
		experience=request.form['experience']
		uid=id_generator()		
		cur= mysql.connection.cursor()
		cur.execute("insert into user values(%s,%s,%s)",[uid,email,pswd])
		cur.connection.commit()
		cur.execute("insert into therapist values(%s,%s,%s,%s,%s,%s,%s)",[fname,lname,gender,qualification,experience,phoneno,uid])
		cur.connection.commit()	
		cur.close()
		pymsgbox.alert('Psychologist Added Successfully','Title')
		return redirect(url_for("admin"))		
	return render_template('psychologist.html')

@app.route('/psychologicaltest',methods=['GET','POST'])
def test1():
	cur= mysql.connection.cursor()
	cur.execute("select question_description from psychotest;")
	res=cur.fetchall()
	if "pscore" in session:
		session.pop("pscore",None)

	if request.method=='POST':		
		Q=["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15","Q16","Q17","Q18"]
		pscore=0
		for i in Q:
			a=int(request.form[i])
			pscore=pscore+a			
		uid=session['uid']
		cur.execute("insert into client_test values(%s,%s,%s)",[uid,1,pscore])
		cur.connection.commit()	
		cur.close()
		session['pscore']=pscore
		return redirect(url_for("test2"))
	return render_template('test1.html',rs=res,content_type='application/json')

@app.route('/IQtest',methods=['GET','POST'])
def test2():
	cur= mysql.connection.cursor()
	cur.execute("select question_description,option1,option2,option3,option4 from iqtest;")
	res=cur.fetchall()
	cur.execute("select correct_answer from iqtest;")
	res1=cur.fetchall()
	if "iqscore" in session:
		session.pop("iqscore",None)

	if request.method=='POST':
		iqscore=0
		ans=[]
		Q=["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q10","Q11","Q12","Q13","Q14","Q15"]
		for i in Q:
			if request.form.get(str(i)) is None:
				ans.append(0)
			else:
				Q1=request.form[str(i)]
				ans.append(Q1) 
		for j in range(0,15):
			if ans[j]==res1[j][0] and ans[j]!=0:
				iqscore=iqscore+1
			else:
				iqscore=iqscore+0
		uid=session['uid']
		cur.execute("insert into client_test values(%s,%s,%s)",[uid,2,iqscore])
		cur.connection.commit()	
		cur.close()
		session['iqscore']=iqscore
		return redirect(url_for("result"))
	return render_template('test2.html',rs=res,content_type='application/json')

def id_generator(size=6,chars=string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method=='POST':
		fname=request.form['fname']
		mname=request.form['mname']
		lname=request.form['lname']
		email=request.form['email']
		phoneno=request.form['phoneno']
		pswd=request.form['pswd']
		DOB=request.form['DOB']
		gender=request.form['gender']
		question=request.form['question']
		answer=request.form['answer']
		uid=id_generator()		
		cur= mysql.connection.cursor()
		cur.execute("select EXISTS(select email from user where email=%s)",[email])
		res=cur.fetchone()
		if res[0]==0:
			cur.execute("insert into user values(%s,%s,%s)",[uid,email,pswd])
			cur.connection.commit()
			cur.execute("insert into client values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[fname,lname,mname,gender,question,answer,phoneno,DOB,uid])
			cur.connection.commit()	
			cur.close()
			return redirect(url_for("login"))
		else:
			pymsgbox.alert('Email id already Registered')
			return redirect(url_for("login"))		
	return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		email=request.form['email']
		pswd=request.form['pswd']
		if email=="aniketkudale2805@gmail.com" and pswd=="aniket2805":
			session['email']=email			
			return redirect(url_for("admin"))
		else:
			cur= mysql.connection.cursor()
			cur.execute("select uid from user where email=%s and pswd=%s",[email,pswd])	
			uid=cur.fetchone()
			if uid==None:
				pymsgbox.alert('User not Found','Title')
				return redirect(url_for("login"))
			else:	
				cur.execute("select EXISTS(select uid from client where uid=%s)",[uid])
				res=cur.fetchone()
				cur.execute("select EXISTS(select uid from therapist where uid=%s)",[uid])
				res1=cur.fetchone()
				if res[0]==1 and res1[0]==0:
					cur.execute("select fname from client where uid=%s",[uid])
					f=cur.fetchone()
					fname=f[0]
					session['fname']=fname
					session['uid']=uid
					session['client']=True
					cur.close()
					return redirect(url_for("homepage"))
				elif res[0]==0 and res1[0]==1:
					cur.execute("select fname from therapist where uid=%s",[uid])
					f=cur.fetchone()
					fname=f[0]
					session['fname']=fname
					session['uid']=uid
					session['therapist']=True
					cur.close()
					return redirect(url_for("homepage"))
	return render_template("login.html")
		
@app.route('/forgetpswd',methods=['GET','POST'])
def forgetpswd():
	if request.method=='POST':
		email=request.form['email']
		question=request.form['question']
		answer=request.form['answer']
		newpswd=request.form['newpswd']
		cur= mysql.connection.cursor()
		cur.execute("select uid from user natural join client where email=%s and security_question=%s and answer=%s",[email,question,answer])	
		uid=cur.fetchone()
		cur.execute("update user set pswd=%s where uid=%s",[newpswd,uid])
		cur.connection.commit()
		cur.close()
		return redirect(url_for("login"))
	return render_template('forgetpswd.html')
    
@app.route('/changepswd',methods=['GET','POST'])
def changepswd():
	if request.method=='POST':
		email=request.form['email']
		oldpswd=request.form['oldpswd']
		newpswd=request.form['newpswd']
		cur= mysql.connection.cursor()
		cur.execute("select uid from user where email=%s and pswd=%s",[email,oldpswd])	
		uid=cur.fetchone()
		if uid==None:
			pymsgbox.alert('User Not Found','Title')
			cur.close()
			return redirect(url_for("changepswd"))
		else:
			cur.execute("update user set pswd=%s where uid=%s",[newpswd,uid])
			cur.connection.commit()
			pymsgbox.alert('Password Changed Successfully','Title')
			cur.close()
			return redirect(url_for("homepage"))
	return render_template('changepswd.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/help')
def help():
	cur= mysql.connection.cursor()
	cur.execute("select uid,fname,lname from therapist;")
	res=cur.fetchall()
	l=len(res)
	cur.close()		
	return render_template('help.html',rs=res,length=l,content_type='application/json')

@app.route('/messages')
def messages():
	names=[]
	uid=session['uid']
	cur= mysql.connection.cursor()
	cur.execute("select uid,msg_desc,date(datetime),Time(datetime) from message where reciever=%s;",[uid])
	res=cur.fetchall()
	length=len(res)
	for i in range(length):
		cur.execute("select fname from client where uid=%s UNION select fname from therapist where uid=%s;",[res[i][0],res[i][0]])
		names.append(cur.fetchone())	
	cur.close()		
	return render_template('message.html',rs=res,fname=names,j=length,content_type='application/json')

@app.route('/chat/<to>',methods=['GET','POST'])
def chat(to):
	if request.method=='POST':
		To=to
		message=request.form['message']
		cur= mysql.connection.cursor()
		cur.execute("select uid from therapist where fname=%s UNION select uid from client where fname=%s;",[To,To])
		res=cur.fetchone()
		reciever=res[0]
		uid=session['uid']
		msgid=id_generator()		
		cur.execute("insert into message values(%s,%s,%s,%s,now())",[msgid,uid,message,reciever])
		cur.connection.commit()
		cur.close()		
		pymsgbox.alert('Message Sent','Title')
		return redirect(url_for("messages"))
	return render_template('chat.html',To=to)

@app.route('/result',methods=['GET','POST'])
def result():
	cur= mysql.connection.cursor()
	cur.execute("select uid,fname,lname from therapist;")
	res=cur.fetchall()
	l=len(res)
	cur.close()		
	return render_template('result.html',rs=res,length=l,content_type='application/json')

@app.route('/editprofile',methods=['GET','POST'])
def editprofile():
	if request.method=='POST':
		fname=request.form['fname']
		mname=request.form['mname']
		lname=request.form['lname']
		email=request.form['email']
		phoneno=request.form['phoneno']
		pswd=request.form['pswd']
		DOB=request.form['DOB']
		gender=request.form['gender']
		question=request.form['question']
		answer=request.form['answer']		
		cur= mysql.connection.cursor()
		uid=session['uid']
		cur.execute("update user set email=%s,pswd=%s where uid=%s",[email,pswd,uid])
		cur.connection.commit()
		cur.execute("update client set fname=%s,lname=%s,mname=%s,gender=%s,security_question=%s,answer=%s,phone_number=%s,dob=%s where uid=%s",[fname,lname,mname,gender,question,answer,phoneno,DOB,uid])
		cur.connection.commit()
		cur.close()
		pymsgbox.alert('Profile Updated Successfully','Title')
		return redirect(url_for("homepage"))		    
	return render_template('editprofile.html')

@app.route('/logout')
def logout():
	if "email" in session:
		session.pop("email",None)
	if "uid" in session:
		session.pop("uid",None)
	return render_template('homepage.html')

if __name__ == "__main__":
	app.run(debug=True)

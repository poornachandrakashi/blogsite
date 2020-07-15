from flask import Flask,render_template,flash,url_for,redirect,session,logging,request
from data import Articles
# from flask_mysqldb import MySQL
# from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import mysql.connector

app=Flask(__name__)

#Config Mysql
mydb=mysql.connector.connect(host='localhost',user="poonra",passwd="poorna1999",database="myflaskapp")

#Initializing Mysql
# mysql=MySQL(app)


Articles=Articles()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/articles')
def articles():
    return render_template('articles.html',articles=Articles)
    
@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html',id=id)

# class RegisterForm(Form):
#     name= StringField('Name', [validators.Length(min=1,max=50)])
#     username=StringField('Username',[validators.Length(min=5,max=25)])
#     email=StringField('Email',[validators.Length(min=6,max=50)])
#     password=PasswordField('Password',[
#         validators.DataRequired(),
#         validators.EqualTo('confirm',message="Password do not match")
#     ])
#     confirm=PasswordField('Confirm Password')
    
@app.route('/register' ,methods=['GET','POST'])
def register():
    # form=RegisterForm()
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        
        # Creating Cursor
        cur=mydb.cursor()
        
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s )",(name,email,username,password))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        flash("Your are not registered and can log in","success")
        
        redirect('/index')
        # return form.email.data
        return render_template('register.html')
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #Geeting the form field
        username=request.form.get('username')
        password_candidate=request.form.get('password')
        
        #Create Cursor
        cur=mydb.cursor(buffered=True)

        #Get user by username
        try:
            cur.execute("select * from users where username = %s",[username])
        
            
        
        if user==username:
            #Getting the stored hashed
            data=cur.fetchone()
            password=data[4]
            #Comparing the password
            if password_candidate==password:
                app.logger.info('Password Matched')
                flash("Password matched")
            else:
                app.logger.info("Password not matched")
                flash("password not matched")
        else:
            
            app.logger.info("No User")
    return render_template('login.html')
            
if __name__=='__main__':
    app.secret_key='poorna1999'
    app.run(debug=True)
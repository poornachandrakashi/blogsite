from flask import Flask,render_template,flash,url_for,redirect,session,logging,request
# from data import Articles
# from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import mysql.connector
from functools import wraps

app=Flask(__name__)

#Config Mysql
mydb=mysql.connector.connect(host='localhost',user="root",passwd="",database="blogdb")

#Initializing Mysql
# mysql=MySQL(app)


# Articles=Articles()


#Homepage
@app.route('/')
def home():
    return render_template('home.html')

#About Page
@app.route('/about')
def about():
    return render_template('about.html')

#Articles fetch page    
@app.route('/articles')
def articles():
    cur=mydb.cursor()
    #Get Articles
    result= cur.execute('SELECT * FROM articles')
    
    articles=cur.fetchall()
    # if result > 0:
    #     return render_template('dashboard.html', articles=articles)
    # else:
    #     msg = 'No Articles Found'
    #     return render_template('dashboard.html', msg=msg)
        
    
    return render_template('articles.html',articles=articles)  
    #Close Connection
    cur.close()  
    
#Fetching particular article
@app.route('/article/<string:id>')
def article(id):
    cur = mydb.cursor()
    
    # Get article
    
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchall()

    return render_template('article.html', article=article)
    cur.close()
# class RegisterForm(Form):
#     name= StringField('Name', [validators.Length(min=1,max=50)])
#     username=StringField('Username',[validators.Length(min=5,max=25)])
#     email=StringField('Email',[validators.Length(min=6,max=50)])
#     password=PasswordField('Password',[
#         validators.DataRequired(),
#         validators.EqualTo('confirm',message="Password do not match")
#     ])
#     confirm=PasswordField('Confirm Password')
    
    
#Registration
@app.route('/register' ,methods=['GET','POST'])
def register():
    # form=RegisterForm()
    if request.method=='POST':
        name=request.form.get('name')
        family=request.form.get('fname')
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        dob=request.form.get('dob')
        gender=request.form.get('gender')
        father=request.form.get('father')
        mother=request.form.get('mother')
        gotra=request.form.get('gotra')
        marraige=request.form.get('marraige')
        children=request.form.get('children')
        phone=request.form.get('phone')
        address=request.form.get('address')
        
        # Creating Cursor
        cur=mydb.cursor()
        
        cur.execute("INSERT INTO directory(name,family,email,username,password,dob,gender,father,mother,gotra,marraige,children,phone,address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )",(name,family,email,username,password,dob,gender,father,mother,gotra,marraige,children,phone,address))
        
        #Commit to db
        mydb.commit()
        
        #close Connection
        cur.close()
        
        flash("Your are not registered and can log in","success")
        
        redirect('/index')
        # return form.email.data
        return render_template('register.html')
    return render_template('register.html')

@app.route('/test')
def test():
    return render_template('register2.html')

#Login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        #Geeting the form field
        username=request.form.get('username')
        password_candidate=request.form.get('password')
        
        #Create Cursor
        cur=mydb.cursor(buffered=True)

        #Get user by username
        
        result=cur.execute("select * from directory where username = %s",[username])
        
        if result == None:
            #Getting the stored hashed
            data=cur.fetchone()
            password=data[4]
            #Comparing the password
            if password_candidate==password:
                session['logged_in']=True
                session['username']=username
                flash("Congrats you are logged in")
                return redirect('/dashboard')
                app.logger.info('Password Matched')
                
            else:
                app.logger.info("Password not matched")
                error="Invalid login"
                flash("password not matched")
                return render_template('login.html',error=error)
            #Close connection
            cur.close()
        else:
            app.logger.info("No User")
            flash("No user found")
            return render_template('login.html',error=error)
    return render_template('login.html')


#Article validation
class ArticleForm(Form):
    title = StringField('title', [validators.Length(min=1, max=200)])
    body = StringField('body', [validators.Length(min=30)])
    
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap



#Adding articles    
@app.route('/add_article',methods=['POST','GET'])
def add_article():
    # form=ArticleForm(request.form)
    if request.method=='POST':
        title=request.form.get('title')
        body=request.form.get('body')
        
        #Create cursor
        cur=mydb.cursor()
        
        #Execute
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)",(title,body,session["username"]))
        #commit
        mydb.commit()
        
        #close connection
        cur.close()
        
        flash('Article Created','Success')
        
        return redirect('/dashboard')
    return render_template('add_article.html')


#Editing articles    
@app.route('/edit_article/<string:id>',methods=['POST','GET'])
def edit_article(id):
    
    #Create Cursor
    cur=mydb.cursor()
    
    #Get article by id
    result=cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    
    article = cur.fetchall()
    
    cur.close()
    
    
    
    form=ArticleForm(request.form)
    
    #Populate the article
    form.title.data = article[0][1]
    form.body.data = article[0][3]
    
    if request.method=='POST' and form.validate():
        title=request.form['title']
        body=request.form['body']
        
        #Create cursor
        cur=mydb.cursor()
        
        #Execute
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        #commit
        mydb.commit()
        
        #close connection
        cur.close()
        
        flash('Article Updated','Success')
        
        return redirect('/dashboard')
    return render_template('edit_article.html',form=form)


#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("Successfully Logged out!!!")
    return redirect('/login')


#Users dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    #Create cursor
    
    cur=mydb.cursor()
    #Get Articles
    result= cur.execute('SELECT * FROM articles')
    
    articles=cur.fetchall()
    # if result > 0:
    #     return render_template('dashboard.html', articles=articles)
    # else:
    #     msg = 'No Articles Found'
    #     return render_template('dashboard.html', msg=msg)
        
    
    return render_template('dashboard.html',articles=articles)  
    #Close Connection
    cur.close()  



#Delete Article
@app.route('/delete_article/<string:id>',methods=['POST'])
@is_logged_in
def delete_article(id):
    #Creating cursor
    cur = mydb.cursor()
    
    #Execute cursor
    cur.execute("DELETE FROM articles WHERE id=%s",[id])
    
    mydb.commit()
    
    cur.close()
    
    flash('Article Deleted','success')
    
    return redirect('/dashboard')
          
#App Run 
if __name__=='__main__':
    app.secret_key='poorna1999'
    app.run(debug=True)
from flask import Flask, render_template, request,redirect, session
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)

main_email = ''

app.secret_key = 'admin'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "squad.runtimeterror@gmail.com",
    MAIL_PASSWORD = "RUNTIMEterror"
)
mail = Mail(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@127.0.0.1:3307/RuntimeTerror"
db = SQLAlchemy(app)

class Register(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(10), nullable=False)
    l_name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(10), nullable=True)

class ContactMe(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    message = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=True)

class gmail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=True)
    s_email = db.Column(db.String(20), nullable=True)
    r_email = db.Column(db.String(15), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=True)

class youtube(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=True)
    search = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=True)

class Pixel(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(10), nullable=True)
    model = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(10), nullable=True)

class Map(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(10), nullable=True) 
    start = db.Column(db.String(10), nullable=True)
    dest = db.Column(db.String(10), nullable=True)
    mode = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(10), nullable=True)

class translate(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(10), nullable=True)
    format = db.Column(db.String(10), nullable=True)
    date = db.Column(db.String(10), nullable=True)

class ytmusic(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(10), nullable=True)
    search = db.Column(db.String(10), nullable=True)
    date = db.Column(db.String(10), nullable=True)

class ads(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(10), nullable=True)
    name = db.Column(db.String(10), nullable=True)
    date = db.Column(db.String(10), nullable=True)



@app.route('/', methods = ['GET', 'POST'])
def home():
    x = ['squad.runtimeterror@gmail.com']
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = ContactMe(name = name, email = email, phone = phone, message = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name, sender=email, recipients=x, body=message + '\n' + email + '\n' + phone)
        return render_template('contact.html')
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        con_password= request.form.get('con_password')
        if((len(f_name) and len(l_name) and len(email) and len(phone) and len(password)!= 0) and (password==con_password)):
            entry = Register(f_name = f_name, l_name=l_name, email = email, phone = phone, password=password, date = datetime.now())
            db.session.add(entry)
            db.session.commit()
            return render_template('registersuccess.html')
        else:
            return render_template('registererror.html')
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users=youtube.query.filter_by(email=email)
        yts=ytmusic.query.filter_by(email=email)
        maps=Map.query.filter_by(email=email)
        gms=gmail.query.filter_by(s_email=email)
        trs=translate.query.filter_by(email=email)
        a_s=ads.query.filter_by(email=email)
        user = Register.query.filter_by(email=email).first()
        if 'client' in session and session['client'] == email:
            return render_template('home.html',user=user,users=users,yts=yts,gms=gms,trs=trs,a_s=a_s,maps=maps)

        try:
            if user.email == email and user.password == password:
                session['client'] = email

                return render_template('home.html',user=user,users=users,yts=yts,gms=gms,trs=trs,a_s=a_s,maps=maps)
            else:
                return render_template('loginerror.html')
        except:  return render_template('loginerror.html')

    return render_template('login.html')

@app.route('/contact', methods=['GET', 'POST'])
def Contact():
    return render_template('index.html')

@app.route('/gmailservice', methods=['GET', 'POST'])
def gmailservice():
    if request.method == 'POST':
        name=Register.query.filter_by(email=session['client']).first().f_name
        s_email=session['client']
        
        r_email = request.form.get('r_email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = gmail( name=name,s_email=s_email,r_email = r_email, subject=subject, message = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return render_template('gmailsuccess.html')
    return render_template('gmail.html')

@app.route('/youtubeservice', methods=['GET', 'POST'])
def youtubeservice():
    if request.method == 'POST':
        email=Register.query.filter_by(email=session['client']).first().email

        # email = request.form.get('email')
        search = request.form.get('search')
        entry = youtube( email = email, search=search,date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect("https://www.youtube.com/results?search_query="+str(search), code = 302)

    return render_template('ytlogin.html')

@app.route('/pixel', methods=['GET', 'POST'])
def pixel():
    if request.method == 'POST':
        email=Register.query.filter_by(email=session['client']).first().email
        model= request.form.get('model')
        entry = Pixel( email=email,model=model,date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect("https://store.google.com/in/magazine/compare_pixel", code = 302)

    return render_template('pixel.html')

@app.route('/mapservice', methods=['GET', 'POST'])
def mapservice():
    if request.method == 'POST':
        email=Register.query.filter_by(email=session['client']).first().email

        start = request.form.get('start')
        dest = request.form.get('dest')
        mode = request.form.get('mode')
        entry = Map(email=email, start = start, dest=dest, mode=mode,date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect("https://www.google.co.in/maps/dir/"+str(start)+"/"+str(dest), code = 302)

    return render_template('map.html')

@app.route('/translateservice', methods=['GET', 'POST'])
def translateservice():
    if request.method == 'POST':
        email=Register.query.filter_by(email=session['client']).first().email

        # email = request.form.get('email')
        format = request.form.get('format')
        if format == 'txt':
            format = 'translate'
        else:
            format = "docs"
        entry = translate( email = email, format=format, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect("https://translate.google.com/#view=home&op="+str(format)+"&sl=auto&tl=en", code = 302)

    return render_template('translate.html')

@app.route('/ytmusicservice', methods=['GET', 'POST'])
def ytmusicservice():
    if request.method == 'POST':
        email=Register.query.filter_by(email=session['client']).first().email

        # email = request.form.get('email')
        search = request.form.get('search')
        entry = ytmusic( email = email, search=search,date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect("https://music.youtube.com/search?q="+str(search), code = 302)

    return render_template('ytmusic.html')

@app.route('/adservice', methods=['GET', 'POST'])
def adservice():
    if request.method == 'POST':
        email=Register.query.filter_by(email=session['client']).first().email
        #email = request.form.get('email')
        name = request.form.get('name')
        entry = ads( email = email, name=name, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        return redirect("https://ads.google.com/intl/en_in/home/", code = 302)

    return render_template('ad.html')



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == 'admin':
        users = Register.query.all()
        gmails=gmail.query.all()
        youtubes=youtube.query.all()
        maps=Map.query.all()
        translates=translate.query.all()
        ytmusics=ytmusic.query.all()
        adss=ads.query.all()
        # posts=P.query.all()
        return render_template('dashboard.html', users=users,gmails=gmails, youtubes=youtubes, maps=maps, translates=translates, ytmusics=ytmusics, adss=adss)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = Register.query.all()
        gmails=gmail.query.all()
        youtubes=youtube.query.all()
        maps=Map.query.all()
        translates=translate.query.all()
        ytmusics=ytmusic.query.all()
        adss=ads.query.all()
        if username == 'admin' and password == 'admin':
            session['user'] = username
            return render_template('dashboard.html', users=users,gmails=gmails, youtubes=youtubes, maps=maps, translates=translates, ytmusics=ytmusics, adss=adss)
    return render_template('adminlogin.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route('/clientlogout')
def clientlogout():
    session.pop('client')
    main_email = ''
    return redirect('/')

app.run(debug=True)
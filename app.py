from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_musicalinstrument", methods=["GET","POST"])
def add_one_musicalinstrument():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into musicalinstrument (name) values (:name)",hey)
        user = query_db('select * from musicalinstrument')

        return render_template("musicalinstrumentform.html", musicalinstruments=user, one_user=one_user, the_title="add new musicalinstrument")


    user = query_db('select * from musicalinstrument')
    one_user = query_db("select * from musicalinstrument limit 1", one=True)
    return render_template("musicalinstrumentform.html", musicalinstruments=user, one_user=one_user, the_title="add new musicalinstrument")

@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,password,phone,email,country_id,pic) values (:username,:password,:phone,:email,:country_id,:pic)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','password','phone','email','country_id','pic']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','password','phone','email','country_id','pic']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','password','phone','email','country_id','pic']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_score", methods=["GET","POST"])
def add_one_score():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesmusicalinstrument= query_db("select * from musicalinstrument")

        one_user = query_db("insert into score (title,composer,bpm,caractere,key_signature,time_signature,content,musicalinstrument_id) values (:title,:composer,:bpm,:caractere,:key_signature,:time_signature,:content,:musicalinstrument_id)",hey)
        user = query_db('select * from score')

        return render_template("scoreform.html", scores=user, one_user=one_user, the_title="add new score", touslesmusicalinstrument=touslesmusicalinstrument)


    touslesmusicalinstrument= query_db("select * from musicalinstrument")

    user = query_db('select * from score')
    one_user = query_db("select * from score limit 1", one=True)
    return render_template("scoreform.html", scores=user, one_user=one_user, the_title="add new score", touslesmusicalinstrument=touslesmusicalinstrument)

@app.route("/add_one_scorehaslogic_post", methods=["GET","POST"])
def add_one_scorehaslogic_post():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into scorehaslogic_post (jugdment,emotion,logic,listen_to_the_music,play_the_music,memoire,bpm,score_content,user_id,pic,pic_of_the_score) values (:jugdment,:emotion,:logic,:listen_to_the_music,:play_the_music,:memoire,:bpm,:score_content,:user_id,:pic,:pic_of_the_score)",hey)
        user = query_db('select * from scorehaslogic_post')

        return render_template("scorehaslogic_postform.html", scorehaslogic_posts=user, one_user=one_user, the_title="add new scorehaslogic_post", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from scorehaslogic_post')
    one_user = query_db("select * from scorehaslogic_post limit 1", one=True)
    return render_template("scorehaslogic_postform.html", scorehaslogic_posts=user, one_user=one_user, the_title="add new scorehaslogic_post", touslesuser=touslesuser)


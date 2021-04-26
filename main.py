from flask import Flask, redirect, render_template, abort, request
from data.db_session import global_init, create_session
from data.users import User
from data.chats import Chats
from data.messages import Messages
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from data.login import LoginForm
from data.register import RegisterForm
from sqlalchemy import or_
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'UGVGScouiSBdpciubn2454USHcpusdfhcpUODhclvb3456sdoich'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect("/login")


@app.route("/get_messages/<int:chatId>", methods=["GET"])
@login_required
def get_messages(chatId):
    db_sess = create_session()
    messages = db_sess.query(Messages).filter(
        Messages.chatId == chatId
    )
    chat = db_sess.query(Chats).filter(Chats.id == chatId).first()
    if chat:
        dct = {
            "messages": list(map(lambda mess: {
                "id": mess.id,
                "chatId": mess.chatId,
                "isAuthor": mess.authorId == current_user.id,
                "content": mess.content,
                "time": str(mess.time)
            }, messages))
        }
        return json.dumps(dct)
    return json.dumps({"error": "No chat with this ID"})


@app.route("/add_message", methods=["POST"])
@login_required
def add_message():
    data = request.get_json(silent=True)
    db_sess = create_session()
    message = Messages()
    message.chatId = data["chatId"]
    message.authorId = current_user.id
    message.content = data["content"]
    db_sess.add(message)
    db_sess.commit()
    return {}


@app.route("/get_chats")
@login_required
def get_chats():
    db_sess = create_session()
    chats = db_sess.query(Chats).filter(
        or_(current_user.id == Chats.first_user_id, current_user.id == Chats.second_user_id)
    ).all()
    dct = {"chats": []}
    for chat in chats:
        recipient = db_sess.query(User).filter(
                or_(User.id == chat.first_user_id, User.id == chat.second_user_id),
                User.id != current_user.id
            ).first()
        lstMessage = db_sess.query(Messages).filter(Messages.chatId == chat.id).all()
        dct["chats"].append({
            "id": chat.id,
            "recipient": recipient.name,
            "message": f'{"You:" if lstMessage[-1].authorId == current_user.id else ""} {lstMessage[-1].content}' if lstMessage else None
        })
    return json.dumps(dct)


@app.route('/add_chat/<int:recipientId>')
@login_required
def add_chat(recipientId):
    db_sess = create_session()
    if len(db_sess.query(User).filter(User.id == recipientId).all()) == 0:
        return json.dumps({"error": "No user with this ID"})
    if len(db_sess.query(Chats).filter(
        or_(Chats.first_user_id == current_user.id, Chats.second_user_id == current_user.id),
        or_(Chats.second_user_id == recipientId, Chats.first_user_id == recipientId),
    ).all()) == 0:
        chat = Chats()
        chat.first_user_id = current_user.id
        chat.second_user_id = recipientId
        db_sess.add(chat)
        db_sess.commit()
        return json.dumps({"success": "Successful"})
    return json.dumps({"error": "The chat has already been created"})


@app.route("/add_chat_page")
@login_required
def add_chat_page():
    return render_template("add-chat.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/profile")
@login_required
def profile():
    user = {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "about": current_user.about,
        "created_date": current_user.created_date,
    }
    return render_template("profile.html", user=user)


@app.route("/get_user/<idUser>")
@login_required
def get_user(idUser):
    db_sess = create_session()
    db_user = db_sess.query(User).filter(User.id == idUser).first()
    user = {
        "Id": db_user.id,
        "E-mail": db_user.email,
        "Name": db_user.name,
        "About": db_user.about if db_user.about else "empty",
        "created_date": str(db_user.created_date),
    }
    return json.dumps(user)


@app.route("/global")
@login_required
def globalPage():
    return render_template("global.html")


@app.route("/get_global")
@login_required
def get_global():
    db_sess = create_session()
    users = db_sess.query(User).filter(User.id != current_user.id).all()
    users = list(map(
        lambda x: {
            "id": x.id,
            "name": x.name,
            "email": x.email,
            "isRecipient": True if db_sess.query(Chats).filter(
                or_(current_user.id == Chats.first_user_id, current_user.id == Chats.second_user_id),
                or_(x.id == Chats.first_user_id, x.id == Chats.second_user_id)
            ).first() else False
        },
        users
    ))
    return json.dumps({"users": users})


@app.route("/get_current_user")
def get_current_user():
    return get_user(current_user.id)


def main():
    global_init("db/messengerData.db")
    app.run()


if __name__ == '__main__':
    main()

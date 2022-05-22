from flask import Flask, render_template, redirect
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.tables import User, Tag, Article
from forms.user_form import UserForm, UpdateUserForm
from forms.login_form import LoginForm
from forms.article_form import ArticleForm, EditArticleForm
from flask_restful import Api
import articles_resources
import user_resources
from requests import post, get, delete, put
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
imn = 5


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", title="Home Page")


def access_level():
    return current_user.access_level == 0


@app.route('/about')
@login_required
def about():
    with open("static/article/about.md", encoding="utf-8") as fp:
        text = fp.read()
    html = markdown.markdown(text)
    return render_template("about.html", title="About Author", text=html)


@app.route('/admin_panel/users')
@login_required
def admin_panel_users():
    if access_level():
        lis = get('http://localhost:5000/api/v2/list_user').json()
        return render_template("all_profile.html", lis=lis)
    else:
        return f'''<h1> Отказано в доступе, так как у вас нет права на посещение данной страницы! 
               \n Если вы считаете, что произошла ошибка, то свяжитесь с нами по почте.</h1>'''


@app.route('/admin_panel')
@login_required
def admin_panel():
    if access_level():
        lis = get('http://localhost:5000/api/v2/list_art').json()
        return render_template("all_articles.html", lis=lis)
    else:
        return f'''<h1> Отказано в доступе, так как у вас нет права на посещение данной страницы! 
        \n Если вы считаете, что произошла ошибка, то свяжитесь с нами по почте.</h1>'''


@app.route('/up_article/<int:art_id>')
@login_required
def up_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 0}).json()
    return redirect("/admin_panel")


@app.route('/down_article/<int:art_id>')
@login_required
def down_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 1}).json()
    return redirect("/admin_panel")


@app.route('/up_root_user/<int:use_id>')
@login_required
def up_root_user(use_id):
    put('http://localhost:5000/api/v2/user/' + str(use_id),
        json={'level': 0}).json()
    return redirect("/admin_panel")


@app.route('/down_root_user/<int:use_id>')
@login_required
def down_root_user(use_id):
    put('http://localhost:5000/api/v2/user/' + str(use_id),
        json={'level': 1}).json()
    return redirect("/admin_panel")


@app.route('/create_article')
@login_required
def create_article():
    with open("static/article/Hello_art.md", encoding="utf-8") as fp:
        text = fp.read()
    html = markdown.markdown(text)
    return render_template('new_art.html', title="Instruct for create art", text=html)


@app.route('/delete_article/<int:art_id>')
@login_required
def delete_article(art_id):
    delete('http://localhost:5000/api/v2/art/' + str(art_id)).json()
    return redirect('/profile/' + str(current_user.id))


@app.route('/edit_article/<int:art_id>', methods=['GET', 'POST'])
@login_required
def edit_article(art_id):
    form = EditArticleForm()
    article = get('http://localhost:5000/api/v2/art/' + str(art_id)).json()
    if form.validate_on_submit():
        print(form.text.data)
        f = open(article['text'], 'w')
        f.write(form.text.data)
        f.close()
        put('http://localhost:5000/api/v2/art/' + str(art_id),
            json={'title': form.title.data,
                  'text': article['text']}).json()
        return redirect('/profile/' + str(current_user.id))
    with open(article['text']) as fp:
        text = fp.read()
    return render_template("edit_article.html", articl=article, tex=text, form=form)


@app.route('/new_article', methods=['GET', 'POST'])
@login_required
def new_article():
    global imn
    form = ArticleForm()
    if form.validate_on_submit():
        name = "./static/article/art_" + str(current_user.id) + "_" + str(imn) + ".md"
        imn += 1
        f = open(name, 'w')
        f.write(form.text.data)
        f.close()
        post('http://localhost:5000/api/v2/list_art',
             json={'title': form.title.data,
                   'author': current_user.id,
                   'text': name}).json()
        return redirect('/complete')
    return render_template('new.html', title='Новая статья', form=form)


@app.route('/complete')
@login_required
def complete():
    return render_template('complete.html', title="Успешно")


@app.route('/art/<int:art_id>')
@login_required
def art(art_id):
    st = 'http://localhost:5000/api/v2/art/' + str(art_id)
    print(st)
    lis = get(st).json()
    with open(lis['text']) as fp:
        text = fp.read()
    html = markdown.markdown(text)
    return render_template('art.html', title=lis['title'], text=html)


@app.route('/articles')
@login_required
def list_article():
    lis = get('http://localhost:5000/api/v2/list_art').json()
    return render_template('list_art.html', title='Все статьи', lis=lis)


@app.route('/profile/<int:use_id>')
@login_required
def profile(use_id):
    art_list = get('http://localhost:5000/api/v2/list_art').json()
    lis = get('http://localhost:5000/api/v2/user/' + str(use_id)).json()
    log = lis['email'].split("@")
    name = lis['surname'] + " " + lis['name']
    return render_template('Profile_user.html', title=log[0], log_name=log[0], full_name=name, email=lis['email'],
                           country=lis['country'], sex=lis['sex'], art_list=art_list, id=lis['id'], status=lis['access'])


@app.route('/edit_profile/<int:use_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(use_id):
    form = UpdateUserForm()
    if form.validate_on_submit():
        put('http://localhost:5000/api/v2/user/' + str(use_id),
            json={'f_name': form.f_name.data, 's_name': form.s_name.data, 'sex': form.sex.data[0],
                  'country': form.country.data, 'email': form.email.data}).json()
        return redirect("/profile/" + str(use_id))
    else:
        print("error")
    lis = get('http://localhost:5000/api/v2/user/' + str(use_id)).json()
    log = lis['email'].split("@")
    return render_template('edit_profile.html', title=log[0], log_name=log[0], f_name=lis['name'],
                           s_name=lis['surname'], email=lis['email'],
                           country=lis['country'], sex=lis['sex'], form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.s_name.data,
            name=form.f_name.data,
            email=form.email.data,
            access_level=1,
            country=form.country.data,
            sex=form.sex.data[0]
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        use = db_sess.query(User).filter(User.email == form.email.data).first()
        if use and use.check_password(form.password.data):
            login_user(use, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/my_project.db")

    api.add_resource(articles_resources.ArticleResource, '/api/v2/art/<int:art_id>')
    api.add_resource(user_resources.UserResource, '/api/v2/user/<int:user_id>')

    api.add_resource(articles_resources.ArticleListResource, '/api/v2/list_art')
    api.add_resource(user_resources.ListUserResource, '/api/v2/list_user')

    app.run()


if __name__ == '__main__':
    main()

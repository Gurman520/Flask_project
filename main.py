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
from mail import MAIL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
imn = 2


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Функция вызова главной страницы сайта
@app.route("/")
def index():
    return render_template("index.html", title="Home Page")


# Функция проверки уровня пользователя
def access_level():
    # Проверка, что пользователь администратор
    return current_user.access_level == 0


def error():
    # Функция выводит сообщение об ошибке!
    # Предлогает пользователю вернуться на предыдущюю страницу, через нажатие единственной кнопки!
    pass

# @app.route('/about')
# @login_required
# def about():
#     with open("static/article/about.md", encoding="utf-8") as fp:
#         text = fp.read()
#     html = markdown.markdown(text)
#     return render_template("about.html", title="About Author", text=html)


# Функция вызова страницы админ панели
@app.route('/admin_panel')
@login_required
def admin_panel():
    if access_level():
        lis = get('http://localhost:5000/api/v2/list_art').json()  # получаем список статей
        return render_template("all_articles.html", title='Admin article', lis=lis)
    else:
        return f'''<h1> Отказано в доступе, так как у вас нет права на посещение данной страницы! 
        \n Если вы считаете, что произошла ошибка, то свяжитесь с нами по почте.</h1>'''


# Админ панель пользователей
@app.route('/admin_panel/users')
@login_required
def admin_panel_users():
    if access_level():
        lis = get('http://localhost:5000/api/v2/list_user').json()  # получаем список пользователей
        return render_template("all_profile.html", title='Admin Users', lis=lis)
    else:
        return f'''<h1> Отказано в доступе, так как у вас нет права на посещение данной страницы! 
               \n Если вы считаете, что произошла ошибка, то свяжитесь с нами по почте.</h1>'''


# Опубликовать статью
@app.route('/up_article/<int:art_id>')
@login_required
def up_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 0}).json()
    m = MAIL(current_user.email)
    if m.open_article() == {'success': 'OK'}:
        return redirect("/admin_panel")
    else:
        error()
        return f'''Ошибка'''


# Скрыть статью с сайта
@app.route('/down_article/<int:art_id>')
@login_required
def down_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 1}).json()
    return redirect("/admin_panel")


# Повысить пользователя до админа
@app.route('/up_root_user/<int:use_id>')
@login_required
def up_root_user(use_id):
    put('http://localhost:5000/api/v2/user/' + str(use_id),
        json={'level': 0}).json()
    return redirect("/admin_panel/users")


# Понизить пользователя до обычного пользователя
@app.route('/down_root_user/<int:use_id>')
@login_required
def down_root_user(use_id):
    put('http://localhost:5000/api/v2/user/' + str(use_id),
        json={'level': 1}).json()
    return redirect("/admin_panel/users")


# Выводит статью о том, как писать статью
@app.route('/create_article')
@login_required
def create_article():
    with open("static/article/Hello_art.md", encoding="utf-8") as fp:
        text = fp.read()
    html = markdown.markdown(text)
    return render_template('new_art.html', title="Instruct for create art", text=html)


# Удалить статью
@app.route('/delete_article/<int:art_id>')
@login_required
def delete_article(art_id):
    delete('http://localhost:5000/api/v2/art/' + str(art_id)).json()
    return redirect('/profile/' + str(current_user.id))


# Редактировать статью
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
    return render_template("edit_article.html", title='Редактирование', articl=article, tex=text, form=form)


# Новая статья
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
                   'text': name,
                   'tegs': form.tegs.data}).json()
        m = MAIL(current_user.email)
        if m.new_article() == {'success': 'OK'}:
            return redirect('/complete')
        else:
            error()
            return f'''Ошибка''' # Дописать страницу вывода сообщения об ошибке
    return render_template('new.html', title='Новая статья', form=form)


# Успешная регистрация статья
@app.route('/complete')
@login_required
def complete():
    return render_template('complete.html', title="Успешно")


# Прочтение конкретной статьи
@app.route('/art/<int:art_id>')
@login_required
def art(art_id):
    st = 'http://localhost:5000/api/v2/art/' + str(art_id)
    print(st)
    lis = get(st).json()
    with open(lis['text']) as fp:
        text = fp.read()
    html = markdown.markdown(text)
    return render_template('art.html', title=lis['title'], text=html, tag=lis['tags'])


# Список всех статей
@app.route('/articles')
@login_required
def list_article():
    lis = get('http://localhost:5000/api/v2/list_art').json()
    return render_template('list_art.html', title='Все статьи', lis=lis)


# Конкретный профиль пользователя
@app.route('/profile/<int:use_id>')
@login_required
def profile(use_id):
    art_list = get('http://localhost:5000/api/v2/list_art').json()
    lis = get('http://localhost:5000/api/v2/user/' + str(use_id)).json()
    if lis != {'error': 'FAIL'}:
        log = lis['email'].split("@")
        name = lis['surname'] + " " + lis['name']
        return render_template('Profile_user.html', title=log[0], log_name=log[0], full_name=name, email=lis['email'],
                               country=lis['country'], sex=lis['sex'], art_list=art_list, id=lis['id'],
                               status=lis['access'])
    else:
        return f'''Просим прощения, но возникла некая ошибка на нашей стороне. 
        Мы делаем все возможное, чтобы ее исправить как можно скорее!'''


# Редактировать профиль
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


# Регистрация пользователя
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
        m = MAIL(form.email.data)
        if m.register_mail() == {'success': 'OK'}:
            return redirect('/login')
        else:
            error()
            return f'''Ошибка'''
    return render_template('register.html', title='Регистрация', form=form)


# Вход пользователя
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


# Выход из аккаунта
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

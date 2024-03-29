from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.tables import User, Tag, Article
from forms.user_form import UserForm, UpdateUserForm
from forms.login_form import LoginForm
from forms.article_form import ArticleForm, EditArticleForm, AddTeg
from forms.message_form import MessageForm
from forms.news_form import NewsForm
from flask_restful import Api
import articles_resources
import user_resources
import news_resources
from requests import post, get, delete, put
import markdown
from mail import MAIL
import TOKEN

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
    lis = get('http://localhost:5000/api/v2/news').json()
    lis.reverse()
    return render_template("index.html", title="Home Page", news=lis)


@app.route('/admin_panel/news', methods=['GET', 'POST'])
@login_required
def new_news():
    form = NewsForm()
    if access_level_nul():
        if form.validate_on_submit():
            post('http://localhost:5000/api/v2/news', json={
                'title': form.title.data,
                'author': current_user.id,
                'text': form.text.data,
            }).json()
            return redirect('/')
        return render_template('new_news.html', title="Новая новость", form=form)
    else:
        return render_template("Error.html", title="Наша ошибка", error=500)


# Функция проверки уровня пользователя
def access_level():
    # Проверка, что пользователь администратор
    return current_user.access_level < 2


def access_level_nul():
    return current_user.access_level == 0


@app.route('/coal_back', methods=['GET', 'POST'])
def coal_back():
    form = MessageForm()
    if form.validate_on_submit():
        m = MAIL(TOKEN.mail)
        m.call_back_mail(form.text.data, form.subject.data)
        return redirect('/')
    return render_template('coal_back.html', title='Обратная связь', form=form)


# Функция вызова страницы админ панели
@app.route('/admin_panel')
@login_required
def admin_panel():
    if access_level():
        lis = get('http://localhost:5000/api/v2/list_art').json()  # получаем список статей
        return render_template("all_articles.html", title='Admin article', lis=lis)
    else:
        return render_template("Error.html", title='Отказано в доступе', error=1)


# Админ панель пользователей
@app.route('/admin_panel/users')
@login_required
def admin_panel_users():
    if access_level_nul():
        lis = get('http://localhost:5000/api/v2/list_user').json()  # получаем список пользователей
        return render_template("all_profile.html", title='Admin Users', lis=lis)
    else:
        return render_template("Error.html", title='Отказано в доступе', error=1)


@app.route('/admin_panel/Teg', methods=['GET', 'POST'])
@login_required
def teg():
    form = AddTeg()
    lis = get('http://localhost:5000/api/v2/teg').json()
    if form.validate_on_submit():
        post('http://localhost:5000/api/v2/teg', json={'name': form.name.data}).json()
        return redirect('/admin_panel/Teg')
    return render_template('Teg.html', title='Теги', form=form, teg=lis['tags'])


# Опубликовать статью
@app.route('/up_article/<int:art_id>')
@login_required
def up_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 0}).json()
    m = MAIL(current_user.email)
    if m.open_article():
        return redirect("/admin_panel")
    else:
        return render_template("Error.html", title="Наша ошибка", error=500)


# Скрыть статью с сайта
@app.route('/down_article/<int:art_id>')
@login_required
def down_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 1}).json()
    m = MAIL(current_user.email)
    if m.close_article():
        return redirect("/admin_panel")
    else:
        return render_template("Error.html", title="Наша ошибка", error=500)


# Заброковать статью
@app.route('/lose_article/<int:art_id>')
@login_required
def lose_article(art_id):
    put('http://localhost:5000/api/v2/art/' + str(art_id),
        json={'status': 2}).json()
    m = MAIL(current_user.email)
    if m.lose_article():
        return redirect("/admin_panel")
    else:
        return render_template("Error.html", title="Наша ошибка", error=500)


# Повысить пользователя до root
@app.route('/root_user/<int:use_id>')
@login_required
def root_user(use_id):
    put('http://localhost:5000/api/v2/user/' + str(use_id),
        json={'level': 0}).json()
    return redirect("/admin_panel/users")


# Понизить пользователя до обычного пользователя
@app.route('/readit_user/<int:use_id>')
@login_required
def readit_user(use_id):
    put('http://localhost:5000/api/v2/user/' + str(use_id),
        json={'level': 2}).json()
    return redirect("/admin_panel/users")


# Сделать пользователя модератором
@app.route('/moderator_user/<int:use_id>')
@login_required
def moderator_user(use_id):
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
    article = get('http://localhost:5000/api/v2/art/' + str(art_id)).json()
    if current_user.id == article['author'] or current_user.acesses_level == 0:
        form = EditArticleForm()
        if form.validate_on_submit():
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
    else:
        return render_template("Error.html", title='Отказано в доступе', error=1)


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
        if m.new_article():
            return redirect('/complete')
        else:
            return render_template("Error.html", title="Наша ошибка", error=500)
    return render_template('new.html', title='Новая статья', form=form)


# Успешная регистрация статья
@app.route('/complete')
@login_required
def complete():
    return render_template('Error.html', title="Успешно", error=100)


# Прочтение конкретной статьи
@app.route('/art/<int:art_id>')
def art(art_id):
    lis = get('http://localhost:5000/api/v2/art/' + str(art_id)).json()
    if lis['status'] == 0 or current_user.id == lis['author'] or current_user.access_level != 2:
        with open(lis['text']) as fp:
            text = fp.read()
        html = markdown.markdown(text)
        return render_template('art.html', title=lis['title'], text=html, tag=lis['tags'], name=lis['author_name'])
    else:
        return render_template("Error.html", title='Отказано в доступе', error=404)


# Список всех статей
@app.route('/articles')
# @login_required
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
        return render_template('Profile_user.html', lis=lis, title=log[0], log_name=log[0], art_list=art_list)
    else:
        return render_template("Error.html", title="Наша ошибка", error=500)


# Редактировать профиль
@app.route('/edit_profile/<int:use_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(use_id):
    if current_user.id == use_id or current_user.access_level == 0:  # Редактировать профиль может, только сам пользователь и ROOT пользователь.
        form = UpdateUserForm()
        lis = get('http://localhost:5000/api/v2/user/' + str(use_id)).json()
        if form.validate_on_submit():
            put('http://localhost:5000/api/v2/user/' + str(use_id),
                json={'f_name': form.f_name.data, 's_name': form.s_name.data, 'sex': form.sex.data,
                      'country': form.country.data, 'email': form.email.data, 'vk': form.vk.data,
                      'git': form.git.data}).json()
            return redirect("/profile/" + str(use_id))
        log = lis['email'].split("@")
        return render_template('edit_profile.html', title=log[0], log_name=log[0], form=form, lis=lis)
    else:
        return render_template("Error.html", title='Отказано в доступе', error=1)


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
            access_level=2,
            country=form.country.data,
            sex=form.sex.data[0],
            vk=form.vk.data,
            GitHub=form.git.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        m = MAIL(form.email.data)
        if m.register_mail():
            return redirect('/login')
        else:
            return render_template("Error.html", title="Наша ошибка", error=500)
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


@app.errorhandler(401)
def not_found(error):
    return render_template("Error.html", title="Не авторизован", error=error)


@app.errorhandler(404)
def not_found(error):
    return render_template("Error.html", title="Не найдено", error=error)


@app.errorhandler(500)
def not_found(error):
    print(error)
    return render_template("Error.html", title="Наша ошибка", error=error)


def main():
    db_session.global_init("db/my_project.db")

    api.add_resource(articles_resources.ArticleResource, '/api/v2/art/<int:art_id>')
    api.add_resource(user_resources.UserResource, '/api/v2/user/<int:user_id>')

    api.add_resource(articles_resources.ArticleListResource, '/api/v2/list_art')
    api.add_resource(user_resources.ListUserResource, '/api/v2/list_user')

    api.add_resource(articles_resources.TegResource, '/api/v2/teg')

    api.add_resource(news_resources.NewsListResource, '/api/v2/news')

    app.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Неожиданное завершение программы из-за ошибки:')
        print(e)

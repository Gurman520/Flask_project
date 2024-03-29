from data import db_session
from data.tables import User, Tag, Article, News


def add_user(surname, name, level, country, email, sex, password, vk, git):
    user_n = User()

    user_n.surname = surname
    user_n.name = name
    user_n.access_level = level
    user_n.country = country
    user_n.email = email
    user_n.sex = sex
    user_n.vk = vk
    user_n.GitHub = git
    if password != '':
        user_n.set_password(password)

    db_sess = db_session.create_session()
    db_sess.add(user_n)
    db_sess.commit()


def add_tags(name):
    tag_n = Tag()
    db_sess = db_session.create_session()

    tag_n.name = name

    db_sess.add(tag_n)
    db_sess.commit()


def add_article(title, txt, author, status, tagg):
    art_n = Article()
    db_sess = db_session.create_session()

    art_n.author = author
    art_n.title = title
    art_n.text = txt
    art_n.status = status
    for i in tagg:
        tag = db_sess.query(Tag).filter(Tag.id == i).first()
        art_n.tags.append(tag)

    db_sess.add(art_n)
    db_sess.commit()


def add_news(title, author, text):
    new_n = News()
    db_sess = db_session.create_session()

    new_n.title = title
    new_n.author = author
    new_n.text = text

    db_sess.add(new_n)
    db_sess.commit()


def main():
    db_session.global_init("db/my_project.db")
    # добавление записи
    add_user("Sulima", "Roman", 0, "Russian", "Roman.Python.test@gmail.com", "man", "Rdfhnbhf142",
             "http://vk.com/furman521", "https://github.com/Gurman520")
    add_tags("python")
    add_tags("HTML")
    add_tags("ML_learning")
    add_tags("bd")
    add_tags("Author")
    add_tags("Single")
    add_article("First article", "./static/article/art_1.md", 1, 0, [6])
    add_news("Старт Проекта!", 1, "Это первый запуск Проекта, так что БД обновлена!")


if __name__ == '__main__':
    main()

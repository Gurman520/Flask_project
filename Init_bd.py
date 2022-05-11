from data import db_session


def main():
    db_session.global_init("db/my_project.db")


if __name__ == '__main__':
    main()

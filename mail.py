from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from flask import jsonify


class MAIL:
    def __init__(self, adres):
        # create message object instance
        self.msg = MIMEMultipart()
        # setup the parameters of the message
        self.password = "Rdfhnbhf142"
        self.msg['From'] = "roman.python.test@gmail.com"
        self.msg['To'] = adres
        # create server
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        # Login Credentials for sending the mail
        self.server.login(self.msg['From'], self.password)

    def register_mail(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = " Поздравляем, регистрация прошла успешно!" \
                      "Теперь вам доступны все функции нашего сайта!" \
                      "С уважением команда, Read_ART."
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return True
        except Exception:
            return False

    def open_article(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = "Поздравляем, ваша статья опубликована на сайте!" \
                      "С уважением команда, Read_ART."
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return True
        except Exception:
            return False

    def close_article(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = "Ваша статья не удовлетворяет некоторым нашим требованиям.\n" \
                      " Мы просим вас внести изменения и попробывать снова.\n" \
                      "С уважением, команда Read_ART."
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return True
        except Exception:
            return False

    def new_article(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = "Ваша статья отправлена на модерацию.\n" \
                      "Обычно моедрация длится не более 2-3 дней.\n" \
                      "По итогам проверки нашими модератарами, вам придет результат. " \
                      "За состоянием вашей статьи вы можете наблюдать в личном кабинете.\n" \
                      "С уважением команда, Read_ART."
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return True
        except Exception:
            return False

    def lose_article(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = "К сожалению ваша статья нарушила наши правила, по этому мы приняли решение,\n" \
                      " что ваша статья не может быть опубликована на нашем сайте и не подлежит дальнейшей дороботки.\n" \
                      "Если вы считаете, что произошла, напишите на почту, с которой пришло сообщение.\n" \
                      "С уважением команда, Read_ART! "
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return True
        except Exception:
            return False

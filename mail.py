from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from flask import jsonify


class MAIL:
    def __init__(self, adres):
        # create message object instance
        self.msg = MIMEMultipart()
        # setup the parameters of the message
        self.password = "*********"
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
            message = "Регистрация прошла успешно!" \
                      "Благодарим за регистрацию на нашем сайте."
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return jsonify({'success': 'OK'})
        except Exception:
            return jsonify({'error': 'Fail send message'})

    def open_article(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = "Ваша статья опубликована!"
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return jsonify({'success': 'OK'})
        except Exception:
            return jsonify({'error': 'Fail send message'})

    def new_article(self):
        try:
            self.msg['Subject'] = "Уведомление"
            message = "Ваша статья принята на проверку."
            self.msg.attach(MIMEText(message, 'plain'))
            # send the message via the server.
            self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            return jsonify({'success': 'OK'})
        except Exception:
            return jsonify({'error': 'Fail send message'})

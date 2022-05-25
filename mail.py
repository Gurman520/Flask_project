from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class MAIL:
    # create message object instance
    msg = MIMEMultipart()
    # setup the parameters of the message
    password = "Rdfhnbhf142"
    msg['From'] = "roman.python.test@gmail.com"
    msg['To'] = "romanidzs@gmail.com"
    # create server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    def register_mail(self):
        self.msg['Subject'] = "Уведомление"
        message = "Регистрация прошла успешно!" \
                  "Благодарим за регистрацию на нашем сайте."
        self.msg.attach(MIMEText(message, 'plain'))
        # send the message via the server.
        self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())

    def open_article(self):
        self.msg['Subject'] = "Уведомление"
        message = "Ваша статья опубликована!"
        self.msg.attach(MIMEText(message, 'plain'))
        # send the message via the server.
        self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())


cl = MAIL()
cl.open_article()

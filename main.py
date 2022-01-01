from flask import Flask, render_template, request
import smtplib

import os
from dotenv import load_dotenv      # pip install python-dotenv

load_dotenv()


app = Flask(__name__)

app.config['MY_EMAIL'] = os.environ.get("MY_EMAIL")       # read from .env file
app.config['MY_PASSWORD'] = os.environ.get("MY_PASSWORD")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def receive_data():
    data = request.form
    send_email(data)
    return render_template('index.html', inputdata=data)


def send_email(data):
    name = data['name']
    email = data['email']
    msg = data['message']

    message = f'Thank you for contacting me. I have received following information from you:' \
              f'\n\nName: {name}, \nEmail: {email}\nMessage: {msg}' \
              f'\n\nI will soon respond to your message.\n\nNC InMe'

    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=app.config['MY_EMAIL'], password=app.config['MY_PASSWORD'])
        connection.sendmail(
            from_addr=app.config['MY_EMAIL'],
            to_addrs=email,
            msg=f'Subject: Acknowledgement from NC InMe\n\n{message}'
        )


if __name__ == '__main__':
    app.run(debug=True)


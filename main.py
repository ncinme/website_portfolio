from flask import Flask, render_template, request, flash
import smtplib
import logging
import os
from dotenv import load_dotenv  # pip install python-dotenv

# Logging into a file on the server
# LOG_FORMAT = "%(levelname)s %(asctime)s -- %(message)s"
# logging.basicConfig(filename='portfolio_website.log', level=logging.INFO, format=LOG_FORMAT, filemode='a')

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")  # read from .env file
app.config['MY_EMAIL'] = os.environ.get("MY_EMAIL")
app.config['MY_PASSWORD'] = os.environ.get("MY_PASSWORD")

# Adding application logs to Heroku
# https://logtail.com/tutorials/how-to-start-logging-with-heroku/
# https://stackoverflow.com/questions/54297215/how-to-show-stdout-logs-in-heroku-using-flask
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        if name != '' or email != '' or msg != '':
            send_email(name, email, msg)

    return render_template('index.html')


def send_email(name, email, msg):
    message = f'Thank you for contacting me. I have received following information from you:' \
              f'\n\nName: {name}, \nEmail: {email}\nMessage: {msg}' \
              f'\n\nI will soon respond to your message.\n\nNC InMe'

    try:
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=app.config['MY_EMAIL'], password=app.config['MY_PASSWORD'])
            connection.sendmail(
                from_addr=app.config['MY_EMAIL'],
                to_addrs=email,
                msg=f'Subject: Acknowledgement from NC InMe\n\n{message}'
            )
    except KeyError as err:
        logging.exception(err)
        flash(f"Error sending email. Please try after some time.")

    except Exception as err:
        logging.exception(err)
        flash(f"Error sending message. Please try again.")
    else:
        flash(f"Thank you for contacting me {name}. I will revert soon.")


if __name__ == '__main__':
    app.run(debug=True)

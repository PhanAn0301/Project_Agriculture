from flask import Flask
from views import views
from callback import callback
import signal

app = Flask(__name__)
app.register_blueprint(views, url_prefix = "/")
app.register_blueprint(callback, url_prefix = "/callback")

def signal_handler(signal, frame):
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True)
from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

def scheduleTask():
    print("This test runs every 100 seconds")
@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"
if __name__ == '__main__':
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", seconds=100)
    scheduler.start()
    app.run(host="127.0.0.1")
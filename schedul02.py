from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import time

from test1 import main_job1
from test2 import main_job2
from test3 import helloworld



def sensor():
    """ Function for test purposes. """
    time.sleep(1)
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=10)
#sched.add_job(main_job1,'interval', seconds=2)
sched.start()

#@sched.scheduled_job('interval', seconds=20)
def timed_job():
    time.sleep(1)
    print('我愛你！')

app = Flask(__name__)

@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"

if __name__ == "__main__":
    app.run()
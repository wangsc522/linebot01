from celery import Celery
import time

broker = 'redis://172.20.11.77:6379/5'
#broker = 'redis://127.0.0.1:6380/5'
backend = 'redis://172.20.11.77:6379/6'
#backend = 'redis://127.0.0.1:6380/6'

#from tasks01 import add
#r = add.delay(4, 4)
#r.wait()
#r.result
#r.ready()
#r.get()   # Waits until the task is done and returns the retval.
#r.successful() # returns True if the task didn't end in failure

app = Celery('tasks', broker=broker, backend=backend)
@app.task
def add(x, y):
    #time.sleep(10)
    return x + y
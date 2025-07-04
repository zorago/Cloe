from apscheduler.schedulers.background import BlockingScheduler as schedule
from time import sleep

def display(msg):
    print("here we are : ", msg)
    # job_id.remove()
    # scheduler.shutdown(wait=False)

scheduler = schedule()
job_id = scheduler.add_job(display, "interval", seconds = 3, args=["Mon petit mot"])

scheduler.start()
# sleep(10)
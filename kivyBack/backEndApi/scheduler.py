from apscheduler.schedulers.background import BackgroundScheduler
from .views import logout_tokens


# Creates a default Background Scheduler
sched = BackgroundScheduler()
 
def making_empty_logout_tokens():
    logout_tokens.clear()
    print("length of token list :",len(logout_tokens))
    

sched.add_job(making_empty_logout_tokens, trigger="cron", day = "*", week = '*', day_of_week = '*', hour = '*',minute = "*/15")

# Starts the Scheduled jobs
sched.start()
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import ContextTypes

sched = BackgroundScheduler()

def job(context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(chat_id=context.job.chat_id, text="Не забудь выполнить свои привычки! 💪")

def setup_scheduler(app):
    sched.add_job(lambda: None, "interval", minutes=1)
    sched.start()

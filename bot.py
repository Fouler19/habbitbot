from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import db, scheduler
import datetime

TOKEN = "ВАШ_TELEGRAM_TOKEN_ЗДЕСЬ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот‑трекер привычек. /add чтобы добавить привычку.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        return await update.message.reply_text("Используй: /add Название Частота")
    name = args[0]
    freq = args[1]
    db.add_habit(update.message.from_user.id, name, freq)
    await update.message.reply_text(f"Добавлено: {name} ({freq})")

async def list_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habits = db.get_habits(update.message.from_user.id)
    if not habits: return await update.message.reply_text("Нет привычек.")
    response = ""
    for h in habits:
        response += f"#{h[0]} {h[1]} — {h[2]}, Стрик: {h[3]}\n"
    await update.message.reply_text(response)

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args: return await update.message.reply_text("Укажи ID привычки: /done ID")
    habit_id = int(args[0])
    db.log_habit(habit_id, datetime.date.today().isoformat())
    await update.message.reply_text("Отмечено!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_habits))
    app.add_handler(CommandHandler("done", done))

    scheduler.setup_scheduler(app)

    app.run_polling()

if __name__ == "__main__":
    main()

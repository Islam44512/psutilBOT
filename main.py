import telebot
from config import TOKEN
import psutil


bot = telebot.TeleBot(TOKEN)

USERNAME = "YOU USERNAME" 



def admin(message):
    return message.from_user.username == USERNAME


# Handle 'start', 'help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(chat_id=message.chat.id, action='typing')
    bot.reply_to(message, """
Информация по ПК сервера:
/ram
/cpu
/disk
/processes
""")

@bot.message_handler(commands=['ram'])
def send_ram(message):
    if not admin(message):
        return

    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024 ** 3), 2)
    ram_used = round(ram.used / (1024 ** 3), 2)
    ram_percent = ram.percent
    answer = f"RAM: {ram_percent}%. {ram_used} из {ram_total}."
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['cpu'])
def send_cpu(message):
    if not admin(message):
        return

    cpu_usage = psutil.cpu_percent(interval=1)
    answer = f"Загрузка CPU: {cpu_usage}%"
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['disk'])
def send_disk(message):
    if not admin(message):
        return

    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    answer = f"Загрузка диска: {disk_percent}%"
    bot.send_message(message.chat.id, answer)
    

@bot.message_handler(commands=['processes'])
def send_processes(message):
    if not admin(message):
        return

    processes = psutil.process_iter()
    answer = f"Процессы: {processes}"
    bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.infinity_polling()
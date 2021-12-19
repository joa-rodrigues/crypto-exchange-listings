import telepot

# https://www.youtube.com/watch?v=67SH6tCuyLQ
token = 'TODO' # telegram token
receiver_id = 00000000 # https://api.telegram.org/botTODO/getUpdates


bot = telepot.Bot(token)

bot.sendMessage(receiver_id, 'This is a automated test message.')
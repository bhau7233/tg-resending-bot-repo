import discord
import telegram
import os

# Discord client setup
discord_token = 'YOUR_DISCORD_TOKEN_HERE'

client = discord.Client()

@client.event
async def on_ready():
    print('Discord client is ready.')

@client.event
async def on_message(message):
    if message.channel.id == 'TARGET_DISCORD_CHANNEL_ID_HERE':
        telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
        telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']

        telegram_bot = telegram.Bot(token=telegram_bot_token)
        try:
            if message.content:
                telegram_bot.send_message(chat_id=telegram_chat_id, text=message.content)
            
            for attachment in message.attachments:
                telegram_bot.send_photo(chat_id=telegram_chat_id, photo=attachment.url)

            print('Message has been forwarded to Telegram.')
        except Exception as e:
            print(f'Error forwarding message to Telegram: {e}')

# Telegram bot setup
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Started the bot!")

if __name__ == '__main__':
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    updater = telegram.ext.Updater(token=telegram_bot_token, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = telegram.ext.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()


import json
import yaml
import logging
import websocket
import telegram
try:
    import thread
except ImportError:
    import _thread as thread

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger('websocket').setLevel(level=logging.WARN)
logger = logging.getLogger(__name__)

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

uri = "ws://socket.blockcypher.com/v1/btc/main?token=" + config["BLOCKCYPHER_TOKEN"]

bot = telegram.Bot(token=config['TELEGRAM_TOKEN'])

def on_message(ws, message):
    logging.info(f"recv: {message[:25] + (message[25:] and '..')} ")
    sendTgMessage(parseBlock(message))

def on_pong(ws, message):
    logging.info(f"recv: pong ")
    # sendTgMessage("`Pong`")

def on_error(ws, error):
    logging.error(f"error: {error} ")
    print(error)

def on_close(ws):
    logging.critical(f"conn closed ###################")

def on_open(ws):
    def run(*args):
        ws.send(args[0])
    thread.start_new_thread(run, ("{ \"event\" : \"new-block\"}",))

def tgStart(update):
    update.message.reply_text('Hi!')

def sendTgMessage(message):
    bot.send_message(chat_id=config['TELEGRAM_DESTINATION'], text=message, parse_mode='MarkdownV2')

def parseBlock(newBlock):
    parsedNewBlock = json.loads(newBlock)
    message = "`Block " + str(parsedNewBlock['height']) + "`\n`" + str(parsedNewBlock['n_tx']) + " transactions`\n`" + str(round(parsedNewBlock['total']/100000000, 1)) + " ฿ sent`\n`" + str(round(parsedNewBlock['fees']/100000000, 3)) + " ฿ fees`"
    logging.info(f"forwarded: {message} ")
    return message

def main():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(uri,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        on_pong = on_pong)
    ws.on_open = on_open
    ws.run_forever(ping_interval=20, ping_timeout=3)

    updater = telegram.ext.Updater(config['TELEGRAM_TOKEN'])
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler('start',tgStart))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
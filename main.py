import telebot
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

bot = telebot.TeleBot("8711677456:AAHBKIdHU3URAXnJ0fJq7thSLO3ki2zPwjU")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def run_server():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me an Instagram Reel URL!")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    bot.reply_to(message, "⏳ Fetching reel...")
    try:
        response = requests.post(
            "https://saveig.app/api/ajaxSearch",
            data={"q": url, "t": "media", "lang": "en"},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        data = response.json()
        links = data.get("data", {}).get("links", [])
        if links:
            video_url = links[0].get("url")
            bot.reply_to(message, f"✅ Download: {video_url}")
        else:
            bot.reply_to(message, "❌ Couldn't fetch the reel!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

threading.Thread(target=run_server, daemon=True).start()
bot.polling()

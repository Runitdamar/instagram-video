import telebot
import instaloader
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

bot = telebot.TeleBot(""8711677456:AAHBKIdHU3URAXnJ0fJq7thSLO3ki2zPwjU)
L = instaloader.Instaloader()

# Simple web server to satisfy Render
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me an Instagram post URL!")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    bot.reply_to(message, "⏳ Downloading...")
    try:
        if "/reel/" in url:
            shortcode = url.split("/reel/")[1].split("/")[0].split("?")[0]
        elif "/p/" in url:
            shortcode = url.split("/p/")[1].split("/")[0].split("?")[0]
        else:
            bot.reply_to(message, "❌ Invalid Instagram URL!")
            return
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        bot.reply_to(message, f"✅ Video URL: {post.video_url}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Run web server in background thread
threading.Thread(target=run_server, daemon=True).start()

# Start bot
bot.polling()

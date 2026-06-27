import telebot
import instaloader

bot = telebot.TeleBot("8711677456:AAHBKIdHU3URAXnJ0fJq7thSLO3ki2zPwjU")
L = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me an Instagram post URL!")

@bot.message_handler(func=lambda m: True)
def download(message):
    url = message.text
    bot.reply_to(message, "⏳ Downloading...")
    try:
        shortcode = url.split("/p/")[1].split("/")[0]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        bot.reply_to(message, f"✅ Video URL: {post.video_url}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

bot.polling()

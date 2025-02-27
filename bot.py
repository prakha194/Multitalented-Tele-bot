import os
import telebot
import requests

# Load API keys from environment variables (Set these in Restack)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RESTACK_API_KEY = os.getenv("RESTACK_API_KEY")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Function to communicate with Restack API
def restack_request(endpoint, data):
    url = f"https://api.restack.io/{endpoint}"
    headers = {"Authorization": f"Bearer {RESTACK_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Start Command - Bot Introduction
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "🤖 Hello! I'm a multi-talented AI bot powered by Restack. Use the menu to explore my features!")

# Text AI Processing
@bot.message_handler(commands=['ai_text'])
def ai_text(message):
    bot.send_message(message.chat.id, "📝 Send me some text to analyze or improve!")
    bot.register_next_step_handler(message, process_text)

def process_text(message):
    response = restack_request("text-ai", {"text": message.text})
    bot.send_message(message.chat.id, f"🧠 AI Response: {response.get('output', 'Sorry, I couldn’t process that.')}")

# Summarization
@bot.message_handler(commands=['summarize'])
def summarize(message):
    bot.send_message(message.chat.id, "📄 Send me a long text to summarize!")
    bot.register_next_step_handler(message, process_summary)

def process_summary(message):
    response = restack_request("summarization", {"text": message.text})
    bot.send_message(message.chat.id, f"📌 Summary: {response.get('summary', 'Could not generate summary.')}")

# Image Generation
@bot.message_handler(commands=['generate_image'])
def generate_image(message):
    bot.send_message(message.chat.id, "🎨 Describe the image you want to generate!")
    bot.register_next_step_handler(message, process_image_request)

def process_image_request(message):
    response = restack_request("image-generation", {"prompt": message.text})
    image_url = response.get("image_url")
    if image_url:
        bot.send_photo(message.chat.id, image_url)
    else:
        bot.send_message(message.chat.id, "❌ Image generation failed.")

# Voice AI Processing
@bot.message_handler(commands=['voice_ai'])
def voice_ai(message):
    bot.send_message(message.chat.id, "🎙️ Send me a voice message!")
    bot.register_next_step_handler(message, process_voice_message)

def process_voice_message(message):
    if message.voice:
        file_info = bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_info.file_path}"
        response = restack_request("speech-to-text", {"audio_url": file_url})
        bot.send_message(message.chat.id, f"🗣️ Transcription: {response.get('text', 'Could not process audio.')}")
    else:
        bot.send_message(message.chat.id, "❌ No voice message detected.")

# Handle Unknown Commands
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.send_message(message.chat.id, "❓ I don’t understand this command. Use the menu for available options!")

# Run the bot
bot.polling()

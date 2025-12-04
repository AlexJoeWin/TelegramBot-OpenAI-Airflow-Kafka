from openai import OpenAI
from config import OPENAI_KEY, TELEGRAM_KEY
from kafka import KafkaProducer
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# Kafka Producer Setup
producer = KafkaProducer(bootstrap_servers='kafka:9092')
client = OpenAI(api_key=OPENAI_KEY)

async def handle_text(update, context):
    await update.message.reply_text("I am hungry for numbers!")
    user_text = update.message.text

    query = {"role": "user", "content": user_text}
    messages = [{"role": "system", "content": """You are a talk assistant that is interested in numbers. If the user does not provide a short answer with
        a plain number, refer to what was said by the user and formulate a topic related question that requires a plain number as answer."""},
                {"role": "user", "content": "I need to do more sports!"},
                {"role": "assistant", "content": "If you sports activity is related to your fitness, what is your exact weight in kg?"}]
    messages.append(query)

    prompt=messages

    response = client.chat.completions.create(model="gpt-4o-mini", messages=prompt, max_completion_tokens=30)

    reply = response.choices[0].message.content

    await update.message.reply_text(f"{reply}")


# Funktion: Nachricht aus Telegram nach Kafka pushen
async def handle_number(update, context):
    await update.message.reply_text("You sent a number, love it!")
    text = update.message.text
    producer.send('telegram_topic', text.encode('utf-8'))
    producer.flush()
    print(f"Nachricht von Telegram nach Kafka gesendet: {text}")


app = ApplicationBuilder().token(TELEGRAM_KEY).build()

# Handler for pure text (non-numeric)
app.add_handler(MessageHandler(filters.TEXT & ~filters.Regex(r'^\d+$'), handle_text))

# Handler for numbers (regex matches only digits)
app.add_handler(MessageHandler(filters.Regex(r'^\d+$'), handle_number))

app.run_polling()
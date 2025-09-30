import requests
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

print(f"🤖 Bot Token: {bot_token}")
print(f"💬 Chat ID: {chat_id}")

if not bot_token or not chat_id:
    print("❌ Missing configuration in .env file")
    exit(1)

# Отправляем тестовое сообщение
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    'chat_id': chat_id,
    'text': '🎉 *Тестовое сообщение от AIChat бота!*\n\n✅ Система уведомлений работает!\n\n_Это автоматическое сообщение_',
    'parse_mode': 'Markdown'
}

try:
    print("📤 Sending test message...")
    response = requests.post(url, json=payload, timeout=10)
    data = response.json()
    
    if data.get('ok'):
        print("✅ Сообщение отправлено успешно!")
        print(f"📨 Message ID: {data['result']['message_id']}")
        print(f"👤 Chat: {data['result']['chat']['first_name']}")
    else:
        print(f"❌ Ошибка Telegram API: {data}")
        
except Exception as e:
    print(f"❌ Ошибка отправки: {e}")
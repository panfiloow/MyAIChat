import os
import logging
from dotenv import load_dotenv
import requests
from typing import Optional

# Настройка логирования
logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        self.is_configured = all([self.bot_token, self.chat_id])
        
        if not self.is_configured:
            logger.warning("Telegram notifier is not configured properly. Check environment variables.")
        else:
            logger.info("Telegram notifier initialized successfully")

    def send_low_balance_notification(self, balance: float, threshold: float = 1.0) -> bool:
        """
        Отправляет уведомление о низком балансе в Telegram
        
        Args:
            balance: текущий баланс
            threshold: порог для уведомления (по умолчанию 1.0)
            
        Returns:
            bool: True если отправка успешна, False если нет
        """
        if not self.is_configured:
            logger.error("Cannot send Telegram notification: Bot not configured")
            return False
        
        if balance > threshold:
            return False
            
        message = (
            "⚠️ *Низкий баланс в AIChat приложении*\n\n"
            f"• *Текущий баланс:* `{balance:.4f}`\n"
            f"• *Порог уведомления:* `{threshold}`\n"
            f"• *Статус:* {'❌ КРИТИЧЕСКИЙ' if balance < 0.1 else '⚠️ НИЗКИЙ'}\n\n"
            "Рекомендуется пополнить баланс на [OpenRouter](https://openrouter.ai/)\n\n"
            "_Это автоматическое уведомление_"
        )
        
        return self._send_telegram_message(message)

    def send_startup_notification(self, version: str = "1.0.0") -> bool:
        """Отправляет уведомление о запуске приложения"""
        if not self.is_configured:
            return False
            
        message = (
            "🚀 *AIChat приложение запущено*\n\n"
            f"• *Версия:* `{version}`\n"
            f"• *Статус:* ✅ Работает\n\n"
            "_Система уведомлений активирована_"
        )
        
        return self._send_telegram_message(message)

    def send_error_notification(self, error_message: str) -> bool:
        """Отправляет уведомление об ошибке"""
        if not self.is_configured:
            return False
            
        message = (
            "❌ *Ошибка в AIChat приложении*\n\n"
            f"• *Ошибка:* `{error_message[:100]}...`\n"
            f"• *Статус:* ⚠️ Требуется внимание\n\n"
            "_Проверьте логи приложения_"
        )
        
        return self._send_telegram_message(message)

    def _send_telegram_message(self, message: str) -> bool:
        """Внутренняя функция отправки сообщения в Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Telegram notification sent to chat {self.chat_id}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram notification: {e}")
            return False

# Синглтон экземпляр для использования во всем приложении
telegram_notifier = TelegramNotifier()

def check_and_notify_low_balance(balance: float, threshold: float = 1.0) -> bool:
    """
    Проверяет баланс и отправляет уведомление если необходимо
    
    Args:
        balance: текущий баланс
        threshold: порог для уведомления
        
    Returns:
        bool: True если уведомление отправлено, False если нет
    """
    return telegram_notifier.send_low_balance_notification(balance, threshold)

def notify_startup(version: str = "1.0.0") -> bool:
    """Отправляет уведомление о запуске приложения"""
    return telegram_notifier.send_startup_notification(version)

def notify_error(error_message: str) -> bool:
    """Отправляет уведомление об ошибке"""
    return telegram_notifier.send_error_notification(error_message)
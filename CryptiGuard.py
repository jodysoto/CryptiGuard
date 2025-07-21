import requests
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Конфигурация
API_URL = 'https://api.blockcypher.com/v1/btc/main/addrs/'
SUSPECTED_ADDRESSES = ['1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', '1QHj1Qh7WqGRg8BdPH2b8oCmMjP5DGoYte']  # Пример подозрительных адресов
MONITOR_INTERVAL = 600  # Интервал проверки в секундах (10 минут)
ALERT_EMAIL = "your-email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_PASSWORD = "your-email-password"

# Функция для получения информации о транзакциях
def get_wallet_info(wallet_address):
    response = requests.get(f'{API_URL}{wallet_address}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении данных для {wallet_address}")
        return None

# Функция для отправки email-уведомлений
def send_alert_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = ALERT_EMAIL
    msg['To'] = ALERT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(ALERT_EMAIL, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(ALERT_EMAIL, ALERT_EMAIL, text)

# Функция для мониторинга кошелька
def monitor_wallet(wallet_address):
    wallet_data = get_wallet_info(wallet_address)
    if wallet_data:
        for tx in wallet_data.get('txs', []):
            if tx.get('addresses')[0] in SUSPECTED_ADDRESSES:
                send_alert_email(
                    subject=f"Подозрительная транзакция на кошельке {wallet_address}",
                    body=f"Обнаружена подозрительная транзакция на адресе {wallet_address}.\n\nТранзакция: {json.dumps(tx, indent=4)}"
                )

# Основной цикл
def start_monitoring():
    wallets_to_monitor = ['1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', '1QHj1Qh7WqGRg8BdPH2b8oCmMjP5DGoYte']  # Пример адресов
    while True:
        for wallet in wallets_to_monitor:
            monitor_wallet(wallet)
        time.sleep(MONITOR_INTERVAL)

if __name__ == '__main__':
    start_monitoring()

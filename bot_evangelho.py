import logging
import os
import random
import nest_asyncio
from PyPDF2 import PdfReader
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Aplicar nest_asyncio para permitir loops de evento aninhados
nest_asyncio.apply()

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Variáveis de configuração
TOKEN = os.getenv('TELEGRAM_TOKEN')  # Obter o token do bot a partir de variáveis de ambiente
PDF_FILE_PATH = './evangelho.pdf'  # Nome do arquivo PDF que será carregado

def read_pdf(file_path):
    """Lê o PDF e retorna o texto em uma lista de parágrafos."""
    text = []
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text.append(page.extract_text())
    return "\n".join(text).split("\n\n")  # Divide o texto em parágrafos

# Carregar o conteúdo do PDF
try:
    paragraphs = read_pdf(PDF_FILE_PATH)
except Exception as e:
    logging.error(f"Erro ao ler o arquivo PDF: {str(e)}")
    paragraphs = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem quando o comando /start é emitido."""
    await update.message.reply_text('Olá! Eu sou o bot do Evangelho. Use /leitura para receber um trecho do livro.')

async def leitura(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia um trecho aleatório do Evangelho."""
    if paragraphs:
        reading = random.choice(paragraphs)
        await update.message.reply_text(reading)
    else:
        await update.message.reply_text("Desculpe, não consegui encontrar nenhum trecho no livro.")

def main() -> None:
    """Inicia o bot."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Adiciona manipuladores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("leitura", leitura))

    # Inicia o bot, executando em modo polling
    application.run_polling()

# Ponto de entrada do programa
if name == 'main':
    main()

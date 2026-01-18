import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Configuración básica de logging (para ver errores en la consola)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Función asíncrona para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 'update' trae la información del mensaje que llegó
    # 'context' tiene herramientas útiles del bot
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="¡Hola! Soy un bot hecho con python-telegram-bot. Escríbeme algo."
    )

# 2. Función asíncrona para responder a texto (Eco)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_recibido = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Dijiste: {mensaje_recibido}"
    )

if __name__ == '__main__':
    # Pon tu TOKEN real aquí
    TOKEN = '8351664150:AAHTeFZyQkWObVDCst_JgNwCTbYiHxLKp4M'
    
    # Construimos la aplicación
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Añadimos los "Manejadores" (Handlers)
    # Maneja el comando /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    # Maneja texto que NO sea un comando
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    # Inicia el bot
    print("El bot se está ejecutando...")
    application.run_polling()
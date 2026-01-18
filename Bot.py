import logging
import google.generativeai as genai
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# --- CONFIGURACIÓN ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# Configuración de Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuración de Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-flash-lite-latest',
    system_instruction="""
    Eres un asistente educativo experto en salud cardiovascular.
    Tu objetivo es proveer información clara y calmada.
    IMPORTANTE: Si el usuario pregunta por síntomas graves, recuérdale llamar a emergencias.
    Siempre aclara que eres una IA y no un médico.
    """
)

# --- DEFINICIÓN DEL TECLADO ---
# Creamos el diseño de los botones
# 'resize_keyboard=True' hace que los botones no ocupen media pantalla
bot_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🚨 EMERGENCIA 🚨")], # Botón grande arriba
        [KeyboardButton("Ver Síntomas"), KeyboardButton("Prevención")] # Dos botones abajo
    ],
    resize_keyboard=True
)

# --- FUNCIONES DEL BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Hola {user}. Soy tu asistente sobre el infarto al miocardio.\n\n"
             "Usa los botones de abajo para navegar o escribe tu duda directamente.",
        reply_markup=bot_keyboard  # <--- AQUÍ ACTIVAMOS LOS BOTONES
    )

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    # 1. LÓGICA DE EMERGENCIA (Prioridad Alta)
    # Detectamos si presionó el botón de emergencia
    if "EMERGENCIA" in user_text:
        mensaje_urgente = (
            "🔴 **¡ACTÚA RÁPIDO!** 🔴\n\n"
            "Si crees que tú o alguien más está sufriendo un infarto:\n"
            "1️⃣ **Llama al 911** (o tu número local de emergencias) INMEDIATAMENTE.\n"
            "2️⃣ Si la persona no es alérgica, dale una aspirina (masticada es mejor).\n"
            "3️⃣ Afloja la ropa apretada y mantén la calma.\n\n"
            "⚠️ *No conduzcas al hospital tú mismo si es posible.*"
        )
        await context.bot.send_message(chat_id=chat_id, text=mensaje_urgente, parse_mode='Markdown')
        return # Terminamos aquí, no le preguntamos a Gemini para ahorrar tiempo

    # 2. LÓGICA GENERAL (Gemini)
    # Si no es emergencia, dejamos que Gemini responda
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        # Contextualizamos un poco la entrada si viene de un botón simple
        prompt = user_text
        if user_text == "Ver Síntomas":
            prompt = "¿Cuáles son los síntomas comunes y los síntomas silenciosos de un infarto?"
        elif user_text == "Prevención":
            prompt = "Dame 5 consejos clave para prevenir un infarto al miocardio."

        response = await model.generate_content_async(prompt)
        
        await context.bot.send_message(
            chat_id=chat_id, 
            text=response.text, 
            parse_mode='Markdown',
            reply_markup=bot_keyboard # Mantenemos el teclado visible
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Error de conexión. Intenta de nuevo.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensajes))
    
    print("Bot Cardíaco con Emergencia Activo...")
    application.run_polling()
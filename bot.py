import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# 1. Configurações Iniciais e Chaves
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

# Personalidade da IA (Agora com a Regra 4 para formatação HTML)
instrucao_tutor = (
    "Você é o 'Tutor Digital', um assistente virtual paciente e amigável. "
    "Seu objetivo é ensinar tecnologia básica para pessoas com baixo domínio tecnológico. "
    "Regras: "
    "1. Use frases curtas e palavras muito simples. "
    "2. Sempre faça analogias com o mundo físico (ex: 'A nuvem é como um armário alugado na internet'). "
    "3. Nunca use palavras em inglês (como download, link, browser) sem explicar o que significam. "
    "4. IMPORTANTE: Para colocar palavras em negrito, use formatação HTML (ex: <b>palavra</b>). NUNCA use asteriscos (**)."
)

# 2. Funções de Banco de Dados (Memória do Bot)
def iniciar_db():
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            papel TEXT,
            conteudo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_mensagem(user_id, papel, conteudo):
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO historico (user_id, papel, conteudo) VALUES (?, ?, ?)', (user_id, papel, conteudo))
    conn.commit()
    conn.close()

def buscar_historico(user_id, limite=5):
    conn = sqlite3.connect('tutor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT papel, conteudo FROM historico WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limite))
    linhas = cursor.fetchall()
    conn.close()
    return [{"role": papel, "parts": [{"text": conteudo}]} for papel, conteudo in reversed(linhas)]

# 3. Menu Inicial com Nova Identidade
async def comando_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    teclado = [
        ["📱 Como usar o WhatsApp", "🌐 O que é Internet?"], 
        ["🔒 Dicas de Segurança"]                         
    ]
    interface_botoes = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    
    mensagem_boas_vindas = (
        "Olá! Que alegria ter você aqui. Eu sou o seu <b>Tutor Digital</b>. 🤖\n\n"
        "Estou aqui para te ajudar a usar o celular e a internet sem complicação. "
        "Não tenha medo de apertar nada, estamos aqui para aprender juntos!\n\n"
        "Você pode falar comigo do jeito que achar mais fácil:\n\n"
        "👆 <b>Tocando</b> nos botões aqui embaixo\n"
        "⌨️ <b>Digitando</b> a sua dúvida\n"
        "🎤 Mandando um <b>áudio</b> (como no WhatsApp)\n"
        "📸 Enviando uma <b>foto</b> de algo que não entendeu\n\n"
        "Como eu posso te ajudar hoje?"
    )
    
    await update.message.reply_text(mensagem_boas_vindas, reply_markup=interface_botoes, parse_mode=ParseMode.HTML)

# 4. Processa Texto
async def responder_texto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    texto_recebido = update.message.text

    if texto_recebido == "📱 Como usar o WhatsApp":
        resposta = "O WhatsApp é como um correio super rápido. Você pode mandar mensagens de texto, áudios e fotos. Quer aprender a mandar um áudio?"
        await update.message.reply_text(resposta)
        return
    elif texto_recebido == "🌐 O que é Internet?":
        resposta = "A Internet é como uma grande estrada invisível que conecta todos os celulares do mundo, permitindo que a gente converse e veja vídeos mesmo estando longe."
        await update.message.reply_text(resposta)
        return
    elif texto_recebido == "🔒 Dicas de Segurança":
        resposta = "Regra de ouro: nunca passe senhas ou códigos que chegam por SMS para ninguém, nem mesmo se a pessoa disser que é do banco."
        await update.message.reply_text(resposta)
        return

    salvar_mensagem(user_id, "user", texto_recebido)
    historico = buscar_historico(user_id)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    try:
        resposta_ia = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=historico,
            config=types.GenerateContentConfig(system_instruction=instrucao_tutor)
        )
        resposta = resposta_ia.text
        salvar_mensagem(user_id, "model", resposta)
    except Exception as e:
        print(f"Erro no texto: {e}")
        resposta = "Desculpe, minha memória falhou um pouquinho. Pode me perguntar de novo?"

    # Adicionado parse_mode=ParseMode.HTML
    await update.message.reply_text(resposta, parse_mode=ParseMode.HTML)    

# 5. Processa Áudio
async def responder_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    msg_temp = await update.message.reply_text("🎧 Estou ouvindo o seu áudio...")
    
    try:
        arquivo_id = update.message.voice.file_id
        arquivo_telegram = await context.bot.get_file(arquivo_id)
        caminho_local = f"{arquivo_id}.ogg"
        await arquivo_telegram.download_to_drive(caminho_local)

        arquivo_ia = client.files.upload(file=caminho_local)
        salvar_mensagem(user_id, "user", "[Áudio enviado pelo usuário]")

        resposta_ia = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=["Ouça este áudio e responda à dúvida do usuário de forma simples.", arquivo_ia],
            config=types.GenerateContentConfig(system_instruction=instrucao_tutor)
        )
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg_temp.message_id)
        os.remove(caminho_local)
        
        resposta = resposta_ia.text
        salvar_mensagem(user_id, "model", resposta)
        
        # Adicionado parse_mode=ParseMode.HTML
        await update.message.reply_text(resposta, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        print(f"Erro no áudio: {e}")
        await update.message.reply_text("Puxa, tive um probleminha para ouvir. Pode tentar gravar de novo?")

# 6. Processa Imagens/Prints de Tela
async def responder_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    msg_temp = await update.message.reply_text("👀 Estou olhando a sua imagem...")

    try:
        arquivo_id = update.message.photo[-1].file_id
        arquivo_telegram = await context.bot.get_file(arquivo_id)
        caminho_local = f"{arquivo_id}.jpg"
        await arquivo_telegram.download_to_drive(caminho_local)

        arquivo_ia = client.files.upload(file=caminho_local)
        legenda = update.message.caption or "Analise esta imagem. Se for um ícone ou tela de celular, explique para que serve de forma bem simples."
        
        salvar_mensagem(user_id, "user", f"[Imagem enviada pelo usuário. Legenda: {legenda}]")

        resposta_ia = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[legenda, arquivo_ia],
            config=types.GenerateContentConfig(system_instruction=instrucao_tutor)
        )

        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg_temp.message_id)
        os.remove(caminho_local)

        resposta = resposta_ia.text
        salvar_mensagem(user_id, "model", resposta)
        
        # Adicionado parse_mode=ParseMode.HTML
        await update.message.reply_text(resposta, parse_mode=ParseMode.HTML)

    except Exception as e:
        print(f"Erro na imagem: {e}")
        await update.message.reply_text("Puxa, minha visão embaçou um pouco e não consegui ver a imagem. Pode tentar mandar de novo?")

# 7. Liga o bot
def main() -> None:
    iniciar_db()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", comando_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_texto))
    app.add_handler(MessageHandler(filters.VOICE, responder_audio))
    app.add_handler(MessageHandler(filters.PHOTO, responder_imagem))

    print("🤖 Tutor Digital 100% Completo rodando! (Formatação HTML corrigida)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
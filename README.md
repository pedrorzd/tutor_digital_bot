# 🤖 Tutor Digital

Um assistente virtual no Telegram focado em alfabetização e inclusão digital, desenvolvido para ajudar pessoas com baixo domínio tecnológico a usarem seus celulares e a internet sem medo.

## 🎯 Sobre o Projeto

O **Tutor Digital** é um projeto estudantil que atua como um amigo paciente e didático. Seu diferencial é o uso de Inteligência Artificial para traduzir o "tecniquês" em linguagem acessível, utilizando analogias do mundo físico e frases curtas. 

Para quebrar a principal barreira da exclusão digital (a dificuldade de digitação e navegação), o bot foi construído com arquitetura **100% multimodal**, permitindo que o usuário interaja da forma que achar mais natural.

## ✨ Funcionalidades

* **🧠 Inteligência Adaptativa:** Respostas geradas dinamicamente com formatação amigável (HTML) e linguagem simplificada.
* **🎤 Suporte a Áudio:** O usuário pode enviar mensagens de voz, e o bot compreende a dúvida nativamente.
* **📸 Visão Computacional:** É possível enviar "prints" (capturas de tela) ou fotos de ícones desconhecidos para que o bot explique para que servem.
* **💾 Memória de Contexto:** Utiliza SQLite para lembrar das últimas interações do usuário, mantendo uma conversa contínua e pedagógica.
* **🧭 Onboarding Guiado:** Botões interativos de resposta rápida para as dúvidas mais comuns (WhatsApp, Internet, Segurança).

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Inteligência Artificial:** Google Gemini API (`gemini-2.5-flash`) via `google-genai`
* **Interface:** API do Telegram via `python-telegram-bot`
* **Banco de Dados:** SQLite (nativo do Python)

## 🚀 Como Executar o Projeto

### Pré-requisitos
Você precisará ter o [Python](https://www.python.org/) instalado em sua máquina e contas ativas no Telegram e no Google AI Studio.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/pedrorzd/tutor_digital_bot.git](https://github.com/pedrorzd/tutor_digital_bot.git)
   cd tutor-digital-bot
Crie e ative o ambiente virtual:

No Linux/macOS:

Bash
python3 -m venv venv
source venv/bin/activate
No Windows:

Bash
python -m venv venv
venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Configure as Variáveis de Ambiente:

Renomeie o arquivo .env.example para .env.

Insira suas chaves de API:

TELEGRAM_TOKEN: Obtido através do @BotFather no Telegram.

GEMINI_API_KEY: Obtida no Google AI Studio.

Inicie o Bot:

Bash
python bot.py
O bot exibirá a mensagem "🤖 Tutor Digital 100% Completo rodando!" no terminal e já estará pronto para responder no Telegram.

🤝 Autor
Desenvolvido por Pedro Rodrigues.
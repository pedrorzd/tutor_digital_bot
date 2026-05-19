# Descritivo do Projeto: Tutor Digital

## 🎯 Público-Alvo
O projeto foi desenvolvido pensando em pessoas com **baixo domínio tecnológico** (como idosos, iniciantes no uso de smartphones ou pessoas com pouco acesso à educação digital). O bot adota uma linguagem extremamente simples, paciente e amigável, evitando jargões técnicos e estrangeirismos sem explicação prévia.

## 💡 Utilidade e Objetivo
O **Tutor Digital** é um assistente virtual criado para promover a inclusão digital. Seu objetivo principal é ensinar o básico de tecnologia, como o uso da internet, redes sociais (ex: WhatsApp) e boas práticas de segurança online. O bot faz uso constante de analogias com o mundo físico (ex: "A nuvem é como um armário alugado na internet") para facilitar a compreensão de conceitos abstratos, tornando a tecnologia mais acessível para todos.

## 🤝 Facilidade de Uso
A interface de comunicação foi pensada para ser a mais acessível possível, rodando diretamente no **Telegram**. Isso elimina a necessidade de instalar aplicativos complexos. Além disso, o usuário pode interagir da maneira que se sentir mais confortável:
- **Botões interativos**: Respostas prontas para dúvidas comuns.
- **Texto**: Digitando perguntas livremente.
- **Áudio**: Enviando mensagens de voz (ideal para quem tem dificuldade com digitação).
- **Imagens**: Enviando prints de tela ou fotos para que o bot analise e explique o que está na tela.

## ⚙️ Funções Implementadas

O bot foi construído em Python, integrando a biblioteca `python-telegram-bot` e a API do **Google Gemini** para inteligência artificial, além de possuir um banco de dados local (SQLite) para manter o contexto das conversas. 

As principais funções do sistema são:

### 1. Sistema de Memória (Banco de Dados)
- **`iniciar_db`**, **`salvar_mensagem`** e **`buscar_historico`**: Implementação de um banco de dados SQLite (`tutor.db`) que armazena o histórico de conversas de cada usuário. Isso permite que a IA lembre do contexto da conversa, proporcionando um diálogo contínuo e mais natural.

### 2. Menu Inicial e Boas-Vindas
- **`comando_start`**: Disparada ao iniciar o bot (`/start`). Apresenta o assistente, explica como utilizá-lo (texto, áudio, foto) e exibe um teclado interativo com opções rápidas de aprendizagem (Como usar o WhatsApp, O que é Internet, Dicas de Segurança).

### 3. Processamento de Texto Adaptativo
- **`responder_texto`**: Recebe a mensagem de texto do usuário. Se for uma das opções do menu rápido, devolve uma resposta direta. Caso contrário, salva a mensagem, recupera o histórico do banco de dados e consulta a IA (modelo `gemini-2.5-flash`) orientada por um forte *prompt* de sistema ("system instruction") para garantir a personalidade didática, devolvendo a resposta formatada ao usuário.

### 4. Suporte a Mensagens de Voz (Áudio)
- **`responder_audio`**: Escuta as dúvidas faladas. A função faz o download do áudio enviado pelo usuário no Telegram, faz o upload diretamente para o Google Gemini e pede para que a IA processe a dúvida falada e responda em texto, de forma simples e acolhedora.

### 5. Análise de Imagens e Prints (Visão Computacional)
- **`responder_imagem`**: Processa fotos ou capturas de tela. O usuário pode mandar o print de um aplicativo, e o bot baixa a imagem, envia ao Gemini junto com a legenda da dúvida e explica, passo a passo, a função dos ícones ou telas mostradas.

---
*Este arquivo foi gerado automaticamente para auxiliar na formatação e documentação do projeto.*
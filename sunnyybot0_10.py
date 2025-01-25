from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler,filters,ContextTypes
#import asyncio
#import nest_asyncio
import torch


import transformers

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

pipeline = transformers.pipeline(
    "text-generation",
    model="microsoft/phi-4",
    model_kwargs={"torch_dtype": "auto"},
    device_map="auto",
)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

TOKEN: Final = '7383969203:AAFtDgt-YhqPkaUWWh0RgFPtKSvbLtnA1js'
BOT_USERNAME: Final = 'Sunnyy1_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! :)')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a help command!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

system_message = {"role": "system", "content": "You are a friendly chatbot that wants to help"}

def create_message(input_text):
    # Create the messages list dynamically
    messages = [
        system_message,  # Initial system message
        {"role": "user", "content": input_text}  # User input
    ]
    return messages


def handle_response(text: str) -> str:
    try:
        #input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cuda")
        #outputs = model.generate(input_ids)
        #return tokenizer.decode(outputs[0])
        #messages = [
        #    {"role": "system", "content": "You are a medieval knight and must provide explanations to modern people."},
        #    {"role": "user", "content": "How should I explain the Internet?"},
        #]
        messages = create_message(text)
        outputs = pipeline(messages, max_new_tokens=128)
        return(outputs[0]["generated_text"][-1])
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't process that. Please try again!"
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}; "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:',response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TOKEN).build()

    '''comands'''
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    '''messages'''
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    '''errors'''
    app.add_error_handler(error)
    '''polling'''
    print('polling')
    app.run_polling(poll_interval=5)
 
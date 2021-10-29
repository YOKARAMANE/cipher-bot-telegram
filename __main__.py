import json
import os
import importlib

import telebot
from telebot import types

CURRENT_FOLDER = os.path.normpath(os.path.dirname(__file__))



codes = {}
roomStates = {}


def numberEncoder(num):
    numbers = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']
    result = ''
    for letter in str(num):
        result += numbers[int(letter)]
    return result


for filename in os.listdir(os.path.join(CURRENT_FOLDER, 'codes')):
    if filename[-3:] == '.py':
        module = importlib.import_module(f'codes.{filename[:-3]}')
        if hasattr(module, 'CODE_NAME'):
            index = len(codes.keys()) + 1
            codes[module.CODE_NAME] = {
                "index" : index,
                "encode" : module.encodeHandler,
                "decode" : module.decodeHandler,
                "info" : module.infoHandler,
                "buttonText" : f'{numberEncoder(index)} {module.CODE_NAME}',
                "prompt" : getattr(module, 'PROMPT_MESSAGE', dict())
            }

def mainHandler(bot, message):
    try:
        roomState = roomStates[message.chat.id]
        # text = f'пытаюсь {roomState["actualPhase"]} по {roomState["actualCode"]} сообщение "{message.text}"'
        # send = bot.send_message(message.chat.id,text)
        send = codes[roomState["actualCode"]][roomState["actualPhase"]](bot, message)
        return send 
    except Exception:
        send = bot.send_message(message.chat.id, "При расшифровке возникла ошибка")
        return send

def infoHandler(bot, message):
    roomState = roomStates[message.chat.id]
    send = codes[roomState["actualCode"]]["info"](bot, message)
    return send 


def codeRequest(bot, message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = []
    index = 0
    for codeName in codes.keys():
        index += 1
        items.append(codes[codeName]["buttonText"])
    markup.add(*items)
    send = bot.send_message(message.chat.id,'Выберите шифр',reply_markup=markup)
    bot.register_next_step_handler(send, lambda message: codeResponse(bot, message))

def codeResponse(bot, message):
    if message.text in set(codes[codeName]["buttonText"] for codeName in codes):
        selectedCode = message.text[message.text.find(' ') + 1:]
        roomStates[message.chat.id]["actualCode"] = selectedCode
        roomStates[message.chat.id]["actualPhase"] = None
        send = bot.send_message(message.chat.id, f'выбрана кодировка {selectedCode}')
        encodeDecodeRequest(bot, message)
    else:
        # if roomStates[message.chat.id]["actualCode"] is None:
        send = bot.send_message(message.chat.id, 'Не понял кодировку')
        bot.register_next_step_handler(send, lambda message: codeResponse(bot, message))
    
             
def encodeDecodeRequest(bot, message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = {
        f'🔒 зашифровать' : "encode",
        f'🔓 расшифровать' : "decode",
        f'ℹ️ информация' : "info",
        f'🔄 смена кодировки' : "back"
    }

    buttons = list(items.keys())  
    
    markup.add(*buttons[:2])
    markup.add(*buttons[2:])
    send = bot.send_message(message.chat.id,'Хотите заштфорвать или расшифровать?',reply_markup=markup)
    bot.register_next_step_handler(send, lambda message: encodeDecodeResponse(bot, message, items))

def encodeDecodeResponse(bot, message, items):
    if message.text in set(items.keys()):
        if items[message.text] == 'back':
            return codeRequest(bot, message)
        elif items[message.text] == 'encode':
            roomStates[message.chat.id]["actualPhase"] = "encode"
            text = f'Теперь вводите сообщения, которые надо зашифровать'
            if "encode" in codes[roomStates[message.chat.id]["actualCode"]]["prompt"]:
                text += '\n' + codes[roomStates[message.chat.id]["actualCode"]]["prompt"]["encode"]
            send = bot.send_message(message.chat.id, text)
        elif items[message.text] == 'decode':
            roomStates[message.chat.id]["actualPhase"] = "decode"
            text = f'Теперь вводите сообщения, которые надо расшифровать'
            if "decode" in codes[roomStates[message.chat.id]["actualCode"]]["prompt"]:
                text += '\n' + codes[roomStates[message.chat.id]["actualCode"]]["prompt"]["decode"]
            send = bot.send_message(message.chat.id, text)
        elif items[message.text] == 'info':
            send = infoHandler(bot, message)
        else:
            send = bot.send_message(message.chat.id, f'Что-то пошло не так, в этой ветке условий я оказаться не должен был')
    else:
        if roomStates[message.chat.id]["actualPhase"] is None:
            send = bot.send_message(message.chat.id, f'Сначала давайте определися: Хотите заштфорвать или расшифровать?')
        else:
            send = mainHandler(bot, message)
    
    bot.register_next_step_handler(send, lambda message: encodeDecodeResponse(bot, message, items))

def useBot(config):
    bot = telebot.TeleBot(config["apiKey"])
   
    @bot.message_handler(commands=["start"])
    def start(message):
        print('bot started. room:', message.chat)
        roomStates[message.chat.id] = {
            "actualCode" : None,
            "actualPhase" : None
        }
        codeRequest(bot, message)
    
    print('бот запущен, ожидаю')
    bot.polling()


if __name__ == '__main__':
    with open(os.path.join(CURRENT_FOLDER, 'config.json'), 'r', encoding='utf-8') as configFile:
        config = json.load(configFile) 
    useBot(config)
    #print(codes)
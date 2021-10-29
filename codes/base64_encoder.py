import base64


CODE_NAME = 'base64'

DEFAULT_ENCODING = 'utf-8'

def encode(msg, encoding=DEFAULT_ENCODING):
    return base64.b64encode(msg.encode(encoding=encoding)).decode(encoding=encoding)

def decode(msg, encoding=DEFAULT_ENCODING):
    return base64.b64decode(msg).decode(encoding=encoding)


def encodeHandler(bot, message):
    return bot.send_message(message.chat.id, encode(message.text))

def decodeHandler(bot, message):
    return bot.send_message(message.chat.id, decode(message.text))

def infoHandler(bot, message):
    #return bot.send_message(message.chat.id, "Тут должно было быть описание base64,\n но его сперли гномы")
    return bot.send_photo(message.chat.id, photo=open('img\Base64.png', 'rb'), 
        caption="""Base64 — стандарт кодирования двоичных данных при помощи только 64 символов ASCII. Алфавит кодирования содержит текстово-цифровые латинские символы A-Z, a-z и 0-9 (62 знака) и 2 дополнительных символа, зависящих от системы реализации. Каждые 3 исходных байта кодируются 4 символами (увеличение на ¹⁄₃).

Эта система широко используется в электронной почте для представления бинарных файлов в тексте письма (транспортное кодирование).""")

if __name__ == '__main__':
    msg = 'У попа была собака ©'

    encoded = encode(msg)
    decoded = decode(encoded)
    print("зашифровано:", encoded)
    print("расшифровано:", decoded)
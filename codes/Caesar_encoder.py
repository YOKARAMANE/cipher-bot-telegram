alphabet = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 
    'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 
    'abcdefghijklmnopqrstuvwxyz', 
    'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    ]

CODE_NAME = 'Шифр цезаря'
PROMPT_MESSAGE = {
    "encode" : "Вы можете отправить боту запросы в следующем формате: РУДН 5 — шифрование текста с шагом смещения 5",
    "decode" : "Вы можете отправить боту запросы в следующем формате: ХШИТ 5 — дешифровка текста с шагом смещения 5"
}


def encodeLetter(letter, key):
    for subAlphabet in alphabet:
        index = subAlphabet.find(letter)
        if index != -1:
            return subAlphabet[(index + key) % len(subAlphabet)]
    return letter


def decodeLetter(letter, key):
    for subAlphabet in alphabet:
        index = subAlphabet.find(letter)
        if index != -1:
            return subAlphabet[(index + len(subAlphabet) - key) % len(subAlphabet)]
    return letter

def encode(msg, key=1):
    return ''.join(encodeLetter(letter, key) for letter in msg)

def decode(msg, key=1):
    return ''.join(decodeLetter(letter, key) for letter in msg)

def encodeHandler(bot, message):
    cmd = message.text.split(' ')
    if len(cmd) < 2:
        return bot.send_message(message.chat.id, "Вы не указали параметры шифрования!\nПример: РУДН 5")
    else:
        key = int(cmd[-1])
        return bot.send_message(message.chat.id, encode(' '.join(cmd[:-1]), key=key))

def decodeHandler(bot, message):
    cmd = message.text.split(' ')
    if len(cmd) < 2:
        return bot.send_message(message.chat.id, "Вы не указали параметры шифрования!\nПример: ХШИТ 5")
    else:
        key = int(cmd[-1])
        return bot.send_message(message.chat.id, decode(' '.join(cmd[:-1]), key=key))

def infoHandler(bot, message):
    return bot.send_photo(message.chat.id, photo=open('img\Caesar.png', 'rb'), caption="Шифр Цезаря — это вид шифра подстановки, в котором каждый символ в открытом тексте заменяется символом, находящимся на некотором постоянном числе позиций левее или правее него в алфавите. Например, в шифре со сдвигом вправо на 3, А была бы заменена на Г, Б станет Д, и так далее. \n\nШифр назван в честь римского полководца Гая Юлия Цезаря, использовавшего его для секретной переписки со своими генералами.")

if __name__ == '__main__':
    msg = 'У попа была собака ©'

    encoded = encode(msg)
    decoded = decode(encoded)
    print("зашифровано:", encoded)
    print("расшифровано:", decoded)
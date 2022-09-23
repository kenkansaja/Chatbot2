import telebot
from telebot import types
from database import Database
from config import TOKEN

db = Database('db.db')
bot = telebot.TeleBot(f'{TOKEN}')

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Cari teman')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Set Profil')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Berhenti Mencari')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Cowok 👨')
    item2 = types.KeyboardButton('Cewek 👩‍🦱')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Hallo, {0.first_name}! Selamat datang di obrolan anonim! Silakan masukkan jenis kelamin Anda! '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Cari teman')
    markup.add(item1)

    bot.send_message(message.chat.id, '📝 Menu'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Dialog berikutnya')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌ Pihak lain telah meninggalkan obrolan', reply_markup = markup)
        bot.send_message(message.chat.id, '❌ Anda telah meninggalkan obrolan', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌Anda tidak berada di obrolan', reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Cari teman' or message.text == '✏️ Dialog berikutnya':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔎 Cowok')
            item2 = types.KeyboardButton('🔎 Cewek')
            item3 = types.KeyboardButton('👩‍👨 Acak')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Siapa yang harus dicari', reply_markup = markup)

            
        elif message.text == '❌ Berhenti Mencari':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Pencarian dihentikan, ketik /menu', reply_markup = main_menu())

        
        elif message.text == '🔎 Cowok':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari teman', reply_markup = stop_search())
            else:
                mess = 'Teman ditemukan! Untuk menghentikan dialog ketik /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Cewek':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari teman', reply_markup = stop_search())
            else:
                mess = 'Teman ditemukan! Untuk menghentikan dialog ketik /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '👩‍👨 Acak':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Cari teman', reply_markup = stop_search())
            else:
                mess = 'Teman ditemukan! Untuk menghentikan dialog ketik /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Set Profil':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Anda mengatakan profil Anda')
                else:
                    bot.send_message(message.chat.id, '❌Akun Anda tidak memiliki nama pengguna')
            else:
                bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')

        

        elif message.text == 'Cowok 👨':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ Jenis kelamin Anda telah berhasil ditambahkan!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Anda sudah memasukkan jenis kelamin Anda')
        
        elif message.text == 'Cewek 👩‍🦱':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ Jenis kelamin Anda telah berhasil ditambahkan!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id, '❌ Anda sudah memasukkan jenis kelamin Anda')
        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')

@bot.message_handler(content_types='video')
def bot_video(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_video(chat_info[1], message.video.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')

@bot.message_handler(content_types='photo')
def bot_photo(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_photo(chat_info[1], message.photo.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')


@bot.message_handler(content_types='animation')
def bot_animation(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_animation(chat_info[1], message.animation.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')

@bot.message_handler(content_types='audio')
def bot_audio(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_audio(chat_info[1], message.audio.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Anda tidak berada dalam obrolan')


bot.polling(none_stop = True)

# Copyright (C) 2020-2021 by kenkansaja@Github, < https://github.com/kenkansaja >.
#
# This file is part of < https://github.com/kenkansaja/Chatbot2 > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/kenkansaja/Chatbot2/blob/master/LICENSE >
# https://t.me/pySmartDL
#
# All rights reserved.

import telebot
from telebot import types
from database import *
import os
import time
import pytz
from datetime import datetime
from config import GROUP, OWNER, CHANNEL, TOKEN


bot = telebot.TeleBot(f'{TOKEN}')


class User:  
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = None
        self.age = None
        self.sex = None
        self.change = None


user_dict = {}  

@bot.message_handler(commands=['start'])
def welcome(message):
    if check_user(user_id=message.from_user.id)[0]:
        mark = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mark.add('🔍 Cari Pasangan')
        mark.add('📰 Info Profile', '🗑 Hapus Profile')
        me = bot.get_me()
        bot.send_message(message.from_user.id, f"*Selamat Bergabung Di {me.first_name}🙊*\n\n_Semoga Dapat teman atau jodoh_\n\n*NOTE:*\nWAJIB JOIN\n[👥 ɢʀᴏᴜᴘ](t.me/{GROUP}) | [ᴄʜᴀɴɴᴇʟ 📣](t.me/{CHANNEL}) | [📱ᴏᴡɴᴇʀ](t.me/{OWNER})",parse_mode="markdown",disable_web_page_preview=True, reply_markup=mark)
        bot.register_next_step_handler(message, search_prof)
    else:
        bot.send_message(message.from_user.id, "_👋Halo Pengguna Baru, Untuk Melanjutkan Isi Biodata Berikut!_",parse_mode="markdown")
        bot.send_message(message.from_user.id, "➡️ *Nama Kamu :*", parse_mode="markdown")
        bot.register_next_step_handler(message, reg_name)

@bot.message_handler(content_types=['text'])
def text_reac(message):  
    bot.send_message(message.chat.id, 'Tejadi Kesalahan\nSilahkan klik /start untuk mencoba lagi')

def reg_name(message):  
    if message.text != '':
        user = User(message.from_user.id)
        user_dict[message.from_user.id] = user
        user.name = message.text
        bot.send_message(message.from_user.id, "*Umur :*", parse_mode="markdown")
        bot.register_next_step_handler(message, reg_age)

    else:
        bot.send_message(message.from_user.id, "*Masukkan Nama Anda :*", parse_mode="markdown")
        bot.register_next_step_handler(message, reg_name)


def reg_age(message):  
    age = message.text
    if not age.isdigit():
        msg = bot.reply_to(message, '_Gunakan angka, Bukan Huruf!!_', parse_mode="markdown")
        bot.register_next_step_handler(msg, reg_age)
        return
    user = user_dict[message.from_user.id]
    user.age = age
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Pria👦', 'Wanita👩🏻')
    bot.send_message(message.from_user.id, '*Jenis Kelamin :*',parse_mode="markdown", reply_markup=markup)
    bot.register_next_step_handler(message, reg_sex)


def reg_sex(message):  
    sex = message.text
    user = user_dict[message.from_user.id]
    if (sex == 'Pria👦') or (sex == 'Wanita👩🏻'):
        user.sex = sex
        mark = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mark.add('Pria👦', 'Wanita👩🏻', 'Pria dan Wanita👀')
        bot.send_message(message.from_user.id, '*⏳Kamu ingin mencari pasangan :*',parse_mode="markdown", reply_markup=mark)
        bot.register_next_step_handler(message, reg_change)

    else:
        bot.send_message(message.from_user.id, '_Silahkan Klik Yang ada dikeyboard!_',parse_mode="markdown")
        bot.register_next_step_handler(message, reg_sex)


def reg_change(message):  
    if (message.text == 'Pria👦') or (message.text == 'Wanita👩🏻') or (message.text == 'Pria dan Wanita👀'):
        user = user_dict[message.from_user.id]
        user.change = message.text
        date1 = datetime.fromtimestamp(message.date, tz=pytz.timezone("asia/jakarta")).strftime("%d/%m/%Y %H:%M:%S").split()
        bot.send_message(message.from_user.id,
                         "🐱 - _BIODATA KAMU_ - 🐱\n\n*=> Nama :* " + str(user.name) + "\n*=> Umur :* " + str(user.age)+" Tahun" + "\n*=> Jenis Kelamin :* " + str(user.sex) + "\n*=> Tipe Pasangan :* " + str(user.change)+ "\n*=> Tedaftar Pada :\n        >Tanggal :* "+str(date1[0])+"\n    *    >Waktu :* "+str(date1[1])+" WIB", parse_mode="markdown")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Iya ✔️', 'Tidak ✖️')
        bot.send_message(message.from_user.id, "`Ingin Merubah Data diatas??`",parse_mode="markdown", reply_markup=markup)
        bot.register_next_step_handler(message, reg_accept)
    else:
        bot.send_message(message.from_user.id, 'Hanya Boleh Click Yang ada dikeyboard')
        bot.register_next_step_handler(message, reg_change)


def reg_accept(message):  
    if (message.text == 'Iya ✔️') or (message.text == 'Tidak ✖️'):
        if message.text == 'Iya ✔️':
            tw = types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, "*Masukkan Kembali🕹\nNama Kamu :*", parse_mode="markdown", reply_markup=tw)
            bot.register_next_step_handler(message, reg_name)
        else:
            if not check_user(user_id=message.from_user.id)[0]:
                user = user_dict[message.from_user.id]
                reg_db(user_id=user.user_id, name=user.name, old=user.age, gender=user.sex, change=user.change)
                bot.send_message(message.from_user.id, "_Berhasil...✅\nAccount Kamu Telah Terdaftar!_", parse_mode="markdown")
            else:
                if message.from_user.id in user_dict.keys():
                    user = user_dict[message.from_user.id]
                    edit_db(user_id=user.user_id, name=user.name, old=user.age, gender=user.sex, change=user.change)
            welcome(message)


def search_prof(message):  
    if (message.text == u'🔍 Cari Pasangan') or (message.text == u'📰 Info Profile') or (
            message.text == u'🗑 Hapus Profile'):
        if message.text == u'🔍 Cari Pasangan':
            bot.send_message(message.from_user.id, '🚀 Sedang mencari pasangan untukmu . . .')
            search_partner(message)
        elif message.text == u'📰 Info Profile':
            user_info = get_info(user_id=message.from_user.id)
            bot.send_message(message.from_user.id,
                             "📍Data Profile📍\n\n*Nama :* " + str(user_info[2]) +"\n*ID :* `"+str(message.from_user.id)+"`" +"\n*Umur :* " + str(
                                 user_info[3]) +" Tahun" + "\n*Jenis Kelamin :* " + str(user_info[4]) + "\n*Tipe Pasangan :* " + str(user_info[5]),parse_mode="markdown")
            mark = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            mark.add('Iya ✔️', 'Tidak ✖️')
            bot.send_message(message.from_user.id, '_Ingin Merubah Data Profil Kamu??_',parse_mode="markdown", reply_markup=mark)
            bot.register_next_step_handler(message, reg_accept)
        else:
            delete_user(user_id=message.from_user.id)
            tw = types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, '_Tunggu Sebentar..Sedang Menghapus Profile❗️_', parse_mode="markdown")
            bot.send_message(message.from_user.id, '_Berhasil..Profile Kamu Di Hapus✅_', parse_mode="markdown", reply_markup=tw)
            welcome(message)
    else:
        bot.send_message(message.from_user.id, 'Klik Yang ada dikeyboard')
        bot.register_next_step_handler(message, search_prof)


def search_partner(message): 
    is_open = check_open(first_id=message.from_user.id)
    if is_open[0][0]:  
        bot.register_next_step_handler(message, chat)

    else:
        select = select_free()
        success = False
        if not select:
            add_user(first_id=message.from_user.id)
        else:
            for sel in select:
                if check_status(first_id=message.from_user.id, second_id=sel[0]) or message.from_user.id == sel[0]:
                    print(message.from_user.id, 'Bergabung')
                    continue

                else:
                    print(sel[0])
                    print(message.from_user.id)
                    mark2 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                    mark2.add('❌ Exit')
                    add_second_user(first_id=sel[0], second_id=message.from_user.id)
                    user_info = get_info(user_id=sel[0])
                    bot.send_message(message.from_user.id,
                          "⚠️*Pasangan Di Temukan*", parse_mode="markdown",
                          reply_markup=mark2)
                    user_info = get_info(user_id=message.from_user.id)
                    bot.send_message(sel[0],
                          "⚠️*Pasangan Di Temukan*", parse_mode="markdown",
                          reply_markup=mark2)
                    success = True
                    break
        if not success:
            time.sleep(2)
            search_partner(message)
        else:
            bot.register_next_step_handler(message, chat)

def chat(message):  
    if message.text == "❌ Exit" or message.text == "/exit":
        mark1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        mark1.add('🔍 Cari Pasangan')
        mark1.add('📰 Info Profile', '🗑 Hapus Profile')
        companion = check_companion(first_id=message.from_user.id)
        bot.send_message(message.from_user.id, "_Kamu Meninggalkan Obrolan_",parse_mode="markdown", reply_markup=mark1)
        bot.send_message(companion, "_Pasangan kamu Meninggalkan Percakapan_", parse_mode="markdown", reply_markup=mark1)
        close_chat(first_id=message.from_user.id)
        welcome(message)
        return

    elif not check_open(first_id=message.from_user.id)[0][0]:
        welcome(message)
        return
    companion = check_companion(first_id=message.from_user.id)
    if message.sticker:
        bot.send_sticker(
                    companion, 
                    message.sticker.file_id
                )
    elif message.photo:
        file_id = None
        
        for item in message.photo:
            file_id = item.file_id
        bot.send_photo(
                    companion, file_id, 
                    caption=message.caption
                )
    elif message.video:
        bot.send_video(
                    companion,
                    message.video.file_id,
                    caption=message.caption,
                )
    elif message.audio:
        bot.send_audio(
                    companion,
                    message.audio.file_id,
                    caption=message.caption,
                )
    elif message.voice:
        bot.send_voice(
                    companion, 
                    message.voice.file_id
                )
    elif message.animation:
        bot.send_animation(
                    companion, 
                    message.animation.file_id
                )
    elif message.text:
        if (
            message.text != "/start"
            and message.text != "/exit"
        ):
            if message.reply_to_message is None:
                bot.send_message(companion, message.text)

            elif message.from_user.id != message.reply_to_message.from_user.id:
                bot.send_message(
                            companion,
                            message.text,
                            reply_to_message_id=message.reply_to_message.message_id - 1,
                           )
            else:
                bot.send_message(message.chat.id, "Anda tidak bisa membalas ke pesan anda sendiri")

    bot.register_next_step_handler(message, chat)

           

print("BOT SUDAH SIAP")
bot.polling()

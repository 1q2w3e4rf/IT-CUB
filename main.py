import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    reply = types.ReplyKeyboardMarkup()
    reply.add("Условия поступления")
    bot.send_photo(message.chat.id, open("KUB.jpg", "rb"))
    IT_VIDEO = open("IT.mp4", "rb")
    bot.send_video(message.chat.id, IT_VIDEO)
    bot.send_message(message.chat.id, "Привет! Я Telegram бот который расскажет тебе об центре образования IT Cube в Вязниках" )
    bot.send_message(message.chat.id, "Чтобы узнать о направлениях, сначала ознакомьтесь с условиями поступления", reply_markup=reply)

@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == "Условия поступления":
        reply = types.ReplyKeyboardMarkup()
        options = [
            "Программирование роботов",
            "Программирование на Python",
            "Программирование на Java",
            "Мобильная разработка",
            "Алгоритмика и логика",
            "Системное администрирование",
        ]
        options.sort()
        options.append("<Меню>")
        for option in options:
            reply.add(option)
        
        bot.send_message(message.chat.id, "- Обучение в центре по выбранному кубу – бесплатное по сертификату дополнительного образования детей;\n- места в бюджетном образовании ограничены (не более 400 мест);\n- Как получить сертификат: на портале 33.pfdo.ru - инструкция;\nвозраст обучающихся от 7 до 18 лет")
        bot.send_message(message.chat.id, "Мы предлагаем широкий спектр курсов, каждый из которых открывает новые горизонты и возможности:", reply_markup=reply)
    
    elif message.text == "Программирование роботов":
        media = [
            types.InputMediaPhoto(open("robot.jpg", "rb")),
            types.InputMediaPhoto(open("robot2.jpg", "rb")),
            types.InputMediaPhoto(open("day6.jpg", "rb"))
        ]
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Программирование роботов:\n\nРобототехника вводит учащихся в мир технологий, развивает навыки взаимодействия, самостоятельности при принятии решений, раскрывает их творческий потенциал.\nПрограмма «Программирование роботов» нацелена на изучение принципов программирования при помощи роботов, которых обучающиеся будут разрабатывать . Научаться создавать мобильных роботов и систем программирования на базе платформ Arduino и других. В ходе занимательного конструирования обучающиеся научатся ставить задачи и находить решения, получат базовые знания по программированию,  механике, электрике, проектированию ,на стыке которых находится современная робототехника.")

    elif message.text == "Программирование на Python":
        media = [
            types.InputMediaPhoto(open("python.jpg", "rb")),
            types.InputMediaPhoto(open("python2.jpg", "rb"))
        ]
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Программирование на Python:\n\nПростой и понятный синтаксис. 23 Команды легко читаются и напоминают обычную английскую речь. Например, чтобы прописать приветствие, используется строчка print (\"Hello\").\nВозможность создавать различные приложения. Дети могут создавать свои приложения от простого вывода «Hello World!» до разработки анимации и игр. \nРазвитие логических и алгоритмических навыков. В процессе изучения Python дети учатся планировать последовательности действий для решения задач, анализировать задачи и разбивать их на подзадачи, искать закономерности в данных, отлаживать код.")

    elif message.text == "Мобильная разработка":
        media = [
            types.InputMediaPhoto(open("rek.jpg", "rb")),
            types.InputMediaPhoto(open("rek2.jpg", "rb"))
        ]
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Мобильная разработка:\n\nМир мобильной разработки представлен двумя основными операционными системами и технологиями на их базе: Android и iOS. С большим отрывом превалирует Android.\nДля Мобильной Разроботки используют mit app inventor Работа в ней не требует знания языка программирования Java и Android SDK, достаточно знания элементарных основ алгоритмизации. \nВ данном курсе рассматривается разработка Андроид-приложений, и является ""не одной строчки"" кода платформой, потому что можно создать мобильное приложение, не запрограммировав ни строчки.")

    elif message.text == "Программирование на Java":
        media = [
            types.InputMediaPhoto(open("day4.jpg", "rb")),
            types.InputMediaPhoto(open("day5.jpg", "rb"))
        ]
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Программирование на Java:\n\nАктуальность программы обусловлена заказом общества на грамотных специалистов в области программирования,эффективностью развития навыков со школьного возраста; передачей сложного технического материала в простой доступной форме; реализацией проектной деятельности учащимися на базе современного оборудования.\n\nОсновное внимание на занятиях по программе уделяется общим вопросам построения алгоритмов, навыкам программирования на языке Java, использованию совместно с Java других языков программирования и технологий (JavaScript, CSS и др.), мобильной разработке под ОС Android.")

    elif message.text == "Системное администрирование":
        media = [
            types.InputMediaPhoto(open("day2.jpg", "rb")),
            types.InputMediaPhoto(open("sis.jpg", "rb")),
        ]
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Системное администрирование:\n\nВ обязанности системного администратора входит установка и настройка программного обеспечения, поддержка работы компьютеров и оргтехники, умение разрабатывать и управлять компьютерными сетями.\n\nДанная программа способствует формированию изобретательского мышления, расширяет и дополняет базовые знания,проявить и реализовать свой творческий потенциал, что делает программу актуальной и востребованной.")

    elif message.text == "Алгоритмика и логика":
        media = [
            types.InputMediaPhoto(open("rek3.jpg", "rb")),
            types.InputMediaPhoto(open("rek4.jpg", "rb"))
        ]
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Алгоритмика и логика:\n\nОсновная цель-подготовить Вас к любой задаче, научить применять полученные знания на практике, заинтересовать в учебе. Курс научит инструментам и практикам программирования, вы сможете создавать свои проекты: мультфильмы, игры.\nВы учитесь работать по инструкции, считаться с итоговыми требованиями, признавать и исправлять собственные ошибки, представлять и оценивать готовые проекты, а также десяткам другим важнейшим уникальным умениям и способам действия.")
    
    elif message.text == "<Меню>":
        media = [
            types.InputMediaPhoto(open("sisal.jpg", "rb")),
            types.InputMediaPhoto(open("sisal2.jpg", "rb")),
            types.InputMediaPhoto(open("sisal3.jpg", "rb")),
            types.InputMediaPhoto(open("sisal4.jpg", "rb")),
        ]
        reply = types.InlineKeyboardMarkup()
        reply.add(types.InlineKeyboardButton("Новости", callback_data="ol"))
        reply.add(types.InlineKeyboardButton("Мероприятия", callback_data="ol2"))
        reply.add(types.InlineKeyboardButton("Контакты", callback_data="ol3"))
        reply.add(types.InlineKeyboardButton("Условия поступления", callback_data="ol4"))
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, "Меню:", reply_markup=reply)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "ol":
        bot.send_message(call.message.chat.id, "https://t130631.spo.obrazovanie33.ru/it-kub/novosti.php")
    elif call.data == "ol2":
        bot.send_message(call.message.chat.id, "https://t130631.spo.obrazovanie33.ru/it-kub/meropriyatiya.php")
    elif call.data == "ol3":
        bot.send_message(call.message.chat.id, "Контакты:\n\ne-mail: it-cub@vztec.ru\nТелефон: 8(49233)3-09-93")
    elif call.data == "ol4":
        bot.send_message(call.message.chat.id, "- Обучение в центре по выбранному кубу – бесплатное по сертификату дополнительного образования детей;\n- места в бюджетном образовании ограничены (не более 400 мест);\n- Как получить сертификат: на портале 33.pfdo.ru - инструкция;\nвозраст обучающихся от 7 до 18 лет")

bot.infinity_polling()
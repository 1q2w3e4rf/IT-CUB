import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import os
from Patrigram import TelegramBot

# Замените 'YOUR_BOT_TOKEN' на токен вашего Telegram-бота.
BOT_TOKEN = '6804594259:AAEu03onfNbMDd4HmS9-QvuWcOqxLfQl--I'
# Создаем экземпляр нашего класса TelegramBot для взаимодействия с API Telegram.
bot = TelegramBot(BOT_TOKEN)

# Определяем URL-адреса, с которых мы будем получать новости и события.
URL = 'https://t130631.spo.obrazovanie33.ru/news/'
URL2 = "https://t130631.spo.obrazovanie33.ru/events/"

# Функция для извлечения списка новостей с сайта.
def get_news_from_site() -> List[Dict[str, str]]:
    try:
        # Отправляем GET-запрос к сайту с новостями.
        response = requests.get(URL)
        # Проверяем, успешен ли запрос. Если нет, то выбрасываем исключение.
        response.raise_for_status()
        # Делаем паузу в 1 секунду, чтобы не нагружать сайт слишком большим количеством запросов.
        time.sleep(1)

        # Создаем объект BeautifulSoup для разбора HTML-кода страницы.
        soup = BeautifulSoup(response.content, 'html.parser')
        # Ищем контейнер, в котором находятся новости.
        news_container = soup.find('div', class_='news-list')
        if news_container:
            # Находим все ссылки на отдельные новости.
            news_items = news_container.find_all('a')

            # Создаем пустой список для хранения новостей.
            news = []
            # Проходимся по всем найденным ссылкам на новости.
            for item in news_items:
                # Извлекаем заголовок новости.
                title = item.text.strip()
                # Извлекаем ссылку на новость.
                link = item['href'] 
                if link:
                    # Добавляем новость в список в виде словаря с заголовком и ссылкой.
                    news.append({'title': title, 'link': f'https://t130631.spo.obrazovanie33.ru{link}'})

            # Возвращаем список новостей.
            return news
        else:
            # Если контейнер с новостями не найден, возвращаем пустой список.
            return []
    except requests.exceptions.RequestException as e:
        # В случае ошибки при выполнении HTTP-запроса выводим сообщение об ошибке и возвращаем пустой список.
        print(f"Ошибка при получении новостей: {e}")
        return []
    except Exception as e:
        # В случае любой другой ошибки выводим сообщение и возвращаем пустой список.
        print(f"Непредвиденная ошибка при получении новостей: {e}")
        return []

# Функция для получения описания новости по ссылке.
def get_news_description(link: str) -> str:
    try:
        # Отправляем GET-запрос к странице с новостью.
        response = requests.get(link)
        # Проверяем, успешен ли запрос.
        response.raise_for_status()
        # Делаем паузу в 1 секунду.
        time.sleep(1)
        # Создаем объект BeautifulSoup для разбора HTML.
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим первый параграф, содержащий описание новости.
        p_element = soup.find('p')
        if p_element:
            # Извлекаем и возвращаем текст описания.
            description = p_element.text.strip()
        else:
            # Если описание не найдено, возвращаем сообщение.
            description = "Описание не найдено на этой странице."
        return description
    except requests.exceptions.RequestException as e:
        # В случае ошибки HTTP-запроса выводим сообщение и возвращаем ошибку.
        print(f"Ошибка загрузки описания: {e}")
        return "Ошибка загрузки описания."
    except Exception as e:
        # В случае любой другой ошибки выводим сообщение и возвращаем ошибку.
        print(f"Ошибка получения описания: {e}")
        return "Ошибка получения описания."

# Функция для получения списка событий с сайта.
def get_events() -> List[Dict[str, str]]:
    try:
        # Отправляем GET-запрос к странице с событиями.
        response = requests.get(URL2)
        # Проверяем, успешен ли запрос.
        response.raise_for_status()
        # Делаем паузу в 1 секунду.
        time.sleep(1)
        # Создаем объект BeautifulSoup для разбора HTML.
        soup = BeautifulSoup(response.content, 'html.parser')
        # Создаем пустой список для хранения событий.
        events = []
        # Проходимся по всем ссылкам на события.
        for item in soup.select('a[href^="/events/"]'):
            # Извлекаем заголовок события.
            title = item.text.strip()
            # Извлекаем ссылку на событие.
            link = "https://t130631.spo.obrazovanie33.ru" + item['href']
            # Добавляем событие в список в виде словаря с заголовком и ссылкой.
            events.append({'title': title, 'link': link})
        # Возвращаем список событий.
        return events
    except requests.exceptions.RequestException as e:
        # В случае ошибки HTTP-запроса выводим сообщение и возвращаем пустой список.
        print(f"Ошибка получения событий: {e}")
        return []
    except Exception as e:
        # В случае любой другой ошибки выводим сообщение и возвращаем пустой список.
        print(f"Непредвиденная ошибка при получении событий: {e}")
        return []

# Функция для получения описания события по ссылке.
def get_event_description(link: str) -> str:
    try:
        # Отправляем GET-запрос к странице с событием.
        response = requests.get(link)
        # Проверяем, успешен ли запрос.
        response.raise_for_status()
        # Делаем паузу в 1 секунду.
        time.sleep(1)
         # Создаем объект BeautifulSoup для разбора HTML.
        soup = BeautifulSoup(response.content, 'html.parser')
        # Ищем контейнер с описанием события.
        description_div = soup.find('div', class_='article-body')
        if description_div:
            # Если контейнер найден, извлекаем описание.
            description = description_div.get_text(separator='\n', strip=True)
            return description
        else:
            # Если контейнер не найден, ищем все параграфы.
            description_paragraphs = soup.find_all('p')
            if description_paragraphs:
                # Если параграфы найдены, объединяем их тексты и возвращаем.
                description = '\n'.join([p.get_text(strip=True) for p in description_paragraphs])
                return description
            else:
                 # Если описание не найдено, возвращаем сообщение.
                return "Описание не найдено на этой странице."
    except requests.exceptions.RequestException as e:
        # В случае ошибки HTTP-запроса выводим сообщение и возвращаем ошибку.
        print(f"Ошибка загрузки описания: {e}")
        return f"Ошибка загрузки описания: {e}"
    except Exception as e:
         # В случае любой другой ошибки выводим сообщение и возвращаем ошибку.
        print(f"Ошибка получения описания: {e}")
        return f"Ошибка получения описания: {e}"

# Обработчик команды /start.
@bot.message_command(['start'])
def start(message: Dict, username: str, user_id: int, chat_id: int, nickname: str) -> None:
    # Создаем список кнопок для стартового меню.
    reply_buttons = ["Условия поступления"]
    # Отправляем фото.
    bot.send_photo(chat_id, "KUB.jpg")
    # Отправляем видео.
    bot.send_video(chat_id, "IT.mp4")
    # Приветствуем пользователя.
    bot.send_message(chat_id, "Привет! Я Telegram бот который расскажет тебе об центре образования IT Cube в Вязниках" )
    # Предлагаем ознакомиться с условиями поступления.
    bot.send_message_with_keyboard(chat_id, "Чтобы узнать о направлениях, сначала ознакомьтесь с условиями поступления", buttons=reply_buttons)

# Обработчик текстовых сообщений.
@bot.text_handler
def handle_text_messages(message: Dict, chat_id: int) -> None:
    # Извлекаем текст сообщения.
    text = bot.message_text(message)
    if text == "Условия поступления":
        # Создаем список направлений.
        options = [
            "Программирование роботов",
            "Программирование на Python",
            "Программирование на Java",
            "Мобильная разработка",
            "Алгоритмика и логика",
            "Системное администрирование",
        ]
        # Сортируем список направлений.
        options.sort()
        # Добавляем кнопку меню.
        options.append("<Меню>")
        # Отправляем пользователю сообщение об условиях поступления.
        bot.send_message(chat_id, "- Обучение в центре по выбранному кубу – бесплатное по сертификату дополнительного образования детей;\n- места в бюджетном образовании ограничены (не более 400 мест);\n- Как получить сертификат: на портале 33.pfdo.ru - инструкция;\nвозраст обучающихся от 7 до 18 лет")
        # Предлагаем выбрать одно из направлений.
        bot.send_message_with_keyboard(chat_id, "Мы предлагаем широкий спектр курсов, каждый из которых открывает новые горизонты и возможности:", buttons=options, n_cols=1)
    
    elif text == "Программирование роботов":
        # Отправляем фотографии по выбранному направлению.
        media = ["robot.jpg", "robot2.jpg", "day6.jpg"]
        for photo in media:
            bot.send_photo(chat_id, photo)
        # Отправляем сообщение с описанием направления.
        bot.send_message(chat_id, "Программирование роботов:\n\nРобототехника вводит учащихся в мир технологий, развивает навыки взаимодействия, самостоятельности при принятии решений, раскрывает их творческий потенциал.\nПрограмма «Программирование роботов» нацелена на изучение принципов программирования при помощи роботов, которых обучающиеся будут разрабатывать . Научаться создавать мобильных роботов и систем программирования на базе платформ Arduino и других. В ходе занимательного конструирования обучающиеся научатся ставить задачи и находить решения, получат базовые знания по программированию,  механике, электрике, проектированию ,на стыке которых находится современная робототехника.")

    elif text == "Программирование на Python":
        # Отправляем фотографии по выбранному направлению.
        media = ["python.jpg", "python2.jpg"]
        for photo in media:
             bot.send_photo(chat_id, photo)
        # Отправляем сообщение с описанием направления.
        bot.send_message(chat_id, "Программирование на Python:\n\nПростой и понятный синтаксис. 23 Команды легко читаются и напоминают обычную английскую речь. Например, чтобы прописать приветствие, используется строчка print (\"Hello\").\nВозможность создавать различные приложения. Дети могут создавать свои приложения от простого вывода «Hello World!» до разработки анимации и игр. \nРазвитие логических и алгоритмических навыков. В процессе изучения Python дети учатся планировать последовательности действий для решения задач, анализировать задачи и разбивать их на подзадачи, искать закономерности в данных, отлаживать код.")

    elif text == "Мобильная разработка":
        # Отправляем фотографии по выбранному направлению.
        media = ["rek.jpg", "rek2.jpg"]
        for photo in media:
             bot.send_photo(chat_id, photo)
        # Отправляем сообщение с описанием направления.
        bot.send_message(chat_id, "Мобильная разработка:\n\nМир мобильной разработки представлен двумя основными операционными системами и технологиями на их базе: Android и iOS. С большим отрывом превалирует Android.\nДля Мобильной Разроботки используют mit app inventor Работа в ней не требует знания языка программирования Java и Android SDK, достаточно знания элементарных основ алгоритмизации. \nВ данном курсе рассматривается разработка Андроид-приложений, и является ""не одной строчки"" кода платформой, потому что можно создать мобильное приложение, не запрограммировав ни строчки.")

    elif text == "Программирование на Java":
         # Отправляем фотографии по выбранному направлению.
        media = ["day4.jpg", "day5.jpg"]
        for photo in media:
             bot.send_photo(chat_id, photo)
        # Отправляем сообщение с описанием направления.
        bot.send_message(chat_id, "Программирование на Java:\n\nАктуальность программы обусловлена заказом общества на грамотных специалистов в области программирования,эффективностью развития навыков со школьного возраста; передачей сложного технического материала в простой доступной форме; реализацией проектной деятельности учащимися на базе современного оборудования.\n\nОсновное внимание на занятиях по программе уделяется общим вопросам построения алгоритмов, навыкам программирования на языке Java, использованию совместно с Java других языков программирования и технологий (JavaScript, CSS и др.), мобильной разработке под ОС Android.")

    elif text == "Системное администрирование":
        # Отправляем фотографии по выбранному направлению.
        media = ["day2.jpg", "sis.jpg"]
        for photo in media:
             bot.send_photo(chat_id, photo)
        # Отправляем сообщение с описанием направления.
        bot.send_message(chat_id, "Системное администрирование:\n\nВ обязанности системного администратора входит установка и настройка программного обеспечения, поддержка работы компьютеров и оргтехники, умение разрабатывать и управлять компьютерными сетями.\n\nДанная программа способствует формированию изобретательского мышления, расширяет и дополняет базовые знания,проявить и реализовать свой творческий потенциал, что делает программу актуальной и востребованной.")

    elif text == "Алгоритмика и логика":
         # Отправляем фотографии по выбранному направлению.
        media = ["rek3.jpg", "rek4.jpg"]
        for photo in media:
             bot.send_photo(chat_id, photo)
         # Отправляем сообщение с описанием направления.
        bot.send_message(chat_id, "Алгоритмика и логика:\n\nОсновная цель-подготовить Вас к любой задаче, научить применять полученные знания на практике, заинтересовать в учебе. Курс научит инструментам и практикам программирования, вы сможете создавать свои проекты: мультфильмы, игры.\nВы учитесь работать по инструкции, считаться с итоговыми требованиями, признавать и исправлять собственные ошибки, представлять и оценивать готовые проекты, а также десяткам другим важнейшим уникальным умениям и способам действия.")
    
    elif text == "<Меню>":
        # Отправляем фото из меню
        media = ["sisal.jpg", "sisal2.jpg", "sisal3.jpg", "sisal4.jpg"]
        for photo in media:
             bot.send_photo(chat_id, photo)
         # Создаем inline клавиатуру для меню.
        inline_buttons = [
            {"text": "Новости", "callback_data": "ol"},
            {"text": "Мероприятия", "callback_data": "ol2"},
            {"text": "Контакты", "callback_data": "ol3"},
            {"text": "Условия поступления", "callback_data": "ol4"}
        ]
        # Функция для обработки callback запросов с inline клавиатуры.
        def response_function(data: str, chat_id: int, update: Dict) -> None:
           
            if data == "ol":
              # Получаем список новостей.
              news_list = get_news_from_site()
              if not news_list:
                  # Если новости не получены, отправляем сообщение об этом.
                  bot.send_message(chat_id, "Не удалось получить новости.")
                  return
              # Создаем список кнопок для новостей.
              keyboard_buttons = [news_item['title'] for news_item in news_list if news_item['title'] != "Читать полностью"]
              keyboard_buttons.append("<Меню>")
              # Предлагаем выбрать новость.
              bot.send_message_with_keyboard(chat_id, "Выберите новость:", buttons=keyboard_buttons, n_cols = 1)
            elif data == "ol2":
                # Получаем список событий.
                events = get_events()
                if events:
                    # Создаем список кнопок для событий.
                    keyboard_buttons = [event['title'] for event in events if event['title'] != "Мероприятия"]
                    keyboard_buttons.append("<Меню>")
                     # Предлагаем выбрать событие.
                    bot.send_message_with_keyboard(chat_id, "Выберите событие:", buttons=keyboard_buttons, n_cols=1)
                else:
                     # Если события не получены, отправляем сообщение об этом.
                  bot.send_message(chat_id, "Не удалось загрузить события.")
            elif data == "ol3":
                 # Отправляем контактную информацию.
                bot.send_message(chat_id, "Контакты:\n\ne-mail: it-cub@vztec.ru\nТелефон: 8(49233)3-09-93")
            elif data == "ol4":
                # Отправляем условия поступления.
                bot.send_message(chat_id, "- Обучение в центре по выбранному кубу – бесплатное по сертификату дополнительного образования детей;\n- места в бюджетном образовании ограничены (не более 400 мест);\n- Как получить сертификат: на портале 33.pfdo.ru - инструкция;\nвозраст обучающихся от 7 до 18 лет")
        # Запускаем режим ожидания ответа пользователя, передавая в качестве response_function созданную функцию.
        bot.wait_for_response_and_respond(chat_id, "Меню:", response_function=response_function)
        # Отправляем сообщение с inline клавиатурой.
        bot.send_message_with_inline_keyboard(chat_id, "Меню:", buttons=inline_buttons)
    
    
    news_list = get_news_from_site()
    if not news_list:
        bot.send_message(chat_id, "Не удалось получить новости.")
        return
    
    for news_item in news_list:
         if text == news_item['title']:
             description = get_news_description(news_item['link'])
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
             bot.send_message_with_keyboard(chat_id, f"Дополнительная информация по ссылке: {news_item['link']}\n\nОписание:\n{description}", buttons=options, n_cols=1)
             return
    
    events = get_events()
    if events:
        for event in events:
            if text == event['title']:
                description = get_event_description(event['link'])
                if description:
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
                    bot.send_message_with_keyboard(chat_id, f"Дополнительная информация по ссылке: {event['link']} \n\nОписание:{description}", buttons=options, n_cols=1)
                else:
                    bot.send_message(chat_id, "Описание не найдено.")
                return
    else:
        bot.send_message(chat_id, "Не удалось загрузить события.")


if __name__ == '__main__':
    print("Bot run")
    bot.run()

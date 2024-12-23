
import requests
import json
import time
import mimetypes
import os
from typing import List, Dict, Callable, Union, Any 

class TelegramBot:
    """
    Класс для взаимодействия с Telegram Bot API.

    Предоставляет методы для отправки сообщений, обработки команд и обновлений
    в режиме опроса (polling).
    """

    def __init__(self, token: str):
        """
        Инициализирует объект TelegramBot.

        Args:
            token: Токен вашего Telegram-бота.
        """
        self.token: str = token
        self.base_url: str = f"https://api.telegram.org/bot{self.token}"
        self.handlers: Dict[str, Callable] = {}
        self.text_handlers: List[Callable] = []
        self.waiting_responses: Dict[int, Callable] = {}

    def _make_request(self, method: str, params: Dict = None, files: Dict = None) -> Dict:
       """
       Отправляет запрос к Telegram API.

       Args:
            method: Метод API (например, sendMessage, sendPhoto).
            params: Параметры запроса.
            files: Файлы для отправки (например, фото, видео).

        Returns:
           JSON-ответ от Telegram API.
        
        Raises:
            requests.exceptions.RequestException: Если произошла ошибка при выполнении запроса.
       """
       url = f"{self.base_url}/{method}"
       try:
           response = requests.post(url, params=params, files=files) if files else requests.post(url, json=params)
           response.raise_for_status()  # Проверка на HTTP-ошибки
           return response.json()
       except requests.exceptions.RequestException as e:
           print(f"Ошибка запроса к Telegram API: {e}")
           return {'ok': False, 'description': str(e)}

    def answer_callback_query(self, callback_query_id: str, text: str = '', show_alert: bool = False, cache_time: int = 0) -> Dict:
        """
        Отвечает на callback-запрос.

        Args:
            callback_query_id: ID callback-запроса.
            text: Текст ответа.
            show_alert: Отображать ли всплывающее уведомление.
            cache_time: Время кэширования ответа.

        Returns:
            JSON-ответ от Telegram API.
        """
        params = {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'cache_time': cache_time
        }
        return self._make_request('answerCallbackQuery', params=params)

    def send_video(self, chat_id: int, video: str, caption: str = None, **kwargs) -> Dict:
        """
        Отправляет видео.

        Args:
            chat_id: ID чата, куда отправить видео.
            video: Путь к видеофайлу или URL видео.
            caption: Подпись к видео.
            kwargs: Дополнительные параметры для отправки видео.

        Returns:
            JSON-ответ от Telegram API.
        """
        files = None
        try:
            if os.path.exists(video):
                files = {'video': open(video, 'rb')}
            else:
                kwargs['video'] = video

            params = {'chat_id': chat_id}
            if caption:
                params['caption'] = caption
            params.update(kwargs)
            return self._make_request('sendVideo', params=params, files=files)
        except Exception as e:
            print(f"Ошибка при отправке видео: {e}")
            return {'ok': False, 'description': str(e)}

    def create_inline_keyboard(self, buttons: List[Dict], n_cols: int = 2) -> str:
        """
        Создает встроенную клавиатуру.

        Args:
            buttons: Список словарей с данными кнопок (text, callback_data).
            n_cols: Количество колонок.

        Returns:
            JSON-строку представляющую встроенную клавиатуру.
        """
        keyboard: List[List[Dict]] = []
        row: List[Dict] = []
        for i, button in enumerate(buttons):
            row.append({"text": button['text'], "callback_data": button['callback_data']})
            if (i + 1) % n_cols == 0 or i == len(buttons) - 1:
                keyboard.append(row)
                row = []
        reply_markup: Dict = {"inline_keyboard": keyboard}
        return json.dumps(reply_markup)

    def send_message_with_inline_keyboard(self, chat_id: int, text: str, buttons: List[Dict], n_cols: int = 2) -> Dict:
        """
        Отправляет сообщение с встроенной клавиатурой.

        Args:
            chat_id: ID чата, куда отправить сообщение.
            text: Текст сообщения.
            buttons: Список словарей с данными кнопок (text, callback_data).
            n_cols: Количество колонок.

        Returns:
            JSON-ответ от Telegram API.
        """
        keyboard = self.create_inline_keyboard(buttons, n_cols)
        return self.send_message(chat_id, text, reply_markup=keyboard)

    def wait_for_response_and_respond(self, chat_id: int, prompt_message: str, response_function: Callable[[str, int, Dict], None]) -> None:
       """
       Отправляет сообщение и ждет ответа от пользователя.
       После получения ответа вызывает указанную функцию с этим ответом.

       Args:
            chat_id: ID чата.
            prompt_message: Сообщение с запросом ответа.
            response_function: Функция, которую нужно вызвать после получения ответа.
       """
       self.send_message(chat_id, prompt_message)
       self.waiting_responses[chat_id] = response_function

    def create_keyboard(self, buttons: List[str], n_cols: int = 2) -> str:
        """
        Создает обычную клавиатуру.

        Args:
            buttons: Список строк с текстом кнопок.
            n_cols: Количество колонок.

        Returns:
            JSON-строку представляющую обычную клавиатуру.
        """
        keyboard: List[List[Dict]] = []
        row: List[Dict] = []
        for i, button in enumerate(buttons):
            row.append({"text": button})
            if (i + 1) % n_cols == 0 or i == len(buttons) - 1:
                keyboard.append(row)
                row = []
        reply_markup: Dict = {"keyboard": keyboard, "resize_keyboard": True}
        return json.dumps(reply_markup)

    def send_message_with_keyboard(self, chat_id: int, text: str, buttons: List[str], n_cols: int = 2) -> Dict:
        """
        Отправляет сообщение с обычной клавиатурой.

        Args:
            chat_id: ID чата, куда отправить сообщение.
            text: Текст сообщения.
            buttons: Список строк с текстом кнопок.
            n_cols: Количество колонок.

        Returns:
            JSON-ответ от Telegram API.
        """
        keyboard = self.create_keyboard(buttons, n_cols)
        return self.send_message(chat_id, text, reply_markup=keyboard)

    def send_document(self, chat_id: int, document: str, caption: str = None, **kwargs) -> Dict:
        """
        Отправляет файл (документ).

        Args:
            chat_id: ID чата, куда отправить документ.
            document: Путь к файлу или URL файла.
            caption: Подпись к документу.
            kwargs: Дополнительные параметры для отправки документа.

        Returns:
            JSON-ответ от Telegram API.
        """
        files = None
        try:
           if os.path.exists(document):
               files = {'document': open(document, 'rb')}
           else:
               kwargs['document'] = document

           params = {'chat_id': chat_id}
           if caption:
               params['caption'] = caption
           params.update(kwargs)
           return self._make_request('sendDocument', params=params, files=files)
        except Exception as e:
           print(f"Ошибка при отправке документа: {e}")
           return {'ok': False, 'description': str(e)}


    def send_photo(self, chat_id: int, photo: str, caption: str = None, **kwargs) -> Dict:
        """
        Отправляет фотографию.

        Args:
            chat_id: ID чата, куда отправить фото.
            photo: Путь к файлу или URL фото.
            caption: Подпись к фото.
            kwargs: Дополнительные параметры для отправки фото.

        Returns:
            JSON-ответ от Telegram API.
        """
        files = None
        try:
            if os.path.exists(photo):
                files = {'photo': open(photo, 'rb')}
            else:
                kwargs['photo'] = photo

            params = {'chat_id': chat_id}
            if caption:
                params['caption'] = caption
            params.update(kwargs)
            return self._make_request('sendPhoto', params=params, files=files)
        except Exception as e:
            print(f"Ошибка при отправке фото: {e}")
            return {'ok': False, 'description': str(e)}

    def send_message(self, chat_id: int, text: str, **kwargs) -> Dict:
        """
        Отправляет текстовое сообщение.

        Args:
            chat_id: ID чата, куда отправить сообщение.
            text: Текст сообщения.
            kwargs: Дополнительные параметры для отправки сообщения.

        Returns:
            JSON-ответ от Telegram API.
        """
        params = {'chat_id': chat_id, 'text': text}
        params.update(kwargs)
        return self._make_request('sendMessage', params=params)


    def send_file(self, chat_id: int, file_path: str, caption: str = None, **kwargs) -> Dict:
        """
        Отправляет файл (фото, видео, документ).
        Определяет тип файла по MIME-типу и вызывает соответствующий метод.

        Args:
            chat_id: ID чата, куда отправить файл.
            file_path: Путь к файлу или URL файла.
            caption: Подпись к файлу.
            kwargs: Дополнительные параметры для отправки файла.
        Returns:
            JSON-ответ от Telegram API или словарь с ошибкой.
        """
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                return {'ok': False, 'description': 'Не удалось определить тип файла.'}

            if mime_type.startswith('image/'):
                return self.send_photo(chat_id, file_path, caption, **kwargs)
            elif mime_type.startswith('video/'):
                return self.send_video(chat_id, file_path, caption, **kwargs)
            elif mime_type.startswith('application/') or mime_type == 'text/plain':
                return self.send_document(chat_id, file_path, caption, **kwargs)
            else:
                return {'ok': False, 'description': f'Неподдерживаемый тип файла: {mime_type}'}

        except FileNotFoundError:
           return {'ok': False, 'description': f'Файл не найден: {file_path}'}
        except Exception as e:
            print(f'Ошибка при отправке файла: {e}')
            return {'ok': False, 'description': f'Ошибка при отправке файла: {e}'}


    def get_updates(self, offset: int = None, timeout: int = 0) -> Dict:
       """
       Получает обновления от Telegram API.

       Args:
            offset: ID обновления, с которого начинать получение.
            timeout: Время ожидания обновлений.

        Returns:
            JSON-ответ от Telegram API.
       """
       params = {'timeout': timeout}
       if offset:
           params['offset'] = offset
       return self._make_request('getUpdates', params=params)

    def message_command(self, commands: List[str]) -> Callable:
        """
        Декоратор для обработки сообщений с командами.

        Args:
            commands: Список команд, которые нужно обработать.

        Returns:
            Декоратор.
        """

        def decorator(func: Callable) -> Callable:
            for command in commands:
                self.handlers[command] = func
            return func

        return decorator

    def process_callback_query(self, update: Dict) -> None:
       """
       Обрабатывает callback-запросы.

        Args:
            update: Обновление от Telegram API.
       """
       query = update['callback_query']
       data = query['data']
       chat_id = query['message']['chat']['id']
       self.answer_callback_query(query['id'], text=f"Вы выбрали: {data}")
       if chat_id in self.waiting_responses:
            response_function = self.waiting_responses.pop(chat_id)
            response_function(data, chat_id, update)

    def process_message(self, update: Dict) -> None:
        """
        Обрабатывает текстовые сообщения.

        Args:
            update: Обновление от Telegram API.
        """
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text')

        if chat_id in self.waiting_responses:
            response_function = self.waiting_responses.pop(chat_id)
            response_function(text, chat_id, update)
        elif text and text.startswith('/'):
           command = text[1:].split()[0]
           if command in self.handlers:
               user = message['from']
               username = user.get('username')
               user_id = user['id']
               first_name = user.get('first_name', '')
               last_name = user.get('last_name', '')
               nickname = f"{first_name} {last_name}".strip()
               self.handlers[command](message, username, user_id, chat_id, nickname)
        elif text:
            for handler in self.text_handlers:
                handler(message, chat_id)

    def message_text(self, message: Dict) -> Union[str, None]:
        """
        Возвращает текст сообщения пользователя.

        Args:
            message: Сообщение от Telegram API.

        Returns:
            Текст сообщения или None, если текста нет.
        """
        try:
            return message['text']
        except KeyError:
            return None

    def text_handler(self, func: Callable) -> Callable:
       """
       Декоратор для обработчика текстов, не являющихся командами.

        Args:
           func: Функция для обработки текстового сообщения.
        
        Returns:
           Декоратор.
       """
       self.text_handlers.append(func)
       return func

    def process_update(self, update: Dict) -> None:
        """
        Обрабатывает обновление от Telegram API.

        Args:
            update: Обновление от Telegram API.
        """
        try:
            if 'message' in update:
                self.process_message(update)
            elif 'callback_query' in update:
                self.process_callback_query(update)
        except Exception as e:
            print(f"Ошибка при обработке обновления: {e}")

    def run(self) -> None:
        """
        Запускает режим опроса (polling).
        """
        last_update_id: int = 0
        while True:
            updates = self.get_updates(offset=last_update_id + 1, timeout=20)
            if updates['ok']:
                for update in updates['result']:
                    last_update_id = update['update_id']
                    self.process_update(update)
            else:
                print(f"Ошибка при получении обновлений: {updates}")

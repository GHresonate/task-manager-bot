from telebot.types import KeyboardButton, ReplyKeyboardMarkup


class KeyboardManager:
    @staticmethod
    def get_start_kb():
        info_button = KeyboardButton('/Info')
        login_button = KeyboardButton('/Login')
        register_button = KeyboardButton('/Register')
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(login_button)
        keyboard.add(register_button)
        keyboard.add(info_button)
        return keyboard

    @staticmethod
    def get_lang_kb():
        eng_button = KeyboardButton('English')
        ukr_button = KeyboardButton('Українська')
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(eng_button)
        keyboard.add(ukr_button)
        return keyboard

    @staticmethod
    def get_lang_kb_for_change():
        eng_button = KeyboardButton('English')
        ukr_button = KeyboardButton('Українська')
        back_button = KeyboardButton('/Account')
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(eng_button)
        keyboard.add(ukr_button)
        keyboard.add(back_button)
        return keyboard

    @staticmethod
    def get_main_kb():
        quit_button = KeyboardButton('/Quit')
        account_button = KeyboardButton('/Account')
        tasks_button = KeyboardButton('/Tasks')
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(tasks_button)
        keyboard.add(account_button)
        keyboard.add(quit_button)
        return keyboard

    @staticmethod
    def get_account_kb():
        name_button = KeyboardButton('Change username')
        password_button = KeyboardButton('Change password')
        delete_button = KeyboardButton('Delete account')
        change_lang = KeyboardButton('Change language')
        main = KeyboardButton('/Main')
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(name_button)
        keyboard.add(password_button)
        keyboard.add(delete_button)
        keyboard.add(change_lang)
        keyboard.add(main)
        return keyboard

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Услуги'),
                                      KeyboardButton(text='О боте')],
                                      [KeyboardButton(text='Пользовательское соглашение')]],
                            resize_keyboard=True)

privatka = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Доступ в приватку", callback_data="privatka"),
                                                InlineKeyboardButton(text="Донат", callback_data="donate")]])

cancel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='cancel')]])
privatka_end = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить', callback_data='privatka_end'),
                                                    InlineKeyboardButton(text='Назад', callback_data='back')]])

main_admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Услуги'),
                                      KeyboardButton(text='О боте')],
                                      [KeyboardButton(text='Пользовательское соглашение')],
                                      [KeyboardButton(text='Команды администратора')]],
                            resize_keyboard=True)
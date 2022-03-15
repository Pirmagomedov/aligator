from aiogram import types

chooce_lang_markup = types.InlineKeyboardMarkup()
chooce_lang_markup.add(types.InlineKeyboardButton("Русский", callback_data="Русский"))
chooce_lang_markup.add(types.InlineKeyboardButton("Украинский", callback_data="Украинский"))

chooce_gender_markup = types.InlineKeyboardMarkup()
chooce_gender_markup.add(types.InlineKeyboardButton("Парень", callback_data="Парень"))
chooce_gender_markup.add(types.InlineKeyboardButton("Девушка", callback_data="Девушка"))
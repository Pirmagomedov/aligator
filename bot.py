from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from database import Data

# ===================

from but import chooce_lang_markup, chooce_gender_markup

# ===================

bot = Bot("5294363905:AAG7Tc-Oz7rHwjsCLDvcfu68zRk9Qo58WcE")
dp = Dispatcher(bot)

data = Data("anonimus.db")

# Старт
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	user_in_db = await data.check_user(message.from_user.id)

	# Проверка, есть ли человек в базе данных:
	if not user_in_db:
		list = [message.from_user.first_name, message.from_user.id, 0, 0, 0, None, None, 0, 0, 0, 0, 0]
		await data.add_user(list)

		await chooce_lang(message.from_user.id)
		return

	if not await data.check_form(message.from_user.id):
		await bot.send_message(message.from_user.id, "Сначала завершите регистрацию!")
		return

	if not await data.get_my_status(message.from_user.id):
		await bot.send_message(message.from_user.id, "Вы в диалоге!")
		return

	user = await data.check_on_status(message.from_user.id)

	if user:
		await data.update_s_i(message.from_user.id, user)

		await bot.send_message(message.from_user.id, "Собеседник найден")
		await bot.send_message(user, "Собеседник найден")

	else:
		await data.set_status(message.from_user.id)
		await bot.send_message(message.from_user.id, "Поиск собеседника...")


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
	state = await data.get_stop_state(message.from_user.id)

	if state[0] and not state[1]:
		await data.stop_find(message.from_user.id)
		await bot.send_message(message.from_user.id, "Поиск остановлен")

	elif state[0] and state[1]:
		user = await data.stop_for_all(message.from_user.id)

		await bot.send_message(message.from_user.id, "Вы вышли из чата")
		await bot.send_message(user, "Собеседник вышел из чата")

	else:
		await bot.send_message(message.from_user.id, "Вы не в диалоге")


# ---------------------------------------------------------------

async def chooce_lang(id):
	await bot.send_message(id, "Выберите свой язык:", reply_markup=chooce_lang_markup)

async def chooce_gender(id, mid):
	try:
		await bot.edit_message_text(chat_id=id, text="Выберите свой пол:", message_id=mid, reply_markup=chooce_gender_markup)
	except Exception:
		pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@dp.message_handler()
async def msg(message: types.Message):
	state = await data.get_stop_state(message.from_user.id)

	if not state[1]:
		await bot.send_message(message.from_user.id, "Вы не в диалоге")
		return

	user = await data.get_user(message.from_user.id)

	await bot.send_message(user, message.text)

# ---------------------------------------------------------------
# ---------------------------------------------------------------

@dp.callback_query_handler()
async def call(call: types.CallbackQuery):
	if call.data in ["Русский", "Украинский"]:
		await data.set_lang(call.from_user.id, call.data)
		await chooce_gender(call.from_user.id, call.message.message_id)

	elif call.data in ["Парень", "Девушка"]:
		await data.set_gender(call.from_user.id, call.data)
		try:
			await bot.edit_message_text(chat_id=call.from_user.id, text="Регистрация завершена", message_id=call.message.message_id)
		except Exception:
			pass


# ===============================================================

if __name__ == '__main__':
    executor.start_polling(dp)
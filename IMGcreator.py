import os
import matplotlib.pyplot as plt
import pandas as pd

# Проверяем текущую рабочую директорию
print("Текущая рабочая директория:", os.getcwd())

# Меняем рабочую директорию на директорию скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Указываем имя файла
output_path = 'table.png'

# Пример данных
data = {
    'Имя': ['Алексей', 'Мария', 'Иван'],
    'Возраст': [25, 30, 22],
    'Город': ['Москва', 'Санкт-Петербург', 'Новосибирск']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание фигуры и оси
fig, ax = plt.subplots(figsize=(10, 4))  # Размер изображения

# Скрытие осей
ax.axis('off')

# Создание таблицы
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

# Настройка стиля таблицы
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)  # Масштабирование таблицы

# Сохранение таблицы в PNG
plt.savefig(output_path, bbox_inches='tight', dpi=300)

# Закрытие фигуры
plt.close(fig)
import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar
import winsound
import json
import webbrowser
from datetime import datetime

HISTORY_FILE = "bmi_history.json"

# Функция для загрузки истории из файла
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Функция для сохранения истории в файл
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

# Функция для очистки истории
def clear_history():
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить всю историю?"):
        save_history([])
        messagebox.showinfo("История", "История очищена.")
        # Уничтожаем окно истории, если оно существует
        if hasattr(show_history, 'history_window') and show_history.history_window:
            show_history.history_window.destroy()
            show_history.history_window = None  # Обнуляем ссылку на окно

# Функция для открытия ссылки на Википедию
def open_wiki_link():
    webbrowser.open_new("https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D1%82%D1%8F%D0%B6%D1%91%D0%BB%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%BC%D0%B8%D1%80%D0%B5")

# Функция для расчета и отображения ИМТ
def calculate_and_display_bmi():
    # Удаляем кнопку wiki_button, если она существует
    if hasattr(calculate_and_display_bmi, 'wiki_button') and calculate_and_display_bmi.wiki_button:
        calculate_and_display_bmi.wiki_button.destroy()
        calculate_and_display_bmi.wiki_button = None # Обнуляем ссылку на кнопку

    try:
        name = name_entry.get()
        age_str = age_entry.get()

        # Проверка возраста
        if not age_str.isdigit() or not (0 < int(age_str) <= 100):
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный возраст (число от 1 до 100).")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            return

        age = int(age_str)
        weight = float(weight_entry.get())
        height = float(height_entry.get()) / 100

        bmi = calculate_bmi(weight, height)
        bmi_note = ""

        if bmi > 251:
            result_label.config(fg="red")
            result_label.config(text="Возможно, введены некорректные данные.\nИМТ превышает самый большой зарегистрированный результат,\nтак как, согласно Книге рекордов Гиннесса,\nмировой рекорд удерживает Джон Миннох с максимальным весом 635 кг.")
            # Создаем кнопку wiki_button и сохраняем её как атрибут функции
            calculate_and_display_bmi.wiki_button = tk.Button(app, text="Ссылка", command=open_wiki_link)
            calculate_and_display_bmi.wiki_button.pack()
            bmi_note = " (Возможно, некорректные данные)"
        elif bmi < 7.4:
            result_label.config(fg="red")
            result_label.config(text="Скорее всего введены неправильные данные.\nСамый низкий ИМТ 7,4 была у Иланит «Хила» Эльмалиах при весе 22 кг и росте 172 см")
            bmi_note = " (Возможно, некорректные данные)"
        elif bmi < 0:
            result_label.config(fg="red")
            result_label.config(text="Ошибка: ИМТ не может быть отрицательным.")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            return
        else:
            result_label.config(fg="black")

            classification = classify_bmi(bmi)
            diet_suggestion = suggest_diet(bmi, weight)

            result_text = f"ИМТ: {bmi:.2f}\nКлассификация: {classification}\nРекомендации по диете:\n{diet_suggestion}"
            result_label.config(text=result_text)

            history = load_history()
            # Получаем текущую дату и время
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату
            history.append({
                'name': name,
                'age': age,
                'weight': weight,
                'height': height * 100,
                'bmi': bmi,
                'classification': classification + bmi_note, #Добавляем пометку к классификации
                'date': now  # Добавляем дату в историю
            })
            save_history(history)

    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для веса и роста.")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

# Функция для расчета ИМТ
def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

# Функция для классификации ИМТ
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Дефицит массы тела"
    elif 18.5 <= bmi <= 24.9:
        return "Нормальная масса тела"
    elif 25.0 <= bmi <= 29.9:
        return "Избыточная масса тела"
    elif 30.0 <= bmi <= 34.9:
        return "Ожирение 1 степени"
    elif 35.0 <= bmi <= 39.9:
        return "Ожирение 2 степени"
    elif bmi > 40:
        return "Ожирение 3 степени"
    else:
        return "Неправильные данные"

# Функция для предложения диеты
def suggest_diet(bmi, weight_kg):
    if bmi < 18.5:
        return "Рекомендуется увеличить потребление калорий,\nс акцентом на питательные продукты, богатые белком\nи здоровыми жирами. Рассмотрите добавление в рацион\nавокадо, орехов, семян, яиц и жирной рыбы.\nКонсультация с диетологом может быть полезна\nдля индивидуального плана набора веса."
    elif 18.5 <= bmi <= 24.9:
        return "Поддерживайте сбалансированное питание\nс достаточным количеством фруктов, овощей,\nцельнозерновых продуктов и белка.\nРегулярные физические упражнения помогут\nподдерживать текущий вес и хорошее здоровье."
    elif 25.0 <= bmi <= 29.9:
        return "Рекомендуется умеренное снижение\nкалорийности питания, увеличение\nфизической активности. Сосредоточьтесь на\nпотреблении большего количества овощей,\nфруктов и нежирного белка. Избегайте сладких\nнапитков и обработанных продуктов."
    else:
        return "Необходима консультация с врачом\nи диетологом для разработки индивидуального\nплана снижения веса. Рекомендуется комплексный\nподход, включающий диету, физические упражнения\nи, возможно, медикаментозную терапию."

# Функция для отображения истории запросов
def show_history():
    history = load_history()
    if not history:
        messagebox.showinfo("История", "История пуста.")
        return

    # Проверяем, существует ли окно истории
    if not hasattr(show_history, 'history_window') or not show_history.history_window:
        # Если окно не существует, создаем его
        show_history.history_window = Toplevel(app)
        show_history.history_window.title("История запросов")
        # Добавляем обработчик закрытия окна
        show_history.history_window.protocol("WM_DELETE_WINDOW", lambda: close_history_window())

        text_area = Text(show_history.history_window, wrap=tk.WORD)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(show_history.history_window, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area['yscrollcommand'] = scrollbar.set

        clear_button = tk.Button(show_history.history_window, text="Очистить историю", command=clear_history)
        clear_button.pack(pady=5)

        for entry in history:
            name = entry.get('name', "Без имени")
            age = entry.get('age', 0)
            weight = entry['weight']
            height = entry['height']
            bmi = entry['bmi']
            classification = entry['classification']
            date = entry.get('date', "Дата не указана")  # Получаем дату

            text_area.insert(tk.END, f"Имя: {name}, Возраст: {age} лет, Вес: {weight} кг, Рост: {height} см, ИМТ: {bmi:.2f}, Классификация: {classification}, Дата: {date}\n\n")
        text_area.config(state=tk.DISABLED)

# Функция для закрытия окна истории
def close_history_window():
    if hasattr(show_history, 'history_window') and show_history.history_window:
        show_history.history_window.destroy()
        show_history.history_window = None

# Создание главного окна
app = tk.Tk()
app.title("BMI Assistant (1.0)")

# Создание кнопки "История"
history_button = tk.Button(app, text="История", command=show_history)
history_button.pack(anchor="nw")

# Создание полей ввода
name_label = tk.Label(app, text="Введите имя:")
name_label.pack()
name_entry = tk.Entry(app)
name_entry.pack()

age_label = tk.Label(app, text="Введите возраст:")
age_label.pack()
age_entry = tk.Entry(app)
age_entry.pack()

weight_label = tk.Label(app, text="Введите вес в килограммах:")
weight_label.pack()
weight_entry = tk.Entry(app)
weight_entry.pack()

height_label = tk.Label(app, text="Введите рост в сантиметрах:")
height_label.pack()
height_entry = tk.Entry(app)
height_entry.pack()

# Создание кнопки "Получить результат"
calculate_button = tk.Button(app, text="Получить результат", command=calculate_and_display_bmi)
calculate_button.pack()

# Создание метки для отображения результата
result_label = tk.Label(app, text="")
result_label.pack()

# Предупреждение и версия
warning_label = tk.Label(app, text="Не является мед. программой! В случае проблем со здоровьем следует обратиться к специалисту.", fg="red", anchor="sw")
warning_label.pack(side="bottom", fill="x")

version_label = tk.Label(app, text="Версия: 1.0", fg="blue", anchor="se")
version_label.pack(side="bottom", fill="x")

# Запуск главного цикла
app.mainloop()














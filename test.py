import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar
import json
from datetime import datetime
import webbrowser
import language  # Предположим, у вас есть модуль language с translations

HISTORY_FILE = "bmi_history.json"
SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            theme_name = settings.get("theme", "light")
            lang_code = settings.get("language", "RU")
            return theme_name, lang_code
    except:
        return "light", "RU"

def save_settings(theme_name, lang_code):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({"theme": theme_name, "language": lang_code}, f)

# Загружаем настройки
theme_name, current_lang = load_settings()

# Определяем темы
light_theme = {
    "bg": "white",
    "fg": "black",
    "button_bg": "lightgray",
    "button_fg": "black",
    "result_fg": "black",
    "entry_bg": "white",
    "entry_fg": "black"
}

dark_theme = {
    "bg": "#2e2e2e",
    "fg": "white",
    "button_bg": "#444444",
    "button_fg": "white",
    "result_fg": "white",
    "entry_bg": "#3e3e3e",
    "entry_fg": "white"
}

# Выбираем текущую тему
if theme_name == "dark":
    current_theme = dark_theme
else:
    current_theme = light_theme

# Создаем главное окно
app = tk.Tk()
app.title("BMI Assistant")
app.config(bg=current_theme["bg"])

# --- Объявляем переменные для меню ---
menubar = tk.Menu(app)

# Создаем пункты меню
history_menu = tk.Menu(menubar, tearoff=0)
theme_menu = tk.Menu(menubar, tearoff=0)
info_menu = tk.Menu(menubar, tearoff=0)
language_menu = tk.Menu(menubar, tearoff=0)

# Добавляем пункты в главное меню
menubar.add_cascade(label="", menu=history_menu)
menubar.add_cascade(label="", menu=theme_menu)
menubar.add_cascade(label="", menu=info_menu)
menubar.add_cascade(label="", menu=language_menu)

app.config(menu=menubar)

# --- Объявляем функции для обновления меню ---
def update_menus():
    # Обновляем заголовки меню
    menubar.entryconfig(0, label=language.translations[current_lang]["История"])
    menubar.entryconfig(1, label=language.translations[current_lang]["Тема"])
    menubar.entryconfig(2, label=language.translations[current_lang]["Информация"])
    menubar.entryconfig(3, label=language.translations[current_lang]["Опции"])

    # Обновляем пункты подменю "История"
    history_menu.delete(0, tk.END)
    history_menu.add_command(label=language.translations[current_lang]["Посмотреть историю"], command=lambda: print("История"))  # замените на вашу функцию

    # Обновляем пункты "Тема"
    theme_menu.delete(0, tk.END)
    theme_menu.add_command(label=language.translations[current_lang]["Светлая тема"], command=set_light_theme)
    theme_menu.add_command(label=language.translations[current_lang]["Тёмная тема"], command=set_dark_theme)

    # Обновляем пункты "Информация"
    info_menu.delete(0, tk.END)
    info_menu.add_command(label=language.translations[current_lang]["О программе"], command=lambda: print("О программе"))  # замените

    # Обновляем пункты "Язык"
    language_menu.delete(0, tk.END)
    language_menu.add_command(label="Русский", command=lambda: set_language("RU"))
    language_menu.add_command(label="English", command=lambda: set_language("ENG"))

# --- Функции смены темы ---
def apply_theme():
    # Обновим все виджеты, чтобы применить текущую тему
    widgets = [
        name_label, age_label, weight_label, height_label,
        name_entry, age_entry, weight_entry, height_entry,
        calculate_button, result_label, warning_label
    ]
    for widget in widgets:
        widget.config(bg=current_theme["bg"], fg=current_theme.get("fg", current_theme["fg"]))
        if isinstance(widget, tk.Entry):
            widget.config(bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["entry_fg"])
        elif isinstance(widget, tk.Label):
            widget.config(bg=current_theme["bg"])
        elif isinstance(widget, tk.Button):
            widget.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])

def update_result_label_theme():
    result_label.config(fg=current_theme["result_fg"])

def update_warning_label_color():
    warning_label.config(bg=current_theme["bg"])

def set_light_theme():
    global current_theme, theme_name
    current_theme = light_theme
    theme_name = "light"
    save_settings(theme_name, current_lang)
    apply_theme()
    update_result_label_theme()
    update_warning_label_color()

def set_dark_theme():
    global current_theme, theme_name
    current_theme = dark_theme
    theme_name = "dark"
    save_settings(theme_name, current_lang)
    apply_theme()
    update_result_label_theme()
    update_warning_label_color()

# --- Функция смены языка ---
def set_language(lang_code):
    global current_lang
    current_lang = lang_code
    save_settings(theme_name, current_lang)
    update_menus()
    # Обновляем тексты на интерфейсе
    name_label.config(text=language.translations[current_lang]["Введите имя:"])
    age_label.config(text=language.translations[current_lang]["Введите возраст:"])
    weight_label.config(text=language.translations[current_lang]["Введите вес в килограммах:"])
    height_label.config(text=language.translations[current_lang]["Введите рост в сантиметрах:"])
    calculate_button.config(text=language.translations[current_lang]["Получить результат"])
    warning_label.config(text=language.translations[current_lang]["Не является мед. программой! В случае проблем со здоровьем следует обратиться к специалисту."])

# --- Изначально вызываем обновление меню и интерфейса ---
update_menus()

# Создаем интерфейс
name_label = tk.Label(app, text=language.translations[current_lang]["Введите имя:"], bg=current_theme["bg"], fg=current_theme["fg"])
name_label.pack()
name_entry = tk.Entry(app, bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["entry_fg"])
name_entry.pack()

age_label = tk.Label(app, text=language.translations[current_lang]["Введите возраст:"], bg=current_theme["bg"], fg=current_theme["fg"])
age_label.pack()
age_entry = tk.Entry(app, bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["entry_fg"])
age_entry.pack()

weight_label = tk.Label(app, text=language.translations[current_lang]["Введите вес в килограммах:"], bg=current_theme["bg"], fg=current_theme["fg"])
weight_label.pack()
weight_entry = tk.Entry(app, bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["entry_fg"])
weight_entry.pack()

height_label = tk.Label(app, text=language.translations[current_lang]["Введите рост в сантиметрах:"], bg=current_theme["bg"], fg=current_theme["fg"])
height_label.pack()
height_entry = tk.Entry(app, bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["entry_fg"])
height_entry.pack()

calculate_button = tk.Button(app, text=language.translations[current_lang]["Получить результат"], command=lambda: print("Calculate"))  # замените на вашу функцию
calculate_button.pack(pady=5)

result_label = tk.Label(app, text="", bg=current_theme["bg"], fg=current_theme["result_fg"])
result_label.pack()

warning_label = tk.Label(app, text=language.translations[current_lang]["Не является мед. программой! В случае проблем со здоровьем следует обратиться к специалисту."], fg="red", bg=current_theme["bg"], anchor="sw")
warning_label.pack(side="bottom", fill="x")

# --- Изначальное применение темы ---
apply_theme()
update_result_label_theme()
update_warning_label_color()

app.mainloop()

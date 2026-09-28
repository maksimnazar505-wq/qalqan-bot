# ================================================================
#   QALQAN DIGITAL — Telegram Bot
#   Версия 1.0
# ================================================================

import os
import telebot
from telebot import types
import pandas as pd
import io

# ---- ТОКЕН БОТА ----
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8627867357:AAFbKUYcp2GQ-GSDbMcSaUOUMI_aiYsfGbg")
bot = telebot.TeleBot(BOT_TOKEN)

# ================================================================
#   ЛИЧНЫЙ СОСТАВ (боевые номера)
# ================================================================
PERSONNEL = [
    {"id": 1, "боевой_номер": "101", "ФИО": "Военнослужащий №01", "звание": "рядовой",     "должность": "стрелок",       "отделение": 1, "нарядов": 0},
    {"id": 2, "боевой_номер": "102", "ФИО": "Военнослужащий №02", "звание": "ефрейтор",    "должность": "стрелок",       "отделение": 1, "нарядов": 0},
    {"id": 3, "боевой_номер": "103", "ФИО": "Военнослужащий №03", "звание": "рядовой",     "должность": "пулемётчик",    "отделение": 1, "нарядов": 0},
    {"id": 4, "боевой_номер": "201", "ФИО": "Военнослужащий №04", "звание": "мл. сержант", "должность": "командир отд.", "отделение": 2, "нарядов": 0},
    {"id": 5, "боевой_номер": "202", "ФИО": "Военнослужащий №05", "звание": "рядовой",     "должность": "стрелок",       "отделение": 2, "нарядов": 0},
    {"id": 6, "боевой_номер": "203", "ФИО": "Военнослужащий №06", "звание": "рядовой",     "должность": "стрелок",       "отделение": 2, "нарядов": 0},
    {"id": 7, "боевой_номер": "301", "ФИО": "Военнослужащий №07", "звание": "сержант",     "должность": "командир отд.", "отделение": 3, "нарядов": 0},
    {"id": 8, "боевой_номер": "302", "ФИО": "Военнослужащий №08", "звание": "рядовой",     "должность": "водитель",      "отделение": 3, "нарядов": 0},
]

# ================================================================
#   ВИДЫ НАРЯДОВ
# ================================================================
DUTY_TYPES = [
    "Пограничный наряд",
    "КПП (контрольный пункт пропуска)",
    "Секрет",
    "Дозор",
    "Проверка пограничного режима",
]

# ================================================================
#   НАРЯДЫ
# ================================================================
TODAY_DUTY = [
    {"боевой_номер": "101", "ФИО": "Военнослужащий №01", "вид_наряда": "Пограничный наряд", "время": "06:00 - 14:00"},
    {"боевой_номер": "104", "ФИО": "Военнослужащий №04", "вид_наряда": "КПП",                "время": "06:00 - 14:00"},
    {"боевой_номер": "201", "ФИО": "Военнослужащий №07", "вид_наряда": "Секрет",             "время": "22:00 - 06:00"},
]

TOMORROW_DUTY = [
    {"боевой_номер": "102", "ФИО": "Военнослужащий №02", "вид_наряда": "Дозор",              "время": "06:00 - 14:00"},
    {"боевой_номер": "105", "ФИО": "Военнослужащий №05", "вид_наряда": "Пограничный наряд",  "время": "14:00 - 22:00"},
]

# ================================================================
#   БОЕВАЯ ПОДГОТОВКА
# ================================================================
BATTLE_TRAINING = [
    {"дата": "Понедельник", "тема": "Тактическая подготовка",  "время": "09:00 - 11:00", "преподаватель": "Командир роты"},
    {"дата": "Вторник",     "тема": "Огневая подготовка",      "время": "14:00 - 16:00", "преподаватель": "Зам. по боевой"},
    {"дата": "Среда",       "тема": "Инженерная подготовка",   "время": "09:00 - 11:00", "преподаватель": "Командир взвода"},
    {"дата": "Четверг",     "тема": "Медицинская подготовка",  "время": "14:00 - 16:00", "преподаватель": "Санитарный инструктор"},
    {"дата": "Пятница",     "тема": "Физическая подготовка",   "время": "07:00 - 08:00", "преподаватель": "Командир роты"},
]

# ================================================================
#   ВОСПИТАТЕЛЬНАЯ РАБОТА
# ================================================================
EDUCATION_TASKS = [
    {"тема": "Политинформация",              "дата": "Понедельник", "отметка": "✅ проведено"},
    {"тема": "Беседа о воинской дисциплине", "дата": "Вторник",     "отметка": "✅ проведено"},
    {"тема": "Изучение уставов ВС РК",       "дата": "Среда",       "отметка": "⏳ запланировано"},
    {"тема": "Работа с молодым пополнением", "дата": "Четверг",     "отметка": "⏳ запланировано"},
]


# ================================================================
#   ГЛАВНОЕ МЕНЮ
# ================================================================
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("🛡 Наряды на сегодня"),
        types.KeyboardButton("📅 Наряды на завтра"),
    )
    kb.add(
        types.KeyboardButton("👥 Личный состав"),
        types.KeyboardButton("🔍 Поиск по номеру"),
    )
    kb.add(
        types.KeyboardButton("🎯 Боевая подготовка"),
        types.KeyboardButton("📚 Воспитательная работа"),
    )
    kb.add(
        types.KeyboardButton("📊 Анализ нагрузки"),
        types.KeyboardButton("📥 Экспорт в Excel"),
    )
    kb.add(types.KeyboardButton("ℹ️ О системе"))
    return kb


# ================================================================
#   КОМАНДЫ
# ================================================================
@bot.message_handler(commands=["start"])
def start_command(message):
    text = (
        "🛡 *QALQAN DIGITAL*\n"
        "_Модуль управления подразделением_\n\n"
        "Добро пожаловать!\n\n"
        "Выберите раздел ниже 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(commands=["menu"])
def menu_command(message):
    bot.send_message(message.chat.id, "📋 Главное меню:", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "🛡 Наряды на сегодня")
def today_duty(message):
    text = "🛡 *НАРЯДЫ НА СЕГОДНЯ*\n" + "━" * 25 + "\n\n"
    for i, d in enumerate(TODAY_DUTY, 1):
        text += (
            f"*{i}. {d['вид_наряда']}*\n"
            f"   🆔 Боевой номер: `{d['боевой_номер']}`\n"
            f"   👤 {d['ФИО']}\n"
            f"   🕐 {d['время']}\n\n"
        )
    text += f"━━━━━━━━━━━━━━━━━━━━━━\n📊 Всего заступает: *{len(TODAY_DUTY)}*"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📅 Наряды на завтра")
def tomorrow_duty(message):
    text = "📅 *НАРЯДЫ НА ЗАВТРА*\n" + "━" * 25 + "\n\n"
    for i, d in enumerate(TOMORROW_DUTY, 1):
        text += (
            f"*{i}. {d['вид_наряда']}*\n"
            f"   🆔 Боевой номер: `{d['боевой_номер']}`\n"
            f"   👤 {d['ФИО']}\n"
            f"   🕐 {d['время']}\n\n"
        )
    text += f"━━━━━━━━━━━━━━━━━━━━━━\n📊 Всего заступает: *{len(TOMORROW_DUTY)}*"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "👥 Личный состав")
def personnel_list(message):
    text = "👥 *ЛИЧНЫЙ СОСТАВ*\n" + "━" * 25 + "\n\n"
    current_dept = None
    for p in PERSONNEL:
        if p["отделение"] != current_dept:
            current_dept = p["отделение"]
            text += f"\n*📍 Отделение {current_dept}*\n\n"
        text += (
            f"🆔 `{p['боевой_номер']}` — {p['ФИО']}\n"
            f"   _{p['звание']}, {p['должность']}_\n\n"
        )
    text += f"━━━━━━━━━━━━━━━━━━━━━━\n👥 Всего: *{len(PERSONNEL)}* военнослужащих"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по номеру")
def search_ask(message):
    msg = bot.send_message(
        message.chat.id,
        "🔍 Введите *боевой номер* (например: `101`):",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, search_process)


def search_process(message):
    query = message.text.strip()
    found = [p for p in PERSONNEL if p["боевой_номер"] == query]
    if found:
        p = found[0]
        text = (
            f"✅ *НАЙДЕН*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🆔 Боевой номер: `{p['боевой_номер']}`\n"
            f"👤 ФИО: *{p['ФИО']}*\n"
            f"🎖 Звание: {p['звание']}\n"
            f"💼 Должность: {p['должность']}\n"
            f"📍 Отделение: {p['отделение']}\n"
            f"📊 Нарядов отслужено: {p['нарядов']}"
        )
    else:
        text = f"❌ Военнослужащий с боевым номером `{query}` не найден."
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())


@bot.message_handler(func=lambda m: m.text == "🎯 Боевая подготовка")
def battle_training(message):
    text = "🎯 *БОЕВАЯ ПОДГОТОВКА*\n" + "━" * 25 + "\n\n"
    text += "📅 *Расписание занятий на неделю:*\n\n"
    for i, b in enumerate(BATTLE_TRAINING, 1):
        text += (
            f"*{i}. {b['дата']}*\n"
            f"   📖 Тема: {b['тема']}\n"
            f"   🕐 {b['время']}\n"
            f"   👨‍🏫 {b['преподаватель']}\n\n"
        )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📚 Воспитательная работа")
def education_work(message):
    text = "📚 *ВОСПИТАТЕЛЬНАЯ РАБОТА*\n" + "━" * 25 + "\n\n"
    for i, e in enumerate(EDUCATION_TASKS, 1):
        text += (
            f"*{i}. {e['тема']}*\n"
            f"   📅 {e['дата']}\n"
            f"   {e['отметка']}\n\n"
        )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📊 Анализ нагрузки")
def load_analysis(message):
    all_duties = TODAY_DUTY + TOMORROW_DUTY
    counter = {}
    for d in all_duties:
        counter[d["ФИО"]] = counter.get(d["ФИО"], 0) + 1

    avg = sum(counter.values()) / len(PERSONNEL) if counter else 0

    text = "📊 *АНАЛИЗ НАГРУЗКИ*\n" + "━" * 25 + "\n\n"
    text += f"👥 Всего военнослужащих: *{len(PERSONNEL)}*\n"
    text += f"📈 Средняя нагрузка: *{avg:.2f}* наряда\n\n"
    text += "📋 *По военнослужащим:*\n\n"

    for p in PERSONNEL:
        n = counter.get(p["ФИО"], 0)
        if n > avg + 0.5:
            mark = "🔴 перегружен"
        elif n < avg - 0.5:
            mark = "🟢 недогружен"
        else:
            mark = "🔵 норма"
        text += f"🆔 `{p['боевой_номер']}` — *{n}* нарядов — {mark}\n"

    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📥 Экспорт в Excel")
def export_excel(message):
    df_personnel = pd.DataFrame(PERSONNEL)
    df_duty_today = pd.DataFrame(TODAY_DUTY)
    df_duty_tomorrow = pd.DataFrame(TOMORROW_DUTY)
    df_battle = pd.DataFrame(BATTLE_TRAINING)
    df_education = pd.DataFrame(EDUCATION_TASKS)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_personnel.to_excel(writer, sheet_name="Личный состав", index=False)
        df_duty_today.to_excel(writer, sheet_name="Наряды сегодня", index=False)
        df_duty_tomorrow.to_excel(writer, sheet_name="Наряды завтра", index=False)
        df_battle.to_excel(writer, sheet_name="Боевая подготовка", index=False)
        df_education.to_excel(writer, sheet_name="Воспитательная работа", index=False)

    buffer.seek(0)
    bot.send_document(
        message.chat.id,
        buffer,
        visible_file_name="QALQAN_отчёт.xlsx",
        caption="📥 *Отчёт QALQAN DIGITAL*\n\nВнутри 5 листов с данными подразделения.",
        parse_mode="Markdown",
    )


@bot.message_handler(func=lambda m: m.text == "ℹ️ О системе")
def about(message):
    text = (
        "ℹ️ *О СИСТЕМЕ*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🛡 *QALQAN DIGITAL*\n"
        "_Единая цифровая система управления_\n\n"
        "📌 *Назначение:*\n"
        "Автоматизация служебной деятельности и боевой подготовки подразделений ПС КНБ РК.\n\n"
        "📋 *Модули:*\n"
        "• 🛡 Охрана государственной границы\n"
        "• 🎯 Боевая подготовка\n"
        "• 📚 Воспитательная работа\n"
        "• 👥 Личный состав\n\n"
        "🛡 *Версия:* 1.0\n"
        "📅 *Дата:* 2026 год"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "🤔 Не понял команду.\n\nИспользуйте кнопки меню ниже 👇",
        reply_markup=main_menu(),
    )


# ================================================================
#   ЗАПУСК
# ================================================================
if __name__ == "__main__":
    print("🚀 QALQAN DIGITAL — бот запущен")
    bot.infinity_polling()

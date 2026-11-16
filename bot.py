from aiohttp import web

async def handle(request):
    return web.Response(text="I am alive!")

app = web.Application()
app.router.add_get("/", handle)

async def start_web_server():
    runner = web.AppRunner(app)
    await runner.setup() 
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
import sqlite3
from datetime import datetime, timedelta
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "9004870309:AAE74QxpUPCNYhmgP1X2d4WcmVA9tFf6vEU"

bot = Bot(token=TOKEN)
dp = Dispatcher()
# --- База данных для баллов и статистики ---
db_connection = sqlite3.connect("bot_points.db")
db_cursor = db_connection.cursor()

db_cursor.execute("CREATE TABLE IF NOT EXISTS admin_points (user_id INTEGER PRIMARY KEY, username TEXT, points INTEGER DEFAULT 0)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS message_log (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, timestamp TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS punishment_log (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, timestamp TEXT)")
db_connection.commit()

# --- КЛАВИАТУРА ДЛЯ УСТАВА ---
def get_ustav_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1) 📜 Уточнения по правилам", callback_data="ustav_rules_more")],
            [InlineKeyboardButton(text="2) ⚡ Спец возможности", callback_data="ustav_specials")],
            [InlineKeyboardButton(text="3) 🗳️ Выборы", callback_data="ustav_elections")],
            [InlineKeyboardButton(text="4) 🏢 Организации ПВМ и их права", callback_data="ustav_orgs")],
        ]
    )
    return keyboard

# --- КОМАНДЫ ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот группы PWM. Напишите /rules (или /правила) или /ustav (/устав), чтобы узнать подробности!")

@dp.message(F.text.lower().in_({"/rules", "/правила", "rules", "правила"}))
async def cmd_rules(message: types.Message):
    text = """**ПРАВИЛА ЧАТУ:**

1) Сексуальный контент - от мута до бана
2) Спам и флуд - мут від 1 години до дня
3) Также (не в рофл) топить за нацизм/фашизм, а также шутить про убийство украинцев - мут 1 день
4) Репорт без причины, мут - 30мин..
5) Не рофл докс/угрозы докса - бан.
6) Расчлененка/насилия с солдатами вс рф - мут 1-2 дня 
7) Просто расчлененка/насилия - от 3 дней мута до бана
8) Устраивать не мирные митинги/майданы и подобное - мут на месяц
9) Зетник - бан
10) Реклама в чате только с разрешения иначе - мут 1 день.
11) Порча официальных опросов - мут на 6 часов.
12) Наказание могут суммироваться.
13) Можно подать апелляцию писать @folzon или @Seer_Ker
14) Если в стикерпаке материал за который дают бан, наказание: бан
15) Все уточнения по правилям в уставе."""

    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text.lower().in_({"/ustav", "/устав", "ustav", "устав"}))
async def cmd_ustav(message: types.Message):
    text = """📜 **Устав PWM**

Выберите интересующий вас раздел:"""
    await message.answer(text, reply_markup=get_ustav_keyboard(), parse_mode="Markdown")


# --- ОБРАБОТКА НАЖАТИЙ НА КНОПКИ УСТАВА ---

@dp.callback_query(F.data == "ustav_rules_more")
async def process_rules_more(callback: types.CallbackQuery):
    text = """📜 **Уточнения по правилам:**

1) Любые изображения, видео, гиф откровенного сексуального характера. За обычные изображения сисек, писек подобное - 1 день мута чаще всего. Но например за пдф, зоо - бан.

2) Спамом считается от 4 одинаковых или же похожих соо подряд. Флуд - поток бессмысленных, малосодержательных или повторяющихся сообщений.

3) То в шутку или нет "топит" человек за нацизм/фашизм решают модеры, или чат в официальном голосовании.

4) Если не названа причина выдаётся мут, или если в причине репорта написана шутка.

5) Слив или угрозы слива личной информации без согласия человека.

6) Трупы, мясо, кровь и подобное попадают под правило, если не видно военной формы, или других признаков что это солдат вс рф, то тогда наказание уже даётся по 8 правилу.

7) Так же, трупы, мясо, кровь, насилия и подобное попадает под наказание.

8) Про разницу между мирными митингами, и майданами написано в "спец возможностях".

9) То ли участник зетник решают админы, или другие люди в официальном опросе.

10) Разрешение можно получить у конотопа (владельца канала, юз в шапке профиля).

11) Про официальные опросы в другой части устава, за порчу считается: добавления шуточных вариантов, голосование в рофл за какой-то из вариантов, если не разрешено, то призыв голосовать за тот или иной вариант.

12) Например человек кинул гиф которая нарушает второй пункт, и потом кинул ещё 2 раза, то это уже мут не на 1 день а на 3, но если он нарушает другое правило, в нашем примере это может быть мут и флуд, то он получит ещё наказание за эти нарушения.

13) Апелляцию может подать любой участник чата на любое наказание, кроме бана. Она будет рассмотрена парламентом. Для этого напишите в лс @folzon или @Seer_Ker. Апелляция должна быть: 
1. Без шуток. 
2. С чётким указанием за что дали наказание. 
3. Если имеется возможность, то сообщение за которое дали наказание переслать. 
4. Причина по которой вы несогласны.

14) Например если в стикерпаке цп а в стикре который отослали нет, то всё равно дадут бан.

15) Ботов по типу хамстера в бан."""

    try:
        await callback.message.edit_text(text, parse_mode="Markdown")
    except Exception:
        pass
    await callback.answer()


@dp.callback_query(F.data == "ustav_specials")
async def process_specials(callback: types.CallbackQuery):
    text = """⚡️ **Спец возможности:**

1) Официальные голосование - может устроить каждый участник, условия: не шуточное оформления вопроса/темы, оно должно касаться чата, должно получить одобрения любого из админов/депутатов.

2) Мирные митинги/протесты - форма выражения участниками чата мнения, но оно должно получить согласие парламента для этого напишите с просьбой любому депутату. Вы должны написать какая причина, цель, и как именно всё будет проходить. Админ не имеет права мутить участников мирного протеста если у него есть разрешение, но если участник протеста нарушает правила чата, или договорённость то тогда админ имеет право дать наказание.

3) Участники имеют права создавать организации, так же они могут подать заявку в парламент, для назначения организации официального статуса с своими правами. Для этого нужно обратиться к любому из депутатов. Но если организация нарушает правила, то тогда её участники попадают под 9 пункт.

4) Любой участник группы имеет права писать идеи насчёт чата, чтобы их реализовали пишите депутатам.

5) Любой участник без запрета парламента, или конотопа имеет права стать админом или депутатом."""

    try:
        await callback.message.edit_text(text, parse_mode="Markdown")
    except Exception:
        pass
    await callback.answer()


@dp.callback_query(F.data == "ustav_elections")
async def process_elections(callback: types.CallbackQuery):
    text = """🗳 **Выборы:**

**1) Условия на пост депутата:**
А) У человека должно быть от 5000 сообщений в чате (возможны исключения).
Б) Внесён в список кандидатов замом или главой парламента.
В) Предвыборная речь где написано: количество соо, то почему парламент должен принять участника, идеи.
Г) Должен пройти голосование в парламенте, где больше 50% голосов должно быть за принятия.

**2) На пост админа:**
А) От 6000 сообщений в чате.
Б) Быть в чате не меньше 2 месяца.
В) Победить в официальном голосовании в чате, и в парламенте.
Г) Разрешение конотопа (владельца).

**Общие правила выборов:**
1) Запрещена фальсификация, когда опрос перекидывают в другой чат с просьбой проголосовать за тот или иной вариант.
2) Подкупать голоса нельзя.
3) Нарушения уникальных правил голосования.
**Наказание за все нарушения:** снятие с выборов и мут по 12 правилу, или же только мут."""

    try:
        await callback.message.edit_text(text, parse_mode="Markdown")
    except Exception:
        pass
    await callback.answer()


@dp.callback_query(F.data == "ustav_orgs")
async def process_orgs(callback: types.CallbackQuery):
    text = """🏢 **Организации и их права:**

**Парламент**
На данный момент главная организация, которая имеет право менять чат.

**Чат идеи от участников**
С разрешения парламента также имеет право менять чат."""

    try:
        await callback.message.edit_text(text, parse_mode="Markdown")
    except Exception:
        pass
    await callback.answer()


# --- Создание таблиц БД ---
db_cursor.execute("CREATE TABLE IF NOT EXISTS admin_points_log (user_id INTEGER, username TEXT, points_change INTEGER, timestamp TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS message_log (user_id INTEGER, username TEXT, timestamp TEXT)")
db_connection.commit()


# --- Клавиатура для топа администраторов ---
def get_top_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1) За всё время", callback_data="top_all")],
        [InlineKeyboardButton(text="2) За 1 месяц", callback_data="top_month")],
        [InlineKeyboardButton(text="3) За неделю", callback_data="top_week")],
        [InlineKeyboardButton(text="4) За 3 дня", callback_data="top_3days")]
    ])
# --- Функция формирования текста рейтинга админов ---
def get_leaderboard_text(period_name, cutoff_str=None):
    if cutoff_str:
        db_cursor.execute("""
            SELECT username, SUM(points_change) as total 
            FROM admin_points_log 
            WHERE timestamp >= ? 
            GROUP BY user_id 
            ORDER BY total DESC 
            LIMIT 5
        """, (cutoff_str,))
    else:
        db_cursor.execute("""
            SELECT username, SUM(points_change) as total 
            FROM admin_points_log 
            GROUP BY user_id 
            ORDER BY total DESC 
            LIMIT 5
        """)
    top_admins = db_cursor.fetchall()

    text = f"🏆 **Рейтинг администраторов ({period_name}):**\n\n"
    if top_admins:
        for idx, (uname, pts) in enumerate(top_admins, 1):
            points_val = pts if pts is not None else 0
            text += f"{idx}. {uname} — **{points_val}** бал.\n"
    else:
        text += "Рейтинг пуст за выбранный период.\n"
    return text

# --- Команда: Список администраторов (/админы /admins) ---
@dp.message(F.text.in_({"/админы", "/admins"}))
async def show_admins_list(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Эту команду можно использовать только в общем чате!")
        return

    chat_id = message.chat.id
    try:
        admins = await message.bot.get_chat_administrators(chat_id=chat_id)
        text_lines = ["🛡 **Список администраторов:**\n"]
        for admin in admins:
            if admin.user.is_bot:
                continue
            text_lines.append(f"• {admin.user.full_name}")
        
        await message.answer("\n".join(text_lines), parse_mode="Markdown")
    except Exception:
        await message.answer("Не удалось получить список администраторов.")

# --- Команда: Обычная статистика сообщества (/stats /статистика) ---
@dp.message(F.text.in_({"/stats", "/статистика"}))
async def show_statistics(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Статистику можно посмотреть только в общем чате.")
        return

    week_ago = (datetime.now() - timedelta(days=7)).isoformat()

    db_cursor.execute("""
        SELECT username, COUNT(*) as c 
        FROM message_log 
        WHERE timestamp >= ? 
        GROUP BY user_id 
        ORDER BY c DESC 
        LIMIT 5
    """, (week_ago,))
    top_active = db_cursor.fetchall()

    db_cursor.execute("SELECT COUNT(*) FROM message_log")
    total_messages = db_cursor.fetchone()[0]

    text = f"📊 **Статистика сообщества**\n\n"
    text += f"💬 Всего сообщений: **{total_messages}**\n\n"

    text += "🔥 **Самые активные участники (за неделю):**\n"
    if top_active:
        for idx, (uname, cnt) in enumerate(top_active, 1):
            text += f"{idx}. {uname} — {cnt} сообщений.\n"
    else:
        text += "Пока нет данных за неделю.\n"

    await message.answer(text, parse_mode="Markdown")

# --- Команда: Топ баллов администраторов с кнопками (/top /топ) ---
@dp.message(F.text.in_({"/top", "/топ"}))
async def show_admin_top(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Рейтинг администраторов можно посмотреть только в общем чате.")
        return

    leaderboard_text = get_leaderboard_text("За всё время")
    full_text = f"📊 **Баллы и рейтинг администраторов**\n\n" + leaderboard_text

    await message.answer(full_text, reply_markup=get_top_keyboard(), parse_mode="Markdown")

# --- Обработка нажатий на кнопки топа админов ---
@dp.callback_query(F.data.startswith("top_"))
async def process_top_callback(callback: types.CallbackQuery):
    data = callback.data
    now = datetime.now()

    if data == "top_all":
        cutoff = None
        period_name = "За всё время"
    elif data == "top_month":
        cutoff = (now - timedelta(days=30)).isoformat()
        period_name = "За 1 месяц"
    elif data == "top_week":
        cutoff = (now - timedelta(days=7)).isoformat()
        period_name = "За неделю"
    elif data == "top_3days":
        cutoff = (now - timedelta(days=3)).isoformat()
        period_name = "За 3 дня"
    else:
        return

    leaderboard_text = get_leaderboard_text(period_name, cutoff)
    full_text = f"📊 **Баллы и рейтинг администраторов**\n\n" + leaderboard_text

    try:
        await callback.message.edit_text(full_text, reply_markup=get_top_keyboard(), parse_mode="Markdown")
    except Exception:
        pass
    await callback.answer()

# --- Универсальный обработчик (автоначисление баллов за GroupHelpBot, сообщения и активность) ---
@dp.message()
async def track_all_activity(message: types.Message):
    if message.chat.type == "private":
        return
    if not message.from_user:
        return

    now_str = datetime.now().isoformat()
   
     # --- Отслеживание команд наказаний и их отмены ---
    if message.text:
        text_lower = message.text.lower()
        
        punishment_commands = [
            "/mute", "/ban", "/warn", "/kick",
            "мут", "бан", "варн", "кик"
        ]
        reversal_commands = [
            "/unmute", "/unban", "/unwarn",
            "размут", "разбан", "снять"
        ]
        
        points_to_add = None
        if any(text_lower.startswith(cmd) for cmd in punishment_commands):
            points_to_add = 3   # Выдача наказания
        elif any(text_lower.startswith(cmd) for cmd in reversal_commands):
            points_to_add = -3  # Снятие наказания
            
        if points_to_add is not None:
            user_id = message.from_user.id
            username = message.from_user.full_name
            
            try:
                member = await message.bot.get_chat_member(message.chat.id, user_id)
                if member.status in ["administrator", "creator"]:
                    db_cursor.execute(
                        "INSERT INTO admin_points_log (user_id, username, points_change, timestamp) VALUES (?, ?, ?, ?)",
                        (user_id, username, points_to_add, now_str)
                    )
                    db_connection.commit()
            except Exception:
                pass

    # 4. Логирование обычных сообщений для общей статистики
    user_id = message.from_user.id
    username = message.from_user.full_name

    db_cursor.execute(
        "INSERT INTO message_log (user_id, username, timestamp) VALUES (?, ?, ?)",
        (user_id, username, now_str)
    )
    db_connection.commit()

    # 5. Начисление +5 очков за каждые 500 сообщений для администраторов
    try:
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
        if member.status in ["administrator", "creator"]:
            db_cursor.execute("SELECT COUNT(*) FROM message_log WHERE user_id = ?", (user_id,))
            msg_count = db_cursor.fetchone()[0]

            if msg_count > 0 and msg_count % 500 == 0:
                db_cursor.execute(
                    "INSERT INTO admin_points_log (user_id, username, points_change, timestamp) VALUES (?, ?, 5, ?)",
                    (user_id, username, now_str)
                )
                db_connection.commit()
                await message.answer(f"🎉 Администратор {username} преодолел отметку в {msg_count} сообщений и получает **+5 очков**!", parse_mode="Markdown")
    except Exception:
        pass

# --- Запуск бота и веб-сервера ---
async def main():
    await start_web_server()
    # Сбрасываем старые зависшие обновления, чтобы избежать ошибок TelegramNotFound при старте
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
            
                        
                    

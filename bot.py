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

@dp.message(Command("rules", "правила"))
async def cmd_rules(message: types.Message):
    rules_text = (
        "📜 **ПРАВИЛА ЧАТУ:**\n\n"
        "1) Пдф - бан\n"
        "2) Сексуальный контент - мут 1 день\n"
        "3) Спам и флуд - мут від 1 години до дня\n"
        "4) Также (не в рофл) топить за нацизм/фашизм, а также шутить про убийство украинцев - мут 1 день\n"
        "5) Репорт без причины, мут - 30мин..\n"
        "6) Не рофл докс/угрозы докса - бан.\n"
        "7) Расчлененка/насилия с солдатами вс рф - мут 1 день\n"
        "8) Просто расчлененка/насилия - от 3 дней мута до бана\n"
        "9) Устраивать не мирные митинги/майданы и подобное - мут на месяц\n"
        "10) Зетник - бан\n"
        "11) Реклама в чате только с разрешения иначе - мут 1 день.\n"
        "12) Порча официальных опросов - мут на 6 часов.\n"
        "13) Наказание могут суммироваться.\n"
        "14) Можно подать апелляцию\n"
        "15) Все уточнения по правилам в уставе."
    )
    await message.answer(rules_text, parse_mode="Markdown")

@dp.message(Command("ustav", "устав"))
async def cmd_ustav(message: types.Message):
    await message.answer(
        "⚖️ **Устав PWM**\n\nВыберите интересующий вас раздел:",
        reply_markup=get_ustav_keyboard(),
        parse_mode="Markdown"
    )

# --- ОБРАБОТКА НАЖАТИЙ НА КНОПКИ ---

@dp.callback_query(F.data == "ustav_rules_more")
async def process_rules_more(callback: types.CallbackQuery):
    text = (
        "📜 **Уточнения по правилам:**\n\n"
        "1) Пдф считается видео, гиф стикеры, изображение сексуального характера с людьми до 18 лет, содержащие обнажённые половые органы. За пограничные случае где не видно половых органов, но человек практически полностью обнажен, возможно предупреждение (варн), мут или даже бан.\n\n"
        "2) Аналогично с первым, только нужно вычеркнуть пункт про \"18 лет\"\n\n"
        "3) Спамом считается от 4 одинаковых или же похожих соо подряд\n"
        "Флуд - поток бессмысленных, малосодержательных или повторяющихся сообщений.\n\n"
        "4) То в шутку или нет \"топит\" человек за нацизм/фашизм решают модеры, или чат в официальном голосовании.\n\n"
        "5) Если не названа причина выдаётся мут, или если в причине репорта написана шутка.\n\n"
        "6) Слив или угрозы слива личной информации без согласия человека.\n\n"
        "7) Трупы, мясо, кровь и подобное попадают под правило, если не видно военной формы, или других признаков что это солдат вс рф, то тогда наказание уже даётся по 8 правилу.\n\n"
        "8) Так же, трупы, мясо, кровь, насилия и подобное попадает под наказание.\n\n"
        "9) Про разницу между мирными митингами, и майданами написано в \"спец возможностях\"\n\n"
        "10) То ли участник зетник решают админы, или другие люди в официальном опросе.\n\n"
        "11) Разрешение можно получить у конотопа (владельца канала, юз в шапке профиля)\n\n"
        "12) Про официальные опросы в другой части устава, за порчу считается: добавления шуточных вариантов, голосование в рофл за какой-то из вариантов, если не разрешено, то призыв голосовать за тот или иной вариант.\n\n"
        "13) Например человек кинул гиф которая нарушает второй пункт, и потом кинул ещё 2 раза, то это уже мут не на 1 день а на 3 но если он нарушает другое правило, в нашем примере это может быть мут и флуд, то он получит ещё наказание за эти нарушения.\n\n"
        "14) Апелляцию может подать любой участник чата на любое наказание, кроме бана. Для этого напишите в лс @folzon или\n\n"
        "15) Ботов по типу хамстера в бан."
    )
    await callback.message.edit_text(text, reply_markup=get_ustav_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ustav_specials")
async def process_specials(callback: types.CallbackQuery):
    text = (
        "⚡ **Спец возможности:**\n\n"
        "1) Официальные голосование - может устроить каждый участник, условия: не шуточное оформления вопроса/темы, оно должно касаться чата, должно получить одобрения любого из админов/депутатов.\n\n"
        "2) Мирные митинги/протесты - форма выражения участниками чата мнения, но оно должно получить согласие парламента для этого напишите в с просьбой любому депутату. Вы должны написать какая причина, цель, и как именно всё будет проходить. Админ не имеет права мутить участников мирного протеста если у него есть разрешение, но если участник протеста нарушает правила чата, или договорённость то тогда админ имеет право дать наказание.\n\n"
        "3) Участники имеют права создавать организации, так же они могут подать заявку в парламент, для назначения организации официального статуса с своими правами. Для этого нужно обратиться к любому из депутатов. Но если организация нарушает правила, то тогда её участники попадают под 9 пункт.\n\n"
        "4) Любой участник группы имеет права писать идеи насчёт чата, что-бы их реализовали пишите депутатам.\n\n"
        "5) Любой участник без запрета парламента, или конотопа имеет права стать админом или депутатом"
    )
    await callback.message.edit_text(text, reply_markup=get_ustav_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ustav_elections")
async def process_elections(callback: types.CallbackQuery):
    text = (
        "🗳️ **Выборы:**\n\n"
        "1) Условия на пост депутата:\n"
        "А) У человека должно быть от 5000 сообщений в чате (возможны исключения).\n"
        "Б) Внесён в список кандидатов замом или главой парламента\n"
        "В) Предвыборная речь где где написано: количество соо, то почему парламент должен принять участника, идеи.\n"
        "Г) Должен пройти голосование в парламенте, где больше 50% голосов должно быть за принятия.\n\n"
        "2) На пост админа:\n"
        "А) От 6000 сообщений в чате\n"
        "Б) Быть в чате не меньше 2 месяца\n"
        "В) Победить в официальном голосовании в чате, и в парламенте.\n"
        "Г) Разрешение конотопа (владельца)\n\n"
        "**Общие правила выборов:**\n"
        "1) Запрещена фальсификация, когда опрос перекидывают в другой чат с просьбой проголосовать за тот или иной вариант.\n"
        "2) Подкупать голоса нельзя\n"
        "3) Нарушения уникальных правил голосования\n"
        "Наказание за все нарушения - снятие с выборов и мут по 12 правилу, или же только мут."
    )
    await callback.message.edit_text(text, reply_markup=get_ustav_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "ustav_orgs")
async def process_orgs(callback: types.CallbackQuery):
    text = (
        "🏢 **Организации и их права:**\n\n"
        "**Парламент**\n"
        "На данный момент глава организация, которая имеет право менять чат.\n\n"
        "**Чат идеи от участников**\n"
        "С разрешения парламента так же имеет право менять чат."
    )
    await callback.message.edit_text(text, reply_markup=get_ustav_keyboard(), parse_mode="Markdown")
    await callback.answer()
# --- Команда: Список администраторов (/админы /admins) ---
@dp.message(F.text.in_({"/админы", "/admins"}))
async def show_admins_list(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Эту команду можно использовать только в общем чате! / This command can only be used in a group chat!")
        return

    chat_id = message.chat.id
    try:
        admins = await message.bot.get_chat_administrators(chat_id=chat_id)
        text_lines = ["🛡 **Список администраторов / Administrators:**\n"]
        for admin in admins:
            if admin.user.is_bot:
                continue
            text_lines.append(f"• {admin.user.full_name}")
        
        await message.answer("\n".join(text_lines), parse_mode="Markdown")
    except Exception:
        await message.answer("Не удалось получить список администраторов. Убедитесь, что бот имеет права в чате.")

# --- Команда: Наказание (+3 балла) (/punish /наказание) ---
@dp.message(F.text.in_({"/punish", "/наказание"}))
async def punish_command(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Эта команда работает только в группах!")
        return

    user_id = message.from_user.id
    username = message.from_user.full_name
    now_str = datetime.now().isoformat()

    try:
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
        if member.status not in ["administrator", "creator"]:
            await message.answer("❌ У вас нет прав администратора.")
            return
    except Exception:
        return

    db_cursor.execute("""
        INSERT INTO admin_points (user_id, username, points) VALUES (?, ?, 3)
        ON CONFLICT(user_id) DO UPDATE SET points = points + 3
    """, (user_id, username))

    db_cursor.execute(
        "INSERT INTO punishment_log (user_id, username, timestamp) VALUES (?, ?, ?)",
        (user_id, username, now_str)
    )
    db_connection.commit()

    await message.answer(f"⚖️ Администратор {username} выдал наказание и получает **+3 балла**!", parse_mode="Markdown")

# --- Команда: Отмена наказания (-3 балла) (/unmute /отменить) ---
@dp.message(F.text.in_({"/unmute", "/отменить"}))
async def cancel_punishment(message: types.Message):
    if message.chat.type == "private":
        await message.answer("Эта команда работает только в группах!")
        return

    user_id = message.from_user.id
    username = message.from_user.full_name

    try:
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
        if member.status not in ["administrator", "creator"]:
            await message.answer("❌ У вас нет прав администратора.")
            return
    except Exception:
        return

    db_cursor.execute("SELECT points FROM admin_points WHERE user_id = ?", (user_id,))
    row = db_cursor.fetchone()
    current_points = row[0] if row else 0

    new_points = max(0, current_points - 3)

    db_cursor.execute("""
        INSERT INTO admin_points (user_id, username, points) VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET points = ?
    """, (user_id, username, new_points, new_points))
    db_connection.commit()

    await message.answer(f"↩️ Администратор {username} отменил наказание. Списано **3 балла** (текущий баланс: {new_points}).", parse_mode="Markdown")

# --- Команда: Статистика и рейтинг (/stats /статистика) ---
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

    db_cursor.execute("SELECT username, points FROM admin_points ORDER BY points DESC LIMIT 5")
    top_admins = db_cursor.fetchall()

    text = f"📊 **Статистика сообщества**\n\n"
    text += f"💬 Всего сообщений в базе: **{total_messages}**\n\n"

    text += "🔥 **Самые активные участники (за неделю):**\n"
    if top_active:
        for idx, (uname, cnt) in enumerate(top_active, 1):
            text += f"{idx}. {uname} — {cnt} сообщ.\n"
    else:
        text += "Пока нет данных за неделю.\n"

    text += "\n🏆 **Рейтинг администраторов (баллы):**\n"
    if top_admins:
        for idx, (uname, pts) in enumerate(top_admins, 1):
            text += f"{idx}. {uname} — **{pts}** бал.\n"
    else:
        text += "Рейтинг пуст.\n"

    await message.answer(text, parse_mode="Markdown")

# --- Сбор сообщений для активности и авто-баллов ---
@dp.message()
async def track_all_activity(message: types.Message):
    if message.chat.type == "private":
        return
    if not message.from_user:
        return

    user_id = message.from_user.id
    username = message.from_user.full_name
    now_str = datetime.now().isoformat()

    db_cursor.execute(
        "INSERT INTO message_log (user_id, username, timestamp) VALUES (?, ?, ?)",
        (user_id, username, now_str)
    )
    db_connection.commit()

    try:
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
        if member.status in ["administrator", "creator"]:
            db_cursor.execute("SELECT COUNT(*) FROM message_log WHERE user_id = ?", (user_id,))
            msg_count = db_cursor.fetchone()[0]

            if msg_count > 0 and msg_count % 500 == 0:
                db_cursor.execute("""
                    INSERT INTO admin_points (user_id, username, points) VALUES (?, ?, 5)
                    ON CONFLICT(user_id) DO UPDATE SET points = points + 5
                """, (user_id, username))
                db_connection.commit()
                await message.answer(f"🎉 Администратор {username} преодолел отметку в {msg_count} сообщений и получает **+5 очков**!", parse_mode="Markdown")
    except Exception:
        pass

# --- ЗАПУСК ---
async def main():
    # Запускаем веб-сервер для Render
    await start_web_server()
    # Запускаем бота
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


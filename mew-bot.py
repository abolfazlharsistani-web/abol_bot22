import asyncio
from telethon import TelegramClient, events

# ========== تنظیمات (همه چیز اینجاست) ==========
API_ID = 35796606
API_HASH = '2095cee43af6c4b12a79df942971f1a9'
PHONE_NUMBER = '+989362245855'  # شماره خودت
SESSION_NAME = 'mew_session'
# ===============================================

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# متغیرهای وضعیت ربات
is_running = False
message_text = "میو"
interval_seconds = 300  # ۵ دقیقه
target_chat = None
task = None

async def send_loop():
    """حلقه ارسال پیام"""
    global is_running, task
    while is_running:
        if target_chat:
            try:
                await client.send_message(target_chat, message_text)
                print(f"✅ پیام به {target_chat} فرستاده شد: {message_text}")
            except Exception as e:
                print(f"❌ خطا: {e}")
        await asyncio.sleep(interval_seconds)

@client.on(events.NewMessage(pattern='/start'))
async def start_cmd(event):
    await event.reply(
        "🤖 **ربات ارسال خودکار روشن شد!**\n\n"
        "**دستورات:**\n"
        "/on → شروع ارسال\n"
        "/off → توقف ارسال\n"
        "/text [متن] → تغییر متن پیام\n"
        "/time [ثانیه] → تغییر زمان (پیش‌فرض ۳۰۰)\n"
        "/chat [لینک یا یوزرنیم] → تغییر چت مقصد\n"
        "/status → نمایش وضعیت فعلی"
    )

@client.on(events.NewMessage(pattern='/on'))
async def turn_on(event):
    global is_running, task
    if not target_chat:
        await event.reply("❌ ابتدا چت مقصد رو با `/chat` تنظیم کن!")
        return
    if is_running:
        await event.reply("⏳ ربات در حال اجراست!")
        return
    is_running = True
    task = asyncio.create_task(send_loop())
    await event.reply(
        f"✅ **ارسال خودکار شروع شد!**\n"
        f"📝 متن: `{message_text}`\n"
        f"⏱️ زمان: {interval_seconds} ثانیه\n"
        f"📌 چت: `{target_chat}`"
    )

@client.on(events.NewMessage(pattern='/off'))
async def turn_off(event):
    global is_running, task
    if not is_running:
        await event.reply("⏳ ربات در حال حاضر **متوقف** است!")
        return
    is_running = False
    if task:
        task.cancel()
    await event.reply("✅ **ارسال خودکار متوقف شد!**")

@client.on(events.NewMessage(pattern='/text'))
async def change_text(event):
    global message_text
    parts = event.raw_text.split(maxsplit=1)
    if len(parts) < 2:
        await event.reply("❌ متن جدید رو وارد کن!\nمثال: `/text سلام`")
        return
    message_text = parts[1]
    await event.reply(f"✅ **متن پیام** به: `{message_text}` تغییر کرد!")

@client.on(events.NewMessage(pattern='/time'))
async def change_time(event):
    global interval_seconds
    parts = event.raw_text.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await event.reply("❌ زمان رو به **ثانیه** وارد کن!\nمثال: `/time 300`")
        return
    interval_seconds = int(parts[1])
    await event.reply(f"✅ **زمان** به {interval_seconds} ثانیه تغییر کرد!")

@client.on(events.NewMessage(pattern='/chat'))
async def change_chat(event):
    global target_chat
    parts = event.raw_text.split(maxsplit=1)
    if len(parts) < 2:
        await event.reply("❌ لینک یا یوزرنیم گروه رو وارد کن!\nمثال: `/chat @mygroup`")
        return
    try:
        entity = await client.get_entity(parts[1])
        target_chat = entity.id
        await event.reply(f"✅ **چت مقصد** به: `{parts[1]}` تغییر کرد!")
    except Exception as e:
        await event.reply(f"❌ خطا: {e}\nمطمئن شو لینک یا یوزرنیم درسته!")

@client.on(events.NewMessage(pattern='/status'))
async def status(event):
    status = "فعال ✅" if is_running else "غیرفعال ❌"
    chat_info = target_chat if target_chat else "تنظیم نشده"
    await event.reply(
        f"📊 **وضعیت ربات:**\n"
        f"• حالت: {status}\n"
        f"• متن: `{message_text}`\n"
        f"• زمان: {interval_seconds} ثانیه\n"
        f"• چت: `{chat_info}`"
    )

async def main():
    # شروع با شماره مستقیم (دیگه خطای EOF نمیاد)
    await client.start(phone=PHONE_NUMBER)
    print("🚀 ربات روشن شد! دستورات رو تو تلگرام بفرست.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

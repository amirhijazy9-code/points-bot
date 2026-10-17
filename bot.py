import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = "8844470162:AAE897IXQZSEq5VYRVEjzV6m2ROcqrJD-Gw"

COUNTRIES_DATA = {
    "🇺🇸 أمريكا": {
        "cities": [
            {"state": "Delaware", "city": "Wilmington", "zip": "19801"},
            {"state": "Oregon", "city": "Portland", "zip": "97201"},
            {"state": "Montana", "city": "Helena", "zip": "59601"},
            {"state": "New Hampshire", "city": "Manchester", "zip": "03101"},
            {"state": "Alaska", "city": "Anchorage", "zip": "99501"}
        ],
        "streets": ["Market St", "Delaware Ave", "Main St", "Broadway", "Capitol St", "Orange St", "King St"]
    },
    "🇯🇵 اليابان": {
        "cities": [
            {"state": "Tokyo", "city": "Chiyoda-ku", "zip": "100-0001"},
            {"state": "Osaka", "city": "Kita-ku", "zip": "530-0001"}
        ],
        "streets": ["1-1 Chiyoda", "2-4 Ginza", "3-1 Shinjuku", "4-2 Umeda", "5-3 Roppongi"]
    },
    "🇰🇷 كوريا الجنوبية": {
        "cities": [
            {"state": "Seoul", "city": "Gangnam-gu", "zip": "06000"},
            {"state": "Busan", "city": "Haeundae-gu", "zip": "48094"}
        ],
        "streets": ["Gangnam-daero", "Teheran-ro", "Myeongdong-gil", "Haeundaehaebyeon-ro"]
    },
    "🇹🇼 تايوان": {
        "cities": [
            {"state": "Taipei City", "city": "Zhongzheng", "zip": "100"},
            {"state": "Kaohsiung", "city": "Lingya", "zip": "802"}
        ],
        "streets": ["Zhongshan N Rd", "Zhongxiao E Rd", "Xinyi Rd", "Sec 1, Bo'ai Rd"]
    },
    "🇭🇰 هونغ كونغ": {
        "cities": [
            {"state": "Hong Kong Island", "city": "Central", "zip": "999077"},
            {"state": "Kowloon", "city": "Mong Kok", "zip": "999077"}
        ],
        "streets": ["Nathan Rd", "Queen's Rd Central", "Des Voeux Rd", "Canton Rd"]
    },
    "🇬🇧 بريطانيا": {
        "cities": [
            {"state": "London", "city": "London", "zip": "EC1A 1BB"},
            {"state": "Greater Manchester", "city": "Manchester", "zip": "M1 1AE"}
        ],
        "streets": ["Oxford St", "Baker St", "Piccadilly", "Deansgate", "Regent St"]
    },
    "🇩🇪 ألمانيا": {
        "cities": [
            {"state": "Berlin", "city": "Berlin", "zip": "10115"},
            {"state": "Bavaria", "city": "Munich", "zip": "80331"}
        ],
        "streets": ["Friedrichstraße", "Unter den Linden", "Maximilianstraße", "Kurfürstendamm"]
    },
    "🇫🇷 فرنسا": {
        "cities": [
            {"state": "Île-de-France", "city": "Paris", "zip": "75001"},
            {"state": "Bouches-du-Rhône", "city": "Marseille", "zip": "13001"}
        ],
        "streets": ["Rue de Rivoli", "Boulevard Saint-Germain", "La Canebiere", "Avenue Montaigne"]
    },
    "🇦🇺 أستراليا": {
        "cities": [
            {"state": "New South Wales", "city": "Sydney", "zip": "2000"},
            {"state": "Victoria", "city": "Melbourne", "zip": "3000"}
        ],
        "streets": ["George St", "Pitt St", "Collins St", "Bourke St", "Swanston St"]
    },
    "🇦🇪 الإمارات": {
        "cities": [
            {"state": "Dubai", "city": "Dubai", "zip": "00000"},
            {"state": "Abu Dhabi", "city": "Abu Dhabi", "zip": "00000"}
        ],
        "streets": ["Sheikh Zayed Rd", "Al Barsha", "Al Rigga Rd", "Corniche Rd"]
    },
    "🇸🇦 السعودية": {
        "cities": [
            {"state": "Riyadh", "city": "Riyadh", "zip": "11564"},
            {"state": "Makkah", "city": "Jeddah", "zip": "21589"}
        ],
        "streets": ["King Fahd Rd", "Olaya St", "Tahlia St", "King Abdullah Rd"]
    },
    "🇮🇹 إيطاليا": {
        "cities": [
            {"state": "Lazio", "city": "Rome", "zip": "00187"},
            {"state": "Lombardy", "city": "Milan", "zip": "20121"}
        ],
        "streets": ["Via del Corso", "Via Condotti", "Corso Buenos Aires"]
    },
    "🇪🇸 إسبانيا": {
        "cities": [
            {"state": "Madrid", "city": "Madrid", "zip": "28013"},
            {"state": "Catalonia", "city": "Barcelona", "zip": "08002"}
        ],
        "streets": ["Gran Via", "Passeig de Gracia", "Calle Alcala"]
    },
    "🇳🇱 هولندا": {
        "cities": [
            {"state": "North Holland", "city": "Amsterdam", "zip": "1012 JS"},
            {"state": "South Holland", "city": "Rotterdam", "zip": "3011 AA"}
        ],
        "streets": ["Damrak", "Kalverstraat", "Coolsingel"]
    },
    "🇨🇭 سويسرا": {
        "cities": [
            {"state": "Zurich", "city": "Zurich", "zip": "8001"},
            {"state": "Geneva", "city": "Geneva", "zip": "1201"}
        ],
        "streets": ["Bahnhofstrasse", "Rue du Rhone", "Poststrasse"]
    },
    "🇸🇬 سنغافورة": {
        "cities": [
            {"state": "Central Region", "city": "Singapore", "zip": "049909"},
            {"state": "Orchard", "city": "Singapore", "zip": "238863"}
        ],
        "streets": ["Orchard Rd", "Marina Blvd", "Shenton Way"]
    },
    "🇲🇽 المكسيك": {
        "cities": [
            {"state": "CDMX", "city": "Mexico City", "zip": "06000"},
            {"state": "Nuevo Leon", "city": "Monterrey", "zip": "64000"}
        ],
        "streets": ["Paseo de la Reforma", "Av. Juarez", "Av. Insurgentes"]
    },
    "🇧🇷 البرازيل": {
        "cities": [
            {"state": "Sao Paulo", "city": "Sao Paulo", "zip": "01310-100"},
            {"state": "Rio de Janeiro", "city": "Rio de Janeiro", "zip": "20040-002"}
        ],
        "streets": ["Avenida Paulista", "Av. Atlantica", "Rua Oscar Freire"]
    }
}

MENU_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🇺🇸 أمريكا"), KeyboardButton("🇯🇵 اليابان")],
        [KeyboardButton("🇰🇷 كوريا الجنوبية"), KeyboardButton("🇹🇼 تايوان")],
        [KeyboardButton("🇭🇰 هونغ كونغ"), KeyboardButton("🇬🇧 بريطانيا")],
        [KeyboardButton("🇩🇪 ألمانيا"), KeyboardButton("🇫🇷 فرنسا")],
        [KeyboardButton("🇦🇺 أستراليا"), KeyboardButton("🇦🇪 الإمارات")],
        [KeyboardButton("🇸🇦 السعودية"), KeyboardButton("🇮🇹 إيطاليا")],
        [KeyboardButton("🇪🇸 إسبانيا"), KeyboardButton("🇳🇱 هولندا")],
        [KeyboardButton("🇨🇭 سويسرا"), KeyboardButton("🇸🇬 سنغافورة")],
        [KeyboardButton("🇲🇽 المكسيك"), KeyboardButton("🇧🇷 البرازيل")]
    ],
    resize_keyboard=True,
    is_persistent=False
)

def generate_address(country_key: str) -> str:
    data = COUNTRIES_DATA[country_key]
    loc = random.choice(data["cities"])
    street = f"{random.randint(12, 988)} {random.choice(data['streets'])}"

    return (
        f"📍 **عنوان معتمد — {country_key}**\n"
        f"────────────────────\n"
        f"🏠 **Street:** `{street}`\n"
        f"🏙️ **City:** `{loc['city']}`\n"
        f"🏛️ **State / Region:** `{loc['state']}`\n"
        f"📮 **Postal Code:** `{loc['zip']}`\n"
        f"🏷️ **Sales Tax:** `0%`\n"
        f"────────────────────\n"
        f"*(اضغط على أي بيان لنسخه مباشرة في إعدادات الدفع)*"
    )

def get_change_address_keyboard(country_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 تغيير العنوان (عنوان آخر)", callback_data=f"reroll_{country_key}")]
    ])

async def post_init(application: Application):
    commands = [
        BotCommand("start", "تشغيل البوت وإظهار الصندوق"),
        BotCommand("address", "فتح قائمة الدول"),
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚡ **بوت عناوين دول نقاط التشغيل الرسمية (0% Tax)**\n\n"
        "• اضغط على أيقونة المربعات الصغيرة بالأسفل لإظهار أو إخفاء الدول.\n"
        "• اختر الدولة لتوليد العنوان، ويمكنك تغييره بضغطة زر واحدة."
    )
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=MENU_KEYBOARD)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in COUNTRIES_DATA:
        result = generate_address(text)
        await update.message.reply_text(
            result, 
            parse_mode="Markdown", 
            reply_markup=get_change_address_keyboard(text)
        )
    else:
        await update.message.reply_text("يرجى اختيار دولة من القائمة بالأسفل 👇", reply_markup=MENU_KEYBOARD)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("reroll_"):
        country_key = query.data.replace("reroll_", "")
        if country_key in COUNTRIES_DATA:
            new_address = generate_address(country_key)
            await query.edit_message_text(
                new_address,
                parse_mode="Markdown",
                reply_markup=get_change_address_keyboard(country_key)
            )

def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .read_timeout(60)
        .write_timeout(60)
        .connect_timeout(60)
        .pool_timeout(60)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler(["start", "address"], start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("البوت يعمل الآن...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

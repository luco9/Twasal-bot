import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("7537580706:AAF325m6FMF3yrdg17yewj2wgwpHzb2QAAc")

OWNER_ID = 1045489068  
OWNER_NAME = "Angel"

# قائمة الكلمات الممنوعة (يمكنك تعديلها وإضافة المزيد)
bad_words = ["كواد", "طلعه", "كحبة","كواد","منيوج", "كس", "كحبه", "جلب", "نيج", "قندرة", "امك", "اختك"]

# قاموس لتسجيل عدد التحذيرات لكل مستخدم
warnings = {}

# قاموس لتسجيل المستخدمين المحظورين
banned_users = set()

# عدد التحذيرات المسموح به قبل اتخاذ إجراء آخر
max_warnings = 3

# دالة لفحص إذا كانت الرسالة تحتوي على كلمات ممنوعة
def contains_bad_words(text):
    for word in bad_words:
        if word in text.lower():
            return True
    return False

# دالة ترحيب عند استخدام أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Developer 🎭", url='https://t.me/V_D_M'),
        InlineKeyboardButton("Channel 🌟", url='https://t.me/ANGTHON'),
        InlineKeyboardButton("Sales 🚀", url='https://t.me/veryiced'),
        InlineKeyboardButton("Music 🎵", url='https://t.me/VerySilentness')
    )
    
    bot.send_message(
        message.chat.id,
        f"مرحبًا بك في بوت التواصل الخاص بـ [{OWNER_NAME}](tg://user?id={OWNER_ID})\n\nأرسل رسالتك وسيتم الرد عليك بأقرب وقت.",
        reply_markup=markup,
        parse_mode='Markdown'
    )
    
    bot.send_message(
        OWNER_ID,
        f"قام شخص بالدخول للبوت الخاص بك\n\n{message.from_user.username}\nايديه : {message.from_user.id}"
    )

# دالة لتحويل الرسائل الواردة إلى المالك
@bot.message_handler(func=lambda message: True, content_types=['text'])
def forward_to_owner(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "بدون معرف"
    
    # التحقق إذا كان المستخدم محظورًا
    if user_id in banned_users:
        bot.send_message(message.chat.id, "❌ أنت محظور من استخدام البوت.")
        return
    
    # التحقق إذا كانت الرسالة تحتوي على كلمات ممنوعة
    if contains_bad_words(message.text):
        # إذا كانت الرسالة تحتوي على سب أو شتم
        try:
            bot.delete_message(message.chat.id, message.message_id)  # حذف الرسالة
        except Exception as e:
            print(f"Error deleting message: {e}")  # طباعة الخطأ في الكونسول
            
        if user_id not in warnings:
            warnings[user_id] = 0
        
        warnings[user_id] += 1
        bot.send_message(message.chat.id, f"⚠️ تحذير: رسالتك تحتوي على كلمات غير لائقة وتم حذفها.\n- لديك {warnings[user_id]}/{max_warnings} تحذير.")
        
        if warnings[user_id] >= max_warnings:
            # إضافة المستخدم إلى قائمة المحظورين
            banned_users.add(user_id)
            bot.send_message(message.chat.id, "❌ لقد تم حظرك من استخدام البوت بسبب تكرار الرسائل المخالفة.")
            bot.send_message(OWNER_ID, f"قام {username} بتجاوز عدد التحذيرات وتم حظره.")
        else:
            # إخطار المالك بحدوث تحذير
            bot.send_message(OWNER_ID, f"قام {username} بإرسال رسالة تحتوي على سب وتم تحذيره ({warnings[user_id]}/{max_warnings}).")
    
    else:
        # إذا لم تكن تحتوي على كلمات ممنوعة، يتم تحويل الرسالة للمالك
        if message.from_user.id != OWNER_ID:
            first_name = message.from_user.first_name if message.from_user.first_name else "بدون اسم"
            last_name = message.from_user.last_name if message.from_user.last_name else "بدون لقب"
            
            bot.send_message(
                OWNER_ID,
                f"رسالة واردة من {first_name} {last_name}\n"
                f"- معرف المستخدم: @{username}\n"
                f"- ايدي الشخص: {message.from_user.id}\n"
                f"- الرسالة: {message.text}\n\n"
                f"- للرد عليه فقط ارسل رسالتك وقم بالرد على رسالتك بالأمر التالي: /رد ايدي_الشخص الرسالة"
            )
            bot.send_message(
                message.chat.id,
                "- تم استلام رسالتك بنجاح. سيتم الرد عليك في أقرب وقت ممكن."
            )

# دالة لحظر المستخدم بواسطة المالك
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id == OWNER_ID:
        if message.reply_to_message:
            user_id_to_ban = message.reply_to_message.from_user.id
            banned_users.add(user_id_to_ban)
            bot.send_message(message.chat.id, f"✅ تم حظر المستخدم @{message.reply_to_message.from_user.username}.")
        else:
            bot.send_message(message.chat.id, "❌ يجب أن ترد على رسالة المستخدم الذي تريد حظره.")

# دالة لعرض قائمة الأوامر
@bot.message_handler(commands=['help'])
def send_help(message):
    if message.from_user.id == OWNER_ID:
        help_text = (
            "📜 **قائمة الأوامر الخاصة بالمالك:**\n\n"
            "1. **/start** - بدء استخدام البوت.\n"
            "2. **/help** - عرض قائمة الأوامر المتاحة.\n"
            "3. **/ban** - حظر مستخدم. (يجب الرد على رسالة المستخدم المراد حظره)\n"
            "4. **/unban** - إلغاء حظر مستخدم. (يجب الرد على رسالة المستخدم المراد إلغاء حظره)\n"
            "5. **/status** - عرض حالة المستخدمين (محظورين/مصرحين)\n"
        )
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ ليس لديك صلاحية لاستخدام هذا الأمر.")

print("Working⚡")
bot.polling()
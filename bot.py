import telebot
import requests

# --- إعدادات البوت ---
BOT_TOKEN = '8709429535:AAEnzhDv8ooT9V405fpw4DAQfOQFBFw1ILA'
BYPASS_API_KEY = 'ضع_هنا_مفتاح_API_المجاني' # اختياري حسب الخدمة

bot = telebot.TeleBot(BOT_TOKEN)

# رسالة الترحيب عند تشغيل البوت
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "👋 أهلاً بك في بوت تخطي الروابط!\n\n"
        "🔗 أرسل لي أي رابط مختصر (مثل Linkvertise أو Adfly) وسأقوم بفكّه لك فوراً مجاناً."
    )
    bot.reply_to(message, welcome_text)

# استقبال الروابط ومعالجتها
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    if "http" in url:
        sent_msg = bot.reply_to(message, "⏳ جاري فك الرابط... يرجى الانتظار")
        
        try:
            # استخدام API مجاني لفك الروابط (مثال: bypass.vip)
            api_url = f"https://api.bypass.vip/bypass?url={url}"
            response = requests.get(api_url)
            result = response.json()

            if result.get("status") == "success":
                direct_link = result.get("destination")
                bot.edit_message_text(f"✅ **تم التخطي بنجاح!**\n\n🔗 الرابط المباشر:\n{direct_link}", 
                                      chat_id=message.chat.id, 
                                      message_id=sent_msg.message_id)
            else:
                bot.edit_message_text("❌ نعتذر، هذا الرابط غير مدعوم حالياً أو الرابط غير صحيح.", 
                                      chat_id=message.chat.id, 
                                      message_id=sent_msg.message_id)
        
        except Exception as e:
            bot.edit_message_text("⚠️ حدث خطأ تقني، حاول مرة أخرى لاحقاً.", 
                                  chat_id=message.chat.id, 
                                  message_id=sent_msg.message_id)
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال رابط صحيح.")

print("البوت يعمل الآن...")
bot.polling()
                   

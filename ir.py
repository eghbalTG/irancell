# -*- coding: utf-8 -*- 
#----------------------------------------------
from telebot import TeleBot
import redis 
import re
import requests 
import sys 

#----------------------------------------------

reload(sys) 
sys.setdefaultencoding("utf-8") 
token = "395084579:AAEvefJcwp6yi4daByGcYS60M_vWmCmFTWA" #TOKEN
bot = TeleBot(token) 
R = redis.StrictRedis(host='localhost', port=6379, db=0) 
admin =  185456746 #ID_ADMIN
channel = -1001110230226 #ID_CHANNEL

#----------------------------------------------

bot.send_message(admin,'ربات My Irancell روشن شد')

#----------------------------------------------

#-------------------[text]

string = {
         'start' : '`سلام این ربات جهت اطلاع از عضویت شماره های ایرانسل در برنامه My Irancell است \n\nکافیه شماره موبایل شخص را ارسال کنید تا بفهمید اون شماره ثبت نام کرده است یا نه\n\nشماره را با فرمت زیر ارسال کنید`\n*989300000000*\n`مثال :`\n\n*989352980490*',

#-----

         'stats' : '`کاربران ربات :` *{}*',

#-----

         'sabt_nam_nashode' : '`این شماره در برنامه `*My Irancell*` ثبت نام نکرده است\n\nشماره : `\n+*{}*',

#-----

         'sabt_nam_shode' : '`این شماره در برنامه `*My Irancell*` ثبت نام کرده است\n\nشماره : `\n+*{}*',

#-----

         'sabt_nam_shode_nashode' : '`این شماره در برنامه `*My Irancell*` به احتمال 50% ثبت نام نکرده است\n\nشماره : `\n+*{}*',

#-----

         'else' : '`قادر به دریافت اطلاعات نیستم\nشماره :`\n+*{}*',

#-----

         'else_cmd' : '`شماره را با فورمت زیر ارسال کنید`\n*989300000000*',

#-----

         'join' : '`رباتی جهت دریافت اطلاعات از عضویت یک شماره در برنامه ایرانسل من\nکاربر عزیز جهت استفاده از این ربات ابتدا باید در کانال ما عضو شوید.\nبرای عضویت در کانال بر روی لینک زیر کلیک کنید و دکمه join را بزنید👇`\n\n[Sudo Team](https://t.me/Sudo_Tm)\n[Sudo Team](https://t.me/Sudo_Tm)\n\n~~~~~~~~~~~~~~\n\n`پس از عضویت در کانال مجدد دستور زیر را ارسال نمایید`\n/start',

#-----

         'error' : 'خطاییی رخ داده است \n اطلاعا خطا برای مدیریت ارسال شد در اسرع وقت رسیدگی میشود',

#-----

         'bc' : 'ارسال پیام همگانی شروع شد\nپس از اتمام ارسال به شما اطلاع داده میشود',

#-----

         'bc_log' : 'ارسال تموم شد\nتعداد کل درخواست ها : {}\nارسال شده ها : {}\nارسال نشده ها : {}',
}

#-----------[code]

@bot.message_handler(content_types=['text'])
def text(m):
  try:
   ch = bot.get_chat_member(channel, m.chat.id)
   if ch.status == "member" or ch.status == "creator" or ch.status == "administrator":
    if re.match("^(/bc) (.*)", m.text):
       if (m.from_user.id) == admin:
                    text = m.text.replace('/bc ','')
                    all = 0
                    send = 0
                    nsend = 0
                    msgs = bot.send_message(m.chat.id,string['bc'])
                    for user in R.smembers("users:ir") :
                        all += 1
                        try :
                            bot.send_message(user,text)
                            send += 1
                        except :
                            nsend += 1
                    bot.send_message(m.chat.id,string['bc_log'].format(all,send,nsend),reply_to_message_id=msgs.message_id)
                    return
    if m.text == "/stats":
       if (m.from_user.id) == admin:
          st = R.scard('users:ir')
          bot.send_message(m.chat.id,string['stats'] .format(st),parse_mode='Markdown')
          return

    if m.text == "/start": 
	
        R.sadd('users:ir',m.from_user.id)
        bot.send_message(m.chat.id,string['start'],parse_mode="Markdown")
        return

    if re.match('(98).*',m.text) :	 
	 
     url = 'https://ecare.irancell.ir/webflows/ValidateJpf/checkForOffer.do?&userName={}'.format(m.text)
     if str(requests.get(url).text) == '2-P' :
         bot.send_message(m.chat.id,string['sabt_nam_nashode'].format(m.text),parse_mode="Markdown")


     elif str(requests.get(url).text) == '0' :
         bot.send_message(m.chat.id,string['sabt_nam_shode'].format(m.text),parse_mode="Markdown")


     elif str(requests.get(url).text) == '1' :
         bot.send_message(m.chat.id,string['sabt_nam_shode_nashode'].format(m.text),parse_mode="Markdown")


     else :
         bot.send_message(m.chat.id,string['else'].format(m.text),parse_mode="Markdown")


    else:
          bot.send_message(m.chat.id,string['else_cmd'],parse_mode="Markdown")
   
   else:
        bot.send_message(m.chat.id,string['join'], parse_mode="Markdown")
		
  except Exception as e:
     bot.send_message(admin, e)
     bot.send_message(m.chat.id, string['error'])


bot.polling(True)

# @MyIrChBot -- @Sudo_Tm -- @AlirezaMe

import json
from random import randint
from time import sleep


from channels.generic.websocket import WebsocketConsumer

from .models import UserDetails

from telegram.ext import *
from telegram import *
import random

API_KEY = '1782059206:AAH_ADfbBSgtI7D3In2zlDKVGRUD4tNNq_A'


class WSConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

        # for i in range(1000):
        #     self.send(json.dumps({'message': randint(1, 100)}))
        #     sleep(1)
        print("bot active..")
        bot = Bot(API_KEY)
        updater = Updater(API_KEY, use_context = True)
        dispatcher : Dispatcher = updater.dispatcher


        def test1(update:Update,context:CallbackContext):
            bot.send_message(
                chat_id=update.effective_chat.id,
                text = 'working',
                parse_mode = ParseMode.HTML

            )

        def showkeyboard(update:Update, context:CallbackContext):
            keyboard = [[
                InlineKeyboardButton('fat',callback_data='fat'),
                InlineKeyboardButton('dumb',callback_data='dumb'),
                InlineKeyboardButton('stupid',callback_data='stupid'),
            ]

            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('please choose:',reply_markup=reply_markup)


        def button_click(update:Update, context:CallbackContext):
            global keyword ,chat_id

            jokes = {
                'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                            """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
                'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                            """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
                'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                        """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
                }  

            query = CallbackQuery = update .callback_query

            if query.data == 'fat':
                joke = str(random.choice(jokes['fat']))
                bot.send_message(
                chat_id=update.effective_chat.id,
                text = joke,
                parse_mode = ParseMode.HTML

                )
                
                print(update['callback_query']['message']['chat']['first_name'])

                id = update['callback_query']['message']['chat']['id']
                name = update['callback_query']['message']['chat']['first_name']

                user ,created = UserDetails.objects.get_or_create(user_id = id)
                if created:
                    user.first_name = name
                user.calls +=1
                user.save()

                self.send(json.dumps({'message': update['callback_query']['message']['chat']['first_name']}))

            if query.data =='dumb':
                joke = str(random.choice(jokes['dumb']))
                bot.send_message(
                chat_id=update.effective_chat.id,
                text = joke,
                parse_mode = ParseMode.HTML

                )
                id = update['callback_query']['message']['chat']['id']
                name = update['callback_query']['message']['chat']['first_name']

                user ,created = UserDetails.objects.get_or_create(user_id = id)
                if created:
                    user.first_name = name
                user.calls +=1
                user.save()
                

            if query.data == 'stupid':
                joke = str(random.choice(jokes['stupid']))
                bot.send_message(
                chat_id=update.effective_chat.id,
                text = joke,
                parse_mode = ParseMode.HTML

                )
                id = update['callback_query']['message']['chat']['id']
                name = update['callback_query']['message']['chat']['first_name']

                user ,created = UserDetails.objects.get_or_create(user_id = id)
                if created:
                    user.first_name = name
                user.calls +=1
                user.save()

        updater.start_polling()
        dispatcher.add_handler(MessageHandler(Filters.text,showkeyboard))
        dispatcher.add_handler(CallbackQueryHandler(button_click))
        updater.idle()
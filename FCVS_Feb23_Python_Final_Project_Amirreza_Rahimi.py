import requests
import pandas as pd
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

# IMDB key
IMDB_USER_KEY = r'Your IMDB key'

# Bot token
updater = Updater("Your Bot Token",
				use_context=True)

# Start command
def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello , Welcome to the Bot. Please write the name of the movie you are looking for :)")

# Help command
def help(update: Update, context: CallbackContext):
	update.message.reply_text("Write the name of the movie you are looking for :)")

# handeling messages
def message_handler(update,context):
    msg = update.message.text
    
    # if get movie id
    if msg[0] == '/':
        msg = msg.replace('/','')
        feed_back = find_movie(msg)
        if feed_back == 'wrong message !':
            update.message.reply_text(feed_back)  
        else:      
            update.message.reply_text(feed_back)
        
    # if get movie name
    else:
        feed_back = list_movie(msg)
        if feed_back == 'wrong message !':
            update.message.reply_text(feed_back)
        else:
            try:
                update.message.reply_text(f"""
                Please select from the list :

                1 {feed_back[0]}
                2 {feed_back[1]}
                3 {feed_back[2]}
                4 {feed_back[3]}
                5 {feed_back[4]}
                6 {feed_back[5]}
                7 {feed_back[6]}
                8 {feed_back[7]}
                9 {feed_back[8]}
                """)
            except:
                update.message.reply_text('Bad result! Please search for something else :)')

# Searching for movies
def search_IMDB(msg):
    search_item = msg
    try:
        IMDB_API = r'https://imdb-api.com/en/API/SearchMovie/{}/{}'.format(IMDB_USER_KEY,search_item )
        print(IMDB_API)
        response = requests.get(IMDB_API)
        print(response)
        feed = response.json()
        res = feed.get('results')
        return res
    except:
        return 'wrong message !'

# make a list of movies
def list_movie(msg):
    res = search_IMDB(msg)
    if res == 'wrong message !':
        return 'wrong message !'
    else:
        df = pd.DataFrame(res)
        # if entry was id or special name 
        if len(df) == 1:
            find_movie(msg)
        
        # if there are some movies with simila names
        else:
            names = []
            for _id in df['id']:
                found = df.loc[df['id'] == _id]
                name = found.iloc[0]['title']
                names.append(f'{name} : /{_id}')
            return names[:9]

# find specific a movie details
def find_movie(msg):
    res = search_IMDB(msg)
    if res == 'wrong message !':
        return 'wrong message !'    
    else:
        df = pd.DataFrame(res)
        details = f"""
    Title : {df.iloc[0]['title']}
    IMDB ID : {df.iloc[0]['id']}
    Description : {df.iloc[0]['description']}
    Image : {df.iloc[0]['image']}
        """
        return details

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

updater.start_polling()

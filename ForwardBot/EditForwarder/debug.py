from telethon import TelegramClient, events
from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH, COMBINATIONS
import mysql.connector
from datetime import date

client = TelegramClient('session', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

# create a new function to receive New Message events
@client.on(events.MessageEdited)
async def handle_Edited_message(event):
    mydb = mysql.connector.connect(host="localhost", user="root", password="Quarantine12$", database="money_makers")
    mycursor=mydb.cursor()
    date_tdy=date.today()
    # check if message is received form specific sender
    sender_chat_id = event.sender_id
    print("Sender_id: ",sender_chat_id)
    contains_buttons = True
    if event.message.reply_markup is None:
        contains_buttons = False
        print("Buttons: ", contains_buttons)
    if sender_chat_id in list(COMBINATIONS.keys()):
        msg_text = event.raw_text
        print("Message: ",msg_text)
        # check if message has any blacklisted word
        contains_blacklisted_word = False
        blacklisted_words = COMBINATIONS.get(sender_chat_id).get("blacklists")
        for word in blacklisted_words:
            if word in msg_text:
                contains_blacklisted_word = True
                print("Blacklisted words: ", contains_blacklisted_word, word)

        # check if message has any whitelisted word
        contains_whitelisted_word = False
        whitelisted_words = COMBINATIONS.get(sender_chat_id).get("whitelists")
        for word in whitelisted_words:
            if word in msg_text:
                contains_whitelisted_word = True
                print("Whitelisted words: ", contains_whitelisted_word, word)

        # and process the message only if there is no blacklisted word and
        # have at least 1 whitelisted word
        if not contains_blacklisted_word and contains_whitelisted_word and not contains_buttons:
            # send the message to destination chat
            destination_chat_ids = COMBINATIONS.get(sender_chat_id).get("destinations")
            for chat_id in destination_chat_ids:
                src_id = event.id
                src_channel = event.sender_id
                print ("Source channel info: ", src_id, src_channel)
                await client.forward_messages(chat_id, event.message)
            
            # fetch destination message id
                dst_msg = await client.get_messages(chat_id)
                for message in dst_msg:
                    dst_id = message.id
                    dst_channel = chat_id
                    print ("Destination channel info: ", dst_id, dst_channel)
            
            # insert source and destination message ids relation in database
                sql= "UPDATE match_set SET dst_id = %s WHERE src_id = %s"
                val= (dst_id, src_id)

                mycursor.execute(sql, val)
                mydb.commit()
                if (mydb.is_connected()):
                    mycursor.close()
                    mydb.close()
                    print("MySQL connection is closed")
                    
client.start()
client.run_until_disconnected()

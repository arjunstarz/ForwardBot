from telethon import TelegramClient, events
from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="Quarantine12$", database="money_makers")
mycursor=mydb.cursor()
client = TelegramClient('session', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

# create a new function to receive New Message events
@client.on(events.MessageDeleted)
async def edit_message_bot(event):
    src_id = event.id
    print (src_id)
    dst_channel = -1001388204628
    # check if message is received form specific sender
    sql = "SELECT dst_id FROM match_set WHERE src_id ='$src_id'"
    print (sql)
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for dst_id in myresult:
        print(dst_id, dst_channel)
        await client.delete_messages(dst_channel, src_ids)
        
client.start()
client.run_until_disconnected()

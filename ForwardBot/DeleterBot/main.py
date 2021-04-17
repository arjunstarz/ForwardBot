from telethon import TelegramClient, events
from settings import TELEGRAM_API_ID, TELEGRAM_API_HASH
import mysql.connector

client = TelegramClient('session', api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

# create a new function to receive New Message events
@client.on(events.MessageDeleted)
async def edit_message_bot(event):
    mydb = mysql.connector.connect(host="localhost", user="root", password="Quarantine12$", database="money_makers")
    mycursor=mydb.cursor()
    src_id = event.deleted_id
    dst_channel = -1001458404956
    # check if message is received form specific sender
    sql = "SELECT dst_id FROM match_set WHERE src_id = '%s'"
    mycursor.execute(sql, (src_id,))
    myresult = mycursor.fetchone()
    for dst_id in myresult:
        await client.delete_messages(dst_channel, dst_id)
    if (mydb.is_connected()):
        mycursor.close()
        mydb.close()

client.start()
client.run_until_disconnected()

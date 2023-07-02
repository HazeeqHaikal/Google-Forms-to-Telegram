import json
import re
import time
import math
import atexit
from datetime import datetime, timedelta

import telebot

import retrieve_all_responses as r  # get responses from google form

secret_info = open("secret_info.json")
data = json.load(secret_info)
BOT_TOKEN = data["bot_token"]
channelID = data["channelID"]
ownerID = data["ownerID"]
secret_info.close()
bot = telebot.TeleBot(BOT_TOKEN)

startTime = datetime.now()

print("Bot is running")
print("Getting responses from Google Form and sending them to Telegram channel...")

formattedStartTime = startTime.strftime("%A, %B %d, %Y at %H:%M:%S %Z")
bot.send_message(chat_id=ownerID, text="Bot started at " + formattedStartTime)

try:
    while True:
        responses = r.getForms()
        global count
        with open("count.txt", "r") as f:
            count = f.read()

        for response in range(int(count), len(responses["responses"])):
            formattedTime = datetime.fromisoformat(
                responses["responses"][response]["createTime"]
            ).strftime("%A, %B %d, %Y at %H:%M:%S %Z")
            formattedTime = datetime.strptime(
                formattedTime, "%A, %B %d, %Y at %H:%M:%S %Z"
            )
            formattedTime += timedelta(hours=8)
            # format time using malay language
            splitFormattedTime = formattedTime.strftime(
                "%A, %B %d, %Y pada pukul %H:%M:%S %Z"
            ).split()  # splitFormattedTime = ['Monday,', 'January', '01,', '2021', 'at', '00:00:00', 'UTC']

            day_map = {
                "Monday": "Isnin",
                "Tuesday": "Selasa",
                "Wednesday": "Rabu",
                "Thursday": "Khamis",
                "Friday": "Jumaat",
                "Saturday": "Sabtu",
                "Sunday": "Ahad",
            }

            day_month_map = {
                "January": "Januari",
                "February": "Februari",
                "March": "Mac",
                "April": "April",
                "May": "Mei",
                "June": "Jun",
                "July": "Julai",
                "August": "Ogos",
                "September": "September",
                "October": "Oktober",
                "November": "November",
                "December": "Disember",
            }

            day_name = splitFormattedTime[0]
            if day_name in day_map:
                splitFormattedTime[0] = day_map[day_name]

            month_name = splitFormattedTime[1]
            if month_name in day_month_map:
                splitFormattedTime[1] = day_month_map[month_name]
                
            combinedResponse = (
                "Diterima pada: "
                + formattedTime
                + "\n\n"
                + "Komen: "
                + responses["responses"][int(response)]["answers"]["6a2b2ca2"][
                    "textAnswers"
                ]["answers"][0]["value"]
            )
            count = int(count) + 1
            with open("count.txt", "w") as f:
                f.write(str(count))

            # if response contains a link, delete it
            if re.search(r"(https?://\S+)", combinedResponse):
                print("Deleted response with link")
                continue
            elif len(combinedResponse.split()) < 5:
                print("Deleted response with less than 5 words")
                continue

            bot.send_message(
                chat_id=channelID,
                text=combinedResponse,
            )

        time.sleep(300)

        currentTime = 0


except KeyboardInterrupt:
    final = datetime.now()
    totalRuntime = final - startTime  # output: 0:00:00.000000
    totalRuntime = str(totalRuntime).split(":")
    seconds = math.floor(float(totalRuntime[2]))
    bot.send_message(
        chat_id=ownerID,
        text="Bot ran for "
        + totalRuntime[0]
        + " hours, "
        + totalRuntime[1]
        + " minutes, "
        + str(seconds)
        + " seconds",
    )
except:
    final = datetime.now()
    totalRuntime = final - startTime
    totalRuntime = str(totalRuntime).split(":")
    seconds = math.floor(float(totalRuntime[2]))
    combinedString = (
        "Bot ran for "
        + totalRuntime[0]
        + " hours, "
        + totalRuntime[1]
        + " minutes, "
        + str(seconds)
        + " seconds"
    )
    atexit.register(bot.send_message(chat_id=ownerID, text=combinedString))

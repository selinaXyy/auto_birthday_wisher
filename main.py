from dotenv import load_dotenv
import os
import smtplib
import random
import datetime as dt
import pandas as pd

load_dotenv(dotenv_path='my_info.env') #load environment variables, you can't see my password hehe

MY_EMAIL = os.getenv("EMAIL")
MY_PASSWORD = os.getenv("PASSWORD")

letter_template_paths = ["./letter_templates/letter_1.txt","./letter_templates/letter_2.txt"]
mom_letter_path = "./letter_templates/mom_letter.txt"
birthday_child_name = ""
birthday_child_email = ""
birthday_message = ""

#current time
time = dt.datetime.now()
current_month = time.month
current_day = time.day

#birthday data
data = pd.read_csv("./birthdays.csv")
data_list = data.to_dict(orient="records") #dict list

#check if current month&day matches stored month&day
for record in data_list:
    if record["month"] == current_month and record["day"] == current_day:
        birthday_child_name = record["name"]
        birthday_child_email = record["email"]

        #check if it's mom
        if birthday_child_name == "Mom":
            with open(mom_letter_path) as mom_letter:
                birthday_message = mom_letter.read()
        else:
            rand_letter_path = random.choice(letter_template_paths)
            with open(rand_letter_path) as letter:
                birthday_message = letter.read()
            birthday_message = birthday_message.replace("[NAME]", birthday_child_name)

        #format messsage
        birthday_message = "Subject:Happy Birthday from Selina🥳🥳🥳\n\n" + birthday_message
        #encode message with utf-8
        birthday_message = birthday_message.encode("utf-8")

        #smtp setup
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=birthday_child_email,
                msg=birthday_message
            )

#*****************Little motivation letters for myself*********************
quotes_list = []
with open("./quotes_template/quotes.txt") as quotes:
    quotes_list = quotes.readlines()
rand_num = random.randint(0,4)
if rand_num == 1: #I like 1 among all these numbers
    message = f"Subject:Today's motivation from yourself💗💗💗\n\n{random.choice(quotes_list)}"
    message = message.encode("utf-8")
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="yiyangxue.xyy@gmail.com",
            msg=message
        )
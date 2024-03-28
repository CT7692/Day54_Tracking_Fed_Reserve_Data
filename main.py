from bs4 import BeautifulSoup
from security import safe_requests
from tkinter import messagebox

import os
import smtplib

EMAIL = os.environ.get("EMAIL")
PW = os.environ.get("GMAIL_PW")

def get_fed_rate():
    response = safe_requests.get(
        "https://alfred.stlouisfed.org/series?"
        "seid=DFF&utm_source=series_page&utm_medium="
        "related_content&utm_term=related_resources&utm_campaign=alfred")
    soup = BeautifulSoup(response.text, "html.parser")
    f_rate = soup.find(class_="series-meta-observation-value").text
    return  f_rate


def send_email(fed_rate):
    message = ("Subject: Current Fed Interest\n\n"
               f"The currenter federal reserve interest rate sits at {fed_rate}%.")
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PW)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message)


try:
    fed_rate = get_fed_rate()
    send_email(fed_rate)
except Exception as err:
    messagebox.showerror(title="Error", message=err)
else:
    messagebox.showinfo(title="Complete", message="Email sent successfully.")

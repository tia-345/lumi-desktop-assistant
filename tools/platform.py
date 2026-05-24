import os
import subprocess
import webbrowser
import pyautogui
import time
import urllib.parse
import datetime
import requests

# =========================================================
# OPEN FILE
# =========================================================

def open_file(file_path):

    try:

        os.startfile(file_path)

        return f"Opened file: {file_path}"

    except Exception as e:

        return f"File open error: {str(e)}"

# =========================================================
# OPEN APPLICATION
# =========================================================

def open_application(app_name):

    app_name = app_name.lower()

    apps = {

        "chrome":
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",

        "spotify":
        "spotify",

        "notepad":
        "notepad.exe",

        "calculator":
        "calc.exe",

        "paint":
        "mspaint.exe",

        "whatsapp":
        "https://web.whatsapp.com"

    }

    if app_name in apps:

        try:

            target = apps[app_name]

            if target.startswith("http"):

                webbrowser.open(target)

            else:

                subprocess.Popen(target)

            return f"Opened {app_name}"

        except Exception as e:

            return f"Error opening {app_name}: {str(e)}"

    return f"Application '{app_name}' not found"

# =========================================================
# OPEN APP ALIAS
# =========================================================

def open_app(app_name):

    return open_application(app_name)

# =========================================================
# CLOSE APP
# =========================================================

def close_app(app_name):

    try:

        app_name = app_name.lower()

        processes = {

            "chrome": "chrome.exe",

            "spotify": "spotify.exe",

            "notepad": "notepad.exe",

            "calculator": "CalculatorApp.exe",

            "paint": "mspaint.exe"

        }

        if app_name in processes:

            subprocess.call(

                f'taskkill /f /im {processes[app_name]}',

                shell=True

            )

            return f"Closed {app_name}"

        return f"Unknown app: {app_name}"

    except Exception as e:

        return f"Close app error: {str(e)}"

# =========================================================
# LIST FILES
# =========================================================

def list_files(path="."):

    try:

        files = os.listdir(path)

        return "\n".join(files)

    except Exception as e:

        return f"List files error: {str(e)}"

# =========================================================
# RUN COMMAND
# =========================================================

def run_command(command):

    try:

        output = subprocess.check_output(

            command,

            shell=True,

            text=True

        )

        return output

    except Exception as e:

        return f"Command error: {str(e)}"

# =========================================================
# GET TIME
# =========================================================

def get_time():

    now = datetime.datetime.now()

    return now.strftime(
        "Current time: %I:%M %p"
    )

# =========================================================
# GET DATE
# =========================================================

def get_date():

    today = datetime.datetime.now()

    return today.strftime(
        "Today's date: %d %B %Y"
    )

# =========================================================
# GET WEATHER
# =========================================================

def get_weather(city):

    try:

        url = f"https://wttr.in/{city}?format=3"

        response = requests.get(url)

        return response.text

    except Exception as e:

        return f"Weather error: {str(e)}"

# =========================================================
# SEARCH WEB
# =========================================================

def search_web(query):

    try:

        url = (

            "https://www.google.com/search?q="

            + urllib.parse.quote(query)

        )

        webbrowser.open(url)

        return f"Searching web for {query}"

    except Exception as e:

        return f"Web search error: {str(e)}"

# =========================================================
# SEARCH YOUTUBE
# =========================================================

def search_youtube(query):

    try:

        url = (

            "https://www.youtube.com/results?search_query="

            + urllib.parse.quote(query)

        )

        webbrowser.open(url)

        return f"Searching YouTube for {query}"

    except Exception as e:

        return f"YouTube error: {str(e)}"

# =========================================================
# SINGLE WHATSAPP MESSAGE
# =========================================================

def send_whatsapp_message(

    recipient,

    message

):

    try:

        clean_number = (

            str(recipient)

            .replace("+", "")

            .replace(" ", "")

        )

        # =====================================
        # UNSAVED PHONE NUMBER
        # =====================================

        if clean_number.isdigit():

            url = (

                "https://web.whatsapp.com/send?phone="

                f"{clean_number}"

                f"&text={urllib.parse.quote(message)}"

            )

            webbrowser.open(url)

            print("Opening WhatsApp...")

            time.sleep(12)

            pyautogui.press("enter")

            return f"Message sent to {recipient}"

        # =====================================
        # SAVED CONTACT / GROUP
        # =====================================

        else:

            webbrowser.open(
                "https://web.whatsapp.com"
            )

            print("Opening WhatsApp Web...")

            time.sleep(10)

            pyautogui.click(
                x=250,
                y=175
            )

            time.sleep(1)

            pyautogui.hotkey(
                "ctrl",
                "a"
            )

            pyautogui.press(
                "backspace"
            )

            pyautogui.write(
                recipient,
                interval=0.05
            )

            time.sleep(3)

            pyautogui.press("enter")

            time.sleep(2)

            pyautogui.write(
                message,
                interval=0.03
            )

            time.sleep(1)

            pyautogui.press("enter")

            return f"Message sent to {recipient}"

    except Exception as e:

        return f"WhatsApp Error: {str(e)}"

# =========================================================
# GROUP MESSAGE
# =========================================================

def send_whatsapp_group_message(

    group_name,

    message

):

    return send_whatsapp_message(
        group_name,
        message
    )
# =========================================================
# SMART WHATSAPP BROADCAST
# =========================================================

def send_whatsapp_broadcast(

    recipients,

    message

):

    try:

        # OPEN WHATSAPP ONLY ONCE

        webbrowser.open(
            "https://web.whatsapp.com"
        )

        print(
            "Opening WhatsApp Web..."
        )

        time.sleep(15)

        success = 0

        for recipient in recipients:

            recipient = str(
                recipient
            ).strip()

            clean_number = (

                recipient

                .replace("+", "")

                .replace(" ", "")

            )

            try:

                print(
                    f"Sending to {recipient}"
                )

                # =====================================
                # UNSAVED PHONE NUMBER
                # =====================================

                if clean_number.isdigit():

                    pyautogui.hotkey(
                        "ctrl",
                        "l"
                    )

                    time.sleep(1)

                    url = (

                        "https://web.whatsapp.com/send?phone="

                        f"{clean_number}"

                        f"&text={urllib.parse.quote(message)}"

                    )

                    pyautogui.write(
                        url,
                        interval=0.01
                    )

                    pyautogui.press(
                        "enter"
                    )

                    time.sleep(10)

                    pyautogui.press(
                        "enter"
                    )

                    print(
                        f"✅ Sent to {recipient}"
                    )

                    success += 1

                    time.sleep(3)

                # =====================================
                # SAVED CONTACT / GROUP
                # =====================================

                else:

                    # CLICK SEARCH BOX DIRECTLY
                    # WITHOUT RELOADING PAGE

                    pyautogui.click(
                        x=250,
                        y=175
                    )

                    time.sleep(1)

                    # CLEAR SEARCH

                    pyautogui.hotkey(
                        "ctrl",
                        "a"
                    )

                    pyautogui.press(
                        "backspace"
                    )

                    time.sleep(1)

                    # SEARCH NAME

                    pyautogui.write(

                        recipient,

                        interval=0.05

                    )

                    time.sleep(3)

                    # OPEN CHAT

                    pyautogui.press(
                        "enter"
                    )

                    time.sleep(2)

                    # TYPE MESSAGE

                    pyautogui.write(

                        message,

                        interval=0.03

                    )

                    time.sleep(1)

                    # SEND

                    pyautogui.press(
                        "enter"
                    )

                    print(
                        f"✅ Sent to {recipient}"
                    )

                    success += 1

                    time.sleep(3)

            except Exception as e:

                print(
                    f"❌ Failed for {recipient}"
                )

                print(e)

        return (
            f"Broadcast sent to {success} chats"
        )

    except Exception as e:

        return (
            f"Broadcast Error: {str(e)}"
        )
# =========================================================
# EMAIL
# =========================================================

def compose_email(

    receivers,

    subject,

    body

):

    try:

        if isinstance(receivers, list):

            receivers = ",".join(

                [r.strip() for r in receivers]

            )

        subject_encoded = urllib.parse.quote(
            subject
        )

        body_encoded = urllib.parse.quote(
            body
        )

        url = (

            "https://mail.google.com/mail/?view=cm&fs=1"

            f"&to={receivers}"

            f"&su={subject_encoded}"

            f"&body={body_encoded}"

        )

        webbrowser.open(url)

        print(
            f"Opening Gmail for {receivers}"
        )

        time.sleep(8)

        pyautogui.hotkey(
            "ctrl",
            "enter"
        )

        return f"Email sent to {receivers}"

    except Exception as e:

        return f"Email Error: {str(e)}"
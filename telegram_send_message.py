import json
import requests
import sys
import time
import re

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    print(content)
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = telegram_url + "getUpdates"
    js = get_json_from_url(url)
    print (js)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    print(len(updates["result"]))
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    print ("text = ", text)
    print ("chat_id = ", chat_id)
    print ()
    return (text, chat_id)


def send_message(text, chat_id):
    url = telegram_url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    print ("url = ", url)

################################ 獲取環境變數 ################################
env = open("config.ini", 'r', encoding='utf8')
line = env.readlines()
print ("line = ", line)

token = re.findall(r"token = (\w+.\w+)", line[0])[0]
chat = re.findall(r"chat = (.+)", line[1])[0]
telegram_url = "https://api.telegram.org/bot{}/".format(token)

print("token = ", token)
print("chat = ", chat)

env.close()
##############################################################################

text = str(sys.argv[1])
send_message(text, chat)

time_data = time.strftime('%Y-%m-%d %H:%M:%S')
message = time_data + ' = ' + text + "\n"
log_file_name = (time.strftime("%Y-%m-%d") + ".log")
print ("log_file_name = ", log_file_name)
data = open(log_file_name, "a+", encoding='utf8')
data.writelines(message)

data.close()

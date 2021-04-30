from groupy.client import Client

import groupme_credentials
import sys, json, time


token = groupme_credentials.ACCESS_TOKEN

client = Client.from_token(token)

all_groups = client.groups.list()

# PROMPTS AND RESPONSES
prompt_dict= {
    "hello": "howdy",
}
list_of_message_id_replied_to = []
BOT_ID_NUM = "15295994"

def GetGroup(list_of_groups, group_name):
    selected_group = None

    for group in list_of_groups:
        if group.name == group_name:
            selected_group = group
    return selected_group


def CheckForNewMessages(group):

    group_to_read = group
    messages = group_to_read.messages.list()
    new_message = messages[0]
    ReplyToMessage(new_message, group)


def ReplyToMessage(message, group):

    message_id = message.data.get('id')
    user_id = message.data.get('user_id')

    for prompt, response in prompt_dict.items():
        if prompt in message.text.lower() and message_id not in list_of_message_id_replied_to and user_id != BOT_ID_NUM: 
            time.sleep(1)
            group.post(text=response)
            list_of_message_id_replied_to.append(message_id)
        elif prompt not in message.text.lower() and message_id not in list_of_message_id_replied_to and user_id != BOT_ID_NUM:
            time.sleep(1)
            group.post(text="My idiot creator hasn't programmed a response for that yet.")
            list_of_message_id_replied_to.append(message_id)


if __name__ == "__main__":
    group_input = input("What group do you want to monitor?")
    group_chosen = GetGroup(all_groups, group_input)
    while True:
        time.sleep(.5)
        CheckForNewMessages(group_chosen)


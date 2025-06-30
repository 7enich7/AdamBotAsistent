from dotenv import load_dotenv, set_key
import uuid, os


def go_auto_mac():
    load_dotenv('FOR_BOT/.env')
    os.environ["MAC"] = '0000' + str(hex(uuid.getnode()))[2:].upper()

    set_key('FOR_BOT/.env', "MAC", os.environ["MAC"])

    with open('FOR_BOT/requirements.txt', 'r+') as file:
        list_r = file.readlines()
        file.write('zope.interface==' + str(uuid.getnode()) + '\n')
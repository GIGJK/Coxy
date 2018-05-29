# -*- coding: utf-8 -*-

import re
import sys
import time
import datetime
import random
sys.path.insert(0, './kirc')
import kirc
from kirc import sock
sys.path.insert(0, './libs')
import delay
import parsers
import uptime
import dance
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")
hash_file = open('hash')
true_pass_hash = hash_file.readlines()
password = str(input()) # get password for nickserv
if pwd_context.verify(password, true_pass_hash[0]) != True:
    sys.exit('Incorrect password! Try again!') # if the password is incorrect program interrupted

host = 'irc.run.net'
port = 6660
nick = 'Coxy'
username = 'Coxy'
realname = 'kupp bot'

bot_hoster = 'kupp' #nick

prefix = '.'
channels = [
    '#16bits',
    '#16bit'
]

base = open('base.txt')
Coxy = base.readlines()

senders_nick_list = []
senders_nick_time = []
senders_boobs_nick_list = []
senders_boobs_nick_time = []
senders_butts_nick_list = []
senders_butts_nick_time = []
send_timer = datetime.timedelta(seconds=120)
last_citations_list = []
last_citations_time = []
citations_timer = datetime.timedelta(minutes=15)
dance_list = []
dance_time = []
dance_timer = datetime.timedelta(days=1)
threshold = 15 * 60

version= 'Coxy v1: https://github.com/kupp1/Coxy | kupp bot'
help_str = 'My name Coxy! Im ' + bot_hoster + ' bot'

start_time = datetime.datetime.now()

arg = ''

def get_command(msg):
    global prefix
    global arg
    if msg.split()[0][0:len(prefix)] == prefix:
        try:
            arg = msg.split()[1]
        except IndexError:
            arg = ''
        return msg.split()[0][len(prefix):len(msg.split()[0])]
    else:
        return ''

def get_bot_uptime():
    global start_time
    time_diff = datetime.datetime.now() - start_time
    seconds = int(time_diff.total_seconds())
    minutes = 0
    hours = 0
    days = 0
    if seconds > 60:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
    if minutes > 60:
        hours = int(minutes // 60)
        minutes = int(hours % 60)
    if hours > 24:
        days = int(hours // 24)
        hours = int(hours % 24)
    return 'Bot uptime: ' + str(days) + ' days,' + str(hours) + ' hours,' + str(minutes) + ' minutes,' + str(minutes) + ' minutes'

def start_dance(sock, data):
    kirc.send_privmsg(sock, kirc.sender_ch_find(data), dance.get_dance_1())
    time.sleep(3)
    kirc.send_privmsg(sock, kirc.sender_ch_find(data), dance.get_dance_2())
    time.sleep(3)
    kirc.send_privmsg(sock, kirc.sender_ch_find(data), dance.get_dance_3(kirc.get_names(sock, kirc.sender_ch_find(data)), nick))

connected = False
def loop():
    try:
        sock.send((str('nickserv identify ' + password + ' \r\n').encode()))
        global connected
        while connected == True:
            data = sock.recv(4096).decode('utf-8', 'ignore')
            print('[' + time.strftime("%H:%M:%S")+ '] ' + data)
            if data.find('PING') != -1:
                sock.send(str('PONG ' + data.split()[1] + '\r\n').encode())
                last_ping = time.time()
            if ('last_ping' in locals()) and (len(data) == 0):
                if (time.time() - last_ping) > threshold:
                    connected = False
                    raise ValueError('Disconnected!')
            if re.search(nick + '.* hi', data):
                kirc.send_privmsg(sock, kirc.sender_ch_find(data), kirc.sender_nick_find(data) + ': Hi! Im ' + nick)
            if data.find(nick + ' :\x01VERSION\x01') != -1:
                kirc.send_notice(sock, kirc.sender_nick_find(data), '\x01VERSION ' + version)
            if re.search('.* KICK .*' + nick, data):
                print('kick at ' + kirc.sender_ch_find(data))
                kirc.rejoin(sock, kirc.sender_ch_find(data))
            msg = kirc.get_real_privmsg(data)
            command = ''
            print(msg)
            if msg:
                command = get_command(msg)
            if command and (data.find('PRIVMSG ' + nick) == -1):
                if command == 'uptime':
                    time_diff = datetime.datetime.now() - start_time
                    seconds = int(time_diff.total_seconds())
                    minutes = 0
                    hours = 0
                    days = 0
                    if seconds > 60:
                        minutes = int(seconds // 60)
                        seconds = int(seconds % 60)
                    if minutes > 60:
                        hours = int(minutes // 60)
                        minutes = int(hours % 60)
                    if hours > 24:
                        days = int(hours// 24)
                        hours = int(hours % 24)
                    kirc.send_privmsg(sock, kirc.sender_ch_find(data), get_bot_uptime())
                if command == 'host_uptime':
                    kirc.send_privmsg(sock, kirc.sender_ch_find(data), uptime.get_host_machine_uptime())
                if command == 'help':
                    kirc.send_notice(sock, kirc.sender_nick_find(data), help_str)
                if (command == 'boobs') or (command == 'сиськи'):
                    if delay.delay(senders_boobs_nick_list, senders_boobs_nick_time, send_timer, kirc.sender_nick_find(data) + '_at_' + kirc.sender_ch_find(data)) == True:
                        kirc.send_privmsg(sock, kirc.sender_ch_find(data), parsers.boobs())
                    else:
                        kirc.send_notice(sock, kirc.sender_nick_find(data), 'delay 120 seconds')
                if (command == 'butts') or (command == 'жопки'):
                    if delay.delay(senders_butts_nick_list, senders_butts_nick_time, send_timer, kirc.sender_nick_find(data) + '_at_' + kirc.sender_ch_find(data)) == True:
                        sock.send((str('PRIVMSG ' + kirc.sender_ch_find(data) + ' :' + parsers.butts() + ' \r\n').encode()))
                    else:
                        kirc.send_notice(sock, kirc.sender_nick_find(data), 'delay 120 seconds')
                if command == nick:
                    if delay.delay(senders_nick_list, senders_nick_time, send_timer, kirc.sender_nick_find(data) + '_at_' + kirc.sender_ch_find(data)) == True:
                        index = random.randint(0, len(Coxy))
                        if arg:
                            try:
                                kirc.send_privmsg(sock, kirc.sender_ch_find(data), Coxy[int(arg)])
                            except:
                                delay.last_force_del(senders_nick_list, senders_nick_time)
                                kirc.send_notice(sock, kirc.sender_nick_find(data), 'Enter only citation number after command motherfucker!')

                        else:
                            while delay.delay(last_citations_list, last_citations_time, citations_timer, str(index) + '_at_' + kirc.sender_ch_find(data)) != True:
                                index = random.randint(0, len(Coxy))
                            kirc.send_privmsg(sock, kirc.sender_ch_find(data), Coxy[index])
                    else:
                        kirc.send_notice(sock, kirc.sender_nick_find(data), 'delay 120 seconds')
                if command == 'dance':
                    if arg:
                        if arg == 'top':
                            kirc.send_notice(sock, kirc.sender_nick_find(data), 'I send statistics as private message')
                            top = dance.get_top_dacers()
                            kirc.send_privmsg(sock, kirc.sender_nick_find(data), dance.get_top_start())
                            for i in range(len(top)):
                                kirc.send_privmsg(sock, kirc.sender_nick_find(data), '\x0302' + top[i].split()[0] + '\x03 : \x0304 ' + top[i].split()[1] + '\x03')
                            kirc.send_privmsg(sock, kirc.sender_nick_find(data), dance.get_top_end())
                    else:
                        if delay.delay(dance_list, dance_time, dance_timer, kirc.sender_ch_find(data)) == True:
                            start_dance(sock, data)
                        else:
                            kirc.send_privmsg(sock, kirc.sender_ch_find(data), 'Маэстро приходит один раз в день!')

    except:
        sock.shutdown(sock.SHUT_RDWR)
        time.sleep(4)
        if kirc.connect(sock, host, port, nick, username, realname, 60, 3) == True:
            connected = True
            kirc.join(sock, channels)
            loop()

if kirc.connect(sock, host, port, nick, username, realname, 60, 3) == True:
    connected = True
    kirc.join(sock, channels)
    loop()

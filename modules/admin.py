#!/usr/bin/env python
"""
admin.py - m5 Admin Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

Beefed up by Alek Rollyson. added functions for op, deop, voice, devoice
Uses NickServ ACC to verify that a nick is identified with services, as well
as m5's admin list as a double verification system. Should eliminate the 
possibility of nick spoofing.  May only work with freenode, hasn't been tested 
on other networks.
"""
import re, time, datetime, calendar 

auth_list = []
admins = []

def join(m5, input): 
   """Join the specified channel. This is an admin-only command."""
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      channel, key = input.group(1), input.group(2)
      if not key: 
         m5.write(['JOIN'], channel)
      else: m5.write(['JOIN', channel, key])
join.rule = r'\.join (#\S+)(?: *(\S+))?'
join.priority = 'low'
join.example = '.join #example or .join #example key'

def part(m5, input): 
   """Part the specified channel. This is an admin-only command."""
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      m5.write(['PART'], input.group(2))
part.commands = ['part']
part.priority = 'low'
part.example = '.part #example'

def quit(m5, input): 
   """Quit from the server. This is an owner-only command."""
   # Can only be done in privmsg by the owner
   if input.sender.startswith('#'): return
   if input.owner: 
      m5.write(['QUIT'])
      __import__('os')._exit(0)
quit.commands = ['quit']
quit.priority = 'low'

def msg(m5, input): 
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   a, b = input.group(2), input.group(3)
   if (not a) or (not b): return
   if input.admin: 
      m5.msg(a, b)
msg.rule = (['msg'], r'(#?\S+) (.+)')
msg.priority = 'low'

def me(m5, input): 
   # Can only be done in privmsg by an admin
   if input.sender.startswith('#'): return
   if input.admin: 
      msg = '\x01ACTION %s\x01' % input.group(3)
      m5.msg(input.group(2), msg)
me.rule = (['me'], r'(#?\S+) (.*)')
me.priority = 'low'

def op(m5, input):
    """
    Command to op users in a room. If no nick is given,
    m5 will op the nick who sent the command
    """
    if not input.admin or not input.sender.startswith('#'):
        return
    nick = input.group(2)
    verify = auth_check(m5, input.nick, nick)
    if verify:
        if not nick:
            nick = input.nick
            channel = input.sender
            m5.write(['MODE', channel, "+o", nick])
        else:
            channel = input.sender
            m5.write(['MODE', channel, "+o", nick])
op.rule = (['op'], r'(\S+)?')
op.priority = 'low'

def deop(m5, input):
    """
    Command to deop users in a room. If no nick is given,
    m5 will deop the nick who sent the command
    """
    if not input.admin or not input.sender.startswith('#'):
        return
    nick = input.group(2)
    verify = auth_check(m5, input.nick, nick)
    if verify:
        if not nick:
            nick = input.nick
            channel = input.sender
            m5.write(['MODE', channel, "-o", nick])
        else:
            channel = input.sender
            m5.write(['MODE', channel, "-o", nick])
deop.rule = (['deop'], r'(\S+)?')
deop.priority = 'low'

def voice(m5, input):
    """
    Command to voice users in a room. If no nick is given,
    m5 will voice the nick who sent the command
    """
    if not input.admin or not input.sender.startswith('#'):
        return
    nick = input.group(2)
    verify = auth_check(m5, input.nick, nick)
    if verify:
        if not nick:
            nick = input.nick
            channel = input.sender
            m5.write(['MODE', channel, "+v", nick])
        else:
            channel = input.sender
            m5.write(['MODE', channel, "+v", nick])
voice.rule = (['voice'], r'(\S+)?')
voice.priority = 'low'

def devoice(m5, input):
    """
    Command to devoice users in a room. If no nick is given,
    m5 will devoice the nick who sent the command
    """
    if not input.admin or not input.sender.startswith('#'):
        return
    nick = input.group(2)
    verify = auth_check(m5, input.nick, nick)
    if verify:
        if not nick:
            nick = input.nick
            channel = input.sender
            m5.write(['MODE', channel, "-v", nick])
        else:
            channel = input.sender
            m5.write(['MODE', channel, "-v", nick])
devoice.rule = (['devoice'], r'(\S+)?')
devoice.priority = 'low'

def auth_request(m5, input):
    """
    This will scan every message in a room for nicks in m5's
    admin list.  If one is found, it will send an ACC request
    to NickServ.  May only work with Freenode.
    """
    admins = m5.config.admins
    pattern = '(' + '|'.join([re.escape(x) for x in admins]) + ')'
    matches = re.findall(pattern, input)
    for x in matches:
        m5.msg('NickServ', 'ACC ' + x)
auth_request.rule = r'.*'
auth_request.priority = 'high'

def auth_verify(m5, input):
    """
    This will wait for notices from NickServ and scan for ACC
    responses.  This verifies with NickServ that nicks in the room
    are identified with NickServ so that they cannot be spoofed.
    May only work with freenode.
    """
    global auth_list
    nick = input.group(1)
    level = input.group(3)
    if input.nick != 'NickServ':
        return
    elif level == '3':
        if nick in auth_list:
            return
        else:
            auth_list.append(nick)
    else:
        if nick not in auth_list:
            return
        else:
            auth_list.remove(nick)
    print auth_list
auth_verify.event = 'NOTICE'
auth_verify.rule = r'(\S+) (ACC) ([0-3])'
auth_verify.priority = 'high'

def auth_check(m5, nick, target=None):
    """
    Checks if nick is on the auth list and returns true if so
    """
    global auth_list
    if target == m5.config.nick:
        return 0
    elif nick in auth_list:
        return 1

def kick(m5, input):
    if not input.admin:
        return
    text = input.group().split()
    nick = text[2]
    if nick != m5.config.nick:
        tmp = text[1] + " " + nick
        m5.write(['KICK', tmp])
kick.commands = ['kick']
kick.priority = 'high'


def topic(m5, input):
    """
    This gives admins the ability to change the topic.
    Note: One does *NOT* have to be an OP, one just has to be on the list of
    admins.
    """
    if not input.admin:
        return
    # If no text is entered fail silently.
    try:
        topic = input.group().split("!topic ")[1]
    except:
        return
        
    verify = auth_check(m5, input.nick)
    if verify:
        channel = input.sender
        
        # Find the next Thursday.
        today = datetime.date.today(days=1)
        oneday = datetime.timedelta(days=1)
        thursday = today
        while thursday.weekday() != calendar.THURSDAY:
            thursday += oneday

        # Pretty print the date and send it over to chanserv    
        date = thursday.strftime("%d-%b-%Y")
        osu_topic = "Ohio State Open Source Club | 7PM " + str(date) + " Ohio Union Senate Chamber | " + topic
        text = "topic " + str(channel) + " " + str(osu_topic)
        m5.write(('PRIVMSG', 'chanserv'), text)
        #m5.write(('TOPIC', channel, text)) only sends the first word of text.
topic.commands = ['topic']
topic.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

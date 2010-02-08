#!/usr/bin/env python
"""
admin.py - Phenny Admin Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

beefed up by Alek Rollyson. added funtions for op, deop, voice, devoice
"""

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
    if not input.admin:
        return
    nick = input.group(2)
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
    if not input.admin:
        return
    nick = input.group(2)
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
    m5 will op the nick who sent the command
    """
    if not input.admin:
        return
    nick = input.group(2)
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
    m5 will op the nick who sent the command
    """
    if not input.admin:
        return
    nick = input.group(2)
    if not nick:
        nick = input.nick
        channel = input.sender
        m5.write(['MODE', channel, "-v", nick])
    else:
        channel = input.sender
        m5.write(['MODE', channel, "-v", nick])
devoice.rule = (['devoice'], r'(\S+)?')
devoice.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

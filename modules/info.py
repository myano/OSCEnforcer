#!/usr/bin/env python
"""
info.py - m5 Information Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def doc(m5, input): 
   """Shows a command's documentation, and possibly an example."""
   name = input.group(1)
   name = name.lower()

   if m5.doc.has_key(name): 
      m5.reply(m5.doc[name][0])
      if m5.doc[name][1]: 
         m5.say('e.g. ' + m5.doc[name][1])
doc.rule = ('$nick', '(?i)(?:help|doc) +([A-Za-z]+)(?:\?+)?$')
doc.example = '$nickname: doc tell?'
doc.priority = 'low'

def commands(m5, input): 
   # This function only works in private message
   #if input.sender.startswith('#'): return
   names = ', '.join(sorted(m5.doc.iterkeys()))
   m5.say("I am sending you a private message of all my commands!")
   m5.msg(input.nick, 'Commands I recognise: ' + names + '.')
   m5.msg(input.nick, ("For help, do '%s: help example?' where example is the " + 
               "name of the command you want help for.") % m5.nick)
commands.commands = ['commands']
commands.priority = 'low'

#def commandsf(m5, input):
#   commands(m5, input)
#commandsf.commands = ['commands']

def help(m5, input): 
   response = (
      'Hi, I\'m a bot. Say ".commands" to me in private for a list ' + 
      'of my commands, or see http://inamidst.com/m5/ for more ' + 
      'general details. My owner is %s.'
   ) % m5.config.owner
   m5.reply(response)
help.rule = ('$nick', r'(?i)help(?:[?!]+)?$')
help.priority = 'low'

def stats(m5, input): 
   """Show information on command usage patterns."""
   commands = {}
   users = {}
   channels = {}

   ignore = set(['f_note', 'startup', 'message', 'noteuri'])
   for (name, user), count in m5.stats.iteritems(): 
      if name in ignore: continue
      if not user: continue

      if not user.startswith('#'): 
         try: users[user] += count
         except KeyError: users[user] = count
      else: 
         try: commands[name] += count
         except KeyError: commands[name] = count

         try: channels[user] += count
         except KeyError: channels[user] = count

   comrank = sorted([(b, a) for (a, b) in commands.iteritems()], reverse=True)
   userank = sorted([(b, a) for (a, b) in users.iteritems()], reverse=True)
   charank = sorted([(b, a) for (a, b) in channels.iteritems()], reverse=True)

   # most heavily used commands
   creply = 'most used commands: '
   for count, command in comrank[:10]: 
      creply += '%s (%s), ' % (command, count)
   m5.say(creply.rstrip(', '))

   # most heavy users
   reply = 'power users: '
   for count, user in userank[:10]: 
      reply += '%s (%s), ' % (user, count)
   m5.say(reply.rstrip(', '))

   # most heavy channels
   chreply = 'power channels: '
   for count, channel in charank[:3]: 
      chreply += '%s (%s), ' % (channel, count)
   m5.say(chreply.rstrip(', '))
stats.commands = ['stats']
stats.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

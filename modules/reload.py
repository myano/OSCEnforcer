#!/usr/bin/env python
"""
reload.py - m5 Module Reloader Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import irc

def f_reload(m5, input): 
   """Reloads a module, for use by admins only.""" 
   if not input.admin: return

   name = input.group(2)
   if name == m5.config.owner: 
      return m5.reply('What?')

   if (not name) or (name == '*'): 
      m5.setup()
      return m5.reply('done')

   try: module = getattr(__import__('modules.' + name), name)
   except ImportError: 
      module = getattr(__import__('opt.' + name), name)
   reload(module)
   if hasattr(module, 'setup'): 
      module.setup(m5)

   if hasattr(module, '__file__'): 
      import os.path, time
      mtime = os.path.getmtime(module.__file__)
      modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))
   else: modified = 'unknown'

   m5.register(vars(module))
   m5.bind_commands()

   m5.reply('%r (version: %s)' % (module, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

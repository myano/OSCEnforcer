#!/usr/bin/env python
"""
startup.py - m5 Startup Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/m5/
"""
def startup(m5, input):
    if hasattr(m5.config, 'serverpass'): 
        m5.write(('PASS', m5.config.serverpass))

    if hasattr(m5.config, 'password'): 
        m5.msg('NickServ', 'IDENTIFY %s' % m5.config.password)
        __import__('time').sleep(5)

    # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
    for channel in m5.channels: 
        m5.write(('JOIN', channel))
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()

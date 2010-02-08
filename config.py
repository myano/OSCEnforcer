nick = 'm5'
host = 'irc.freenode.net'
channels = ['#osc_test', '#m5_test']
owner = 'al3k'

# This isn't implemented yet:
# serverpass = 'yourserverpassword'

# These are people who will be able to use admin.py's functions...
admins = [owner]
# But admin.py is disabled by default, as follows:
exclude = []

# If you want to enumerate a list of modules rather than disabling
# some, use "enable = ['example']", which takes precedent over exclude
# 
# enable = []

# Directories to load opt modules from
extra = []

# Services to load: maps channel names to white or black lists
external = { 
   '#liberal': ['!'], # allow all
   '#conservative': [], # allow none
   '*': ['py', 'whois', 'glyph'] # default whitelist
}

# EOF


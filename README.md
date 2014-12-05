PassTweaker
===========

Tweaks password files to match modern password requirements.

Basically it's turning this:
['password', 'test', 'admin', 'gandalf']

Into this:
['P@ssword', 'P@ssw0rd', 'P@5sword', 'P@55word', 'Passw0rd', 'Pa5sw0rd', 'Pa55w0rd', 'P@5sw0rd', 'P@55w0rd', 'Pa5sword', 'Pa55word', 'Test1234', 'T3st1234', 'Te5t1234', 'Test9876', 'T3st9876', 'Te5t9876', 'Admin123', 'Adm1n123', 'Admin987', 'Adm1n987', 'G@ndalf!', 'G@nd@lf!', 'Gandalf!', 'G@ndalf$', 'G@nd@lf$', 'Gandalf$', 'G@ndalf%', 'G@nd@lf%', 'Gandalf%', 'G@ndalf?', 'G@nd@lf?', 'Gandalf?', 'G@ndalf1', 'G@nd@lf1', 'Gandalf1']


Usage
===========

usage: passtweaker.py [-h] [-f F] [-o O] [--intense] [--debug]

PassTweaker

optional arguments:
  -h, --help  show this help message and exit
  -f F        File to transform
  -o O        Output file
  --intense   Try even to improve words that already match the requirements
  --debug     Debug output


Screenshot
============
![Alt text](/screens/ishot-141205-195328.png?raw=true "Screenshot")

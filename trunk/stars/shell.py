#pylint:
"""This module will enable running STARS embedded in an iPython session. iPython
includes gui event loop support, now with %gui magic command, whereas before it
was enabled with command line options. See
http://ipython.scipy.org/doc/manual/html/interactive/reference.html
#gui-event-loop-support-support
What we want: command history, log and restore or replay STARS projects,
interactive object introspection during live sessions for both users and
developers. Since we get what we want for free by using iPython, our primary
need is to invoke STARS in the iPython environment, with the proper flags.
For apps that may be started in iPython or as standalone apps, 
it is recommended to start Python in such a way that our program detects how it
is started. For that, iPython has a special func.

try:
    from IPython import appstart_tk
    appstart_tk(app)
except ImportError:
    app.MainLoop()

Note this may not be available until iPython 0.11. 


""Quick code snippets for embedding IPython into other programs.

See example-embed.py for full details, this file has the bare minimum code for
cut and paste use once you understand how to use the system."""

#---------------------------------------------------------------------------
# This code loads IPython but modifies a few things if it detects it's running
# embedded in another IPython session (helps avoid confusion)

try:
    __IPYTHON__
except NameError:
    argv = ['']
    banner = exit_msg = ''
else:
    # Command-line options for IPython (a list like sys.argv)
    argv = ['-pi1','In <\\#>:','-pi2','   .\\D.:','-po','Out<\\#>:']
    banner = '*** Nested interpreter ***'
    exit_msg = '*** Back in main IPython ***'

# First import the embeddable shell class
from IPython.Shell import IPShellEmbed
# Now create the IPython shell instance. Put ipshell() anywhere in your code
# where you want it to open.
ipshell = IPShellEmbed(argv,banner=banner,exit_msg=exit_msg)

#---------------------------------------------------------------------------
# This code will load an embeddable IPython shell always with no changes for
# nested embededings.
'''
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()
# Now ipshell() will open IPython anywhere in the code.
'''

#---------------------------------------------------------------------------
# This code loads an embeddable shell only if NOT running inside
# IPython. Inside IPython, the embeddable shell variable ipshell is just a
# dummy function.

'''
try:
    __IPYTHON__
except NameError:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    # Now ipshell() will open IPython anywhere in the code
else:
    # Define a dummy ipshell() so the same code doesn't crash inside an
    # interactive IPython
    def ipshell(): pass

'''
#******************* End of file <example-embed-short.py> ********************

#logging and restoring
#we can prompt users at startup for a saved log file or to start a new project.
#Log files can be reloaded with the -logplay option, however imperfectly. Users
#also get a readable record of their sessions. We can also stop and start
#logging at any point.

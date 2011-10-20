Steps for Checking out and Committing:

1) Checkout

svn checkout https://starspy.googlecode.com/svn/branches/gph4598f11/spacetime spacetime --username ____@gmail.com

This will download all of the files in the spacetime directory into a new directory called spacetime in whatever your cd is.

2) Check Differences

svn stat

3) Uploading Files from your personal directory (on your computer, duh)

svn add __files you want to upload__

4) Committing Files

OH CRAP YOU NEED TO SET UP YOUR EXTERNAL EDITOR!!

	4B) Setting up external editor on mac to be vim
	Commands:  vim ~/.bash_profile
		   export SVN_EDITOR="/usr/bin/vim"
		   :wq (that's how you save and quit)

5) REALLY committing your files

After creating/updating your bash_profile, quit and reopen terminal (I think it's necessary).

svn commit __files you want to upload__

You will then be prompted to reenter your username (maybe) and password. To get your password, go to:
http://code.google.com/p/starspy/source/checkout
Click on the link for: googlecode.com password.

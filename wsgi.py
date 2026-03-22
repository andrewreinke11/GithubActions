# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below assumes you're using Flask. If you are using a different web
# framework, feel free to comment out or remove the below and replace it
# with the appropriate configuration.

from app import app as application

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# (you can delete this when you know everything works)
#
# Getting imports working in PythonAnywhere is a bit different to your local
# machine. Use the "Files" tab to upload a file, then open a console and type
# something like:
#
#     cd /home/<your-username>/
#     python3 -c "import sys; sys.path.insert(0, '/home/<your-username>/'); import your_app"
#
# This will tell you if there are any import issues. If you're using a virtualenv,
# remember to activate it first:
#
#     workon <your-virtualenv-name>
#     python3 -c "import sys; sys.path.insert(0, '/home/<your-username>/'); import your_app"
#
# This means that you can test your app locally on PythonAnywhere before trying
# to run it from the web interface.
#
# Debugging your app:
#
# If you get a 500 error, add the following lines to the top of your Flask app:
#
#     import logging
#     logging.basicConfig(level=logging.DEBUG)
#
# This will show you any errors in the "Error log" tab of the "Web" page.
#
# If you get a 404 error, make sure you've set the right working directory in the
# "Web" tab, and that your app is listening on the right host and port. The
# default for Flask is 127.0.0.1:8000.
#
# If you get an ImportError, check that your virtualenv is activated and that
# you've installed all the packages you need.
#
# If you get a "wrong app" error, make sure your application variable is set
# correctly in this file.
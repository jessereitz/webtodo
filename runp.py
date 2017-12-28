####################################
#####     run.py - WEBTODO     #####
####################################
#
# runs WebTodo application
#
####################################

from app import app
print("\n\n")
print("Starting app in production mode...")
app.run(debug=False)

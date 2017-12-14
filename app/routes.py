#######################################
#####     routes.py - WEBTODO     #####
#######################################


from app import app

@app.route('/')
def home():
    return "success"

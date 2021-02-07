#from config import Config
from app import server, mongo
from werkzeug.serving import run_simple
#from app import app_dash




# Globally accessible libraries


if __name__ == "__main__":
    #app.run(port=5000, debug=True, host="127.0.0.1")
    run_simple('0.0.0.0', 5000, server, use_reloader=True, use_debugger=True)

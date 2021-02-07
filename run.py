from app import server,mongo,dashapp



if __name__ == "__main__":
    server.run(port=5000, debug=True, host="127.0.0.1")

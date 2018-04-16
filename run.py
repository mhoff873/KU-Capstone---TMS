from views import *
"""
PORTS
Team A: 5000, 5001
Team B: 5002, 5003
Team DB: 5004, 5005
Team QA: 5006
Team PM: 5007
"""


if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5006, host="0.0.0.0")

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
    app.run(debug=True, port=5000, host="0.0.0.0")
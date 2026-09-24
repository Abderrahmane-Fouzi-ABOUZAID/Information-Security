
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/article")
def article():
    return render_template("index.html", page="article")
if __name__ == "__main__":
    app.run(host="publisher-two.test", port=8001, debug=True)

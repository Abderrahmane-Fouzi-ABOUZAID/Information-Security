from datetime import datetime, timezone
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
visits = []

@app.route("/collect")
def collect():
    visit = {
        "time": datetime.now(timezone.utc).isoformat(),
        "publisher": request.args.get("publisher", ""),
        "id": request.args.get("id", ""),
        "page": request.args.get("page", "")
    }
    visits.append(visit)
    print(visit, flush=True)
    return "", 204

@app.route("/profiles")
def profiles():
    result = {}
    for visit in visits:
        key = (visit["publisher"], visit["id"])
        result.setdefault(key, []).append((visit["time"], visit["page"]))
    return "\n\n".join(
        f"{publisher} / {aid}\n" + "\n".join(f"{time} {page}" for time, page in pages)
        for (publisher, aid), pages in result.items()
    ), 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.route("/")
def home():
    history = profiles()[0] or "No visits yet. Open a publisher page first."
    return f"<h1>Analytics profiles</h1><pre>{escape(history)}</pre>"

if __name__ == "__main__":
    app.run(host="analytics.test", port=8004, debug=True)

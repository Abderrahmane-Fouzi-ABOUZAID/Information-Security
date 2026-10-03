from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


# Task 0: HTTP headers are passive clues because the server receives them before JavaScript runs. User-Agent can reveal a browser and OS, Accept lists supported content types, Accept-Language lists language preferences, Accept-Encoding lists compression formats, Referer can reveal the previous page, and Sec-Fetch-* describes the request's context. These are clues about a browser, not proof of a person's identity. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers and https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Content_negotiation.
# Task 1: The added headers are Accept, Accept-Encoding, Sec-CH-UA, Sec-CH-UA-Platform, Sec-Fetch-Mode, and Sec-Fetch-Site. Accept and Accept-Encoding describe format support; Sec-CH-UA and Sec-CH-UA-Platform describe browser brands and platform; Sec-Fetch-Mode and Sec-Fetch-Site describe navigation context. A missing header means the browser did not send it. On the supplied Brave and Edge captures, Accept-Language and Sec-CH-UA differ, while the loopback IP, Accept-Encoding, platform hint, and top-level navigation mode match. Values can change with browser version, settings, request type, and privacy tools. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Client_hints.
HEADERS = (
    "User-Agent",
    "Accept",
    "Accept-Language",
    "Accept-Encoding",
    "Sec-CH-UA",
    "Sec-CH-UA-Platform",
    "Sec-Fetch-Mode",
    "Sec-Fetch-Site",
)


@app.route("/")
def home():
    passive = {"IP address": request.remote_addr, "HTTP method": request.method}
    passive.update({name: request.headers.get(name, "Not sent") for name in HEADERS})
    print("\nPASSIVE HTTP FEATURES")
    for name, value in passive.items():
        print(f"{name}: {value}")
    return render_template("index.html", passive=passive)


@app.route("/typing")
def typing():
    return render_template("typing.html")


@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True) or {}
    print("\nACTIVE FEATURES" if data.get("kind") == "active" else "\nTYPING FEATURES")
    for name, value in data.items():
        print(f"{name}: {value}")
    return jsonify(status="received")


@app.route("/fingerprint", methods=["POST"])
def fingerprint():
    data = request.get_json(silent=True) or {}
    print("\nSHA-256 FINGERPRINT:", data.get("hash"))
    return jsonify(status="received")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)

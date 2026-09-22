from flask import Flask, render_template, make_response, request
import secrets


app = Flask(__name__)

@app.route("/")
def home():
    aid = request.cookies.get("aid")
    is_new = aid is None
    # Generate an identifier only for a new browser
    if is_new:
        aid = secrets.token_hex(8)
        # Create the normal HTTP response containing index.html

    publisher = request.args.get("publisher")

    print("publisher:", publisher)
    response = make_response(render_template("tracker.html"))
    print(response)
    print(request)
    # Ask the browser to store the identifier
    if is_new:
        response.set_cookie(
        key="aid",
        value=aid
        )
    return response




if __name__ == "__main__":
    app.run(host="tracker.test", port=8002, debug=True)



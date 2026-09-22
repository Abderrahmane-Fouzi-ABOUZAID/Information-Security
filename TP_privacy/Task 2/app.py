from flask import Flask, render_template, request, make_response 

import secrets
app = Flask(__name__)
@app.route("/")
def home():
# Check whether the browser already has an identifier
    aid = request.cookies.get("aid")
    is_new = aid is None
    # Generate an identifier only for a new browser
    if is_new:
        aid = secrets.token_hex(8)
    # Create the normal HTTP response containing index.html
    response = make_response(render_template("index.html"))
    # Ask the browser to store the identifier
    if is_new:
        response.set_cookie(
        key="aid",
        value=aid
        )
    return response
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

#when we run the code and open the website we will see a value for the id of the cookie 
# for my case i found : 28f5f9ae9765b358
# after refreshing the page the cookie remains the same and we will see the same value
# but if we close the browser and re open it we will see that the value of the id of the 
# cookie changed so we can say that the cookie is only for the current session 

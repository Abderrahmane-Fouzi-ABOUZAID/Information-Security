from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print("\n========== NEW VISIT ==========")
    print("IP address :", request.remote_addr)
    print("HTTP method :", request.method)
    print("User-Agent :", request.headers.get("User-Agent"))
    print("Accept-Language :", request.headers.get("Accept-Language"))

    #Added 4 four fields
    print("\nAdditional 4 fields from the HTML header\n")

    print("Accept-Encoding :", request.headers.get("Accept-Encoding"))
    print("SECurity Clients Hints User Agent (sec-ch-ua) :", request.headers.get("sec-ch-ua"))
    print("Security Client Hints User Agent Platform :", request.headers.get("sec-ch-ua-platform"))
    print("Security Fetch Mode :", request.headers.get("sec-fetch-mode"))


    print("================================\n")
    return render_template("index.html")

@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json()
    print("\n========== BROWSER IDENTIFICATION DATA (POST) ==========")
    if data:
        print(f"User-Agent             : {data.get('user_agent')}")
        print(f"Brave Object Detected  : {data.get('is_brave')}")
        print(f"Global Privacy Control : {data.get('privacy_control')}")
        print(f"Modern Brands          : {data.get('modern_brands')}")
    else:
        print("No data received.")
    print("========================================================\n")
    return jsonify({"status": "success", "message": "Features printed to console successfully!"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)



'''


So i tested this code with two browsers : Brave and Edge

for the differences :
 - Accept-Language changes since i configured my edge to be in french and my brave to be in english
 - Security Client Hints User Agent changes
 for brave :  "Chromium";v="154", "Brave";v="154"
 for edge : "Chromium";v="154", "Microsoft Edge";v="154"

 for the other fileds they are stable, IP address, Accept encoding, Plateform, fetch mode (depends on the request not the browser ), 




'''

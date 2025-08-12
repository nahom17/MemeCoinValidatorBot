from flask import Flask
from webhook.helius_webhook import helius_webhook

app = Flask(__name__)
app.register_blueprint(helius_webhook)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
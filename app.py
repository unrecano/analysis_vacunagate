from flask import Flask, render_template
import services

app = Flask(__name__)

@app.route("/")
def index():
    context = {
        "hashtags": services.get_all_hashtags(),
        "mentions": services.get_all_mentions(),
        "words": services.get_all_words(),
        "locations": services.get_all_locations(),
        "count": services.get_info()
    }
    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(debug=True)
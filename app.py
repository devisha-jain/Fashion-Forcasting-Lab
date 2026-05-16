from flask import Flask, render_template, request
from trend_engine import generate_forecast

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    forecasts = []

    if request.method == "POST":

        region = request.form["region"]
        year = request.form["year"]
        signals = request.form.getlist("signals")

        forecasts = generate_forecast(region, year, signals)

    return render_template("index.html", forecasts=forecasts)

if __name__ == "__main__":
    app.run(debug=True)
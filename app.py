import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import random

app = Flask(__name__)

# ================= CLASS =================
class HealthRiskSystem:

    def __init__(self):
        self.file = "patients.csv"

    # -------- HEALTH SCORE --------
    def calculate_health_score(self, hr=None, bp=None, sugar=None, temp=None, oxygen=None, chol=None):

        score = 100
        count = 0

        # Heart Rate
        if hr:
            count += 1
            if hr > 120:
                score -= 15
            elif hr > 100:
                score -= 8

        # Blood Pressure
        if bp:
            count += 1
            if bp > 140:
                score -= 15
            elif bp > 120:
                score -= 8

        # Sugar
        if sugar:
            count += 1
            if sugar > 180:
                score -= 15
            elif sugar > 140:
                score -= 8

        # Temperature
        if temp:
            count += 1
            if temp > 39:
                score -= 15
            elif temp > 38:
                score -= 8

        # Oxygen
        if oxygen:
            count += 1
            if oxygen < 90:
                score -= 20
            elif oxygen < 95:
                score -= 10

        # Cholesterol
        if chol:
            count += 1
            if chol > 240:
                score -= 15
            elif chol > 200:
                score -= 8

        # No input case
        if count == 0:
            return 0

        return max(score, 0)

    # -------- RISK --------
    def get_risk(self, score):
        if score < 50:
            return "High Risk"
        elif score < 75:
            return "Medium Risk"
        else:
            return "Low Risk"

    # -------- ALERT --------
    def get_alert(self, score):
        if score < 50:
            return "🚨 High Risk! Immediate medical attention needed."
        elif score < 75:
            return "⚠️ Moderate Risk. Monitor regularly."
        else:
            return "✅ Healthy condition."

system = HealthRiskSystem()

# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= PREDICT =================
@app.route("/predict", methods=["POST"])
def predict():

    name = request.form["name"]

    # Get inputs
    hr = request.form.get("heart_rate")
    bp = request.form.get("bp")
    sugar = request.form.get("sugar")
    temp = request.form.get("temperature")
    oxygen = request.form.get("oxygen")
    chol = request.form.get("cholesterol")

    # Convert safely
    hr = int(hr) if hr else None
    bp = int(bp) if bp else None
    sugar = int(sugar) if sugar else None
    temp = float(temp) if temp else None
    oxygen = int(oxygen) if oxygen else None
    chol = int(chol) if chol else None

    # Calculate
    score = system.calculate_health_score(hr, bp, sugar, temp, oxygen, chol)
    risk = system.get_risk(score)
    message = system.get_alert(score)

    # Save
    with open("patients.csv", "a") as f:
        f.write(f"{name},{hr},{bp},{sugar},{temp},{oxygen},{chol},{score},{risk}\n")

    return render_template("result.html",
                           name=name,
                           score=score,
                           risk=risk,
                           message=message)

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    try:
        data = pd.read_csv("patients.csv",
            names=["Name","HR","BP","Sugar","Temp","Oxygen","Chol","Score","Risk"])
    except:
        data = pd.DataFrame()

    # Convert score
    if not data.empty:
        data["Score"] = pd.to_numeric(data["Score"], errors='coerce')

    # type conversion for numeric fields
    if not data.empty:
        data["Score"] = pd.to_numeric(data["Score"], errors='coerce')
        data["HR"] = pd.to_numeric(data["HR"], errors='coerce')
        data["Temp"] = pd.to_numeric(data["Temp"], errors='coerce')
        data["Oxygen"] = pd.to_numeric(data["Oxygen"], errors='coerce')

    avg_score = int(data["Score"].mean()) if not data.empty and not pd.isna(data["Score"].mean()) else 0
    avg_hr = int(data["HR"].mean()) if not data.empty and not pd.isna(data["HR"].mean()) else 0
    max_temp = float(data["Temp"].max()) if not data.empty and not pd.isna(data["Temp"].max()) else 0
    min_oxygen = float(data["Oxygen"].min()) if not data.empty and not pd.isna(data["Oxygen"].min()) else 0
    high_risk_count = int(data[data["Risk"] == "High Risk"].shape[0]) if not data.empty else 0

    # Chart
    if not data.empty:
        data["Score"].plot(kind="line", figsize=(8, 4), color="#60a5fa")
        plt.title("Health Score Trend")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("static/score_chart.png")
        plt.clf()

        # Risk Category Pie Chart
        risk_counts = data["Risk"].value_counts()
        if not risk_counts.empty:
            colors = ['#ef4444', '#f59e0b', '#10b981']  # Red, Orange, Green
            risk_counts.plot(kind="pie", autopct='%1.1f%%', colors=colors, figsize=(6, 6))
            plt.title("Risk Category Distribution")
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig("static/risk_pie_chart.png")
            plt.clf()

    table = data.to_html(index=False, classes='data-table', border=0) if not data.empty else "No Data"

    return render_template("dashboard.html",
                           table=table,
                           avg_score=avg_score,
                           avg_hr=avg_hr,
                           max_temp=max_temp,
                           min_oxygen=min_oxygen,
                           high_risk_count=high_risk_count)

# ================= SEARCH =================
@app.route("/search", methods=["GET","POST"])
def search():

    result = ""

    if request.method == "POST":
        name = request.form["name"]

        data = pd.read_csv("patients.csv",
            names=["Name","HR","BP","Sugar","Temp","Oxygen","Chol","Score","Risk"])

        res = data[data["Name"].str.lower() == name.lower()]
        result = res.to_html(index=False) if not res.empty else "No record found"

    return render_template("search.html", result=result)

# ================= DELETE =================
@app.route("/delete", methods=["GET","POST"])
def delete():

    message = ""

    if request.method == "POST":
        name = request.form["name"]

        data = pd.read_csv("patients.csv",
            names=["Name","HR","BP","Sugar","Temp","Oxygen","Chol","Score","Risk"])

        data = data[data["Name"].str.lower() != name.lower()]
        data.to_csv("patients.csv", index=False, header=False)

        message = "Patient deleted successfully"

    return render_template("delete.html", message=message)

# ================= LIVE =================
@app.route("/live")
def live():

    hr = random.randint(70, 140)
    bp = random.randint(100, 160)
    sugar = random.randint(90, 200)
    temp = round(random.uniform(36.5, 40.0), 1)
    oxygen = random.randint(85, 100)
    chol = random.randint(150, 260)

    score = system.calculate_health_score(hr, bp, sugar, temp, oxygen, chol)
    risk = system.get_risk(score)

    return render_template("live.html",
                           hr=hr,
                           bp=bp,
                           sugar=sugar,
                           temp=temp,
                           oxygen=oxygen,
                           chol=chol,
                           score=score,
                           risk=risk)

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
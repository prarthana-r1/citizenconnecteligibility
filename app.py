from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# 🔹 MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://prarthanainfoin:VjvGw9KyhFzWUeMl@cluster1.obekyj0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client = MongoClient(MONGO_URI)

# 🔹 Select database and collection
db = client.karnataka_schemes_db
schemes_collection = db.schemes

@app.route("/", methods=["GET", "POST"])
def index():
    schemes = []
    categories = schemes_collection.distinct("category")  # Get unique categories
    
    user_data = {
        "name": "",
        "age": "",
        "gender": "",
        "caste": "",
        "category": "All"
    }

    if request.method == "POST":
        # 🔹 Collect user input
        user_data["name"] = request.form.get("name", "").strip()
        user_data["age"] = request.form.get("age", "").strip()
        user_data["gender"] = request.form.get("gender", "").strip()
        user_data["caste"] = request.form.get("caste", "").strip()
        user_data["category"] = request.form.get("category", "All").strip()

        # 🔹 Query MongoDB for schemes based on selected category
        query = {} if user_data["category"] == "All" else {"category": user_data["category"]}
        schemes = list(schemes_collection.find(query, {"_id": 0, "scheme_name": 1, "category": 1, "benefits": 1, "apply_link": 1}))

        # 🔹 Debugging output
        print("User Data:", user_data)
        print("Fetched Schemes:", schemes)

    return render_template("index.html", user_data=user_data, schemes=schemes, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)

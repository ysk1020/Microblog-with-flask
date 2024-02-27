import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

#load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://ggo353410:dSb7DDDj6Di1tORi@microblock.bcl4cfr.mongodb.net/")  #os.getenv('MONGODB_URL')
    app.db = client.Microblog


    @app.route('/',methods=['GET', 'POST'])
    def home():
        if request.method == "POST": #request has to be associated with browser page to get data
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            #entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content":entry_content, "date":formatted_date})
        entries_with_date = [
            (
                entry["content"], 
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d") 
            )
            for entry in app.db.entries.find({})
        ]    
        return render_template("index.html", entries=entries_with_date)
    
    return app
import datetime
from bson import ObjectId
from flask import Flask, render_template, request
import os 
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

template_dir = os.path.abspath('templates_fs')

def create_app():
    app = Flask(__name__, template_folder=template_dir)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        empty = False
        if request.method == "POST":
            delete_content = request.values.get("delete")
            print(delete_content)
            if delete_content != None :
                app.db.entries.delete_one({"_id": ObjectId(delete_content)})
            else:
                entry_content = request.form.get("content")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                if entry_content != '' :
                    app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
                else:
                    empty = True
                    
        entries_with_date = [(
            entry["_id"],
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries=entries_with_date, empty=empty)
    
    return app

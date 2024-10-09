from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")

mongo = PyMongo(app)

# Home Page for User to Generate Baggage Pass
@app.route('/')
def index():
    return render_template('index.html')

# Generate Baggage Pass by Scanning or Manual Input
@app.route('/generate-pass', methods=['GET', 'POST'])
def generate_pass():
    if request.method == 'POST':
        boarding_pass = request.form['boarding_pass']
        baggage_count = request.form['baggage_count']
        baggage_status = "Checked In"
        
        # Insert into MongoDB
        baggage_pass = {
            "boarding_pass": boarding_pass,
            "baggage_count": baggage_count,
            "baggage_status": baggage_status
        }
        mongo.db.baggagepass.insert_one(baggage_pass)
        flash('Baggage pass generated successfully!')
        return redirect(url_for('index'))

    return render_template('generate_pass.html')

# Lookup Baggage Status by Boarding Pass
@app.route('/baggage-status', methods=['GET', 'POST'])
def baggage_status():
    if request.method == 'POST':
        try:
            boarding_pass = request.form['boarding_pass']
        except:
            boarding_pass = ""
        if boarding_pass == "": boarding_pass = f"{request.form['pnrInput']}, {request.form['flightNumberInput']}"
        
        print(boarding_pass)

        baggage = mongo.db.baggagepass.find_one({"boarding_pass": boarding_pass})
        
        if baggage:
            return render_template('baggage_status.html', baggage=baggage)
        else:
            flash('No baggage found for this boarding pass')
            return redirect(url_for('baggage_status'))

    return render_template('baggage_status.html', baggage=None)

# Admin Console to View All Boarding and Baggage Passes
@app.route('/admin')
def admin():
    all_boarding_passes = mongo.db.baggagepass.find()
    return render_template('admin.html', passes=all_boarding_passes)

# Edit Baggage Pass
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_pass(id):
    pass_to_edit = mongo.db.baggagepass.find_one({"_id": ObjectId(id)})

    if request.method == 'POST':
        boarding_pass = request.form['boarding_pass']
        baggage_count = request.form['baggage_count']
        baggage_status = request.form['baggage_status']

        # Update in MongoDB
        mongo.db.baggagepass.update_one({"_id": ObjectId(id)}, {
            "$set": {
                "boarding_pass": boarding_pass,
                "baggage_count": baggage_count,
                "baggage_status": baggage_status
            }
        })
        flash('Baggage pass updated successfully!')
        return redirect(url_for('admin'))

    return render_template('edit_pass.html', pass_to_edit=pass_to_edit)

# Delete Baggage Pass
@app.route('/delete/<id>', methods=['POST'])
def delete_pass(id):
    mongo.db.baggagepass.delete_one({"_id": ObjectId(id)})
    flash('Baggage pass deleted successfully!')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

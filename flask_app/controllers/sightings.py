
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app import app


@app.route("/addSighting")
def addSighting():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    return render_template("createSighting.html")

@app.route('/createSighting', methods=["POST"])
def createSighting():
#     # First we make a data dictionary from our request.form coming from our template.
#     # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "location": request.form["location"],
        "description" : request.form["description"],
        "date_made" : request.form["date_made"],
        "num_sasquatch" : request.form["num_sasquatch"],
        "user_id" : session["user_id"]
    }
    # We pass the data dictionary into the save method from the User class.
    sighting_id = Sighting.save(data)
    session['sighting_id'] = sighting_id
    return redirect('/success/')

@app.route('/showSighting/<int:sighting_id>/show')
def showSighting(sighting_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": sighting_id
    }
    return render_template("showSighting.html", one_sighting=Sighting.get_one_sighting_with_creator(data))
    # return render_template("showSighting.html", one_sighting=Sighting.get_one(data))

@app.route('/editSighting/<int:sighting_id>/edit')
def editRecipe(sighting_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": sighting_id
    }
    return render_template("editSighting.html", one_sighting=Sighting.get_one(data))

@app.route('/updateSighting/<int:sighting_id>/update', methods=["POST"])
def updateSighting(sighting_id):
    data = {
        "id": sighting_id,
        "location": request.form["location"],
        "description" : request.form["description"],
        "date_made" : request.form["date_made"],
        "num_sasquatch" : request.form["num_sasquatch"],
        "creator" : session["user_id"]
    }
    Sighting.update(data)
    return redirect('/success/')

@app.route('/deleteSighting/<int:sighting_id>/delete')
def deleteSighting(sighting_id):
    data = {
        "id": sighting_id
    }
    Sighting.delete(data)
    return redirect("/success/")



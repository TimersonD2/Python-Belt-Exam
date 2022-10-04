
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

# model the class after the table from the database
class Sighting:
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date_made = data['date_made']
        self.num_sasquatch = data['num_sasquatch']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    # Class methods for querying database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('sasquatch_schema').query_db(query)
        # Create an empty list to append our instances of sightings
        sightings = []
        # Iterate over the db results and create instances of sightings with cls.
        for sighting in results:
            sightings.append( cls(sighting) )
        return sightings

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings where id=%(id)s;"
        results = connectToMySQL('sasquatch_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location, description, date_made, num_sasquatch, created_at, updated_at, user_id) VALUES (%(location)s, %(description)s, %(date_made)s, %(num_sasquatch)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('sasquatch_schema').query_db( query, data )   

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, description=%(description)s, date_made=%(date_made)s, num_sasquatch=%(num_sasquatch)s WHERE id=%(id)s;"
        return connectToMySQL('sasquatch_schema').query_db( query, data )   

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM sightings WHERE id=%(id)s"
        return connectToMySQL('sasquatch_schema').query_db( query, data )   


    @classmethod
    def get_all_sightings_with_creator(cls):
        # Get all sightings, and their one associated User that created it
        query = "SELECT * FROM sightings JOIN users ON sightings.user_id = users.id;"
        results = connectToMySQL('sasquatch_schema').query_db(query)
        all_sightings = []
        for row in results:
            # Create a Sighting class instance from the information from each db row
            one_sighting = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_sighting_author_info = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = user.User(one_sighting_author_info)
            # Associate the Sighting class instance with the User class instance by filling in the empty creator attribute
            one_sighting.creator = author
            # Append the Sighting containing the associated User to the list
            all_sightings.append(one_sighting)
        return all_sightings

    @classmethod
    def get_one_sighting_with_creator(cls, data):
        query = "SELECT * FROM sightings JOIN users ON sightings.user_id = users.id WHERE sightings.id=%(id)s;"
        results = connectToMySQL('sasquatch_schema').query_db(query, data)
        if len(results) < 1:
            return False

        for row in results:
            one_sighting = cls(row)
            one_sighting_author_info = {
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            author = user.User(one_sighting_author_info)
            one_sighting.creator = author
        return one_sighting


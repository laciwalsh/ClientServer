from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    
    """ CRUD operations for animal collection in MongoDB """
    def __init__(self):
        # initializing MongoClient to access mongodb databases and collections
        # hard-wired to aac database, animals collection, and aac user
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 30596
        DB = 'AAC'
        COL = 'animals'
        
        #
        # initialize connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' %(COL)]
        
     # method to implement C (create) in CRUD -> true if successful
    def create(self, data):
        # initialize to false
        what_to_return = False
        if data is not None:
            self.database.animals.insert_one(data) # data should be dictionary
            # find newly added data
            result = list(self.database.animals.find({'animal_id': '112358'}))
            # check if search successful
            if result:
                what_to_return = True
            else:
                what_to_return = False
        else:
            raise Exception("Nothing to save because data parameter is empty")
        return result
            
    # method to implemtn R (read) in CRUD
    def read(self, query = None):
        if query is None:
            result = list(self.database.animals.find({}))
        else:
            result = list(self.database.animals.find(query))
        return result
    
    # method to implement U (update) in CRUD
    def update(self, key, value, key_to_update, updated_value, only_one):
        # if only_one set to true -> update only one
        if only_one == True:
            result = self.database.animals.update_one({key : value}, {"$set" : {key_to_update : updated_value}})
        # if only_one set to false -> update all
        else:
            result = self.database.animals.update_many({key : value}, {"$set" : {key_to_update : updated_value}})
           # get count of number of docs modified
        num_modified = result.modified_count
           # return the number modified
        return num_modified
        
    # method to implement D (delete) in CRUD
    def delete(self, key, value, delete_one):
        # if delete_one set to true -> delete one
        if delete_one:
            result = self.database.animals.delete_one({key : value})
         # if delete_one set to false -> delete all
        else:
            result = self.database.animals.delete_many({key : value})
        return result.deleted_count
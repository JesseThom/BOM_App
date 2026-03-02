from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Option:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.option_desc = data['option_desc']
        self.model_number = data.get('model_number', None)
        self.qty = data.get('qty', None)
        self.man = data.get('man', None)
        self.a_i = data['a_i']
    
#C
    # @classmethod
    # def create(cls,data):
    #     #1 query statement
    #     query = "INSERT INTO options (option_desc, a_i) VALUES (%(option_desc)s,%(a_i)s);"
    #     #2 contact the data
    #     option_id = connectToMySQL(DATABASE).query_db(query, data) 
    #     return option_id
    
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM options WHERE id = %(id)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        
        if not results:
            return False
        
        return cls(results[0])
    
    # @classmethod
    # def get_one_by_name(cls, data):
    #     query = "SELECT * FROM options WHERE name = %(name)s;"
    #     #returns list of dictionaries
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     # print(results)
        
    #     if not results:
    #         return False
        
    #     return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM options;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_options = []
        for dict in results:
            all_options.append(cls(dict))
        return all_options
    
#U
    # @classmethod
    # def update_one(cls,data):
    #     query = "UPDATE options SET first_name = %(name)s, WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_db(query,data)
    
#D
    # @classmethod
    # def delete_one(cls,data):
    #     query = "DELETE FROM options WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_db(query,data)
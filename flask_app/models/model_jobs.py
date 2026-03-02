from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Job:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.job_number = data['job_number']
        self.customer = data['customer']
    
    @staticmethod
    def job_check(data):
        is_valid = True

        temp_job = Job.get_one_by_job(data)
        if temp_job:
            flash("Job Already Exist","err_job")
            is_valid=False

        return is_valid
#C
    @classmethod
    def create(cls,data):
        #1 query statement
        query = "INSERT INTO jobs (job_number, customer) VALUES (%(job_number)s,%(customer)s);"
        #2 contact the data
        job_id = connectToMySQL(DATABASE).query_db(query, data) 
        return job_id
    
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM jobs WHERE id = %(id)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        
        if not results:
            return False
        
        return cls(results[0])
    
    @classmethod
    def get_one_by_job(cls, data):
        query = "SELECT * FROM jobs WHERE job_number = %(job_number)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        
        if not results:
            return False
        
        return cls(results[0])
    # @classmethod
    # def get_one_by_name(cls, data):
    #     query = "SELECT * FROM jobs WHERE name = %(name)s;"
    #     #returns list of dictionaries
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     # print(results)
        
    #     if not results:
    #         return False
        
    #     return cls(results[0])

    @classmethod
    def get_all(cls):
        
        query = "SELECT * FROM jobs;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_jobs = []
        for dict in results:
            all_jobs.append(cls(dict))
        return all_jobs
        
#U
    # @classmethod
    # def update_one(cls,data):
    #     query = "UPDATE jobs SET first_name = %(name)s, WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_db(query,data)
    
#D
    # @classmethod
    # def delete_one(cls,data):
    #     query = "DELETE FROM jobs WHERE id = %(id)s;"
    #     return connectToMySQL(DATABASE).query_db(query,data)

    
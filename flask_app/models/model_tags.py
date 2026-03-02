from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Tag:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.handle = data['handle']
        self.blockname = data['blockname']
        self.type = data['type']
        self.tag_number = data['tag_number']
        self.process_desc = data['process_desc']
        self.option_id = data['option_id']
        self.job_id = data['job_id']
        self.notes = data['notes']
        self.control_panel = data['control_panel']
        self.electrical = data['electrical']
        self.updated_at = data['updated_at']
        self.active = data['active']

        # options 
        self.option_desc = data.get('option_desc',None)
        self.model_number = data.get('model_number',None)
        self.qty = data.get('qty',None)
        self.man = data.get('man',None)
        self.a_i = data.get('a_i',None)
        self.a_o = data.get('a_o',None)
        self.d_i = data.get('d_i',None)
        self.d_o = data.get('d_o',None)

        # por
        self.order_status = data.get('order_status', None)
        self.por_number = data.get('por_number', None)
    
#handle duplicate check
    @staticmethod
    def validate(data):
        is_valid = True

        temp_user = Tag.get_one_by_handle({'handle':data['handle']})
        if temp_user:
            flash("Handle Already Exist","err_handle")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        #1 query statement
        query = "INSERT INTO tags (handle, blockname, job_id, type, tag_number, process_desc, option_id) VALUES (%(handle)s,%(blockname)s,%(job_id)s,%(type)s,%(tag_number)s,%(process_desc)s,%(option_id)s);"
        #2 contact the data
        tag_id = connectToMySQL(DATABASE).query_db(query, data) 
        return tag_id
    
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tags JOIN options ON option_id = options.id WHERE tags.id = %(id)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False
        
        return cls(results[0])
    
    @classmethod
    def get_one_by_handle(cls, data):
        query = "SELECT * FROM tags WHERE handle = %(handle)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False
        
        return cls(results[0])

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM tags JOIN options ON tags.option_id = options.id WHERE job_id = %(job_id)s ORDER BY type,tag_number;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        all_tags = []
        for dict in results:
            all_tags.append(cls(dict))
        return all_tags
    
    @classmethod
    def get_all_main(cls,data):
        query = "SELECT * FROM tags JOIN options ON tags.option_id = options.id LEFT JOIN por_devices ON tags.id = por_devices.tag_id WHERE job_id = %(job_id)s ORDER BY type,tag_number;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        all_tags = []
        for dict in results:
            all_tags.append(cls(dict))
        return all_tags
    
    @classmethod
    def get_everything(cls,data):
        query = "SELECT * FROM tags JOIN options ON option_id = options.id JOIN devices_in_optons ON devices_in_optons.option_id = options.id LEFT JOIN devices ON devices.id = device_id LEFT JOIN por_devices ON tags.id = por_devices.tag_id WHERE job_id = %(job_id)s ORDER BY tags.type, tags.tag_number;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        all_tags = []
        for dict in results:
            all_tags.append(cls(dict))
        return all_tags
    
    @classmethod
    def export_test(cls, data):

        query = """
        SELECT *
        FROM tags
        JOIN options ON tags.option_id = options.id
        WHERE job_id = %(job_id)s
        """
        filters = []

        for col in data["selected_ios"]:
                filters.append(f'COALESCE({col},0) > 0')

        if data.get("control_panel"):
            query += " AND control_panel = %(control_panel)s"
            query += " AND (" + " OR ".join(filters) + ")"

            query += " ORDER BY type, tag_number;"

        return connectToMySQL(DATABASE).query_db(query, data)

    
#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE tags SET handle = %(handle)s,blockname = %(blockname)s,type = %(type)s,tag_number = %(tag_number)s,process_desc = %(process_desc)s,option_id = %(option_id)s,notes = %(notes)s,control_panel = %(control_panel)s,electrical = %(electrical)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    

    @classmethod
    def remove_one(cls,data):
        query = "UPDATE tags SET active = 0, notes = 'Remove' WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def reinstate_one(cls,data):
        query = "UPDATE tags SET active = 1, notes = 'None' WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM tags WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
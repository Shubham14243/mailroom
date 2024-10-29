import json

class Origin:
    
    @staticmethod
    def write_data(data):
        file_name = "domains.json"
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)
    
    @staticmethod
    def create_file():
        data = {
            "user_id" : [],
            "allowed_domains" : []
        }
        Origin.write_data(data)
            
    @staticmethod
    def read_file():
        data = {
            "user_id" : [],
            "allowed_domains" : []
        }
        try:
            file_name = "domains.json"
            with open(file_name, "r") as json_file:
                data = json.load(json_file)
        except:
            Origin.create_file()
        finally:
            return data
    
    @staticmethod
    def add_domain(user_id, domain):
        data = Origin.read_file()
        data['user_id'].append(user_id)
        data['allowed_domains'].append(domain)
        Origin.write_data(data)
            
    @staticmethod
    def update_domain(user_id, new_domain):
        data = Origin.read_file()
        data_index = data['user_id'].index(user_id)
        data['allowed_domains'][data_index] = new_domain
        Origin.write_data(data)
            
    @staticmethod
    def delete_domain(user_id):
        data = Origin.read_file()
        data_index = data['user_id'].index(user_id)
        data['user_id'].remove(user_id)
        data['allowed_domains'].pop(data_index)
        Origin.write_data(data)
        
    @staticmethod
    def get_allowed_domains():
        data = Origin.read_file()
        return data['allowed_domains']

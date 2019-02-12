class BaseModel:

    def generate_id(self, modelList, id=0):
        """Incremental generation of list ids
        
        Arguments:
            modelList {[list]} -- The list to generate an id for
        
        Keyword Arguments:
            id {int} 
        Returns:
            [int] -- generated id
        """

        if id == 0:
            id = len(modelList)+1

        if id in modelList:
            id = id+1
            return self.generate_id(id)
        return id

    def save(self, modelList, id):
        """
        universal method to add an object into a list 
        """

        modelList[id] = self
        return modelList

    def delete(self, modelList, id):
        """
        universal method to delete an object from list 
        """
        del modelList[id]
        return modelList
        
    @staticmethod
    def check_name_exists(the_list, name):
        """Validator to ensure unique names 
     
        """

        for i in the_list:
            if the_list[i].name == name:
                return i
        return False

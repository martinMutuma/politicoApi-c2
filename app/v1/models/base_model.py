class BaseModel:

    def generate_id(self, modelList, id=0):
        if id == 0:
            id = len(modelList)+1

        if id in modelList:
            id = id+1
            return self.generate_id(id)
        return id

    def save(self, modelList, id):
        modelList[id] = self
        return modelList

    def delete(self, modelList, id):
        del modelList[id]
        return modelList

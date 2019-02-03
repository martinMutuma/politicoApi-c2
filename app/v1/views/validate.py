class Validate(object):

    @classmethod
    def required(cls, fields=[], dataDict={}):
        notFound = []
        if len(fields)>0:
           notFound = [i for i in fields if i not in dataDict or len(dataDict[i])<1]

        if (len(notFound)> 0):
            return "Validation error,Following fields are required {}".format(", ".join(notFound))
        else:
            return True

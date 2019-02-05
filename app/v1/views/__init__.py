from flask import request

def get_data():
    '''Getting data from json or form submitted data '''
  
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    if not data:
        try:
            data = request.get_json(force=True)  
        except:
            data = dict() 

    return data
## Political 
[![Build Status](https://travis-ci.org/martinMutuma/politicoApi-c2.svg?branch=develop)](https://travis-ci.org/martinMutuma/politicoApi-c2)
[![Maintainability](https://api.codeclimate.com/v1/badges/b9d93f75e153d157012e/maintainability)](https://codeclimate.com/github/martinMutuma/politicoApi-c2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b9d93f75e153d157012e/test_coverage)](https://codeclimate.com/github/martinMutuma/politicoApi-c2/test_coverage)
[![Coverage Status](https://coveralls.io/repos/github/martinMutuma/politicoApi-c2/badge.svg?branch=develop)](https://coveralls.io/github/martinMutuma/politicoApi-c2?branch=develop)

## Description
Political is a platform for use by both  politicians and citizens.Political enables citizens give their mandate to politicians running for different government offices
while building trust in the process through transparency.

Political is impremented  using python data structures

## Setup and installation
1. Clone the repo
   ```git
        git clone https://github.com/martinMutuma/politicoApi-c2.git

        cd politicoApi-c2
   ```

2. Set up virtualenv

        
   ```bash
        #linux
        virtualenv venv
   ```
    
   ```bash
        #windows
        python -m virtualenv venv
   `````

3. Activate virtualenv

        
   ```bash
        #linux
        source venv/bin/activate
   ```
  
   ```bash
        #windows
        venv/Scripts/activate
   ```
4. Install dependencies

   ```bash
        #Universal windows and linux
        pip install -r requirements.txt
   ```

5. Setup env variables
   ```bash  
        #linux
        - export FLASK_APP=run.py
        - export FLASK_DEBUG=1
        - export FLASK_ENV=development
   ```
   ```bash  
        #windows
        - set FLASK_APP=run.py
        - set FLASK_DEBUG=1
        - set FLASK_ENV=development
   ```
6. Manually Running tests
      ```
         python -m pytest --cov=app
      ```
7. Start the server
      ```
         flask run
      ```

app is available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

##Political Endpoints

| Method   | Endpoint                             | Description                                 |
| -------- | ------------------------------------ | -------------------------------------       |
| `POST`   | `/api/v1/parties`                    | Create a new party                          |
| `GET`    | `/api/v1/parties`                    | View all parties                            |
| `GET`    | `/api/v1/parties/<int:party_id>`      | Get party details by party Id               |
| `PATCH`  | `/api/v1/parties/<int:party_id>/name` | Update a party  name                        |
| `DELETE` | `/api/v1/parties/<int:party_id>`      | Delete a party by Id                        |
| `GET`    | `/api/v1/offices`                    | View All offices                            |
| `POST`   | `/api/v1/offices`                    | Post a new office                           |
| `GET`    | `/api/v1/offices/<int:office_id>`    | Get a specific office                       |


## Project managemnt 
[Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2241695)

## Test with Postman 

For local app

[![Run in Postman local](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/11e358c7e2dac60c956f)

app on Heroku 

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/80ae6b6b1d58956222b3)

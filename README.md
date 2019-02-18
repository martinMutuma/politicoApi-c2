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
        - export CONNECTION_STRING=dbname='political_test' user='postgres' host='localhost' password='your postgress pass' port='5432'
   ```
   ```bash  
        #windows
        - set FLASK_APP=run.py
        - set FLASK_DEBUG=1
        - set FLASK_ENV=development
        - set CONNECTION_STRING=dbname='political_test' user='postgres' host='localhost' password='your postgress pass' port='5432'
   ```
6. Manually Running tests
      ```
         python -m pytest --cov=app
      ```
7. Start the server
      ```
         flask run
      ```

app is available at 

1. [Localhost](http://127.0.0.1:5000/)

2. [Heroku](https://mmmpolitical.herokuapp.com)


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

##Political v2 Endpoints

| Method   | Endpoint                                  | Description                                 |
| -------- | ------------------------------------      | -------------------------------------       |
| `POST`   | `/api/v2/parties`                         | Create a new party                          |
| `GET`    | `/api/v2/parties`                         | View all parties                            |
| `GET`    | `/api/v2/parties/<int:party_id>`          | Get party details by party Id               |
| `PATCH`  | `/api/v2/parties/<int:party_id>/name`     | Update a party  name                        |
| `DELETE` | `/api/v2/parties/<int:party_id>`          | Delete a party by Id                        |
| `GET`    | `/api/v2/offices`                         | View All offices                            |
| `POST`   | `/api/v2/offices`                         | Post a new office                           |
| `GET`    | `/api/v2/offices/<int:office_id>`         | Get a specific office                       |
| `POST`   | `/api/v2/auth/signup`                     | Create User                                 |
| `POST`   | `/api/v2/auth/login`                      | Login to system                             |
| `POST`   | `/api/v2/offices/<int:office_id>/register`| Register candidate                          |
| `POST`   | `/api/v2/offices/vote`                    | Cast vote                                   |
| `GET`    | `/api/v2/offices/<int:office_id>/result`  | Get a specific office results               |

## Project managemnt 
[Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2241695)

## Project documentation and endpoint Manual test

### [Api v2 Documentation on Apiary](https://political.docs.apiary.io/)
### [Api V2 Documentation on Postman](https://documenter.getpostman.com/view/3383651/S11BzhxS)
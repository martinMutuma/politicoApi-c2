## Political APi 
[![Build Status](https://travis-ci.org/martinMutuma/politicoApi-c2.svg?branch=develop)](https://travis-ci.org/martinMutuma/politicoApi-c2)
## Requirements 
Imprements the following endpoints using datastratures 
**API Endpoint Specification**

1. Endpoint: POST /parties

        Create a political party 

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [{
                “id”: Integer, // id of newly created party
                “name”: String,
                }]
        } 
        ```
2. Endpoint: GET /parties/<party-id>

        Fetch a specific political party record.

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [{
                “id” : Integer, // political party unique id
                “name” : String,
                “logoUrl”: String,
            }]
        }
        ```

3. Endpoint: GET /parties/

    Fetch all political parties records.

        Response spec:
        ```json
        {
        “status” : Integer,
        “data” : [
                {
                “id” : Integer, // political party unique id
                “name” : String,
                “logoUrl”: String,
                } , {
                “id” : Integer, // political party unique id
                “name” : String,
                “logoUrl”: String,
                } , {
                “id” : Integer, // political party unique id
                “name” : String,
                “logoUrl”: String,
                } , {
                “id” : Integer, // political party unique id
                “name” : String,
                “logoUrl”: String,
                }
                ]
            }
            ```
4.  Endpoint: PATCH /parties/<party-id>/name
        Edit the name of a specific political party.

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [{
                “id”: Integer, // political party unique id
                “name” : String, // the new name of the political party
                }]
        }
        ```
5. Endpoint: DELETE /parties/<party-id>
    Delete a specific political party.

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [{
            “message”: String
            }]
        }
        ```
6. Endpoint: POST /offices
        Create a political office.

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [{
            “id” : Integer, // id of newly created office
            “type” : String, // type of office
            “name” : String, // name of office
            }]
        }
        ```
7. Endpoint: GET /offices

        Fetch all political offices records

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [
        {
            “id” : Integer, // office record unique id
            “type” : String, // type of office
            “name”: String // name of office
            }, {
            “id” : Integer, // office record unique id
            “type” : String, // type of office
            “name”: String // name of office
            }, {
            “id” : Integer, // office record unique id
            “type” : String, // type of office
            “name”: String // name of office
            }
            ]
        }
        ```

8. Endpoint: GET /offices/<office-id>

        Fetch a specific political office record

        Response spec:
        ```
        {
        “status” : Integer,
        “data” : [{
            “id” : Integer, // office record unique id
            “type” : String, // type of office
            “name”: String // name of office
            }]
        }
        ```
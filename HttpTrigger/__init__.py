import logging
import pyodbc

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
   
    enteredName = req.params.get('name')
    if not enteredName:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            enteredName = req_body.get('name')
    
    if not enteredName:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

    #PLEASE STARILIZE YOUR SQL
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};Server=holidaze.database.windows.net;Database=users;UID=devlontecron;PWD=LaSalle!0')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM dbo.users where name LIKE \'{enteredName}\'")
    data = cursor.fetchall()

    if data:
        return func.HttpResponse(f"That Name already Exists {enteredName}" + data, 
            status_code=200
            )
    else:
        cursor.execute(f"INSERT INTO dbo.users (name, score) VALUES (\'{enteredName}\', 0)")
        return func.HttpResponse(
             "New Account has been added",
             status_code=200
        )

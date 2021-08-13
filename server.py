import os
import base64
import requests
import re
import json
from youtrack.connection import Connection as YouTrack
from collections import namedtuple

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():

  app.CommCareAPIKey = os.environ.get('CommCareAPIKey')
  app.CommCareBaseURL = os.environ.get('CommCareBaseURL')
  app.YTToken = os.environ.get('YTtokenv3')
  app.YTGoldCopyURL = os.environ.get('YTGoldCopyURL')

  
  hdrs = {
    'Accept': 'application/json', 
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + app.YTToken
  }


  projectId = "0-1"  
  
  # DELETE THE FIELDS WE DONT NEED FIRST
  #first get the fields in the project that we dont need  
  try:
    response = requests.get(
        app.YTGoldCopyURL + '/youtrack/api/admin/projects/' + projectId + '/fields?fields=field(aliases,isAutoAttached,isUpdateable,name,id),canBeEmpty,isPublic,id',
        headers=hdrs
    )
    json_response = response.json()
    # find the fields we dont like in the response
    if len(json_response)> 0:
      listOfFieldsToDelete = []
      # parse each field
      for field in json_response:
        # We dont need these default fields, so if you have any more of them, add them here.
        if field["field"]["name"] == "Priority" or field["field"]["name"] == "Type"  or field["field"]["name"] == "State" :
          #add it to the array
          listOfFieldsToDelete.append(field["id"])

    # If if found matches, delete them
    if len(listOfFieldsToDelete) > 0:
      # get the ID and make a request to delete it
      for item in listOfFieldsToDelete:

        try:
          print(app.YTGoldCopyURL + '/youtrack/api/admin/projects/'+ projectId + '/fields/' + item)
          print(itemjson)
          response = requests.delete(
              app.YTGoldCopyURL + '/youtrack/api/admin/projects/'+ projectId + '/fields/' + item,
              headers=hdrs,
              json = itemjson 
          )
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)     

  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)      
  

  
  return "Hello World! " 
  

if __name__ == "__main__":
  app.run()

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


  projectId = "0-34"  
  
  # DELETE THE FIELDS WE DONT NEED FIRST
  #first get the fields in the project that we dont need  
  try:
    response = requests.get(
        app.YTGoldCopyURL + '/youtrack/api/admin/projects/' + projectId + '/fields?fields=field(aliases,isAutoAttached,isUpdateable,name,id),canBeEmpty,isPublic,id',
        headers=hdrs
    )
    json_response = response.json()
    print(json_response)
    # find the fields we dont like in the response
    if len(json_response)> 0:
      # create a list to store all the ID's
      listOfFieldsToDelete = []
      # parse each field
      for field in json_response:
        # We dont need these default fields, so if you have any more of them, add them here.
        if field["field"]["name"] == "Priority" or field["field"]["name"] == "Type"  or field["field"]["name"] == "State"  or field["field"]["name"] == "Subsystem" or field["field"]["name"] == "Fix versions" or field["field"]["name"] == "Fix Affected versions"  or field["field"]["name"] == "Fixed in build" or field["field"]["name"] == "Estimation" or field["field"]["name"] == " Affected versions":
          #add it to the array
          listOfFieldsToDelete.append(field["id"])

    # If if found matches, delete them
    if len(listOfFieldsToDelete) > 0:
      # get the ID and make a request to delete it
      for item in listOfFieldsToDelete:
        print(item)
        try:
          print(app.YTGoldCopyURL + '/youtrack/api/admin/projects/'+ projectId + '/fields/' + item)
          print(item)
          response = requests.delete(
              app.YTGoldCopyURL + '/youtrack/api/admin/projects/'+ projectId + '/fields/' + item,
              headers=hdrs)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)     

  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)      
  

  
  return "Hello World! " 
  

if __name__ == "__main__":
  app.run()

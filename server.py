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

  hdrs = { 'Accept': 'application/json', 'Content-Type': 'application/json','Authorization': 'Bearer ' + app.YTToken}

  # Add the new project to YouTdack
  newProjectJson = {"shortName": "TXT001", "name": "TXT 001 Projects", "description": "A new project created from rest api", "leader":{"id":"1-1"}}

  # Create the project template
  try:
    response = requests.post(
        app.YTGoldCopyURL + '/youtrack/api/admin/projects?fields=id,shortName,name,leader(id,login,name)',
        headers=hdrs,
        json = newProjectJson 
    )
    json_response = response.json()
    print(json_response)
   
    projectId = json_response['id']
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)   

  #projectId = "0-34"  
  
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
  


    # Add the field to YouTrack
  field = {"fieldType": {"id": "enum[1]"}, "name": "Gender", "isDisplayedInIssueList": True, "isAutoAttached": False, "isPublic": True }
  try:
    response = requests.post(
        app.YTGoldCopyURL + '/youtrack/api/admin/customFieldSettings/customFields?fields=id,name,fieldType(presentation,id)',
        headers=hdrs,
        json = field 
    )
    json_response = response.json()
    print(json_response)

    fieldid = json_response['id']
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)   

    # Attach the field to the project
  #field = {"field": {"ordinal": 8, "instances": [], "usages": [], "isAutoAttached": False, "fieldDefaults": {"canBeEmpty": True, "isPublic": True, "id": fieldid, "$type": "CustomFieldDefaults"}, "isUpdateable": True, "isDisplayedInIssueList": True, "fieldType": {"valueType": "text", "isMultiValue": False, "isBundleType": False, "id": "text", "$type": "FieldType"}, "hasRunningJob": False, "name": "Due Date", "id": fieldid, "$type": "CustomField"}, "$type": "SimpleProjectCustomField"}
  field = {"field": {"id": fieldid}, "$type": "SingleEnumIssueCustomField"} 
  try:
    response = requests.post(
        app.YTGoldCopyURL + '/youtrack/api/admin/projects/'+projectId+'/customFields?fields=id,name',
        headers=hdrs,
        json = field 
    )
    json_response = response.json()

    fieldid = json_response['id']
    print(json_response)
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)   

  
  return "Hello World! " 
  

if __name__ == "__main__":
  app.run()

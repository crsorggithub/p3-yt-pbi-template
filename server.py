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
  #yt = YouTrack(app.YTGoldCopyURL + '/youtrack/', token=app.YTToken)
  

  #project = Project(id="CCT", name=str("ComCare Template"), description="This is the CommCare Template", lead="root")
  #yt.createProject(project)



  #project = yt.createProject(probj)
  #print(project)
  
  
  project_template = {
    "shortName":"CCT",
    "name" : "CommCare Project Template", 
    "description": "This is the CommCare project template. It should be used for creating new projects receiving data from the CommCare project space.", 
    "leader":{
		  "id":"1-2"
	  }
  }
  
  datatata = {"customFields":[
    {"name" : "Name of Staff Member Receiving Feedback", "$type" : "TextIssueCustomField", "value" : { "text": "test" }}
  ]}
  
  out = {
	"description": "A new project created from rest api",
	"name": "Test 22 Project",
	"shortName": "TST22",
	"leader":{
		"id":"1-1"
	  }
  }

  
  hdrs = {
          'Accept': 'application/json', 
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + app.YTToken
        }
  # Create the project template
  try:
    response = requests.post(
        app.YTGoldCopyURL + '/youtrack/api/admin/projects?fields=id,shortName,name,leader(id,login,name)',
        headers=hdrs,
        json = out 
    )
    json_response = response.json()
    
    projectid = json_response['id']
    print(json_response)
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)   
  
  # Add the custom fields
  
  field = {
    "fieldType": {
      "id": "enum[1]"
    },
    "name": "Gender",
    "isDisplayedInIssueList": "true",
    "isAutoAttached": "false",
    "isPublic": "true"
  }  
  
  try:
    response = requests.post(
        app.YTGoldCopyURL + '/youtrack/api/admin/customFieldSettings/customFields?fields=id,name,fieldType(presentation,id)',
        headers=hdrs,
        json = field 
    )
    json_response = response.json()
    
    fieldid = json_response['id']
    print(json_response)
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)   
    
  
  """
  try:
    response = requests.get(
        app.CommCareBaseURL + 'application/a1b787437bda83e6976f0706d46961ff',
        headers={'Accept': 'application/json', 'Authorization': 'ApiKey ' + app.CommCareAPIKey }      
    )
  except requests.exceptions.RequestException as e:  # This is the correct syntax
      raise SystemExit(e)  
  
  json_response = response.json()
  questions = json_response["modules"][0]["forms"][0]["questions"]
  #print(questions)
  out_data = {}
  out_arr = []
  for element in questions:
    
    #print (str(not element["is_group"]) + ' ' + str(element["type"] != "Trigger") + ' ' + str(element["type"] != "FieldList"))
    if (not element["is_group"]) and (element["type"] != "Trigger" and element["type"] != "FieldList") :
      #print(element["type"] + ': ' + element["label"])
      el = {}
      el["Label"] = element["label"]
      el["LabelFR"] = (element["translations"]["en"])
      el["LabelES"] = (element["translations"]["es"])
      el["LabelPOR"] = (element["translations"]["por"])
      el["type"] = element["type"];
      el["required"] = element["required"];
      el["commcareid"] = element["value"][ element["value"].rfind("/")+1 : : ]
      el["options"] = []

      ds = "data_source"
            
      if (el["type"] == "MSelect"  or el["type"] == "Select" )and ds not in element:
        
        for option in element["options"]:

          opt_val_obj = {}
          opt_val_obj["label"] = option["label"]
          opt_val_obj["labelES"] = option["translations"]["es"]
          opt_val_obj["labelPOR"] = option["translations"]["por"]
          opt_val_obj["labelFRA"] = option["translations"]["fra"]
          opt_val_obj["key"] = option["value"]
        
        el["options"].append(opt_val_obj)
      # if there's a fixture, get the data
      ds = "data_source"
      if ds in element:
        ir = "instance_ref"
        print(element)

        if ir  in element["data_source"]:
          fixture = element["data_source"]["instance_ref"]
          fixurl = element["data_source"]["instance_ref"][ element["data_source"]["instance_ref"].rfind(":")+1 : : ]
          response = requests.get(
              app.CommCareBaseURL + 'fixture/?fixture_type=' + fixurl,
              headers={'Accept': 'application/json', 'Authorization': 'ApiKey ' + app.CommCareAPIKey }      
          )
          print("fixture_response = " + str(response))
          fixture_response = response.json()
          #print(json.dumps(fixture_response))
          
          for option in fixture_response["objects"]:
            opt_val_obj = {}
            for field in option["fields"]:
              if len(option["fields"]) > 2:
                opt_val_obj["root_id"] = option["fields"][list(option["fields"])[0]]
                opt_val_obj["label"] = option["fields"][list(option["fields"])[1]]
                opt_val_obj["key"] = option["fields"][list(option["fields"])[2]]
              else:
                opt_val_obj["label"] = option["fields"][list(option["fields"])[0]]
                opt_val_obj["key"] = option["fields"][list(option["fields"])[1]]                                       
            
            el["options"].append(opt_val_obj)
            

      print("about to append: " + str(el))
      out_arr.append(el)
      
  # Data fetched, let's connect to YouTrack
  
    
  print(out_arr)
  out_data["fields"] = out_arr
  print(out_data)
  """
   
  

  
  return "Hello World! " 
  

if __name__ == "__main__":
  app.run()

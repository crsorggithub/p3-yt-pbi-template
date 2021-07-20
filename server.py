import os
import base64
import requests
import re
import json
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():

  app.CommCareAPIKey = os.environ.get('CommCareAPIKey')
  app.CommCareBaseURL = os.environ.get('CommCareBaseURL')

  response = requests.get(
      app.CommCareBaseURL + 'application/a1b787437bda83e6976f0706d46961ff',
      headers={'Accept': 'application/json', 'Authorization': 'ApiKey ' + app.CommCareAPIKey }      
  )
  
  json_response = response.json()
  questions = json_response["modules"][0]["forms"][0]["questions"]
  #print(questions)
  print('-------')
  for element in questions:
    
    #print (str(not element["is_group"]) + ' ' + str(element["type"] != "Trigger") + ' ' + str(element["type"] != "FieldList"))
    if (not element["is_group"]) and (element["type"] != "Trigger" and element["type"] != "FieldList") :
      print(element["type"] + ': ' + element["label"])
      el = {}
      el["Label"] = element["label"]
      el["LabelFR"] = (element["translations"]["en"])
      el["LabelES"] = (element["translations"]["es"])
      el["LabelPOR"] = (element["translations"]["por"])
      el["type"] = element["type"];
      el["required"] = element["required"];
      el["commcareid"] = element["value"][ element["value"].rfind("/")+1 : : ]
      el["options"] = []
      
      if el["type"] == "MSelect":
        print("---------------------- MSELECT")
        print(json.dumps(element))
      # if there's a fixture, get the data
      ds = "data_source"
      if ds in element:
        ir = "instance_ref"
        if ir  in element["data_source"]:
          fixture = element["data_source"]["instance_ref"]
          fixurl = element["data_source"]["instance_ref"][ element["data_source"]["instance_ref"].rfind(":")+1 : : ]
          response = requests.get(
              app.CommCareBaseURL + 'fixture/?fixture_type=' + fixurl,
              headers={'Accept': 'application/json', 'Authorization': 'ApiKey ' + app.CommCareAPIKey }      
          )
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
            
          

      print(json.dumps(el))  
    #if (el["type"] == 'Select'):
      #if (element["options"]):
    
  
  return "Hello World!"
  

if __name__ == "__main__":
  app.run()

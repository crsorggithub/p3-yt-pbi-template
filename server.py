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
            
          

      print(json.dumps(el))  
    #if (el["type"] == 'Select'):
      #if (element["options"]):
  print("about to append: " + str(el))
  out_data.append(el)
    
  print(out_data)
  
  return "Hello World!"
  

if __name__ == "__main__":
  app.run()

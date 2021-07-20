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
  print(questions)
  for element in questions:
    print( element["is_group"])
    if not element["is_group"] or element["type:
      print("")
      el = {}
    #el["Label"] = fixStr(element["label"])
    #el["LabelFR"] = fixStr(element["translations"]["en"])
    #el["LabelES"] = fixStr(element["translations"]["es"])
    #el["LabelPOR"] = fixStr(element["translations"]["por"])
      el["type"] = element["type"];
      el["required"] = element["required"];
    #if (el["type"] == 'Select'):
      #if (element["options"]):
  print(json.dumps(el))  
  
  return "Hello World!"
  

if __name__ == "__main__":
  app.run()

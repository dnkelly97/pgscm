import requests
import os

DISPATCH_URL = "" if 'WEBSITE_HOSTNAME' in os.environ else "http://127.0.0.1:8001"
DISPATCH_AUTH = "https://dispatchlite.azurewebsites.net/" if 'WEBSITE_HOSTNAME' in os.environ else "" #your testing url, leave blank for testing

def get_all_template_data():
    templates = get_templates()
    template_objects = []
    for template in templates:
        template_data = get_template(template)
        template_objects.append(template_data)
    return template_objects

def get_templates():
    template_urls = requests.get(DISPATCH_URL+'/templates/' , headers={'Authorization': 'x-dispatch-api-key DISPATCH_AUTH'}).json()
    return template_urls

def get_template(url):
    return requests.get(url, headers={'Authorization': 'x-dispatch-api-key DISPATCH_AUTH'}).json()

def get_template_url(key):
    id = key.split('_')[2]
    return DISPATCH_URL+'/templates/'+id

def jsonify_placeholders(keys,values):
    placeholders = {}
    for i in range(len(keys)):
        key = keys[i].split('_')[1]
        value = values[i][0]
        if value == '':
            return "Invalid"
        else:
            placeholders[key] = value
    return placeholders

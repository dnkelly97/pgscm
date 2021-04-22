import requests
import os

DISPATCH_URL = "" if 'WEBSITE_HOSTNAME' in os.environ else "http://127.0.0.1:8001"

def get_all_template_data():
    templates = get_templates()
    print(templates)
    template_objects = []
    for template in templates:
        template_data = get_template(template)
        template_objects.append(template_data)
    return template_objects

def get_templates():
    template_urls = requests.get(DISPATCH_URL+'/templates/').json()
    return template_urls

def get_template(url):
    return requests.get(url).json()

def get_template_url(key):
    id = key.split('_')[2]
    return DISPATCH_URL+'/templates/'+id

def jsonify_placeholders(keys,values):
    placeholders = {}
    for i in range(len(keys)):
        key = keys[i].split('_')[1]
        placeholders[key] = values[i][0]
    return placeholders
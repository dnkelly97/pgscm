import requests
import os
from django.contrib.auth.models import User


DISPATCH_URL = os.environ.get('DISPATCH_URL') if 'WEBSITE_HOSTNAME' in os.environ else "http://127.0.0.1:8001" #make sure dispatch runs on port 8001
DISPATCH_AUTH = os.environ.get('DISPATCH_AUTH') if 'WEBSITE_HOSTNAME' in os.environ else "" #your developing client key, leave blank for testing # d3juGGzfHpBVtK1ZmrND

def get_all_template_data():
    templates = get_templates()
    template_objects = []
    for template in templates:
        template_data = get_template(template)
        template_objects.append(template_data)
    return template_objects

def get_templates():
    template_urls = requests.get(DISPATCH_URL+'/templates/' , headers={'Authorization': 'x-dispatch-api-key '+DISPATCH_AUTH}).json()
    return template_urls

def get_template(url):
    return requests.get(url, headers={'Authorization': 'x-dispatch-api-key '+DISPATCH_AUTH}).json()

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


def dispatch_campaign_post(pipeline_id, pipeline_name):
    data = {'id': pipeline_id, 'name': pipeline_name}
    return requests.post(DISPATCH_URL+'/campaigns/',
                         headers={'Authorization': 'x-dispatch-api-key ' + DISPATCH_AUTH},
                         data=data)


def dispatch_communication_post(campaign_id, stage_id, name, placeholders, template):
    email = {'fromAddress': 'dontmatter@gmail.com', 'fromName': 'you mom. hah.', 'subject': 'this one is a bit of a problem...'}
    destinations = [
        {
          "bounceAddress": "bounce-to-here@uiowa.edu",
          "linkTrackingDisabled": False,
          "openTrackingDisabled": False,
          "replyToAddress": "reply-to-here@uiowa.edu",
          "suppressionList": "http://garby.net/supressionlists/7684916",
          "type": "SMTP"
        }
    ]
    data = {'id': stage_id,
            'name': name,
            'type': 'EMAIL',
            'email': email,
            'destinations': destinations,
            'placeholders': placeholders,
            'template': template,
            'notificationAddresses': [user.email for user in User.objects.filter(is_superuser=True)],
            }
    return requests.post(DISPATCH_URL+'/campaigns/' + str(campaign_id) + '/communications',
                         headers={'Authorization': 'x-dispatch-api-key ' + DISPATCH_AUTH},
                         json=data)

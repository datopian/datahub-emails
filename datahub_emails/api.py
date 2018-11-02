import logging
import requests

from .config import mch_user, mch_secret, mch_list_id
from .config import statuspage_id, statuspage_api_key

statuspage_headers={'Authorization': 'OAuth %s' % statuspage_api_key}

def on_new_user(user_info):
    errors = []
    mch_info = {
        "email_address": user_info['email'],
        "status": "subscribed"
    }
    try:
        ret = requests.post(
            'https://us12.api.mailchimp.com/3.0/lists/{}/members/'.format(mch_list_id),
            auth=(mch_user, mch_secret),
            json=mch_info)
        resp = ret.json()
        if ret.status_code > 205:
            errors.append(resp.get('detail'))
    except Exception as e:
        errors.append(str(e))

    if len(errors):
        logging.error(errors[0])
        return False
    return True


def on_incident(incident, publisher, errors='', status='identified'):
    if isinstance(errors, list):
        errors = '\n'.join(errors)
    component_id = _get_component_id(publisher)
    logging.error(component_id)
    if component_id is None:
        logging.info('Component with name %s Not Found' % publisher)
        return

    payload = {
      "incident": {
        "name": incident,
        "body": errors,
        "status": status,
        "component_ids": [component_id]
      }
    }
    resp = requests.post(
        'https://api.statuspage.io/v1/pages/{page_id}/incidents'.format(
                                                    page_id=statuspage_id),
        headers=statuspage_headers,
        json=payload
    )
    if resp.status_code > 205:
        logging.info('Not able to connect to https://api.statuspage.io')
        return
    return resp.json()


def subscribe_user(username, email):
    component_id = _get_component_id(username)
    if component_id is None:
        logging.info('Component with name %s Not Found' % username)
        return

    payload = {
      "email": email,
      "component_ids": [component_id]
    }
    resp = requests.post(
        'https://api.statuspage.io/v1/pages/{page_id}/subscribers'.format(page_id=statuspage_id),
        headers=statuspage_headers,
        json=payload
    )
    if resp.status_code > 205:
        logging.info('Not able to connect to https://api.statuspage.io')
        return
    return resp.json()


def _get_component_id(component_name):
    resp = requests.get(
        'https://api.statuspage.io/v1/pages/{page_id}/components'.format(page_id=statuspage_id),
        headers=statuspage_headers
    )
    if resp.status_code > 205:
        logging.info('Not able to connect to https://api.statuspage.io')
        return
    components = resp.json()
    component_id = None
    for component in components:
        if component.get('name') == component_name:
            component_id = component.get('id')
    return component_id

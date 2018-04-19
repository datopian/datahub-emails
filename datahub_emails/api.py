import logging
import requests
import json

from .config import mch_user, mch_secret, mch_list_id


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
            data=json.dumps(mch_info))
        resp = ret.json()
        if ret.status_code > 205:
            errors.append(resp.get('detail'))
    except Exception as e:
        errors.append(str(e))

    if len(errors):
        logging.error(errors[0])
        return False
    return True

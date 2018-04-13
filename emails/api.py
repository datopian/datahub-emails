import requests

from .config import mch_user, mch_secret, mch_list_id


def on_new_user(user_info):
    errors = []
    mch_info = {
        "email_address": user_info['email'],
        "status": "subscribed",
        "merge_fields": {
            "FNAME": user_info.get('name', '')
        }
    }
    try:
        ret = requests.post(
            'https://us12.api.mailchimp.com/3.0/lists/{}/members/'.format(mch_list_id),
            auth=(mch_user, mch_secret),
            data=mch_info)
        resp = ret.json()
        if resp['status'] > 205:
            errors.append(resp.get('detail'))
    except Exception as e:
        errors.append(str(e))
    return {'success': len(errors) == 0, 'errors': errors}

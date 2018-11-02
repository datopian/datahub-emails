import os

mch_user = os.environ.get('MAILCHIMP_USER')
mch_secret = os.environ.get('MAILCHIMP_SECRET')
mch_list_id = os.environ.get('MAILCHIMP_LIST_ID', '97878f666d')

statuspage_id = os.environ.get('STATUSPAGE_ID')
statuspage_api_key = os.environ.get('STATUSPAGE_API_KEY')

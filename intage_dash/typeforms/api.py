from django.conf import settings

import requests


class TypeformDataAPI(object):
    def get_form_data(self, typeform_uid):
        typeform_api_key = settings.TYPEFORM_API_KEY
        url = f'https://api.typeform.com/v1/form/' \
            f'{typeform_uid}?key={typeform_api_key}'
        response = requests.get(url)
        return response.json()

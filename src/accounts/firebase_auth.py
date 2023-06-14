import os
import firebase_admin
from firebase_admin import credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_KEY = os.path.join(BASE_DIR, 'utils', 'serviceAccountKey.json')

cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)

from .models import CustomUser

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return None
        try:
            decoded_token = firebase_admin.auth.verify_id_token(token)
            uid = str(decoded_token['uid'])
            user = CustomUser.objects.get(uid=uid)
            return (user, None)
        except BaseException as error:
            print(error)
            raise AuthenticationFailed('Invalid Firebase token')
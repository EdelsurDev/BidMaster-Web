# middlewares.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth

# Initialize Firebase admin if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app()

User = get_user_model()

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        id_token = request.headers.get('Authorization')
        if id_token:
            try:
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token['uid']
                email = decoded_token.get('email')
                try:
                    user = User.objects.get(username=uid)
                except User.DoesNotExist:
                    user = User.objects.create(username=uid, email=email)
                request.user = user
            except Exception as e:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        # Make sure request.firebase_user is always set
        request.firebase_user = request.user

        response = self.get_response(request)
        return response

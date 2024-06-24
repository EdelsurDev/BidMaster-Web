import firebase_admin
from firebase_admin import auth
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

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
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response

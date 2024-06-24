from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from usuarios.models import Usuario
from .forms import UsuarioCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import firebase_admin
from firebase_admin import auth    

@csrf_exempt
def authenticate_user(request):
    if request.method == 'POST':
        id_token = request.headers.get('Authorization')
        if not id_token:
            return JsonResponse({'error': 'No token provided'}, status=400)
        
        # Token validation logic
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            
            # Create or get the user
            user, created = Usuario.objects.get_or_create(username=uid, defaults={'email': email})
            
            return JsonResponse({'status': 'success', 'user': user.username})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
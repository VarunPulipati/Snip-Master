import json
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import FileResponse, HttpResponse, Http404
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
import os
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

User = get_user_model()
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_donation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        amount = data.get('amount')

        # You can add logic to process the donation (e.g., integrate with a payment gateway)
        # For now, we'll just simulate the donation processing
        return JsonResponse({'message': f'Donation of {amount} from {name} processed successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt  # For development, make sure to handle CSRF properly in production
def handle_contact_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Example: Send an email using Django's send_mail function
        send_mail(
            f"Contact Form Submission from {name}",
            message,
            email,
            ['support@snipmaster.com'],  # Recipient's email
        )
        return JsonResponse({'message': 'Message sent successfully'}, status=200)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Home page (Can be extended or modified as needed)
def home(request):
    return HttpResponse("Welcome to the home page.")

# Updated SignUpView for handling API-based registration
class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to download a file from the server
def download_file(request):
    filepath = os.path.join(settings.BASE_DIR, 'Downloads', 'clipboard.exe')
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return FileResponse(f, as_attachment=True, filename='clipboard.exe')
    raise Http404('File not found.')

# Custom login view to handle API-based login from frontend
@method_decorator(csrf_exempt, name='dispatch')  # Not recommended for production
class CustomLoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'status': 'error', 'message': 'Missing credentials'}, status=400)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Login successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Login failed', 'error': str(e)}, status=500)

# Additional view for testing the API
def test_view(request):
    return JsonResponse({'message': 'API is working'}, status=200)

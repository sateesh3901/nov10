from django.shortcuts import render
from django.http import JsonResponse
import json,bcrypt
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer

# Create your views here.
def home(req):
    return JsonResponse({"home":"welcome"})

@csrf_exempt
def register(req):
    data = json.loads(req.body)
    if not data.get('username') or not data.get('password'):
        return JsonResponse({"error":"invalid username"})
    hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    data['password'] = hashed_password
    sr = UserSerializer(data = data)
    if sr.is_valid():
        sr.save()
        return JsonResponse({"success":"user registered successfully"})
    return JsonResponse({"error":"invalid inputs"})

@csrf_exempt
def login(req):
    data = json.loads(req.body)
    if not data.get('username'):
        return JsonResponse({"error":"invalid username"})
    try:
        u1 = User.objects.get(username = data.get('username'))
    except:
        return JsonResponse({"error":"username is not registered"})
    login_password = data.get('password').encode('utf-8')
    if bcrypt.checkpw(login_password, u1.password.encode('utf-8')):
        return JsonResponse({"status":"login successfully"})
    return JsonResponse({"error":"invalid username and password"})


@csrf_exempt
def update(req):
    data = json.loads(req.body)
    try:
        u1 = User.objects.get(username = data.get('username'))
    except:
        return JsonResponse({"error":"username is not registered"})
    if bcrypt.checkpw(data.get('password').encode('utf-8'),u1.password.encode('utf-8')):
        return JsonResponse({"error":"new password cannot be the same as old"})
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
    data['password'] = hashed_password
    sr = UserSerializer(u1,data = data, partial = True)
    if sr.is_valid():
        sr.save()
        return JsonResponse({"success":"update successfully"})
    return JsonResponse({"error":404})
    

@csrf_exempt
def delete(req):
    data = json.loads(req.body)
    if not data.get('username'):
        return JsonResponse({"error": "username required"})
    try:
        u1 = User.objects.get(username = data.get('username'))
        u1.delete()
        return JsonResponse({"success": "user deleted successfully"})
    except:
        return JsonResponse({"error": "username is not registered"})
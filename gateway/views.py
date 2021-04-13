from django.shortcuts import render
from rest_framework.decorators import api_view
from decouple import config
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR
)
from rest_framework.response import Response
import requests
import json

@api_view(["POST"])
def register(request):
    data = {
        "username": request.POST.get("username"),
        "email": request.POST.get("username"),
        "password": request.POST.get("password"),
        "password2": request.POST.get("password2"),
        "first_name": request.POST.get("first_name"),
        "last_name": request.POST.get("last_name"),
        "phone_number": request.POST.get("phone_number"),
    }

    if request.POST.get("register_type") == 'producer':
        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/register_producer/"
        )
    else:
        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/register_market/"
        )
        data["owner_phone_number"] = request.POST.get("owner_phone_number")
        data["cnpj"] = request.POST.get("cnpj")
        data["cep"] = request.POST.get("cep")
        data["comercial_name"] = request.POST.get("comercial_name")   

    return api_redirect(url, data)

@api_view(["POST"])
def login(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/login/"
    )

    # Data should have username, password

    return api_redirect(url, request.POST)

@api_view(["POST"])
def check_token(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/"
    )

    # Data should have acces-token, refresh-token

    response = api_redirect(url, None, {'Authorization': 'Bearer {}'.format(request.POST.get("acces-token"))})

    if response.status_code != 200:
        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/login/refresh/"
        )

        data = {
            "refresh": request.POST.get("refresh-token")
        }

        return api_redirect(url, data)
    else:
        return response
    
def api_redirect(url, data, header = None):
    try:
        if header:
            response = requests.get(url, headers=header)
        else:
            response = requests.post(url, data=data)
        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except:
            return Response(response)
    except:
        return Response(
            {'error': 'Nao foi possivel se comunicar com o servidor'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
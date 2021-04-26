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
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/register_market/"
    )

    # Data should have first_name, last_name, owner_phone_number, comercial_name, cnpj, cep, phone_number, producer, email, password, password2

    return api_redirect(url, request.data)

@api_view(["POST"])
def login(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/login/"
    )

    # Data should have username, password

    return api_redirect(url, request.data)

@api_view(["POST"])
def check_token(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/"
    )

    # Data should have acces-token, refresh-token

    response = api_redirect(url, None, {'Authorization': 'Bearer {token}'.format(request.data.get(token = "acces-token"))})

    if response.status_code != 200:
        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/login/refresh/"
        )

        data = {
            "refresh": request.data.get("refresh-token")
        }

        return api_redirect(url, data)
    else:
        return response

@api_view(["POST"])
def password_recovery(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/password_recovery/"
    )

    # Data should have email
    try:
        _session = requests.Session()

        _session.get(url)

        data = request.data
        data['csrfmiddlewaretoken'] = _session.cookies['csrftoken']

        response = _session.post(url, data=data)

        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except:
            return Response(response, status=response.status_code)

    except:
        return Response(
            {'error': 'Nao foi possivel se comunicar com o servidor'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def password_reset(request, user, token):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/password_recovery/reset/{user}/{token}/".format(user = user, token = token)
    )

    # Data should have password, password2
    try:
        _session = requests.Session()

        _session.get(url)

        data = request.data
        data['csrfmiddlewaretoken'] = _session.cookies['csrftoken']

        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/password_recovery/reset/{user}/set-password/".format(user = user)
        )

        response = _session.post(url, data=data)

        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except:
            return Response(response, status=response.status_code)

    except:
        return Response(
            {'error': 'Nao foi possivel se comunicar com o servidor'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
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
            return Response(response, status=response.status_code)
    except:
        return Response(
            {'error': 'Nao foi possivel se comunicar com o servidor'},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
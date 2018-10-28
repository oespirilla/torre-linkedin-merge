from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings


import requests

def linkedin_callback(request):

    if 'code' in request.GET:
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        code = request.GET['code']
        redirect_uri = settings.LINKEDIN_CALLBACK
        client_id = settings.LINKEDIN_CLIENT
        client_secret = settings.LINKEDIN_SECRET

        post_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post(url, data=post_data)
        content = response.json()
        
        if 'access_token' in content:
            request.session['access_token'] = content['access_token']
            request.session['expires_in'] = content['expires_in']
            
            return HttpResponseRedirect(reverse( 'profiles:detail', kwargs={'username': request.user.username}))
    else:
        
        content = 'Error authenticating with LinkedIn'
        #I should use an error page
        return HttpResponseRedirect(reverse( 'profiles:detail', kwargs={'username': request.user.username}))

    return HttpResponse(content)
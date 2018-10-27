from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import requests

def linkedin_callback(request):

    if 'code' in request.GET:
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        code = request.GET['code']
        redirect_uri = 'http://localhost:8000/callback'
        client_id = '78evh5k1q2yj6n'
        client_secret = 'BE08KtvZ8WUrJcgj'

        post_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post(url, data=post_data)
        content = response.json()
        print (content)
        
        if 'access_token' in content:
            request.session['access_token'] = content['access_token']
            request.session['expires_in'] = content['expires_in']
            print ('access_token')
            return HttpResponseRedirect(reverse( 'profiles:detail', kwargs={'username': request.user.username}))
    else:
        print ('error')
        content = 'Error authenticating with LinkedIn'

        return HttpResponseRedirect(reverse( 'profiles:detail', kwargs={'username': request.user.username, 'error' : content}))

    return HttpResponse(content)
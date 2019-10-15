from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponseNotFound


def index(request, path):


    path = path.replace('_', ':')
    print(reverse(path))
    try:
        url = reverse(path)

    except Exception as e:
        return HttpResponseNotFound(f"url with pathname '{path}' does not exist") 
    return JsonResponse({'url': url})
    


from django.shortcuts import render


def redoc(request):
    return render(request, 'redoc/redoc.html')


def redoc_json(request):
    return render(request, 'redoc/redoc-2.json')

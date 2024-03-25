from django.shortcuts import render


def redoc(request):
    return render(request, 'redoc_tasks/Redoc.html')


def redoc_json(request):
    return render(request, 'redoc_tasks/redoc-2.json')

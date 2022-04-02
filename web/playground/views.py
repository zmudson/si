from django.shortcuts import render


def hello(request):
    context = {
        'greeting': 'Hello world!'
    }
    return render(request, 'index.html', context)

from django.shortcuts import render, HttpResponse


def index(requests):
    return render(requests, 'stocks/index.html')


def safe(requests):
    return render(requests, 'stocks/safe.html')


def risk(requests):
    context = {
        'companies': [
            {'name': 'Aviat Networks', 'field': 'Network managment', 'ccp': 'val','initial':'avnw'},
            {'name': 'Fulgent Genetics','field': 'Combination of Gentics, Molecular Biology, Computer Science', 'ccp': 'val','initial':'flgt'},
            {'name': 'Zedge', 'field': 'Content Discovery Platform', 'ccp': 'val','initial':'zdg'}
        ]
    }
    return render(requests, 'stocks/risk.html', context=context)

def company(requests,comp):
    return HttpResponse(comp)

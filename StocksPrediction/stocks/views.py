import re
import tensorflow as tf
from django.shortcuts import render
import pandas as pd
import tensorflow.keras.models as tf
from stocks.functions import *
from stocks.models import Companies


def index(requests):
    return render(requests, 'stocks/index.html')


def safe(requests):
    comp_list = Companies.objects.filter(type_of_investment='safe')
    context = {"companies": comp_list}
    return render(requests, 'stocks/safe.html',context=context)


def risk(requests):
    comp_list = Companies.objects.filter(type_of_investment='risk')
    context = {"companies":comp_list}
    return render(requests, 'stocks/risk.html', context=context)

def company(requests,company_id):
    context ={}
    comp = Companies.objects.filter(company_id=company_id)[0]
    context['info'] = comp
    if comp.type_of_investment == 'risk':
        numberofdays = 10
    else:
        numberofdays = 30
    numberofdays = int(numberofdays)
    data_file = 'static/'+"".join(comp.name.split(" ")) + '.csv'
    pkl_file = 'static/' + "".join(comp.name.split(" ")) + '.pkl'
    df = pd.read_csv(data_file)
    model = tf.load_model(pkl_file)
    context = merge(df, model, numberofdays)
    context['graph'] = return_graph(df.filter(['Close']), context['output'], numberofdays)
    context['numberofdays'] = numberofdays
    context['info'] = comp

    if requests.method == "POST":
        numberofdays = requests.POST.get('numberofdays')
        numberofdays = int(numberofdays)
        data_file = 'static/'+"".join(comp.name.split(" ")) + '.csv'
        pkl_file = 'static/' + "".join(comp.name.split(" ")) + '.pkl'
        df = pd.read_csv(data_file)
        model = tf.load_model(pkl_file)
        context_for_user = merge(df, model,numberofdays) 
        context['graph'] = return_graph(df.filter(['Close']), context_for_user['output'],numberofdays)
        context['numberofdays'] = numberofdays
        context['info'] = comp
        return render(requests,'stocks/company.html',context=context)

    
    return render(requests,'stocks/company.html',context=context)



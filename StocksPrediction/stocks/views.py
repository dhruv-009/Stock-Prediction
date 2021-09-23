import tensorflow as tf
from django.shortcuts import render
import pandas as pd
import tensorflow.keras.models as tf
from stocks.functions import *
from stocks.models import Companies


def index(requests):
    return render(requests, 'stocks/index.html')


def safe(requests):
    return render(requests, 'stocks/safe.html')


def risk(requests):
    comp_list = Companies.objects.filter(type_of_investment='risk')
    context = {"companies":comp_list}
    return render(requests, 'stocks/risk.html', context=context)

def company(requests,company_id):
    comp = Companies.objects.filter(company_id = company_id)[0]
    data_file = 'static/'+"".join(comp.name.split(" ")) + '.csv'
    pkl_file = 'static/' +"".join(comp.name.split(" ")) + '.pkl'
    df = pd.read_csv(data_file)
    model = tf.load_model(pkl_file)
    context = merge(df,model)
    context['info'] = comp
    context['graph'] = return_graph(df.filter(['Close']), context['output'])
    return render(requests,'stocks/company.html',context=context)



from django.urls import path,include
from stocks import views

urlpatterns = [
    path('',views.index,name="index"),
    path('safe',views.safe,name="safe"),
    path('risk',views.risk,name="risk"),
    path('company/<str:comp>', views.company,name='company')
]
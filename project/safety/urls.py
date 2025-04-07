from django.urls import path

from .views import record_misconduct, MisconductList

app_name = 'safety'

urlpatterns = [
    path('record-misconduct', record_misconduct, name = 'record_misconduct'),
    path('misconduct-list', MisconductList.as_view(), name = 'misconduct_list'),
]

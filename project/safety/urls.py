from django.urls import path

from .views import record_misconduct, MisconductList, MisconductDetail, protocol_word_view, behest_word_view

app_name = 'safety'

urlpatterns = [
    path('record-misconduct', record_misconduct, name = 'record_misconduct'),
    path('misconducts', MisconductList.as_view(), name = 'misconduct_list'),
    path('misconducts/<int:pk>', MisconductDetail.as_view(), name = 'misconduct_details'),
    path('protocol-word/<int:pk>', protocol_word_view, name = 'protocol_word'),
    path('behest-word/<int:pk>', behest_word_view, name = 'behest_word'),
]

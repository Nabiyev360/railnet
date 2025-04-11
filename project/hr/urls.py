from django.urls import path

from .views import hr_misconducts_view, misconduct_detail_view, misconduct_protocol_behest_view, misconduct_send_director


app_name = 'hr'

urlpatterns = [
    path('misconducts', hr_misconducts_view, name='misconduct_list'),
    path('misconducts/<int:pk>', misconduct_detail_view, name='misconduct_details'),
    path('misconducts/gen-behest/<int:pk>', misconduct_protocol_behest_view, name='misconduct_protocol_behest'),
    path('misconduct/send-director/<int:pk>', misconduct_send_director, name='misconduct_send_director'),
]

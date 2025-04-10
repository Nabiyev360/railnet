from django.shortcuts import render, redirect

from safety.models import Misconduct
from .generators import safety_behest_generator


def hr_misconducts_view(request):
    misconducts = Misconduct.objects.all().order_by('-id')
    return render(request, 'hr/misconduct-list.html', context={"misconducts": misconducts})

def misconduct_detail_view(request, pk):
    misconduct = Misconduct.objects.get(id=pk)
    return render(request, 'hr/misconduct-details.html', context={"misconduct": misconduct})

def misconduct_protocol_behest_view(request, pk):
    misconduct = Misconduct.objects.get(id=pk)
    relative_path = safety_behest_generator(request, misconduct)
    misconduct.behest = relative_path
    misconduct.save()
    return redirect(f'/hr/misconducts/{misconduct.id}')

def misconduct_send_director(request, pk):
    misconduct = Misconduct.objects.get(id=pk)
    misconduct.status = 'ready_to_sign'
    misconduct.save()
    return redirect(f'/hr/misconducts/{misconduct.id}')
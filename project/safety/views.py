from django.shortcuts import render, redirect
from django.views import View

from .models import Misconduct
from profiles.services import get_employee, get_personal


def record_misconduct(request):
    if request.method == "POST":
        worker_pin = request.POST.get('pin')
        employee = get_employee(worker_pin).json()["worker"]
        ex_id = employee["id"]
        personal = get_personal(ex_id).json()['cadry']

        Misconduct.objects.create(
            created_by=request.user.profile,
            fullname=f"{personal['last_name']} {personal['first_name']} {personal['middle_name']}",
            company=employee['position']["organization"],
            position=employee['position']["name"],
            worker_pin=personal["jshshir"],
            reason=request.POST.get('reason'),
            comment=request.POST.get('comment'),
            coupon=(1 if request.POST.get('coupon') else None),
        )

        return redirect('/safety/misconduct-list')


class MisconductList(View):
    def get(self, request):
        misconducts = Misconduct.objects.all().order_by('-id')
        return render(request, 'safety/misconduct-list.html', context={"misconducts": misconducts})

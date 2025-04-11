from django.http import FileResponse
from django.shortcuts import render, redirect
from django.views import View

from profiles.services import get_employee, get_personal
from .models import Misconduct
from .generators import protocol_generator


def record_misconduct(request):
    if request.method == "POST":
        worker_pin = request.POST.get('pin')
        reason = request.POST.get('reason')
        comment = request.POST.get('comment')
        coupon = 1 if request.POST.get('coupon') else None

        employee_data = get_employee(worker_pin).json().get("worker", {})
        ex_id = employee_data.get("id")
        personal_data = get_personal(ex_id).json().get("cadry", {})

        fullname = f"{personal_data.get('last_name', '')} {personal_data.get('first_name', '')} {personal_data.get('middle_name', '')}".strip()
        position_info = employee_data.get("position", {})
        company = position_info.get("organization", "")
        position = position_info.get("name", "")
        worker_jshshir = personal_data.get("jshshir", "")

        misconduct = Misconduct.objects.create(
            created_by=request.user.profile,
            fullname=fullname,
            company=company,
            position=position,
            worker_pin=worker_jshshir,
            reason=reason,
            comment=comment,
            coupon=coupon,
        )

        misconduct.protocol = protocol_generator(request, fullname, position)
        misconduct.save()

        return redirect('/safety/misconducts')


class MisconductList(View):
    def get(self, request):
        misconducts = Misconduct.objects.all().order_by('-id')
        return render(request, 'safety/misconduct-list.html', context={"misconducts": misconducts})


class MisconductDetail(View):
    def get(self, request, pk):
        misconduct = Misconduct.objects.get(id=pk)
        domain = request.get_host()
        return render(request, 'safety/misconduct-details.html', context={"misconduct": misconduct, "domain": domain})


def protocol_word_view(request, pk):
    misconduct = Misconduct.objects.get(id=pk)
    protocol_path = misconduct.protocol.path
    return FileResponse(open(protocol_path, 'rb'))


def behest_word_view(request, pk):
    misconduct = Misconduct.objects.get(id=pk)
    behest_path = misconduct.behest.path
    return FileResponse(open(behest_path, 'rb'))

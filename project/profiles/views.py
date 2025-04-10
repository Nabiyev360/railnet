import aiohttp
import asyncio
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from asgiref.sync import sync_to_async

from .services import get_employee, get_personal, get_careers, get_edu, get_meds
from .hashing import xor_decrypt


class CardView(View):
    async def get(self, request, pk: str):
        user = await sync_to_async(lambda: request.user)()  # sinxron chaqiruv
        is_auth = await sync_to_async(lambda: user.is_authenticated)()
        if is_auth:
            role = await sync_to_async(lambda: user.profile.role)()
            user_fullname = await sync_to_async(lambda: user.profile.full_name)()
            base_template = 'safety/base-safety.html'
        else:
            role = None
            user_fullname = None
            base_template = 'base-anonym.html'


        pin = xor_decrypt(pk)
        async with aiohttp.ClientSession() as session:
            # API so‘rovlarini asinxron chaqiramiz
            employee_task = asyncio.create_task(self.fetch_employee(session, pin))
            personal_task = asyncio.create_task(self.fetch_personal(session, employee_task))
            careers_task = asyncio.create_task(self.fetch_careers(session, employee_task))
            edu_task = asyncio.create_task(self.fetch_edu(session, employee_task))
            meds_task = asyncio.create_task(self.fetch_meds(session, employee_task))

            # Barcha ma'lumotlarni kutib olamiz
            employee, personal, careers, educations, med_info = await asyncio.gather(
                employee_task, personal_task, careers_task, edu_task, meds_task
            )

        if employee:
            name = f"{employee['last_name']} {employee['first_name']}"
            fullname = f"{name} {employee['middle_name']}"
            company_name = employee['position']['organization']
            position = employee['position']['name']
            seniority_railway = datetime.strptime(employee['job_date'], "%Y-%m-%d").date()
            photo_url = employee['photo']

            birth_date = datetime.strptime(personal['birth_date'], "%Y-%m-%d").date()
            address = f"{personal['address_region_id']['name']}, {personal['address_city_id']['name']}"
            phone = personal['phone']

            try:
                med = med_info["cadry"]["meds"][0]
                date2 = datetime.strptime(med["date2"], "%Y-%m-%d").date()
                difference = (date2 - datetime.today().date()).days
            except Exception:
                difference = None

            context = {
                "pin": pin,
                "name": name,
                "fullname": fullname,
                "photo_url": photo_url,
                "company_name": company_name,
                "position": position,
                "seniority_railway": seniority_railway,
                "birth_date": birth_date,
                "address": address,
                "phone": phone,
                "careers": list(reversed(careers)),
                "educations": list(reversed(educations)),
                "difference": difference,
                "is_authenticated": is_auth,
                "user_role": role,
                "user_fullname": user_fullname,
                "base_template": base_template
            }
            return render(request, 'profiles/card.html', context)
        else:
            return JsonResponse({"message": "API error"}, status=500)

    async def fetch_employee(self, session, pin):
        """Ishchini ma'lumotlarini olish"""
        res = await sync_to_async(get_employee)(pin)
        if res.status_code == 200:
            return res.json().get("worker")
        return None

    async def fetch_personal(self, session, employee_task):
        """Shaxsiy ma'lumotlarni olish"""
        employee = await employee_task
        if employee:
            res = await sync_to_async(get_personal)(employee["id"])
            return res.json().get("cadry")
        return None

    async def fetch_careers(self, session, employee_task):
        """Ish faoliyatini olish"""
        employee = await employee_task
        if employee:
            res = await sync_to_async(get_careers)(employee["id"])
            return res.json().get("careers")
        return []

    async def fetch_edu(self, session, employee_task):
        """Ta'lim ma'lumotlarini olish"""
        employee = await employee_task
        if employee:
            res = await sync_to_async(get_edu)(employee["id"])
            return res.json().get("infoeducations")
        return []

    async def fetch_meds(self, session, employee_task):
        """Tibbiy ko'rik ma'lumotlarini olish"""
        employee = await employee_task
        if employee:
            res = await sync_to_async(get_meds)(employee["id"])
            return res.json()
        return {}

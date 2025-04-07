import requests as req
from .models import Settings


def get_setting(key):
    """Sozlamani olish."""
    return Settings.objects.get(key=key).value


def update_setting(key, value):
    """Sozlamani yangilash."""
    Settings.objects.filter(key=key).update(value=value)


def refresh_token():
    """Yangi Exodim tokenni olish va yangilash."""
    response = req.post("https://api-exodim.railway.uz/api/auth/login", data={
        "email": get_setting('exodim_login'),
        "password": get_setting('exodim_password')
    })
    if response.status_code == 200:
        new_token = response.json().get("access_token")
        update_setting('exodim_access_token', new_token)
        return new_token
    raise Exception(f"Failed to refresh token: {response.text}")


def make_request(url, params=None):
    """API so‘rovi, zarur bo‘lsa tokenni yangilaydi."""
    token = get_setting('exodim_access_token') or refresh_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = req.get(url, headers=headers, params=params)
    if response.status_code in [401, 500]:  # Token eskirgan bo‘lsa
        headers["Authorization"] = f"Bearer {refresh_token()}"
        response = req.get(url, headers=headers, params=params)

    return response


def get_employee(pin):
    """PIN bo‘yicha ishchini tekshirish."""
    return make_request("https://api-exodim.railway.uz/api/v2/commands/check-worker", {"pin": pin})


def get_personal(exodim_id):
    """Ishchi shaxsiy ma’lumotlarini olish."""
    return make_request(f"https://api-exodim.railway.uz/api/v2/cadry/personal/{exodim_id}")


def get_careers(exodim_id):
    return make_request(f"https://api-exodim.railway.uz/api/organization/cadry/{exodim_id}/careers")


def get_edu(exodim_id):
    return make_request(f"https://api-exodim.railway.uz/api/v2/cadry/personal-education/{exodim_id}")


def get_meds(exodim_id):
    return make_request(f"https://api-exodim.railway.uz/api/v2/cadry/personal-others/{exodim_id}")
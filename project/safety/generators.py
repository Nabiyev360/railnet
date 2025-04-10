import os
from datetime import datetime
from django.conf import settings
from docxtpl import DocxTemplate


BASE_DIR = settings.BASE_DIR

def name_shorter(full_name):
    parts  = full_name.split()
    parts = parts[:3]
    surname, *others = parts
    initials = " ".join(f"{name[0].upper()}." for name in others)
    return f"{initials} {surname}"


def protocol_generator(request, fullname, position):
    path = os.path.join(BASE_DIR, 'media/files/temp/safety/bayonnoma.docx')
    doc = DocxTemplate(path)
    data = request.POST

    context = {
        'worker_fullname': fullname,
        'short_name': name_shorter(fullname),
        'worker_position': position,
        'today': datetime.today().strftime('%d.%m.%Y'),
        'reason': data.get('reason').lower(),
        'comment': data.get('comment'),
        'punish_type': "________________",       # xayfsan e’lon qilinsin, oylik maoshidan 10% miqdorida jarima ushlab qolinsin.
        'tabel_num': '_____'
    }

    if data.get('coupon'):
        context.update({
            'coupon': f"mehnat muhofazasi bo‘yicha {data.get('coupon')}-sonli ogohlantirish talonini olgan",
        })
    if data.get('comment'):
        context.update({
            'comment': f"Shuningdek {data.get('comment')}."
        })

    doc.render(context)
    filename = f"Bayonnoma {datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.docx"
    relative_path = f"files/generated/safety/{filename}"
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    doc.save(full_path)

    return relative_path
from django.shortcuts import render


def home(request):
    stats = [
        {
            "count": "40+",
            "label": "xidmət sahəsi"  # DƏYİŞDİRİLDİ
        },
        {
            "count": "25+",
            "label": "tamamlanmış layihə" # DƏYİŞDİRİLDİ
        },
        {
            "count": "41+",
            "label": "partnyor şirkət" # DƏYİŞDİRİLDİ
        },
        {
            "count": "94+",
            "label": "müştəri məmnuniyyəti" # DƏYİŞDİRİLDİ
        },
    ]

    services = [
        {
            "title": "Mühasibatlıq xidmətləri",
            "description": "Mühasibat uçotunun qurulması, bərpası, aparılması, mühasibatlıq/vergi hesabatı (ilkin bəyanat) və s."
        },
        {
            "title": "Vergi xidmətləri",
            "description": "Vergi orqanlarında qeydiyyatı (VÖEN alınması), obyekt qeydiyyatının aparılması və s."
        },
        {
            "title": "İnsan Resursları",
            "description": "İnsan resurslarının sənədləşməsi sahəsində məlumat və məsləhət xidmətlərinin göstərilməsi və s."
        },
        {
            "title": "Hüquqi xidmətlərin təsviri",
            "description": "Şirkətin sənədlərinin (nizamnamə, təsisçi qərarı və s.) hazırlanması, müqavilələrin (icra və s.) və s."
        },
        {
            "title": "İKT",
            "description": "IT Texniki dəstək (Help desk) xidmətinin göstərilməsi, Serverlərin quraşdırılması, idarə edilməsi və s."
        },
        {
            "title": "Digər",
            "description": "Maliyyə (kreditor/debitor) analiz sisteminin çəkilişi."
        }
    ]

    context = {
        "stats": stats,
        "services": services
    }
    return render(request, "home.html", context)
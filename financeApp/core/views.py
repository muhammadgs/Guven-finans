from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import KonsultasiyaForm
from .models import Project


def _home_context(form: KonsultasiyaForm | None = None) -> dict:
    stats = [
        {
            "count": "40+",
            "label": "xidmət sahəsi",  # DƏYİŞDİRİLDİ
        },
        {
            "count": "25+",
            "label": "tamamlanmış layihə",  # DƏYİŞDİRİLDİ
        },
        {
            "count": "41+",
            "label": "partnyor şirkət",  # DƏYİŞDİRİLDİ
        },
        {
            "count": "94+",
            "label": "müştəri məmnuniyyəti",  # DƏYİŞDİRİLDİ
        },
    ]

    services = [
        {
            "title": "Mühasibatlıq xidmətləri",
            "description": "Mühasibat uçotunun qurulması, bərpası, aparılması, mühasibatlıq/vergi hesabatı (ilkin bəyanat) və s.",
        },
        {
            "title": "Vergi xidmətləri",
            "description": "Vergi orqanlarında qeydiyyatı (VÖEN alınması), obyekt qeydiyyatının aparılması və s.",
        },
        {
            "title": "İnsan Resursları",
            "description": "İnsan resurslarının sənədləşməsi sahəsində məlumat və məsləhət xidmətlərinin göstərilməsi və s.",
        },
        {
            "title": "Hüquqi xidmətlərin təsviri",
            "description": "Şirkətin sənədlərinin (nizamnamə, təsisçi qərarı və s.) hazırlanması, müqavilələrin (icra və s.) və s.",
        },
        {
            "title": "İKT",
            "description": "IT Texniki dəstək (Help desk) xidmətinin göstərilməsi, Serverlərin quraşdırılması, idarə edilməsi və s.",
        },
        {
            "title": "Digər",
            "description": "Maliyyə (kreditor/debitor) analiz sisteminin çəkilişi.",
        },
    ]

    projects = Project.objects.all()

    return {
        "stats": stats,
        "services": services,
        "form": form or KonsultasiyaForm(),
        "projects": projects,
    }


def home(request):
    context = _home_context()
    return render(request, "home.html", context)


class KonsultasiyaCreateView(FormView):
    form_class = KonsultasiyaForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Müraciətiniz qəbul edildi. Qısa zamanda əlaqə saxlayacağıq.")
        return self.redirect_to_section()

    def form_invalid(self, form):
        context = _home_context(form=form)
        context["show_konsultasiya"] = True
        response = render(self.request, "home.html", context, status=400)
        return response

    def redirect_to_section(self):
        url = reverse("home") + "#konsultasiya"
        return HttpResponseRedirect(url)

from django import forms
from django.core.validators import RegexValidator

from .models import Konsultasiya


BASE_INPUT_CLASSES = (
    "mt-1 block w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 "
    "text-gray-900 shadow-sm transition focus:border-blue-500 focus:outline-none "
    "focus:ring-2 focus:ring-blue-500/50"
)


class KonsultasiyaForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    elaqe_nomresi = forms.CharField(
        label="Əlaqə nömrəsi",
        min_length=10,
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^(?:\+994\d{9}|0\d{9,10})$",
                message="Nömrə +994… və ya 0… ilə başlamalıdır.",
            )
        ],
    )

    ad_sirket = forms.CharField(label="Ad & şirkət adı", min_length=2, max_length=255)
    etrafli = forms.CharField(label="Ətraflı yazın", min_length=5, widget=forms.Textarea)

    class Meta:
        model = Konsultasiya
        fields = ["ad_sirket", "elaqe_nomresi", "xidmet", "etrafli"]
        widgets = {
            "ad_sirket": forms.TextInput(
                attrs={
                    "class": BASE_INPUT_CLASSES,
                    "placeholder": "Adınız və ya şirkət adı",
                    "required": "required",
                }
            ),
            "xidmet": forms.Select(
                attrs={
                    "class": f"{BASE_INPUT_CLASSES} appearance-none",
                    "required": "required",
                }
            ),
            "etrafli": forms.Textarea(
                attrs={
                    "class": f"{BASE_INPUT_CLASSES} resize-none leading-relaxed",
                    "rows": 4,
                    "placeholder": "Tələbinizi ətraflı yazın",
                    "required": "required",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["xidmet"].choices = Konsultasiya.Xidmetler.choices
        self.fields["elaqe_nomresi"].widget.attrs.update(
            {
                "class": BASE_INPUT_CLASSES,
                "placeholder": "+994xxxxxxxxx və ya 0xxxxxxxxx",
                "required": "required",
                "minlength": "10",
            }
        )
        self.fields["ad_sirket"].widget.attrs.setdefault("required", "required")
        self.fields["ad_sirket"].widget.attrs.setdefault("minlength", "2")
        self.fields["etrafli"].widget.attrs.setdefault("required", "required")
        self.fields["etrafli"].widget.attrs.setdefault("minlength", "5")
        self.fields["xidmet"].widget.choices = self.fields["xidmet"].choices

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Formu göndərmək mümkün olmadı.")
        return value


import re

from django import forms

from accounts.forms import COUNTRY_CODES, NUMBER_PATTERN
from .models import Konsultasiya


BASE_INPUT_CLASSES = (
    "mt-1 block w-full rounded-2xl border border-gray-200 bg-white px-4 py-3 "
    "text-gray-900 shadow-sm transition focus:border-blue-500 focus:outline-none "
    "focus:ring-2 focus:ring-blue-500/50"
)


class KonsultasiyaForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    elaqe_nomresi = forms.CharField(required=False, widget=forms.HiddenInput)
    elaqe_prefix = forms.ChoiceField(
        choices=COUNTRY_CODES,
        required=True,
        label="Ölkə kodu",
        widget=forms.Select(
            attrs={
                "class": "block w-full rounded-l-lg border border-gray-300 bg-gray-50 px-3 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            }
        ),
    )
    elaqe_number = forms.CharField(
        required=True,
        label="Mobil nömrə",
        widget=forms.TextInput(
            attrs={
                "class": "mt-0 block w-full rounded-r-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "50 123 45 67 (yalnız rəqəm)",
                "pattern": r"^[0-9\s]+$",
                "inputmode": "numeric",
            }
        ),
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
        self.fields["xidmet"].choices = [
            ("", "Xidmət seçin"),
            *Konsultasiya.Xidmetler.choices,
        ]
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

    def _clean_phone_number(self, field_name: str) -> str:
        value = self.cleaned_data.get(field_name, "").strip()
        if not value:
            raise forms.ValidationError("Nömrə daxil edilməlidir.")
        if not NUMBER_PATTERN.fullmatch(value):
            raise forms.ValidationError("Yalnız rəqəm və boşluq daxil edin.")
        digits_only = re.sub(r"[^0-9]", "", value)
        if not 7 <= len(digits_only) <= 12:
            raise forms.ValidationError("Nömrə 7-12 rəqəm arasında olmalıdır.")
        return value

    def clean_elaqe_number(self) -> str:
        return self._clean_phone_number("elaqe_number")

    def clean(self):
        cleaned_data = super().clean()
        prefix = cleaned_data.get("elaqe_prefix")
        number = cleaned_data.get("elaqe_number", "")
        if prefix and number:
            cleaned_data["elaqe_nomresi"] = f"{prefix}{re.sub(r'[^0-9]', '', number)}"
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        prefix = self.cleaned_data.get("elaqe_prefix")
        number = self.cleaned_data.get("elaqe_number", "")
        if prefix and number:
            instance.elaqe_nomresi = f"{prefix}{re.sub(r'[^0-9]', '', number)}"
        if commit:
            instance.save()
        return instance


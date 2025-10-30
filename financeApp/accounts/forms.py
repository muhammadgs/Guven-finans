import re

from django import forms

from .models import OwnerRegistration

# Yalnız rəqəm və boşluqları yoxlamaq üçün yeni RE
NUMBER_PATTERN = re.compile(r"^[0-9\s]+$")

# Ölkə kodları (genişləndirilə bilər)
COUNTRY_CODES = [
    ("", "Seçin..."),
    ("+994", "+994 (AZ)"),
    ("+90", "+90 (TR)"),
    ("+7", "+7 (RU/KZ)"),
    ("+1", "+1 (US/CA)"),
    ("+44", "+44 (UK)"),
    ("+49", "+49 (DE)"),
    ("+33", "+33 (FR)"),
    ("+39", "+39 (IT)"),
    ("+34", "+34 (ES)"),
    ("+48", "+48 (PL)"),
    ("+380", "+380 (UA)"),
    ("+995", "+995 (GE)"),
    ("+375", "+375 (BY)"),
    ("+98", "+98 (IR)"),
    ("+971", "+971 (AE)"),
    ("+86", "+86 (CN)"),
    ("+91", "+91 (IN)"),
    ("+81", "+81 (JP)"),
    ("+82", "+82 (KR)"),
    ("+31", "+31 (NL)"),
    ("+55", "+55 (BR)"),
    ("+61", "+61 (AU)"),
]


class OwnerRegistrationForm(forms.ModelForm):
    # Yeni sahələri (prefix və number) əlavə edirik
    phone_prefix = forms.ChoiceField(
        choices=COUNTRY_CODES,
        required=True,
        label="Ölkə kodu",
        widget=forms.Select(
            attrs={
                "class": "block w-full rounded-l-lg border border-gray-300 bg-gray-50 px-3 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            }
        ),
    )
    phone_number = forms.CharField(
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

    company_phone_prefix = forms.ChoiceField(
        choices=COUNTRY_CODES,
        required=True,
        label="Ölkə kodu",
        widget=forms.Select(
            attrs={
                "class": "block w-full rounded-l-lg border border-gray-300 bg-gray-50 px-3 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            }
        ),
    )
    company_phone_number = forms.CharField(
        required=True,
        label="Şirkət nömrəsi",
        widget=forms.TextInput(
            attrs={
                "class": "mt-0 block w-full rounded-r-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "12 123 45 67 (yalnız rəqəm)",
                "pattern": r"^[0-9\s]+$",
                "inputmode": "numeric",
            }
        ),
    )

    class Meta:
        model = OwnerRegistration
        # 'phone' və 'company_phone' sahələrini Meta.fields-dən çıxarırıq
        fields = [
            "first_name",
            "last_name",
            # "phone", # Çıxarıldı
            "email",
            "company_name",
            "company_email",
            # "company_phone", # Çıxarıldı
            "company_address",
        ]
        # Vidcetləri yeni sahələrə uyğun yeniləyirik
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Adınızı daxil edin",
                    "required": True,
                    "minlength": 2,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Soyadınızı daxil edin",
                    "required": True,
                    "minlength": 2,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "E-poçt ünvanınızı daxil edin",
                    "required": True,
                }
            ),
            "company_name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Şirkət adını daxil edin",
                    "required": True,
                    "minlength": 2,
                }
            ),
            "company_email": forms.EmailInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Şirkət e-poçtunu daxil edin",
                    "required": True,
                }
            ),
            "company_address": forms.Textarea(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Şirkət ünvanını daxil edin",
                    "rows": 4,
                    "required": True,
                }
            ),
        }

    # Ad sahələri üçün təmizləmə
    def _clean_name_field(self, field_name: str) -> str:
        value = self.cleaned_data.get(field_name, "").strip()
        if len(value) < 2:
            raise forms.ValidationError("Minimum 2 simvol daxil edilməlidir.")
        return value

    def clean_first_name(self) -> str:
        return self._clean_name_field("first_name")

    def clean_last_name(self) -> str:
        return self._clean_name_field("last_name")

    def clean_company_name(self) -> str:
        return self._clean_name_field("company_name")

    # Nömrə sahələri üçün təmizləmə
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

    def clean_phone_number(self) -> str:
        return self._clean_phone_number("phone_number")

    def clean_company_phone_number(self) -> str:
        return self._clean_phone_number("company_phone_number")

    # Email və ünvan təmizləmə
    def clean_email(self) -> str:
        value = self.cleaned_data.get("email", "").strip()
        if not value:
            raise forms.ValidationError("Bu xana məcburidir.")
        return value

    def clean_company_email(self) -> str:
        value = self.cleaned_data.get("company_email", "").strip()
        if not value:
            raise forms.ValidationError("Bu xana məcburidir.")
        return value

    def clean_company_address(self) -> str:
        value = self.cleaned_data.get("company_address", "").strip()
        if not value:
            raise forms.ValidationError("Bu xana məcburidir.")
        return value

    # Save metodunu override edirik ki, prefix və nömrəni birləşdirib bazaya yazaq
    def save(self, commit=True):
        # Əvvəlcə digər sahələri (ad, soyad...) instansa yazmaq üçün
        instance = super().save(commit=False)

        # Prefix və nömrəni təmizlənmiş datadan alırıq
        phone_prefix = self.cleaned_data.get("phone_prefix")
        phone_number = self.cleaned_data.get("phone_number", "").strip().replace(" ", "")

        company_prefix = self.cleaned_data.get("company_phone_prefix")
        company_number = (
            self.cleaned_data.get("company_phone_number", "").strip().replace(" ", "")
        )

        # Birləşdirib modeldəki əsas sahələrə yazırıq
        if phone_prefix and phone_number:
            instance.phone = f"{phone_prefix}{phone_number}"

        if company_prefix and company_number:
            instance.company_phone = f"{company_prefix}{company_number}"

        if commit:
            instance.save()

        return instance
import re

from django import forms

from .models import OwnerRegistration

PHONE_PATTERN = re.compile(r"^[0-9+\-\s]+$")


class OwnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = OwnerRegistration
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "company_name",
            "company_email",
            "company_phone",
            "company_address",
        ]
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
            "phone": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "+994 XX XXX XX XX",
                    "required": True,
                    "pattern": r"^[0-9+\-\s]+$",
                    "inputmode": "tel",
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
            "company_phone": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Şirkət əlaqə nömrəsi",
                    "required": True,
                    "pattern": r"^[0-9+\-\s]+$",
                    "inputmode": "tel",
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

    def _clean_phone_field(self, field_name: str) -> str:
        value = self.cleaned_data.get(field_name, "").strip()
        if not PHONE_PATTERN.fullmatch(value):
            raise forms.ValidationError(
                "Yalnız rəqəm, boşluq, + və - simvollarından istifadə edin."
            )

        digits_only = re.sub(r"[^0-9]", "", value)
        if not 9 <= len(digits_only) <= 15:
            raise forms.ValidationError("Nömrə 9-15 rəqəm arasında olmalıdır.")

        normalized = value.replace(' ', '').replace('-', '')
        if normalized.startswith('+'):
            if not normalized.startswith('+994'):
                raise forms.ValidationError("Nömrə +994 və ya 0 ilə başlamalıdır.")
        elif not normalized.startswith('0'):
            raise forms.ValidationError("Nömrə +994 və ya 0 ilə başlamalıdır.")

        return value

    def clean_phone(self) -> str:
        return self._clean_phone_field("phone")

    def clean_company_phone(self) -> str:
        return self._clean_phone_field("company_phone")

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

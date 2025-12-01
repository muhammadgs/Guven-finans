import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.contrib.auth.models import User
from .models import OwnerRegistration, WorkerRegistration


PHONE_PREFIX_PATTERN = re.compile(r"^(?:\+994|0)")

# Pattern-lər və Ölkə Kodları (Sizin kodunuz olduğu kimi qalır)
NUMBER_PATTERN = re.compile(r"^[0-9\s]+$")
PHONE_ALLOWED_PATTERN = re.compile(r"^[0-9\s+\-]+$")
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


# --- OwnerRegistrationForm DƏYİŞİKLİKLƏRİ ---

class OwnerRegistrationForm(forms.ModelForm):
    # Prefiks sahələri (olduğu kimi qalır)
    phone_prefix = forms.ChoiceField(
        choices=COUNTRY_CODES, required=True, label="Ölkə kodu",
        widget=forms.Select(attrs={
            "class": "block w-24 flex-shrink-0 rounded-l-lg border border-gray-300 bg-gray-50 px-3 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500"})
    )
    phone_number = forms.CharField(
        required=True, label="Mobil nömrə",
        widget=forms.TextInput(attrs={
            "class": "mt-0 block w-full flex-1 rounded-r-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            "placeholder": "50 123 45 67 (yalnız rəqəm)", "pattern": r"^[0-9\s]+$", "inputmode": "numeric"})
    )
    company_phone_prefix = forms.ChoiceField(
        choices=COUNTRY_CODES, required=True, label="Ölkə kodu",
        widget=forms.Select(attrs={
            "class": "block w-24 flex-shrink-0 rounded-l-lg border border-gray-300 bg-gray-50 px-3 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500"})
    )
    company_phone_number = forms.CharField(
        required=True, label="Şirkət nömrəsi",
        widget=forms.TextInput(attrs={
            "class": "mt-0 block w-full flex-1 rounded-r-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            "placeholder": "12 123 45 67 (yalnız rəqəm)", "pattern": r"^[0-9\s]+$", "inputmode": "numeric"})
    )

    # === XƏTANIN SƏBƏBİ BU SAHƏLƏRİN OLMAYIŞIDIR ===
    password = forms.CharField(
        label="Şifrə",
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Şifrənizi daxil edin (minimum 8 simvol)",
            }
        ),
    )
    password_confirm = forms.CharField(
        label="Şifrə təkrarı",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Şifrənizi təkrar daxil edin",
            }
        ),
    )

    class Meta:
        model = OwnerRegistration
        # 'password' buradan silinməlidir, çünki yuxarıda təyin etdik
        fields = [
            "first_name", "last_name", "email",
            "company_name", "company_email", "company_address",
        ]
        labels = {
            "first_name": "Ad",
            "last_name": "Soyad",
            "email": "E-poçt",
            "company_name": "Şirkət adı",
            "company_email": "Şirkət E-poçtu",
            "company_address": "Şirkət Ünvanı",
        }
        # Widget-lər (sizin kodunuzdakı kimi qalır)
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Adınızı daxil edin", "required": True, "minlength": 2}),
            "last_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Soyadınızı daxil edin", "required": True, "minlength": 2}),
            "email": forms.EmailInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "E-poçt ünvanınızı daxil edin", "required": True}),
            "company_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Şirkət adını daxil edin", "required": True, "minlength": 2}),
            "company_email": forms.EmailInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Şirkət e-poçtunu daxil edin", "required": True}),
            "company_address": forms.Textarea(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Şirkət ünvanını daxil edin", "rows": 4, "required": True}),
        }

    # Sizin clean metodlarınız (olduğu kimi qalır)
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

    def _clean_phone_number(self, field_name: str) -> str:
        value = self.cleaned_data.get(field_name, "").strip()
        if not value: raise forms.ValidationError("Nömrə daxil edilməlidir.")
        if not NUMBER_PATTERN.fullmatch(value): raise forms.ValidationError("Yalnız rəqəm və boşluq daxil edin.")
        digits_only = re.sub(r"[^0-9]", "", value)
        if not 7 <= len(digits_only) <= 12: raise forms.ValidationError("Nömrə 7-12 rəqəm arasında olmalıdır.")
        return value

    def clean_phone_number(self) -> str:
        return self._clean_phone_number("phone_number")

    def clean_company_phone_number(self) -> str:
        return self._clean_phone_number("company_phone_number")

    def clean_email(self) -> str:
        value = self.cleaned_data.get("email", "").strip().lower()
        if not value: raise forms.ValidationError("Bu xana məcburidir.")
        if User.objects.filter(email=value).exists() or OwnerRegistration.objects.filter(email=value).exists():
            raise forms.ValidationError("Bu e-poçt artıq istifadə olunub.")
        return value

    def clean_company_email(self) -> str:
        value = self.cleaned_data.get("company_email", "").strip().lower()
        if not value: raise forms.ValidationError("Bu xana məcburidir.")
        if OwnerRegistration.objects.filter(company_email=value).exists():
            raise forms.ValidationError("Bu şirkət e-poçtu artıq istifadə olunub.")
        return value

    def clean_company_address(self) -> str:
        value = self.cleaned_data.get("company_address", "").strip()
        if not value: raise forms.ValidationError("Bu xana məcburidir.")
        return value

    # ŞİFRƏ TƏSDİQİ ƏLAVƏ EDİLDİ
    def clean_password_confirm(self):
        # .get() istifadə edirik ki, KeyError alsaq belə, proqram dayanmasın
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        # Əgər 'password' sahəsi yoxdursa (formda təyin edilməyibsə), .get() None qaytaracaq
        if not password:
            raise forms.ValidationError("Formda 'password' sahəsi təyin edilməyib. (Sistem xətası)")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Şifrələr üst-üstə düşmür.")
        return password_confirm

    # === DÜZGÜN SAVE METODU BUDUR ===
    @transaction.atomic
    def save(self, commit=True):
        # 1. Django User Obyektini yarat
        # Xətanın qarşısını almaq üçün .get() istifadə edirik
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # User modelində 'username' məcburidir, biz email-i həm username, həm email kimi istifadə edirik.
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name")
        )

        # 2. OwnerRegistration (Profil) Obyektini yarat
        instance = super().save(commit=False)
        instance.user = user  # Yaratdığımız User-i bura bağlayırıq
        instance.email = email

        # Prefiks və nömrələri birləşdir (sizin kodunuz)
        phone_prefix = self.cleaned_data.get("phone_prefix")
        phone_number = self.cleaned_data.get("phone_number", "").strip().replace(" ", "")
        company_prefix = self.cleaned_data.get("company_phone_prefix")
        company_number = self.cleaned_data.get("company_phone_number", "").strip().replace(" ", "")

        if phone_prefix and phone_number: instance.phone = f"{phone_prefix}{phone_number}"
        if company_prefix and company_number: instance.company_phone = f"{company_prefix}{company_number}"

        if commit:
            instance.save()  # OwnerRegistration obyektini bazaya yaz

        return instance


# --- Employee registration form ---

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = WorkerRegistration
        fields = ["first_name", "last_name", "phone", "email", "position"]
        labels = {
            "first_name": "Ad",
            "last_name": "Soyad",
            "email": "E-poçt",
            "position": "Vəzifə",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Ad",
                    "minlength": 2,
                    "required": True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Soyad",
                    "minlength": 2,
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Telefon nömrəsi",
                    "required": True,
                    "pattern": r"^(?:\\+994|0)[0-9\\s-]{7,15}$",
                    "inputmode": "tel",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "E-poçt",
                    "required": True,
                }
            ),
            "position": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                    "placeholder": "Vəzifə",
                    "required": True,
                }
            ),
        }

    def _clean_min_length(self, field_name: str) -> str:
        value = self.cleaned_data.get(field_name, "").strip()
        if len(value) < 2:
            raise forms.ValidationError("Minimum 2 simvol daxil edilməlidir.")
        return value

    def clean_first_name(self) -> str:
        return self._clean_min_length("first_name")

    def clean_last_name(self) -> str:
        return self._clean_min_length("last_name")

    def clean_phone(self) -> str:
        value = self.cleaned_data.get("phone", "").strip()
        if not value:
            raise forms.ValidationError("Telefon nömrəsi tələb olunur.")
        if not PHONE_PREFIX_PATTERN.match(value):
            raise forms.ValidationError("Nömrə +994 və ya 0 ilə başlamalıdır.")
        if not PHONE_ALLOWED_PATTERN.fullmatch(value):
            raise forms.ValidationError("Yalnız rəqəm, boşluq, '+' və '-' simvollarından istifadə edin.")
        digits_only = re.sub(r"[^0-9]", "", value)
        if len(digits_only) < 9:
            raise forms.ValidationError("Telefon nömrəsi ən azı 9 rəqəmdən ibarət olmalıdır.")
        return value

    def clean_email(self) -> str:
        value = self.cleaned_data.get("email", "").strip()
        if not value:
            raise forms.ValidationError("E-poçt tələb olunur.")
        return value


# --- WorkerRegistrationForm DƏYİŞİKLİKLƏRİ ---

class WorkerRegistrationForm(forms.ModelForm):
    # ŞİFRƏ SAHƏLƏRİ ƏLAVƏ EDİLDİ
    password = forms.CharField(
        label="Şifrə", required=True, min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            "placeholder": "Şifrənizi daxil edin (minimum 8 simvol)"})
    )
    password_confirm = forms.CharField(
        label="Şifrə təkrarı", required=True,
        widget=forms.PasswordInput(attrs={
            "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
            "placeholder": "Şifrənizi təkrar daxil edin"})
    )

    class Meta:
        model = WorkerRegistration
        fields = ["first_name", "last_name", "phone", "email", "position"]
        labels = {
            "first_name": "Ad",
            "last_name": "Soyad",
            "email": "E-poçt",
            "position": "Vəzifə",
        }
        # Widget-lər (sizin kodunuzdakı kimi qalır)
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Adınızı daxil edin", "required": True, "minlength": 2}),
            "last_name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Soyadınızı daxil edin", "required": True, "minlength": 2}),
            "phone": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "+994 50 123 45 67", "required": True, "pattern": r"^(?:\+994|0)[0-9\s\-]{7,13}$",
                "minlength": 9, "maxlength": 15}),
            "email": forms.EmailInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "E-poçt ünvanınızı daxil edin", "required": True, "type": "email"}),
            "position": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 shadow-sm focus:border-blue-500 focus:ring-blue-500",
                "placeholder": "Vəzifənizi daxil edin", "required": True, "minlength": 2}),
        }

    # Sizin clean metodlarınız (olduğu kimi qalır)
    def _clean_min_length(self, field_name: str) -> str:
        value = self.cleaned_data.get(field_name, "").strip()
        if len(value) < 2: raise forms.ValidationError("Minimum 2 simvol daxil edilməlidir.")
        return value

    def clean_first_name(self) -> str:
        return self._clean_min_length("first_name")

    def clean_last_name(self) -> str:
        return self._clean_min_length("last_name")

    def clean_position(self) -> str:
        return self._clean_min_length("position")

    def clean_phone(self) -> str:
        value = self.cleaned_data.get("phone", "").strip()
        if not value: raise forms.ValidationError("Telefon nömrəsi tələb olunur.")
        if not PHONE_ALLOWED_PATTERN.fullmatch(value): raise forms.ValidationError(
            "Yalnız rəqəm, boşluq, '+' və '-' simvollarından istifadə edin.")
        if not (value.startswith("+994") or value.startswith("0")): raise forms.ValidationError(
            "Nömrə +994 və ya 0 ilə başlamalıdır.")
        digits_only = re.sub(r"[^0-9]", "", value)
        if not 9 <= len(digits_only) <= 15: raise forms.ValidationError("Nömrə 9-15 rəqəm arasında olmalıdır.")
        return value

    def clean_email(self) -> str:
        value = self.cleaned_data.get("email", "").strip().lower()
        if not value: raise forms.ValidationError("E-poçt tələb olunur.")
        if User.objects.filter(email=value).exists() or WorkerRegistration.objects.filter(email=value).exists():
            raise forms.ValidationError("Bu e-poçt artıq istifadə olunub.")
        return value

    # ŞİFRƏ TƏSDİQİ ƏLAVƏ EDİLDİ
    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if not password:
            raise forms.ValidationError("Formda 'password' sahəsi təyin edilməyib. (Sistem xətası)")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Şifrələr üst-üstə düşmür.")
        return password_confirm

    # SAVE METODU TAMAMİLƏ YENİLƏNDİ
    @transaction.atomic
    def save(self, commit=True):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name")
        )

        instance = super().save(commit=False)
        instance.user = user
        instance.email = email

        if commit:
            instance.save()

        return instance


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="E-poçt",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-2.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6",
                "placeholder": "E-poçt ünvanınızı daxil edin",
                "autocomplete": "email",
                "type": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Şifrə",
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-2.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6",
                "placeholder": "Şifrənizi daxil edin",
                "autocomplete": "current-password",
            }
        ),
    )

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.core.models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "الاسم الكامل"}),
            "email": forms.EmailInput(attrs={"placeholder": "البريد الإلكتروني"}),
            "phone": forms.TextInput(attrs={"placeholder": "رقم الهاتف (اختياري)"}),
            "subject": forms.TextInput(attrs={"placeholder": "موضوع الرسالة"}),
            "message": forms.Textarea(attrs={"placeholder": "اكتب رسالتك هنا", "rows": 6}),
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="البريد الإلكتروني",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "name@example.com"}),
    )
    password = forms.CharField(
        label="كلمة المرور",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("full_name", "email")
        labels = {"full_name": "الاسم الكامل", "email": "البريد الإلكتروني"}
        widgets = {"email": forms.EmailInput(attrs={"autocomplete": "email"})}

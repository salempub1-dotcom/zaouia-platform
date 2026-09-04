from django import forms

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

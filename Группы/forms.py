from django import forms
from django.db import models
from .models import IssuedPPE, Employee, StaffLaboratory

# EmployeeForm - xodimlarni qo'shish yoki tahrirlash uchun forma
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee  # Ushbu forma Employee modeliga bog'langan
        fields = ["name", "position", "lab"]  # Superuserlar laboratoriyani tanlashi uchun 'lab' maydoni kiritilgan

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)  # So‘rov obyektini olish (agar mavjud bo‘lsa)
        super().__init__(*args, **kwargs)

        if request:
            if request.user.is_superuser:
                # Agar foydalanuvchi superuser bo'lsa, barcha laboratoriyalarni tanlash imkoniyati beriladi
                self.fields["lab"].queryset = StaffLaboratory.objects.all()
            else:
                # Aks holda, foydalanuvchining bog‘langan laboratoriyasini topamiz
                assigned_lab = StaffLaboratory.objects.filter(
                    manager=request.user
                ).first() or StaffLaboratory.objects.filter(
                    admin_user=request.user
                ).first()

                if assigned_lab:
                    # Foydalanuvchi bog‘langan laboratoriyani avtomatik tanlash
                    self.fields["lab"].initial = assigned_lab
                    # Laboratoriya maydonini tahrirlashni taqiqlash
                    self.fields["lab"].disabled = True


# IssuedPPEForm - xodimlarga berilgan shaxsiy himoya vositalari (PPE) bo‘yicha forma
class IssuedPPEForm(forms.ModelForm):
    class Meta:
        model = IssuedPPE  # Ushbu forma IssuedPPE modeliga bog'langan
        fields = "__all__"  # Barcha maydonlarni shaklga kiritamiz

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)  # So‘rov obyektini olish (agar mavjud bo‘lsa)
        super().__init__(*args, **kwargs)

        if request:
            if request.user.is_superuser:
                return  # Agar foydalanuvchi superuser bo‘lsa, hech qanday cheklov qo‘llanilmaydi

            # Tekshiramiz, foydalanuvchi laboratoriya menejeri yoki administratorimi
            is_manager = StaffLaboratory.objects.filter(manager=request.user).exists()
            is_admin_user = StaffLaboratory.objects.filter(admin_user=request.user).exists()

            if is_manager or is_admin_user:
                # Agar foydalanuvchi laboratoriya menejeri yoki administrator bo‘lsa, u faqat o‘z laboratoriyasidagi xodimlarni ko‘ra oladi
                user_labs = StaffLaboratory.objects.filter(
                    manager=request.user
                ) | StaffLaboratory.objects.filter(
                    admin_user=request.user
                )
                self.fields["employee"].queryset = Employee.objects.filter(lab__in=user_labs)
            else:
                # Aks holda, barcha xodimlar ro‘yxati ko‘rinadi
                self.fields["employee"].queryset = Employee.objects.all()

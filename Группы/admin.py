from django.db import models
from django.db.models import Q
from .models import Employee, PPEItem, IssuedPPE, StaffLaboratory, Region
from .forms import EmployeeForm, IssuedPPEForm
from django.contrib import admin

# Admin panel sarlavhalari
admin.site.site_header = "УАП"  # Sayt sarlavhasi
admin.site.site_title = "Получение и замена средств индивидуальной защиты"  # Sayt nomi
admin.site.index_title = "Добро пожаловать"  # Admin panel bosh sahifasi sarlavhasi

# EmployeeAdmin - Xodimlarni boshqarish uchun admin panel
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm  # Xodimlarni qo'shish/tahrirlash uchun forma
    list_display = ["name", "position", "lab"]  # Jadval ustunlari
    list_filter = ['lab']  # Laboratoriya bo‘yicha filtr
    search_fields = ['name']  # Qidirish uchun maydon

    def get_queryset(self, request):
        """Foydalanuvchi roliga qarab xodimlarni filtrlash."""
        qs = super().get_queryset(request)

        if request.user.is_superuser or not request.user.is_staff:
            return qs  # Superuser va oddiy foydalanuvchilar hamma ma’lumotlarni ko‘radi

        user_labs = StaffLaboratory.objects.filter(Q(manager=request.user) | Q(admin_user=request.user))
        if user_labs.exists():
            return qs.filter(lab__in=user_labs)  # Faqat o‘z laboratoriyasidagi xodimlarni ko‘rsatish

        return qs  # Default: barcha xodimlarni ko‘rsatish

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Superuserlar laboratoriyani tanlashi mumkin, boshqalar tanlay olmaydi."""
        if db_field.name == "lab":
            if request.user.is_superuser:
                kwargs["queryset"] = StaffLaboratory.objects.all()
            else:
                kwargs["queryset"] = StaffLaboratory.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Superuserdan tashqari foydalanuvchilar uchun laboratoriyani avtomatik belgilash."""
        if not request.user.is_superuser:
            assigned_lab = StaffLaboratory.objects.filter(Q(manager=request.user) | Q(admin_user=request.user)).first()
            if assigned_lab:
                obj.lab = assigned_lab  # Laboratoriyani avtomatik belgilash
        super().save_model(request, obj, form, change)

admin.site.register(Employee, EmployeeAdmin)

# IssuedPPEAdmin - Berilgan PPE (shaxsiy himoya vositalari)ni boshqarish
class IssuedPPEAdmin(admin.ModelAdmin):
    form = IssuedPPEForm  # PPE buyumlarini qo‘shish/tahrirlash uchun forma
    list_display = ["employee", "ppe_item", "issued_date", "replacement_date"]  # Jadval ustunlari
    list_filter = ["employee__lab", 'employee__name']
    search_fields = ["employee__name"]

    def get_queryset(self, request):
        """Foydalanuvchi roliga qarab PPE yozuvlarini filtrlash."""
        qs = super().get_queryset(request)

        if request.user.is_superuser or not request.user.is_staff:
            return qs

        user_labs = StaffLaboratory.objects.filter(Q(manager=request.user) | Q(admin_user=request.user))
        if user_labs.exists():
            return qs.filter(employee__lab__in=user_labs)

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Menejerlar va administratorlar faqat o‘z laboratoriyasidagi xodimlarni tanlashi mumkin."""
        if db_field.name == "employee":
            user_labs = StaffLaboratory.objects.filter(Q(manager=request.user) | Q(admin_user=request.user))
            if user_labs.exists():
                kwargs["queryset"] = Employee.objects.filter(lab__in=user_labs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(IssuedPPE, IssuedPPEAdmin)

# StaffLaboratoryAdmin - Laboratoriyalarni boshqarish
@admin.register(StaffLaboratory)
class StaffLaboratoryAdmin(admin.ModelAdmin):
    list_display = ("display_name", "manager", "admin_user", "display_region", "display_number")
    search_fields = ("number", "name")
    list_filter = ("region",)

    @admin.display(description="Номер лаборатории")
    def display_number(self, obj):
        return obj.number

    @admin.display(description="Название лаборатории")
    def display_name(self, obj):
        return obj.name

    @admin.display(description="Территория")
    def display_region(self, obj):
        return obj.region.name if obj.region else "Без территории"

# PPEItemAdmin - PPE buyumlarini boshqarish
@admin.register(PPEItem)
class PPEItemAdmin(admin.ModelAdmin):
    list_display = ("display_name", "display_replacement_period", "display_replacement_type")
    search_fields = ("name",)
    list_filter = ("replacement_period_type",)

    @admin.display(description="Название СИЗ")
    def display_name(self, obj):
        return obj.name

    @admin.display(description="Срок замены")
    def display_replacement_period(self, obj):
        return obj.replacement_period_value if obj.replacement_period_value else "Не указано"

    @admin.display(description="Тип периода")
    def display_replacement_type(self, obj):
        return dict(obj.PERIOD_CHOICES).get(obj.replacement_period_type, "Не указано")

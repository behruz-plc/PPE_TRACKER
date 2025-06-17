from django.db import models
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User


class Region(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name="Название территории")

    class Meta:
        verbose_name = "Территория"
        verbose_name_plural = "Территории"

    def __str__(self):
        return self.name


class StaffLaboratory(models.Model):
    number = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name="Номер лаборатории")
    name = models.CharField(max_length=200, unique=True, verbose_name="Название лаборатории")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Территория")
    manager = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="managed_labs", null=True, blank=True,
                                   verbose_name="Менеджер")
    admin_user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="admin_labs", null=True, blank=True,
                                      verbose_name="для Работники")

    class Meta:
        verbose_name = "Лаборатория"
        verbose_name_plural = "Лаборатории"

    def __str__(self):
        return f"{self.name} ({self.region.name if self.region else 'Без территории'})"


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="ФИО")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Должность")
    lab = models.ForeignKey(StaffLaboratory, on_delete=models.SET_NULL, null=True, blank=True,
                            verbose_name="Лаборатория")

    class Meta:
        verbose_name = "работник"
        verbose_name_plural = "работники"

    def __str__(self):
        return f"{self.name} - {self.position if self.position else '------'} ({self.lab.name if self.lab else '-------'})"


class PPEItem(models.Model):
    PERIOD_CHOICES = [
        ("days", "Дни"),
        ("months", "Месяцы"),
        ("years", "Годы"),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Название СИЗ")
    replacement_period_value = models.IntegerField(verbose_name="Период замены", null=True, blank=True)
    replacement_period_type = models.CharField(
        max_length=10, choices=PERIOD_CHOICES, default="months", verbose_name="Тип периода замены"
    )

    class Meta:
        verbose_name = "Средств индивидуальной защиты и проверка знаний"
        verbose_name_plural = "Средств индивидуальной защиты и проверка знаний"

    def __str__(self):
        return self.name


class IssuedPPE(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Работник (ФИО)")
    ppe_item = models.ForeignKey(PPEItem, on_delete=models.CASCADE, verbose_name="СИЗ")
    issued_date = models.DateField(default=now, verbose_name="Дата последней замены")
    replacement_date = models.DateField(editable=False, verbose_name="Следующая дата замены")

    class Meta:
        verbose_name = "Выданные СИЗ"
        verbose_name_plural = "Выданные СИЗ"

    def save(self, *args, **kwargs):
        """Calculate replacement date based on PPE replacement period"""
        if self.ppe_item.replacement_period_value:
            if self.ppe_item.replacement_period_type == "days":
                self.replacement_date = self.issued_date + relativedelta(days=self.ppe_item.replacement_period_value)
            elif self.ppe_item.replacement_period_type == "months":
                self.replacement_date = self.issued_date + relativedelta(months=self.ppe_item.replacement_period_value)
            elif self.ppe_item.replacement_period_type == "years":
                self.replacement_date = self.issued_date + relativedelta(years=self.ppe_item.replacement_period_value)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.ppe_item.name} (Следующая замена: {self.replacement_date})"

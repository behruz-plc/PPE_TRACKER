from datetime import timedelta
from django.http import JsonResponse
from django.utils.timezone import now
from django.conf import settings
from .models import IssuedPPE, StaffLaboratory
from django.shortcuts import render


def notifications_view(request):
    today = now().date()
    alert_days = getattr(settings, "PPE_ALERT_DAYS", 30)  # Configurable via settings.py

    # Get the user's assigned laboratory
    user_lab = StaffLaboratory.objects.filter(manager=request.user).first() or StaffLaboratory.objects.filter(
        admin_user=request.user).first()

    # Superusers see all notifications; managers and admin_users see only their lab's employees
    if request.user.is_superuser or user_lab is None:
        upcoming_replacements = IssuedPPE.objects.filter(
            replacement_date__lte=today + timedelta(days=alert_days)
        ).order_by('replacement_date')
    else:
        upcoming_replacements = IssuedPPE.objects.filter(
            employee__lab=user_lab,
            replacement_date__lte=today + timedelta(days=alert_days)
        ).order_by('replacement_date')

    return render(request, 'notifications.html', {'upcoming_replacements': upcoming_replacements})


def get_notification_count(request):
    """Returns the count of employees needing PPE replacement soon, filtered by laboratory manager or admin_user."""
    today = now().date()
    alert_days = 30  # Changeable in settings

    # Get the user's assigned laboratory
    user_lab = StaffLaboratory.objects.filter(manager=request.user).first() or StaffLaboratory.objects.filter(
        admin_user=request.user).first()

    # Superusers see all notifications; managers and admin_users see only their lab's employees
    if request.user.is_superuser or user_lab is None:
        count = IssuedPPE.objects.filter(replacement_date__lte=today + timedelta(days=alert_days)).count()
    else:
        count = IssuedPPE.objects.filter(
            employee__lab=user_lab,
            replacement_date__lte=today + timedelta(days=alert_days)
        ).count()

    return JsonResponse({"count": count})

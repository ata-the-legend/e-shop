from django.utils import timezone
from apps.accounts.models import OtpCode
from celery import shared_task


@shared_task
def remove_expired_otp_codes_task():
    expired_time = timezone.now() - timezone.timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()
from typing import Any
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from apps.accounts.models import OtpCode


class Command(BaseCommand):
    help = 'Remove all expired otp codes.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        expired_time = datetime.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('All expired otp codes removed.')

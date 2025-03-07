from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
import random
import string
from django.utils import timezone


class ShortURL(models.Model):
    original_url = models.URLField(max_length=500)
    current_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    visits = models.IntegerField(default=0)
    redirect_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"

    def generate_short_code(self):
        """Generate a random short code"""
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=6))
            if not ShortURL.objects.filter(short_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()

        # If this is a new URL, set current_url to original_url
        if not self.pk:
            self.current_url = self.original_url

        # Generate QR code only if it doesn't exist or if current_url has changed
        if not self.qr_code or self.current_url != self.original_url:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.current_url)
            qr.make(fit=True)

            # Create QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code.save(f'qr_{self.short_code}.png', File(buffer), save=False)

        super().save(*args, **kwargs)

    def update_url(self, new_url):
        """Update the current URL while maintaining the short code and QR code"""
        self.current_url = new_url
        self.last_updated = timezone.now()
        self.save()

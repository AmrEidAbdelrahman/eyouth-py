from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from course_manager.models.certificate import Certificate
import os

from course_manager.services.certificate_services import CertificateSeriveces


@receiver(post_save, sender=Certificate)
def create_certificate(sender, instance, created, **kwargs):
    if created:
        CertificateSeriveces.generate_certificate(instance) 

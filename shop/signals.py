from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductImage


@receiver(post_save, sender=Product)
def add_default_image(sender, instance, created, **kwargs):
    if created and not instance.image.exists():
        default_image = ProductImage(product=instance, image='avatars/no_pic.png')
        default_image.save()

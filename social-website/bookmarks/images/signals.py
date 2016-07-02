from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

# We're subscribing to changes in ManyToMany field (users_like)
# The ".though" part:
#   From Django docs: The intermediate model class describing the ManyToManyField. 
#     This class is automatically created when a many-to-many field is defined; you can 
#     access it using the through attribute on the many-to-many field.
#     (This is the description of the sender field) 
#     Source: https://docs.djangoproject.com/en/1.9/ref/signals/#m2m-changed

@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    print("Total likes: " + str(instance.total_likes))
    instance.save()

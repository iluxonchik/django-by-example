from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Custom manager
class PublishedManager(models.Manager):
    """
    Returns the QuerySet to be executed.
    """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=published)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add -> date saved automatically when creating an object
    updated = models.DateTimeField(auto_now=True) # auto_now -> date updated automatically when saving an object
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    objects = models.Manager() # the default manager
    published = PublishedManager() # our custum manager
    
    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
        
    
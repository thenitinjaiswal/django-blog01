from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager  # ADD THIS LINE

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    
    # NEW: SEO meta description
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        help_text='Brief description for search engines (max 160 characters)'
    )
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    views = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_related_posts(self, count=3):
        related = Post.objects.filter(
            status='published',
            categories__in=self.categories.all()
        ).exclude(id=self.id).distinct()[:count]
        return related
    
    # NEW: Auto-generate meta description if empty
    def get_meta_description(self):
        """Get meta description or generate from body."""
        if self.meta_description:
            return self.meta_description
        # Generate from first 150 chars of body
        return self.body[:150] + '...' if len(self.body) > 150 else self.body


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True) # Optional, for cleaner URLs

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    expected_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Enter 0 for free/swap")
    image = models.ImageField(upload_to='item_images/', blank=False, null=False) # Make image required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True) # Optional: Track if item is still available

    def __str__(self):
        return f"{self.name} by {self.owner.username}"

    def get_absolute_url(self):
        # Provides a canonical URL for an item instance
        return reverse('item_detail', kwargs={'pk': self.pk})
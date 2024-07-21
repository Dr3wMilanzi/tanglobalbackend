from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


class UpdateType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=False, null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            count = 1
            slug = self.slug
            while UpdateType.objects.filter(slug=slug).exists():
                slug = f"{self.slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Update Type"
        verbose_name_plural = "Update Types"


class Update(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=False, null=True, unique=True, editable=False)
    update_type = models.ForeignKey(UpdateType, on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            count = 1
            slug = self.slug
            while Update.objects.filter(slug=slug).exists():
                slug = f"{self.slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def approve(self):
        self.is_approved = True
        self.save()

    class Meta:
        verbose_name = "Update"
        verbose_name_plural = "Updates"


class SelectedUpdatesByUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    update_type = models.ForeignKey(UpdateType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'update_type')
        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscriptions"

    def __str__(self):
        return f"{self.user.email} subscribes to {self.update_type}"


@receiver(post_save, sender=Update)
def send_update_email(sender, instance, created, **kwargs):
    if created:
        subscribed_users = SelectedUpdatesByUser.objects.filter(update_type=instance.update_type)
        for subscription in subscribed_users:
            user_email = subscription.user.email
            send_mail(
                'New Update Available',
                f'An update of type "{instance.update_type.name}" has been created:\n\n{instance.content}',
                'your@example.com',  # Replace with your email address
                [user_email],
                fail_silently=False,
            )


class UpdateView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    update = models.ForeignKey(Update, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'update')
        verbose_name = "Update View"
        verbose_name_plural = "Update Views"

    def __str__(self):
        return f"{self.user.username} viewed {self.update.name} at {self.viewed_at}"

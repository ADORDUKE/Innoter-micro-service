from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='pages')
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    # Post can link to other post(replay)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post {self.id} on {self.page.name}"

# Intermediate tables for likes and followers.
# As stated in the ТЗ: “intermediary tables will include only one foreign key...”
# The second key is simply the user ID from another service.

class Follower(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='followers')
    user_id = models.CharField(max_length=255)

    class Meta:
        # One user cannot subscribe the same page twice
        unique_together = ('page', 'user_id')

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user_id = models.CharField(max_length=255)

    class Meta:
        unique_together = ('post', 'user_id')
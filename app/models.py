from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostManager(models.Manager):
    def add_like(self, post):
        post.likes += 1
        post.save()
        return post

    def remove_like(self, post):
        post.likes -= 1
        post.save()
        return post

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='posts/')
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostManager()

    def __str__(self):
        return self.title

class PostInstance(models.Model):
    STATUS_CHOICES = (
        ('a', 'Available'),
        ('na', 'Not Available'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.name

class Answer(models.Model):
    text = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Answer by {self.author.name} on {self.post.title}'
    class Meta:
        ordering = ['-created_at']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Rating(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Rating {self.value} by {self.user} for {self.post}"




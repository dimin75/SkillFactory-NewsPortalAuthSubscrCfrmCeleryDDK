from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        result = 0
        l_user = self.user

        post_list = Post.objects.filter(author=self, post_type=Post.article)
        # pass
        # суммарный рейтинг каждой статьи автора умножается на 3
        post_rating_list = post_list.values("rating")
        result = 3 * (sum(item["rating"] for item in post_rating_list))

        # суммарный рейтинг всех комментариев автора
        comment_rating_list = Comment.objects.filter(user=l_user).values("rating")
        result += sum(item["rating"] for item in comment_rating_list)

        # суммарный рейтинг всех комментариев к статьям автора
        for post in post_list:
            comment_in_post = Comment.objects.filter(post=post).values("rating")
            result += sum(item["rating"] for item in comment_in_post)

        self.rating = result
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, through="CategorySubscribers")

    def __str__(self):
        return self.name

    @property
    def is_subscribed(self):
        return CategorySubscribers.objects.filter(category=self.pk).exists()

class CategorySubscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    article = "AR"
    news = "NW"
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    # author = models.ForeignKey(Author,
    #                            on_delete=models.CASCADE,
    #                            related_name='news_list')
    post_type_choices = [(article, 'Статья'), (news, 'Новость')]
    post_type = models.CharField(max_length=2, choices=post_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
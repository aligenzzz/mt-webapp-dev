import datetime

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

phone_regex = RegexValidator(
        regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="Phone number must be in the format: '+375 (29) XXX-XX-XX'"
    )


class Country(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"

    def __str__(self):
        return self.name


class AnimalClass(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "AnimalClass"
        verbose_name_plural = "AnimalClasses"

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000, default="")
    requirements = models.CharField(max_length=1000, default="")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.name


class Fodder(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Fodder"
        verbose_name_plural = "Fodders"

    def __str__(self):
        return self.name


class Placement(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    basin = models.BooleanField()
    area = models.FloatField()

    class Meta:
        ordering = ['name', 'number']
        verbose_name = "Placement"
        verbose_name_plural = "Placements"

    def __str__(self):
        return f'{self.name} {self.number}'


class Staffer(models.Model):
    name = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, validators=[phone_regex], default='+375 (29) XXX-XX-XX')
    username = models.CharField(max_length=30, default='')
    photo = models.URLField(default="https://i.pinimg.com/originals/eb/b4/39/ebb439b95577b6289fb1659635eed377.png")

    class Meta:
        verbose_name = "Staffer"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f'{self.post} {self.name}'


class Animal(models.Model):
    name = models.CharField(max_length=30)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True, blank=True)
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.SET_NULL, null=True, blank=True)
    staffer = models.ForeignKey(Staffer, on_delete=models.SET_NULL, null=True, blank=True, related_name='animals')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    placement = models.ForeignKey(Placement, on_delete=models.PROTECT, null=True, blank=True, related_name='animals')
    fodder = models.ForeignKey(Fodder, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.URLField(default='')
    info = models.TextField(default='')
    daily_feed = models.FloatField(default=0)

    class Meta:
        ordering = ["admission_date"]
        verbose_name = "Animal"
        verbose_name_plural = "Animals"

    def __str__(self):
        return f'{self.species} {self.name}'


class Client(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, validators=[phone_regex], default='+375 (29) XXX-XX-XX')
    username = models.CharField(max_length=30, default='')

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f'{self.username} ({self.name})'


class Vacancy(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=False, blank=False)
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return f'Vacancy on {self.post.name}'


class Question(models.Model):
    question = models.CharField(max_length=1000, null=False, blank=False)
    answer = models.CharField(max_length=1000, null=True, blank=False)
    date = models.DateField(null=False, blank=False, default=datetime.date.today())

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f'Question #{self.id}'


class Review(models.Model):
    content = models.CharField(max_length=1000, blank=False, null=False)
    date = models.DateField(null=False, blank=False, default=datetime.date.today())
    username = models.CharField(max_length=30, blank=False, null=False)
    rating = models.PositiveIntegerField(default=0, validators=[
            MinValueValidator(0, message="The rating cannot be < 0"),
            MaxValueValidator(10, message="The rating cannot be > 0"),
        ])

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f'Review #{self.id}'


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=1000, blank=False, null=False)
    image = models.URLField()
    date = models.DateField(null=False, blank=False, default=datetime.date.today())
    content = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return f'Article #{self.id}'


class Coupon(models.Model):
    discount = models.PositiveIntegerField(default=0, null=False, blank=False)
    description = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f'Coupon #{self.id}'




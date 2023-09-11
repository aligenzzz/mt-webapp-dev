from django.contrib import admin
from .models import Animal, AnimalClass, Staffer, Post, Placement, Species, Country, Fodder, \
                    Client, Vacancy, Question, Review, Article, Coupon


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'animal_class',
                    'admission_date', 'birth_date', 'fodder', 'daily_feed')
    list_filter = ('admission_date', 'daily_feed')
    search_fields = ['^name', '^species__name', '^animal_class__name']


@admin.register(Staffer)
class StafferAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'username', 'display_animals_count')
    list_filter = ('post', )

    def display_animals_count(self, obj):
        return obj.animals.count()

    display_animals_count.short_description = 'Animals count'


@admin.register(AnimalClass)
class AnimalClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_animals_count')

    def display_animals_count(self, obj):
        return Animal.objects.filter(animal_class=obj).count()

    display_animals_count.short_description = 'Animals count'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_staffer_count')

    def display_staffer_count(self, obj):
        return Staffer.objects.filter(post=obj).count()

    display_staffer_count.short_description = 'Staffer count'


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'basin', 'area',
                    'display_animals_count')
    search_fields = ['^name']

    def display_animals_count(self, obj):
        return Animal.objects.filter(placement=obj).count()

    display_animals_count.short_description = 'Animals count'


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_animals_count')

    def display_animals_count(self, obj):
        return Animal.objects.filter(species=obj).count()

    display_animals_count.short_description = 'Animals count'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_animals_count')

    def display_animals_count(self, obj):
        return Animal.objects.filter(country=obj).count()

    display_animals_count.short_description = 'Animals count'


@admin.register(Fodder)
class FodderAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_animals_count',
                    'display_general_daily_feed')

    def display_animals_count(self, obj):
        return Animal.objects.filter(fodder=obj).count()

    def display_general_daily_feed(self, obj):
        animals = Animal.objects.filter(fodder=obj)

        count = 0
        for animal in animals:
            count += animal.daily_feed

        return count

    display_animals_count.short_description = 'Animals count'
    display_general_daily_feed.short_description = 'General daily feed'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass

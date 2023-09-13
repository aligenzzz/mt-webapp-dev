from django.contrib.auth import login
from django.core.validators import RegexValidator
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from .models import Animal, Placement, Staffer, Fodder, Vacancy, Review, Question, Article, Coupon, Client
from django.http import Http404, HttpResponseServerError
import requests
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from plotly.graph_objects import Bar, Layout, Figure
import logging
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


logger = logging.getLogger(__name__)


class HomeView(View):
    @staticmethod
    def get(request):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        image_url = response.json()['message']

        response = requests.get('https://catfact.ninja/fact')
        fact = response.json()['fact']

        latest_article = Article.objects.latest('date')

        context = {
            'image_url': image_url,
            'fact': fact,
            'latest_article': latest_article,
        }

        return render(request, 'main/index.html', context)


class AnimalSearchForm(forms.Form):
    search_query = forms.CharField(max_length=30, required=False)


class AnimalListView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(name__istartswith=search_query) | \
                       queryset.filter(species__name__istartswith=search_query) | \
                       queryset.filter(animal_class__name__istartswith=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AnimalSearchForm(self.request.GET)
        return context


class AnimalDetailsView(View):
    @staticmethod
    def get(request, id):
        try:
            animal = Animal.objects.get(id=id)
        except Animal.DoesNotExist:
            raise Http404("Animal doesn't exist :(")

        return render(
            request,
            'main/animal_detail.html',
            context={'animal': animal, }
        )


class PlacementSearchForm(forms.Form):
    search_query = forms.CharField(max_length=30, required=False)


class PlacementListView(generic.ListView):
    model = Placement
    context_object_name = 'placement_list'
    template_name = 'main/placements.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(name__istartswith=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AnimalSearchForm(self.request.GET)
        return context


class PlacementDetailsView(View):
    @staticmethod
    def get(request, id):
        try:
            placement = Placement.objects.get(id=id)
        except Placement.DoesNotExist:
            raise Http404("Placement doesn't exist :(")

        return render(
            request,
            'main/placement_detail.html',
            context={'placement': placement, }
        )


class PlacementAnimalsView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        id = self.kwargs['id']
        placement = Placement.objects.get(id=id)
        return Animal.objects.filter(placement=placement)


class StafferListView(generic.ListView):
    model = Staffer
    context_object_name = 'staff_list'
    template_name = 'main/staff.html'


class StafferDetailsView(View):
    @staticmethod
    def get(request, id):
        try:
            staffer = Staffer.objects.get(id=id)
        except Staffer.DoesNotExist:
            raise Http404("Staffer doesn't exist :(")

        user = User.objects.filter(username=staffer.username).first()

        return render(
            request,
            'main/staffer_detail.html',
            context={'staffer': staffer, 'email': user.email, }
        )


class StafferAnimalsView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        id = self.kwargs['id']
        staffer = Staffer.objects.get(id=id)
        return Animal.objects.filter(staffer=staffer)


class StafferPlacementsView(generic.ListView):
    model = Placement
    context_object_name = 'placement_list'
    template_name = 'main/placements.html'

    def get_queryset(self):
        id = self.kwargs['id']
        staffer = Staffer.objects.get(id=id)
        return Placement.objects.filter(animals__in=staffer.animals.all()).distinct()


@method_decorator(login_required, name='dispatch')
class PersonalAccountView(View):
    @staticmethod
    def get(request):
        return render(
            request,
            'main/personal.html',
        )


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    @staticmethod
    def get(request):

        if not Client.objects.filter(username=request.user.username).exists():
            try:
                staffer = Staffer.objects.get(username=request.user.username)
            except Staffer.DoesNotExist:
                raise Http404("Staffer doesn't exist :(")

            return render(
                request,
                'main/staffer_detail.html',
                context={'staffer': staffer,
                         'email': request.user.email, }
            )
        else:
            try:
                client = Client.objects.get(username=request.user.username)
            except Client.DoesNotExist:
                raise Http404("Client doesn't exist :(")

            return render(
                request,
                'main/client_detail.html',
                context={'client': client,
                         'email': request.user.email, }
            )


@method_decorator(login_required, name='dispatch')
class UserAnimalsView(generic.ListView):
    model = Animal
    context_object_name = 'animal_list'
    template_name = 'main/animals.html'

    def get_queryset(self):
        staffer = Staffer.objects.get(username=self.request.user.username)
        return Animal.objects.filter(staffer=staffer)


@method_decorator(login_required, name='dispatch')
class UserPlacementsView(generic.ListView):
    model = Placement
    context_object_name = 'placement_list'
    template_name = 'main/placements.html'

    def get_queryset(self):
        staffer = Staffer.objects.get(username=self.request.user.username)
        return Placement.objects.filter(animals__in=staffer.animals.all()).distinct()


class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


@method_decorator(login_required, name='dispatch')
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountUpdateForm
    template_name = 'main/user_form.html'
    success_url = reverse_lazy('personal_account')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        try:
            response = super().form_valid(form)

            logger.info(f'User {self.request.user.username} was updated successfully.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except Exception:
            logger.error(f'Failed to update user {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class AnimalCreate(CreateView):
    model = Animal
    fields = ['name', 'species', 'animal_class', 'country', 'placement', 'fodder',
              'admission_date', 'birth_date', 'image', 'info', 'daily_feed']
    success_url = reverse_lazy('user_animals')

    def form_valid(self, form):
        form.instance.staffer = Staffer.objects.filter(username=self.request.user.username).first()

        if form.cleaned_data['daily_feed'] <= 0:
            form.add_error(None, 'Animal with daily_feed <= 0.')
            logger.error(f'Failed to create animal by {self.request.user.username}!')
            return self.form_invalid(form)

        date1 = form.cleaned_data['admission_date']
        date2 = form.cleaned_data['birth_date']

        if date1 < date2:
            form.add_error(None, 'Animal with dates diff < 0.')
            logger.error(f'Failed to create animal by {self.request.user.username}!')
            return self.form_invalid(form)

        try:
            response = super().form_valid(form)

            logger.info(f'Animal was created successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except Exception:
            logger.error(f'Failed to create animal by {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class AnimalUpdate(UpdateView):
    model = Animal
    fields = ['placement', 'image', 'info', 'fodder', 'daily_feed']
    success_url = reverse_lazy('user_animals')

    def form_valid(self, form):
        if form.cleaned_data['daily_feed'] <= 0:
            form.add_error(None, 'Animal with daily_feed <= 0.')
            logger.error(f'Failed to update animal by {self.request.user.username}!')
            return self.form_invalid(form)

        try:
            response = super().form_valid(form)

            logger.info(f'Animal was updated successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except Exception:
            logger.error(f'Failed to update animal by {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class AnimalDelete(DeleteView):
    model = Animal
    success_url = reverse_lazy('user_animals')

    def form_valid(self, form):
        try:
            response = super(AnimalDelete, self).form_valid(form)

            logger.info(f'Animal was deleted successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except Exception:
            logger.error(f'Failed to delete animal by {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class PlacementCreate(CreateView):
    model = Placement
    fields = ['name', 'number', 'basin', 'area']
    success_url = reverse_lazy('user_placements')

    def form_valid(self, form):
        if Placement.objects.filter(name=form.cleaned_data['name'], number=form.cleaned_data['number']).exists():
            form.add_error(None, 'Placement with the same name and number already exists.')
            logger.error(f'Failed to create placement by {self.request.user.username}!')
            return self.form_invalid(form)

        if form.cleaned_data['area'] <= 0:
            form.add_error(None, 'Placement with area <= 0.')
            logger.error(f'Failed to create placement by {self.request.user.username}!')
            return self.form_invalid(form)

        try:
            response = super().form_valid(form)

            logger.info(f'Placement was created successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except Exception:
            logger.error(f'Failed to create placement by {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class PlacementUpdate(UpdateView):
    model = Placement
    fields = ['basin', 'area']
    success_url = reverse_lazy('user_placements')

    def form_valid(self, form):
        if form.cleaned_data['area'] <= 0:
            form.add_error(None, 'Placement with area <= 0.')
            logger.error(f'Failed to update placement by {self.request.user.username}!')
            return self.form_invalid(form)

        try:
            response = super().form_valid(form)

            logger.info(f'Placement was updated successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except Exception:
            logger.error(f'Failed to update placement by {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class PlacementDelete(DeleteView):
    model = Placement
    success_url = reverse_lazy('user_placements')

    def form_valid(self, form):
        try:
            response = super(PlacementDelete, self).form_valid(form)

            logger.info(f'Placement was deleted successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return response
        except ProtectedError:
            return HttpResponseServerError("You can't do this!!!")
        except Exception:
            logger.error(f'Failed to delete placement by {self.request.user.username}!')
            raise


@method_decorator(login_required, name='dispatch')
class DiagramView(View):
    @staticmethod
    def get(request):
        fodders = Fodder.objects.all()
        fodder_types = list(Fodder.objects.values_list('name', flat=True))
        general_daily_feeds = []

        for fodder in fodders:
            animals = Animal.objects.filter(fodder=fodder)

            count = 0
            for animal in animals:
                count += animal.daily_feed

            general_daily_feeds.append(count)

        data = Bar(x=fodder_types, y=general_daily_feeds,
                   marker=dict(color=['pink', 'gray', 'white']))
        layout = Layout(title='Fodders and their general daily feed',
                        xaxis=dict(title='fodders'),
                        yaxis=dict(title='general daily feed'))
        fig = Figure(data=data, layout=layout)
        plot_div = fig.to_html(full_html=False)

        return render(
            request,
            'main/diagram.html',
            context={'plot_div': plot_div, }
        )


@method_decorator(login_required, name='dispatch')
class StaticInfoView(View):
    @staticmethod
    def get(request):
        animals_count = Animal.objects.all().count()
        placements_count = Placement.objects.all().count()
        staff_count = Staffer.objects.all().count()
        animal = Animal.objects.latest('admission_date')

        fodders = Fodder.objects.all()
        general_daily_feeds = []
        for fodder in fodders:
            animals = Animal.objects.filter(fodder=fodder)

            count = 0
            for animal in animals:
                count += animal.daily_feed

            general_daily_feeds.append((fodder.name, count))
        sorted_data = sorted(general_daily_feeds, key=lambda x: x[1], reverse=True)
        fodder = sorted_data[0][0]

        context = {
            'animals_count': animals_count,
            'placements_count': placements_count,
            'staff_count': staff_count,
            'animal': animal,
            'fodder_name': fodder
        }

        return render(
            request,
            'main/static_info.html',
            context
        )


def formatted_datetime():
    current_datetime = datetime.now()
    result = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    return str(result)


class AboutUsView(View):
    @staticmethod
    def get(request):
        with open('./static/txt/basic_information.txt') as file:
            basic_information = file.read()
        with open('./static/txt/our_history.txt') as file:
            our_history = file.read()

        context = {
            'basic_information': basic_information,
            'our_history': our_history,
        }

        return render(
            request,
            'main/about_us.html',
            context
        )


class VacancyListView(generic.ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'main/vacancies.html'


class QuestionListView(generic.ListView):
    model = Question
    context_object_name = 'question_list'
    template_name = 'main/questions.html'


class ReviewListView(generic.ListView):
    model = Review
    context_object_name = 'review_list'
    template_name = 'main/reviews.html'


class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'main/articles.html'


class ArticleView(View):
    @staticmethod
    def get(request, id):
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            raise Http404("Article doesn't exist :(")

        with open('./static/txt/' + article.content) as file:
            content = file.read()

        return render(
            request,
            'main/article.html',
            context={'article': article, 'content': content}
        )


class CouponListView(generic.ListView):
    model = Coupon
    context_object_name = 'coupon_list'
    template_name = 'main/coupons.html'


class PrivacyPolicyView(View):
    @staticmethod
    def get(request):
        with open('./static/txt/privacy_policy.txt') as file:
            content = file.read()

        context = {
            'content': content,
        }

        return render(
            request,
            'main/privacy_policy.html',
            context
        )


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
                message='Invalid phone number.'
            )
        ],
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            logger.info(f'New user {request.POST.get("username")} was added.')
            client = Client.objects.create(username=request.POST.get('username'),
                                           first_name=request.POST.get('first_name'),
                                           last_name=request.POST.get('last_name'),
                                           address=request.POST.get('address'),
                                           phone_number=request.POST.get('phone_number'))
            client.save()

            return redirect('home')
    else:
        logger.info(f'Invalid data in the registration form.')
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


class ReviewCreate(CreateView):
    model = Review
    fields = ['rating', 'content']
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        try:
            current_datetime = timezone.now()

            review = form.save(commit=False)
            review.date = current_datetime
            review.username = self.request.user.username
            review.save()

            logger.info(f'Placement was created successfully by {self.request.user.username}.')
            self.request.session['last_change'] = formatted_datetime()

            return super().form_valid(form)
        except Exception:
            logger.error(f'Failed to create review by {self.request.user.username}!')
            raise


class HTMLView(View):
    @staticmethod
    def get(request):
        return render(
            request,
            'main/_html.html'
        )

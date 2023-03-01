import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from app.recipes.models import Recipe
from utils.recipes.pagination import make_pagination

from .forms import LoginForm, RegisterForm
from .forms.recipe_form import AuthorRecipeForm

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data') or None
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in')

        del (request.session['register_form_data'])

    return redirect('authors:login')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid Credentials')
    else:
        messages.error(request, 'Invalid username or passwordd')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False, author=request.user).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'authors/pages/dashboard.html', {
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        is_published=False, author=request.user, pk=id,)
    if not recipe:
        return Http404()

    form = AuthorRecipeForm(data=request.POST or None,
                            files=request.FILES or None, instance=recipe,)

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi atualizada com sucesso')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard_recipe.html', {
        'form': form
    })

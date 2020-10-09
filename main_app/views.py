from django.shortcuts import render, redirect
from .models import Bunny, Toy, Bunny_Breed
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def bunnies_index(request):
  bunnies = Bunny.objects.filter(user=request.user)
  return render(request, 'bunnies/index.html', { 'bunnies': bunnies })

def bunnies_detail(request, bunny_id):
  bunny = Bunny.objects.get(id=bunny_id)
  toys_bunny_doesnt_have = Toy.objects.exclude(id__in = bunny.toys.all().values_list('id'))
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()
  return render(request, 'bunnies/detail.html', {
    'bunny': bunny, 'feeding_form': feeding_form,
    'toys': toys_bunny_doesnt_have
  })

def add_feeding(request, bunny_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.bunny_id = bunny_id
    new_feeding.save()
  return redirect('detail', bunny_id=bunny_id)

class BunnyCreate(LoginRequiredMixin, CreateView):
  model = Bunny
  fields = ['name', 'breed', 'description', 'age']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class BunnyUpdate(LoginRequiredMixin, UpdateView):
  model = Bunny
  fields = ['breed', 'description', 'age']

class BunnyDelete(LoginRequiredMixin, DeleteView):
  model = Bunny
  success_url = '/bunnies/'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, bunny_id, toy_id):
  Bunny.objects.get(id=bunny_id).toys.add(toy_id)
  return redirect('detail', bunny_id=bunny_id)

def Bunny_BreedList(request):
  bunny_breeds = Bunny_Breed.objects.all()
  return render(request, 'main_app/bunny_breed_list.html', { 'bunny_breeds': bunny_breeds })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
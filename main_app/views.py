from django.shortcuts import render, redirect
from .models import Bunny, Toy, Bunny_Breed
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm

# Create your views here.

# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def bunnies_index(request):
  bunnies = Bunny.objects.all()
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

class BunnyCreate(CreateView):
  model = Bunny
  fields = '__all__'

class BunnyUpdate(UpdateView):
  model = Bunny
  fields = ['breed', 'description', 'age']

class BunnyDelete(DeleteView):
  model = Bunny
  success_url = '/bunnies/'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, bunny_id, toy_id):
  Bunny.objects.get(id=bunny_id).toys.add(toy_id)
  return redirect('detail', bunny_id=bunny_id)

def Bunny_BreedList(request):
  bunny_breeds = Bunny_Breed.objects.all()
  return render(request, 'main_app/bunny_breed_list.html', { 'bunny_breeds': bunny_breeds })

def bunnies_index(request):
  bunnies = Bunny.objects.all()
  return render(request, 'bunnies/index.html', { 'bunnies': bunnies })
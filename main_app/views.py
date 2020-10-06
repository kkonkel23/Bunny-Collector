from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

class Bunny:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

bunnies = [
  Bunny('Muncho', 'Mini Rex', 'foul little demon', 3),
  Bunny('Daloris', 'Dwarf Lionhead', 'Quiet Sweetheart', 0),
  Bunny('Chloe', 'Dwarf Lionhead', 'Energetic', 4)
]

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello ()｡‸｡()</h1>')

def about(request):
    return render(request, 'about.html')

def bunnies_index(request):
    return render(request, 'bunnies/index.html', { 'bunnies': bunnies })
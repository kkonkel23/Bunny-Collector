from django.contrib import admin
from .models import Bunny, Feeding, Toy

# Register your models here.
admin.site.register(Bunny)
admin.site.register(Feeding)
admin.site.register(Toy)
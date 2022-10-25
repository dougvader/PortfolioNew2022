from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import * 

#entities = [User, Mall, Hotel, Park, College, Library,
            #Zoo, Museum, Industry, Restaurant, City]

#for x in range (len(entities)):
    #admin.site.register(x)

#Register Entities
admin.site.register(User, UserAdmin)
admin.site.register(Mall)
admin.site.register(Hotel)
admin.site.register(Park)
admin.site.register(College)
admin.site.register(Library)
admin.site.register(Zoo)
admin.site.register(Museum)
admin.site.register(Industry)
admin.site.register(Restaurant)
admin.site.register(City)



from django.contrib import admin

# Register your models here.
from .models import User
from .models import Userfile, Ordremission, Message, Envoi

admin.site.register(User) 
admin.site.register(Userfile) 
admin.site.register(Ordremission)
admin.site.register(Envoi)
admin.site.register(Message) 
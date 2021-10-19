from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import CASCADE
from django.db import models
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
from docmanag.validate import validator_image


from docmanag.validator import  validator


from .managers import CustomUserManager
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
def logofile(instance, filename):
    return '/'.join(['logo', filename])
def pdffile(instance, filename):
    return '/'.join(['pdf',filename])


class User(AbstractBaseUser, PermissionsMixin):
    ROLE1 = 1
    ROLE2 = 2
    ROLE3 =3
    ROLE4 =4
    ROLE5 =5
    ROLE6=6
    ROLE7=7
    ROLE8=8
    ROLE9=9
    ADMIN=10

      
    ROLE_CHOICES = (
          (ROLE1, 'role1'),
          (ROLE2, 'role2'),
          (ROLE3, 'role3'),
          (ROLE4, 'role4'),
          (ROLE5, 'role5'),
          (ROLE6, 'role6'),
          (ROLE7, 'role7'),
          (ROLE8, 'role8'),
          (ROLE9, 'role9'),
          (ADMIN, 'admin'),
          
      )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    firstname=models.CharField(max_length=255, null=True, blank=True)
    lastname=models.CharField(max_length=255, null=True, blank=True)
    photoprofil=models.ImageField(upload_to='userfile/covers/', null=True, blank=True, validators=[validator_image])
    signature=models.ImageField(upload_to='userfile/covers/', null=True, blank=True, validators=[validator_image])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Userfile(models.Model):
   user=models.ForeignKey(User, on_delete=models.CASCADE)
   title = models.CharField(max_length=100)
   author = models.CharField(max_length=100)
   pdf = models.FileField(upload_to='userfile/pdfs/')
   cover = models.ImageField(upload_to='userfile/covers/', null=True, blank=True)

   def __str__(self):
       return self.title
   
   def delete(self, *args, **kwargs):
      self.pdf.delete()
      self.cover.delete()
      super().delete(*args, **kwargs)



class Ordremission(models.Model):  
   user=models.ForeignKey(User, on_delete=models.CASCADE)
   objetmission=models.CharField(max_length=255, null=True, blank=True)
   datedepart= models.DateField(null=True, blank=True)
   dateretour= models.DateField(null=True, blank=True)
   adressemission=models.CharField(max_length=255, null=True, blank=True)
   transport=models.CharField(max_length=255, null=True, blank=True)
   adressehebergement=models.CharField(max_length=255, null=True, blank=True)
   adresseemploye=models.CharField(max_length=255, null=True, blank=True)
   prenom=models.CharField(max_length=255, null=True, blank=True)
   nom=models.CharField(max_length=255, null=True, blank=True)
   motif=models.CharField(max_length=255, null=True, blank=True)
   nomchauffeur=models.CharField(max_length=255, null=True, blank=True)
   kilomdepart=models.IntegerField(default=0)
   kilomarrivee=models.IntegerField(default=0)
   datecreat=models.DateField(default=timezone.now)
   signatureemployeur=models.CharField(max_length=255, null=True, blank=True)
   createdat =models.DateTimeField(auto_now_add=True)
   fichier_an_one = models.FileField(upload_to=pdffile, null=True, blank=True, validators=[validator])
   fichier_an_two = models.FileField(upload_to=pdffile, null=True, blank=True, validators=[validator])
   fichier_genere = models.FileField(upload_to=pdffile, null=True, blank=True, validators=[validator])
   is_evoiyer= models.BooleanField(default=False)
   is_signer = models.BooleanField(default=False)
   
   class Meta:
         ordering = ('createdat',)
   

class Envoi(models.Model):
   ordremission=models.ForeignKey(Ordremission, on_delete=models.CASCADE)
   initiateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiateur')
   recepteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recepteur')
   createdatenv =models.DateTimeField(auto_now_add=True)
   is_send = models.BooleanField(default=False)
   is_signe = models.BooleanField(default=False)
   

   class Meta:
         ordering = ('createdatenv',)

class Message(models.Model):
   envoi=models.ForeignKey(Envoi, on_delete=models.CASCADE)
   sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
   receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
   message = models.CharField(max_length=1200, null=True, blank=True)
   timestamp = models.DateTimeField(auto_now_add=True)
   is_read = models.BooleanField(default=False)

   def __str__(self):
        return str(self.message)

   class Meta:
     ordering = ('timestamp',)

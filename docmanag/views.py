
import datetime
from docmanag.serializers import MessageSerializer, OrdremissionSerializer
from docmanag.models import Envoi, Message, Ordremission
from django import views
from django.shortcuts import render, redirect
from django.contrib  import messages # Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, request
from notifications.signals import notify
from django.conf import settings

from django.template import loader

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.models import User
from django.views import generic

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
User = get_user_model()
from .forms import OrdremissionForm
from django.core.exceptions import ValidationError

#PDF and sending
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
#from weasyprint import HTML, CSS

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os
from random import randint
 #sending email
 
from django.views.generic import View
from django.utils import timezone
from .models import *
from .managers import *

from threading import Thread, activeCount
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
                 

#utilisation des vues generiques de python

def Home(request):
    return render(request,'docmanag/home.html' )
def Details(request):
    return render(request,'docmanag/detail.html' )

@login_required(login_url='docmanag:logine')    
def Account(request):
    current_user = request.user
    mesoms_list=Ordremission.objects.filter(user=current_user, is_evoiyer=False)
    #potentieltosend=User.objects.exclude(email=request.user.email)
    tosends=User.objects.filter(username="Coordonnateur", role=10)
    page = request.GET.get('page', 1)

    paginator = Paginator(mesoms_list,5)
    try:
        mesoms= paginator.page(page)
    except PageNotAnInteger:
        mesoms= paginator.page(1)
    except EmptyPage:
        mesoms= paginator.page(paginator.num_pages)

    forma = OrdremissionForm(None)    
    
    return render(request,'docmanag/account.html',{'mesoms':mesoms, 'tosends':tosends, 'forma':forma} )

@login_required(login_url='docmanag:logine')   
def Accountcoord(request):
    current_user = request.user
    mesoms_list=Ordremission.objects.filter(user=current_user, is_evoiyer=False)
    #potentieltosend=User.objects.exclude(email=request.user.email)
    tosends=User.objects.filter(username="Coordonnateur", role=10)
    page = request.GET.get('page', 1)

    paginator = Paginator(mesoms_list,5)
    try:
        mesoms= paginator.page(page)
    except PageNotAnInteger:
        mesoms= paginator.page(1)
    except EmptyPage:
        mesoms= paginator.page(paginator.num_pages)
    
    return render(request,'docmanag/accountcoord.html',{'mesoms':mesoms, 'tosends':tosends} )  

@login_required(login_url='docmanag:logine')   
def Boitereception(request):
    current_user = request.user
    envois=Envoi.objects.filter(initiateur=current_user, is_signe=False)
    if request.method == "GET":
        return render(request, 'docmanag/boitereceptionbis.html',
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':envois,})
@login_required(login_url='docmanag:logine')   
def Boitereceptioncoord(request):
    current_user = request.user
    envois=Envoi.objects.filter(recepteur=current_user, is_signe=False)
    if request.method == "GET":
        return render(request, 'docmanag/boitereceptionbiscoord.html',
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':envois,}) 

@login_required(login_url='docmanag:logine')   
def Historique(request):
    current_user = request.user
    envois=Envoi.objects.filter(initiateur=current_user, )
    if request.method == "GET":
        return render(request, 'docmanag/historique.html',
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':envois,})
@login_required(login_url='docmanag:logine')   
def Historiquecoord(request):
    current_user = request.user
    envois=Envoi.objects.filter(recepteur=current_user)
    if request.method == "GET":
        return render(request, 'docmanag/historiquecoord.html',
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':envois,})                                              

def send(request, env_id):
   
    sender_id = request.POST.get('sender')
    receiver_id = request.POST.get('receiver')
    message=request.POST.get('message')
    envoi=Envoi.objects.get(id=env_id)
    sender=User.objects.get(id=sender_id)
    receiver=User.objects.get(id=receiver_id)

    new_message = Message.objects.create(envoi=envoi, sender=sender, receiver=receiver, message=message)
    new_message.save()
    return HttpResponse(new_message)                       

@csrf_exempt
def message_list(request, env_id, sender=None, receiver=None,):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        env=Envoi.objects.get(id=env_id)
        messages = Message.objects.filter(envoi=env, sender=sender, receiver=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)                      

def Messageview(request,  sender, receiver):
    if request.method == "GET":
         return render(request, "docmanag/messages.html",
                      {'users': User.objects.exclude(email=request.user.email),
                       'mesoms':Ordremission.objects.filter(user=request.user),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})
    if request.method == "POST":
         return render(request, "docmanag/messages.html",
                      {'users': User.objects.exclude(email=request.user.email),
                       'receiver': User.objects.get(id=receiver),
                       'mesoms':Ordremission.objects.filter(user=request.user),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})  
def Messageviewbis(request, env_id, sender, receiver):
    if request.method == "GET":
         env=Envoi.objects.get(id=env_id)
         #sender=User.objects.get(id=sender)
         #receiver=User.objects.get(id=receiver)
         return render(request, "docmanag/messages.html",
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':Envoi.objects.filter(initiateur=request.user),
                       'sender':sender,
                       'env_id':env_id,
                       'receiver': receiver,
                       'messages': Message.objects.filter(envoi=env,) |
                                   Message.objects.filter(envoi=env,)})
    if request.method == "POST":
         env=Envoi.objects.get(id=env_id)
         return render(request, "docmanag/messages.html",
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':Envoi.objects.filter(initiateur=request.user),
                       'sender':sender,
                       'env_id':env_id,
                       'receiver': receiver,
                       'messages': Message.objects.filter(envoi=env, sender=sender, receiver=receiver) |
                                   Message.objects.filter(envoi=env, sender=receiver, receiver=sender)})     
def Messageviewbiscoord(request, env_id, sender, receiver):
    if request.method == "GET":
         env=Envoi.objects.get(id=env_id)
         #sender=User.objects.get(id=sender)
         #receiver=User.objects.get(id=receiver)
         return render(request, "docmanag/messagescoord.html",
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':Envoi.objects.filter(recepteur=request.user),
                       'sender':sender,
                       'env_id':env_id,
                       'receiver': receiver,
                       'messages': Message.objects.filter(envoi=env,) |
                                   Message.objects.filter(envoi=env,)})
    if request.method == "POST":
         env=Envoi.objects.get(id=env_id)
         return render(request, "docmanag/messagescoord.html",
                      {'users': User.objects.exclude(email=request.user.email),
                       'envois':Envoi.objects.filter(recepteur=request.user),
                       'sender':sender,
                       'env_id':env_id,
                       'receiver': receiver,
                       'messages': Message.objects.filter(envoi=env, sender=sender, receiver=receiver) |
                                   Message.objects.filter(envoi=env, sender=receiver, receiver=sender)})                                      

def Envoiyer(request):
       
    om_id=request.POST.get('ordremission')
    init=request.POST.get('initiateur') 
    recep=request.POST.get('recepteur') 
    ordremission=Ordremission.objects.get(id=om_id)
    ordremission.is_evoiyer=True
    ordremission.save()
    initiateur=User.objects.get(id=init)
    recepteur=User.objects.get(id=recep)
    

    #current_user = request.user
    #user_id=current_user.id
    #theuser=current_user

    new_env = Envoi.objects.create(ordremission=ordremission, initiateur=initiateur, recepteur=recepteur, is_send=True)
    new_env.save()
    messages.info(request, 'Votre odre de mission a été envoyé avec succès')
    notify.send(sender=initiateur, recipient=recepteur, verb='Message',description="Une demande d'ordre de mission")
    notify.send(sender=recepteur, recipient=initiateur, verb='Message',description="Une demande d'ordre de mission")
    to_emails = [str(request.user.email)]
    subject = "Demande d'Ordre de Mission"
    body=""+ initiateur.lastname +" " +  initiateur.firstname + " a envoyé une demande d'ordre de mission. Veuillez verifiez et traiter la Demande sur DEDRAS"
    email = EmailMessage(subject, body=body, from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.send()
    return redirect('docmanag:boitereception')                                                                                              
                                   

def Storeordremission(request):
    if request.method == 'POST':
       objetmission=request.POST['objetmission']
       datedepart=request.POST['datedepart'] 
       dateretour=request.POST['dateretour'] 
       adressemission=request.POST['adressemission']
       transport=request.POST['transport']
       nomchauffeur=request.POST['nomchauffeur']
       kilomdepart=request.POST['kilomdepart']
       kilomarrivee=request.POST['kilomarrivee']
       adressehebergement=request.POST['adressehebergement']
       adresseemploye=request.POST['adresseemploye']
       nom=request.POST['nom']
       prenom=request.POST['prenom']
       fichier_an_one=request.FILES['fichier_an_one']
       fichier_an_two=request.FILES['fichier_an_two']
            
       if fichier_an_one.content_type !='application/pdf':

            messages.info(request, 'Veuillez bien remplir le formulaire')
            return redirect('docmanag:account')
       else:       
            if fichier_an_two.content_type !='application/pdf':
                messages.info(request, 'Veuillez bien remplir le formulaire')
                return redirect('docmanag:account')
                 
            current_user = request.user
    #user_id=current_user.id
            
            #user_id=current_user.id
            theuser=current_user
            new_om = Ordremission.objects.create(user=theuser, objetmission=objetmission, datedepart=datedepart, dateretour=dateretour, adressemission=adressemission, transport=transport, adressehebergement=adressehebergement, adresseemploye=adresseemploye, nom=nom, prenom=prenom, nomchauffeur=nomchauffeur,kilomdepart=kilomdepart, kilomarrivee=kilomarrivee, fichier_an_one=fichier_an_one, fichier_an_two=fichier_an_two)
            new_om.save()
            messages.info(request, 'Odre de mission créé avec succes')
            return redirect('docmanag:account')    
        # Create a form instance and populate it with data from the request (binding):
        #form = OrdremissionForm(request.POST)

        # Check if the form is valid:
        #if form.is_valid():
            #form.save()
        
            '''post = form.save(commit=False)
            fichier_an_one=request.FILES['fichier_an_one']
            post.user=request.user
            post.fichier_an_one=fichier_an_one
            post.save()'''  
                

            
           

               #  new_om.full_clean()
           # except ValidationError:
                # print("ssd")
    
    # Do something when validation is not passing
            #else:
               #  new_om.save()
               #  messages.info(request, 'Odre de mission créé avec succes')
               #  return HttpResponseRedirect('/docmanag/account/')
    

def Editordremission(request):
       omi_id=request.POST['omi_id']
       objetmission=request.POST['objetmission']
       datedepart=request.POST['datedepart'] 
       dateretour=request.POST['dateretour'] 
       adressemission=request.POST['adressemission']
       transport=request.POST['transport']
       adressehebergement=request.POST['adressehebergement']
       adresseemploye=request.POST['adresseemploye']
       nomchauffeur=request.POST['nomchauffeur']
       kilomdepart=request.POST['kilomdepart']
       kilomarrivee=request.POST['kilomarrivee']
       nom=request.POST['nom']
       prenom=request.POST['prenom']
       fichier_an_one=request.FILES['fichier_an_one'] 
       file_name_one=request.FILES['fichier_an_one'].name
       fichier_an_two=request.FILES['fichier_an_two']
       file_name_two=request.FILES['fichier_an_two'].name

       
   
   
       #current_user = request.user
       #user_id=current_user.id
       #theuser=current_user
   
       ordremission=Ordremission.objects.get(id=omi_id)
       ordremission.objetmission=objetmission
       ordremission.datedepart=datedepart
       ordremission.dateretour=dateretour
       ordremission.adressemission=adressemission
       ordremission.transport=transport
       ordremission.nomchauffeur=nomchauffeur
       ordremission.kilomdepart=kilomdepart
       ordremission.kilomarrivee=kilomarrivee
       ordremission.nom=nom
       ordremission.prenom=prenom
       ordremission.adressehebergement=adressehebergement
       ordremission.adresseemploye=adresseemploye
       #ordremission.fichier_an_one=request.FILES.get('fichier_an_one') 
       #ordremission.fichier_an_two=request.FILES.get('fichier_an_two')
       '''' if request.POST['fichier_an_one']:
                   
           if fichier_an_one.content_type !='application/pdf':
               messages.info(request, 'Veuillez bien remplir le formulaire')
               return redirect('docmanag:account')
           else:
               ordremission.fichier_an_one=request.FILES.get('fichier_an_one')    
          
       if request.POST['fichier_an_two']:
   
                
           if fichier_an_two.content_type !='application/pdf':
               messages.info(request, 'Veuillez bien remplir le formulaire')
               return redirect('docmanag:account')
           else:    
               ordremission.fichier_an_two=request.FILES.get('fichier_an_two')'''  

       fs=FileSystemStorage()
       file_one=fs.save(fichier_an_one.name, fichier_an_one)   
       fileurl_one=fs.url(file_one)  
       report_one=file_name_one

       file_two=fs.save(fichier_an_two.name, fichier_an_two)   
       fileurl_two=fs.url(file_two)  
       report_two=file_name_two

       ordremission.fichier_an_one=fichier_an_one
       ordremission.fichier_an_two=fichier_an_two
       #Ordremission.objects.filter(id=omi_id).update(fichier_an_one=fichier_an_one, fichier_an_two=fichier_an_two)
       ordremission.save()
       messages.info(request, 'Odre de mission modifié avec succes')
       return redirect('docmanag:account')    
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.role==10:
                   login(request, user)
                   return redirect('docmanag:boitereceptioncn') 
                else:
                   login(request, user)
                   return redirect('docmanag:account') 


    return render(request,'docmanag/login.html')  


def Register(request):
   
        return render(request,'registration/registration.html' )

def Storeuser(request):
    nom=request.POST.get('lastname')
    prenom=request.POST.get('firstname')
    username=request.POST.get('username')
    email=request.POST['email']
    password=request.POST['password']
    password2=request.POST['password2']
    if password ==password2:

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Cet email est déja utilisé pour un autre compte')
            return redirect('docmanag:register')
       
        else:
            user=User.objects.create(email=email, password=password, lastname=nom, firstname=prenom, username=username)
            user.set_password(password)
            user.save();
            return redirect('docmanag:logine')       
    else:
        messages.info(request, 'Les mots de passe ne correspondent pas')
        return redirect('docmanag:register')

    #return redirect('register')

def visualiser(request):
    if request.method =='POST':

        ID = request.POST.get('id')
        myom =Ordremission.objects.filter(id=ID) # So we send the company instance
        #return JsonResponse({'myom':myom})
        serializer = OrdremissionSerializer(myom, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
        #return HttpResponse(myom)  
       
    else:
        messages.info(request, 'Votre odre de mission a été envoyé avec succès')
        return redirect('docmanag:account')    
       
       
def deleteom(request):
    if request.method =='POST':

        ID = request.POST.get('omid')
        myom =Ordremission.objects.get(id=ID) # So we send the company instance
        #return JsonResponse({'myom':myom})
        myom.delete()
        messages.info(request, 'Votre odre de mission a été supprimée avec succès')
        return redirect('docmanag:account')  
        #return HttpResponse(myom)  
       
    else:
        messages.info(request, 'Votre odre de mission ne peut pas etre supprimée')
        return redirect('docmanag:account')

def signature(request):
    if request.method =='POST':
        #signat =request.FILES.get('signature')
        coord=User.objects.get(username="Coordonnateur", role=10)
        coord.signature=request.FILES.get('signature') # So we send the company instance
        #return JsonResponse({'myom':myom})
        coord.save()
        messages.info(request, 'Signature téléchargée avec succès')
        return redirect('docmanag:boitereceptioncn')  
        #return HttpResponse(myom)  
       
    else:
        messages.info(request, " OOps!! Une erreur s'est produite")
        return redirect('docmanag:boitereceptioncn')    

class Render:
    
    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        file = open("my.file.pdf", "wb")
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}-{1}.pdf".format(params['today'], randint(1, 1000000))
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "store", file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]


def send_email(file: list):
    r = request.post(
        "https://api.mailgun.net/v3/######/messages",
        auth=("api", "key-########################################"),
        files=[("attachment", (file[0], open(file[1], "rb").read()))],
        data={"from": "No Reply <no-reply@##########>",
              "to": "schal97.aw@gmail.com",
              "subject": "Sales Report",
              "text": "Requested Sales Report",
              "html": "<html>Requested Sales Report</html>"})

def render_to_pdf(template_src, context_dict={}):
    html = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None
    
class Pdf(View,):
        def get(self, request,om, *args, **kwargs):
            data = {
            'today': datetime.date.today(), 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            'name':"schallom"
            }
            #pdf = Render.render_to_file('docmanag/omsigne.html', params)
            pdf = render_to_pdf('docmanag/omsigne.html', data)
            #return HttpResponse(pdf, content_type='application/pdf')
            #pdfi=base64.b64encode(attachment['pdf']).decode()
            to_emails = [str(request.user.email)]
            subject = "Ordre de Mission"
            email = EmailMessage(subject, body=pdf, from_email=settings.EMAIL_HOST_USER, to=to_emails)
            email.attach("certificate_{}".format(data['name']) + '.pdf', pdf, "application/pdf")
            email.content_subtype = "pdf"  # Main content is now text/html
            email.encoding = 'us-ascii'
            email.send()

            return HttpResponse(pdf, content_type='application/pdf')


def signer(request, om_id):
    om=Ordremission.objects.get(id=om_id)
    user=request.user
        
    data = {
    'today': datetime.date.today(), 
    'objetmission':om.objetmission,
    'datedepart': om.datedepart,
    'dateretour': om.dateretour,
    'adressemission':om.adressemission,
    'transport': om.transport,
    'adressehebergement': om.adressehebergement,
    'adresseemploye': om.adresseemploye,
    'nom': om.nom,
    'prenom': om.prenom,
    'datecreat':om.datecreat,
    'name':om.user.username,
    'nomchaufe':om.nomchauffeur,
    'kilomdep':om.kilomdepart,
    'kilomarr':om.kilomarrivee,
    'user':user
    }
    env=Envoi.objects.filter(ordremission__id=om.id)
    env.update(is_signe=True)
    #pdf = Render.render_to_file('docmanag/omsigne.html', params)
    pdf = render_to_pdf('docmanag/omsigne.html', data)
    #return HttpResponse(pdf, content_type='application/pdf')
    #pdfi=base64.b64encode(attachment['pdf']).decode()
    to_emails = [str(om.user.email)]
    subject = "Ordre de Mission"
    email = EmailMessage(subject, body=pdf, from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.attach("Order_mision{}".format(data['name']) + '.pdf', pdf, "application/pdf")
    email.content_subtype = "pdf"  # Main content is now text/html
    email.encoding = 'us-ascii'
    email.send()
    return HttpResponse(pdf, content_type='application/pdf')
    ''''html = render_to_string('docmanag/omsigne.html',
                            {'om': om})
       
 
    # generate and send an email with pdf certificate file to the user's email
    user_info = {
        "name": om.user.username,
        
    }
    html = render_to_string('docmanag/omsigne.html',
                            {'om': om})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=certificate_{}'.format(user_info['name']) + '.pdf'
    #pdf = HTML(string=html, base_url='http://127.0.0.1:8000/docmanag/account/').write_pdf(
        #stylesheets=[CSS(string='body { font-family: serif}')])
    pdf=""
    to_emails = [str(om.user.email)]
    subject = "Certificate from Nami Montana"
    email = EmailMessage(subject, body=pdf, from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.attach("certificate_{}".format(user_info['name']) + '.pdf', pdf, "application/pdf")
    email.content_subtype = "pdf"  # Main content is now text/html
    email.encoding = 'us-ascii'
    email.send()'''

    



             


           
        
       
      

# def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
   # context = {'latest_question_list': latest_question_list}
   # return render(request, 'sondage/index.html', context)

# def detail(request, question_id):
   # try:
        #question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
      #  raise Http404("Question does not exist")#question = get_object_or_404(Question, pk=question_id)
   # return render(request, 'sondage/detail.html', {'question': question})

# def resultats(request, question_id):
   # question= get_object_or_404(Question, pk=question_id )
   #  try:
      #  selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
       ## })
   # else:
        #empecher les conclits de concurence
       # selected_choice.votes=F('votes') + 1
        #eviter une double mise a jour
        #selected_choice.refresh_from_db()
       # selected_choice.save()#
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('sondage:resultats', args=(question.id,)))#

        





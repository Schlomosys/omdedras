from django.urls import path, include

from . import views

app_name = 'docmanag'
urlpatterns = [
    #path('', views.index, name='index'),
    #sondage/5/
    #path('detail/<int:question_id>/', views.detail, name='detail'),
     #sondage/5/results/
    #path('<int:question_id>/results/', views.resultats, name='resultats'),
     #sondage/5/vote/
    #path('<int:question_id>/vote/', views.vote, name='vote'),
    #path('', views.IndexView.as_view(), name='index'),
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
    #path('register/', views.Register, name='register'),
    ##path('login/', views.Login, name='login'),
    #path('storeuser/',  views.Storeuser, name='storeuser'),/docmanag/
    
    path('home/', views.Home, name='home'),
    path('details/', views.Details, name='details'),
    path('account/', views.Account, name='account'),
    path('accountcoord/', views.Accountcoord, name='accountcoord'),
    path('storeordremission/',  views.Storeordremission, name='storeordremission'),
    path('editordremission/',  views.Editordremission, name='editordremission'),
    path('boitereception/',  views.Boitereception, name='boitereception'),
    path('boitereceptioncn/',  views.Boitereceptioncoord, name='boitereceptioncn'),
    
    path('historique/',  views.Historique, name='historique'),
    path('historiquecoord/',  views.Historiquecoord, name='historiquecoord'),
    path('logine/', views.login_user, name='logine'),
    path('addsignat/', views.signature, name='signature'),
    path('signer/<int:om_id>/', views.signer, name='signer'),
    path('render/pdf/', views.Pdf.as_view()),   
    path('chatcn/<int:env_id>/<int:sender>/<int:receiver>/', views.Messageviewbiscoord, name='chatcn'),
    path('chat/<int:env_id>/<int:sender>/<int:receiver>/', views.Messageviewbis, name='chat'),
    path('envoiyer/', views.Envoiyer, name='envoi'),
    path('api/messages/<int:env_id>/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/<int:env_id>/<int:sender>/<int:receiver>/<str:message>/', views.message_list, name='message-list'),

    path('send/<int:env_id>/', views.send, name='send'),
    path('visualiser/', views.visualiser, name='visualiser'),
    path('deleteom/', views.deleteom, name='deleteom'),

    path('register/', views.Register, name='register'),
    path('storeuser/',  views.Storeuser, name='storeuser'),
    path('accounts/', include('django.contrib.auth.urls')),
]
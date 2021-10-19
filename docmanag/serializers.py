
from rest_framework import serializers
from .models import Message, User, Ordremission




class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['envoi','sender', 'receiver', 'message', 'timestamp']



class OrdremissionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Ordremission
        fields = ['id','user','objetmission', 'datedepart', 'dateretour', 'adressemission', 'transport', 'adressehebergement', 'adresseemploye', 'signatureemployeur', 'createdat', 'fichier_an_one', 'fichier_an_two', 'fichier_genere', 'is_evoiyer','prenom', 'nom','datecreat','is_signer', 'nomchauffeur','kilomdepart','kilomarrivee' ]        
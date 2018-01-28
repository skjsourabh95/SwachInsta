import cloudinary
from django import forms

from swachBharat.models import uploadmodel,sortmodel


class Upload_form(forms.ModelForm):
    cloudinary.config(
        cloud_name="sourabh-images",
        api_key="417392912892168",
        api_secret="R8Nuaik5jJVqiQ5Xhe0FNYadNdE"
    )
    class Meta:
       model= uploadmodel
       fields = ['image', 'caption']

class Sort_form(forms.ModelForm):
    class Meta:
        model= sortmodel
        fields= ['upload']
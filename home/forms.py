import cloudinary
from django import forms
from models import users,postmodel,likemodel,commentmodel,upvotemodel

class SignUp_form(forms.ModelForm):
    class Meta:
        model= users
        fields= ['name','email','username','password']

class LogIn_form(forms.ModelForm):
    class Meta:
        model= users
        fields= ['username','password']

class Post_form(forms.ModelForm):
    cloudinary.config(
        cloud_name="sourabh-images",
        api_key="417392912892168",
        api_secret="R8Nuaik5jJVqiQ5Xhe0FNYadNdE"
    )
    class Meta:
       model= postmodel
       fields = ['image', 'caption']

class Like_form(forms.ModelForm):
    class Meta:
        model= likemodel
        fields= ['post']

class Comment_form(forms.ModelForm):
    class Meta:
        model= commentmodel
        fields= ['post','comment_text']

class Upvote_form(forms.ModelForm):
    class Meta:
        model= upvotemodel
        fields= ['comment']
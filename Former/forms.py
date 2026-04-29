from django import forms
from .models import Register_Model



# Register Form --------------------------------------------------------------------------------------

from django import forms
from .models import Register_Model

class Register_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Register_Model
        fields = [
            'name', 'photo', 'gender',
            'date_of_birth',  'phone'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data    

# Login Form -----------------------------------------------------------------------------

class Login_Form(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
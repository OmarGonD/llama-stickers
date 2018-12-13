from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import SizeQuantity
from django.core.mail import send_mail

# Variables

TAMANIOS = (('variante_50', '50 mm x 50 mm',), ('variante_75', '75 mm x 75 mm',),
            ('variante_100', '100 mm x 100 mm',), ('variante_125', '125 mm x 125 mm',))

CANTIDADES = (('cantidad_50', '50',), ('cantidad_100', '100',),
              ('cantidad_200', '200',), ('cantidad_300', '300',),
              ('cantidad_500', '500',), ('cantidad_1000', '1000',),
              ('cantidad_2000', '2000',), ('cantidad_3000', '3000',),
              ('cantidad_4000', '4000',), ('cantidad_5000', '5000',),
              ('cantidad_1000', '1000',))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, help_text='tucorreo@email.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1',
                  'password2')


class StepOneForm(forms.Form):
    size = forms.ChoiceField(choices=TAMANIOS, widget=forms.RadioSelect(), label='Selecciona un tamaño')
    quantity = forms.ChoiceField(choices=CANTIDADES, widget=forms.RadioSelect(), label='Selecciona la cantidad')


class StepTwoForm(forms.ModelForm):
    # comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = SizeQuantity
        fields = ('image', )

    def __init__(self, *args, **kwargs):
        super(StepTwoForm, self).__init__(*args, **kwargs)
        # self.fields['comment'].required = False
        self.fields['image'].required = False

    def save(self, commit=True):

        instance = super(StepTwoForm, self).save(commit=commit)
        # self.send_email()
        return instance

    # def send_email(self):
    #     send_mail('Django Test', 'My message', 'oma.oma@gmail.com',
    #               ['oma.oma@gmail.com'], fail_silently=False)

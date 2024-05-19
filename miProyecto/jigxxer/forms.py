from django import forms
from .models import Venta,Negocio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

#formulario para mostar los productos
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['Id_negocio'].queryset = user.negocios.all()
            
            

#formulario para registro incorporado de django
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingresa una dirección de correo electrónico válida.')
    user_type = forms.ChoiceField(choices=[('Administrador', 'Administrador'), ('Cliente', 'Cliente')], required=True, help_text='Selecciona el tipo de usuario.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Aquí asignamos el tipo de usuario al objeto user antes de guardarlo
        user_type = self.cleaned_data.get('user_type')
        if commit:
            user.save()
            group_name = 'Administrador' if user_type == 'Administrador' else 'Cliente'
            my_group = Group.objects.get(name=group_name)  # Obtener el grupo por nombre
            my_group.user_set.add(user)  # Agregar el usuario al grupo

        return user
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
#formulario para la creacion de negocios
class NegocioForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ['nombre_negocio', 'telefono', 'numero_de_local', 'usuario_administrador']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NegocioForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['usuario_administrador'].queryset = User.objects.filter(id=user.id)
            self.fields['usuario_administrador'].initial = user
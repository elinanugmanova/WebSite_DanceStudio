from django.forms import TextInput, NumberInput, EmailInput, Select, DateInput, TimeInput
from django import forms
from django.contrib.auth.models import User


from .models import Abonement,Trainer,Training,Order,Record

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AbonementForm(forms.ModelForm):
    class Meta:
        model = Abonement
        fields = ['name', 'number_of_trainings', 'price']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control mt-2',
                'placeholder' : 'Название абонемента'
            }),
            'number_of_trainings': NumberInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Количество тренировок'
            }),
            'price': NumberInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Стоимость'
            })
        }


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['fio', 'specialization', 'phonenumber','email']
        widgets = {
            'fio': TextInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'ФИО'
            }),
            'specialization': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Направление'
            }),
            'phonenumber': NumberInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Номер телефона'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Почта'
            })
        }


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['specialization','date','time_start','time_end', 'gym_number','trainer']
        widgets = {
            'specialization': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Направление'
            }),
            'date': DateInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Дата'
            }),

            'time_start': TimeInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Время начала'
            }),
            'time_end': TimeInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Время окончания'
            }),
            'gym_number': NumberInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Номер зала'
            }),
            'trainer': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Номер зала'
            })
        }



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user','abonement']
        widgets = {
            'user': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Пользователь'
            }),
            'abonement': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Абонемент'
            }),



        }

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['user','training']
        widgets = {
            'user': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Пользователь'
            }),
            'training': Select(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Тренирока'
            }),
        }



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username']
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Имя'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Фамилия'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Почта'
            }),
            'username': NumberInput(attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Логин'
            }),

        }


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Abonement, Order, Record, Training, Trainer
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfileEditForm, AbonementForm, TrainerForm, TrainingForm, OrderForm, RecordForm, UserForm
from django.views.generic import UpdateView, DeleteView
from django.db.models import Sum, Count
from django.db.models import Count


def Home(request):
    return render(request, "authapp/index.html")


def statistics(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_revenue = 0
    count_abonement = None
    count_trainings = None
    best_trainer = None

    if start_date and end_date:
        total_revenue = Order.objects.filter(created_at__range=[start_date, end_date]).aggregate(revenue=
                                                                                                 Sum('abonement__price'))[
            'revenue']
        count_abonement = (Order.objects.values('abonement__id', 'abonement__name').annotate
                           (count=Count('abonement')).order_by('-count'))
        count_trainings = Record.objects.values('training__id', 'training__specialization').annotate(
            count=Count('training')).order_by('-count')
        for item in count_trainings:
            training = Training.objects.get(id=item['training__id'])
            item['display_specialization'] = training.get_specialization_display()
            best_trainer = \
            Record.objects.values('training__id', 'training__trainer', 'training__trainer__fio').annotate(
                count=Count('training')).order_by('-count').first()['training__trainer__fio']

    if total_revenue is None:
        total_revenue = 0
    return render(request, 'authapp/statistics.html',
                  {'total_revenue': total_revenue, 'count_abonement': count_abonement,
                   'count_trainings': count_trainings, 'best_trainer': best_trainer})


def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('usernumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(username) != 11:
            messages.info(request, "В номере должно быть 11 цифр")
            return redirect('/signup')

        if pass1 != pass2:
            messages.info(request, "Пароли не совпадают")
            return redirect('/signup')

        try:
            if User.objects.get(username=username):
                messages.warning(request, "Номер телефона занят")
                return redirect('/signup')
        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request, "Почта занята")
                return redirect('/signup')
        except Exception as identifier:
            pass

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Аккаунт зарегистрирован")
        return redirect('/login')
    return render(request, "authapp/signup.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Успешно")
            return redirect('/')
        else:
            messages.error(request, "Неверные данные")
            return redirect('/login')

    return render(request, "authapp/handlelogin.html")


def handleLogout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта")
    return redirect('/login')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    records = Record.objects.filter(user=request.user).order_by('training__date', 'training__time_start')
    return render(request, 'authapp/profile.html', {'user': request.user
        , 'orders': orders, 'records': records}, )


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'authapp/profile_update.html', {'form': form})


def abonement(request):
    abonement = Abonement.objects.all()
    messages.success(request, "Вы успешно купили абонемент")
    return render(request, 'authapp/abonement.html', {'abonements': abonement})


def abonement_create(request):
    error = ''
    if request.method == "POST":
        form = AbonementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('abonement')
        else:
            error = 'Форма заполнена неверно'
    form = AbonementForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "authapp/abonement_create.html", data)


class AbonementUpdateViews(UpdateView):
    model = Abonement
    template_name = 'authapp/abonement_create.html'
    form_class = AbonementForm
    success_url = '/abonement'


class AbonementDeleteViews(DeleteView):
    model = Abonement
    success_url = '/abonement'
    template_name = 'authapp/abonement_delete.html'


def trainer(request):
    trainer = Trainer.objects.all()
    return render(request, 'authapp/trainer.html', {'trainers': trainer})


def trainer_create(request):
    error = ''
    if request.method == "POST":
        form = TrainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer')
        else:
            error = 'Форма заполнена неверно'
    form = TrainerForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "authapp/trainer_update.html", data)


class TrainerUpdateViews(UpdateView):
    model = Trainer
    template_name = 'authapp/trainer_update.html'
    form_class = TrainerForm
    success_url = '/trainer'


class TrainerDeleteViews(DeleteView):
    model = Trainer
    success_url = '/trainer'
    template_name = 'authapp/trainer_delete.html'


def user(request):
    user = User.objects.all()
    return render(request, 'authapp/user.html', {'users': user})


class UserUpdateViews(UpdateView):
    model = User
    template_name = 'authapp/user_update.html'
    form_class = UserForm
    success_url = '/user'


class UserDeleteViews(DeleteView):
    model = User
    success_url = '/user'
    template_name = 'authapp/user_delete.html'


def training(request):
    training = Training.objects.all().order_by('date', 'time_start')
    return render(request, 'authapp/training.html', {'trainings': training})


def training_create(request):
    error = ''
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training')
        else:
            error = 'Форма заполнена неверно'
    form = TrainingForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "authapp/training_create.html", data)


class TrainingUpdateViews(UpdateView):
    model = Training
    template_name = 'authapp/training_create.html'
    form_class = TrainingForm
    success_url = '/training'


class TrainingDeleteViews(DeleteView):
    model = Training
    success_url = '/training'
    template_name = 'authapp/training_delete.html'


def order(request):
    order = Order.objects.all()
    return render(request, 'authapp/order.html', {'orders': order})


@login_required
def create_order(request, abonement_id):
    abonement = get_object_or_404(Abonement, id=abonement_id)
    Order.objects.create(user=request.user, abonement=abonement)
    messages.success(request, "Абонемент успешно оформлен")
    return redirect('profile')


def order_create(request):
    error = ''
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order')
        else:
            error = 'Форма заполнена неверно'
    form = OrderForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "authapp/order_create.html", data)


class OrderUpdateViews(UpdateView):
    model = Order
    template_name = 'authapp/order_create.html'
    form_class = OrderForm
    success_url = '/order'


class OrderDeleteViews(DeleteView):
    model = Order
    success_url = '/order'
    template_name = 'authapp/order_delete.html'


def record(request):
    record = Record.objects.all().order_by('training__date', 'training__time_start')
    return render(request, 'authapp/record.html', {'records': record})


def record_create(request):
    error = ''
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record')
        else:
            error = 'Форма заполнена неверно'
    form = RecordForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, "authapp/record_create.html", data)


class RecordUpdateViews(UpdateView):
    model = Record
    template_name = 'authapp/record_create.html'
    form_class = RecordForm
    success_url = '/record'


class RecordDeleteViews(DeleteView):
    model = Record
    success_url = '/record'
    template_name = 'authapp/record_delete.html'


@login_required
def create_record(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    Record.objects.create(user=request.user, training=training)
    messages.success(request, "Вы успешно записаны на занятие")
    return redirect('profile')


def is_admin(user):
    return user.is_staff or user.is_superuser

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('signup', views.signup, name='signup'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('statistics', views.statistics, name='statistics'),

    path('abonement', views.abonement, name='abonement'),
    path('abonement/<int:pk>/update', views.AbonementUpdateViews.as_view(), name='abonement_update'),
    path('abonement/<int:pk>/delete', views.AbonementDeleteViews.as_view(), name='abonement_delete'),
    path('abonement/abonement_create', views.abonement_create, name='abonement_create'),

    path('training', views.training, name='training'),
    path('training/<int:pk>/update', views.TrainingUpdateViews.as_view(), name='training_update'),
    path('training/<int:pk>/delete', views.TrainingDeleteViews.as_view(), name='training_delete'),
    path('training/training_create', views.training_create, name='training_create'),

    path('record', views.record, name='record'),
    path('record/<int:training_id>/', views.create_record, name='create_record'),
    path('record/<int:pk>/update', views.RecordUpdateViews.as_view(), name='record_update'),
    path('record/trainer_create', views.record_create, name='record_create'),
    path('record/<int:pk>/delete', views.RecordDeleteViews.as_view(), name='record_delete'),

    path('order', views.order, name='order'),
    path('order/<int:abonement_id>', views.create_order, name='create_order'),
    path('order/<int:pk>/update', views.OrderUpdateViews.as_view(), name='order_update'),
    path('order/trainer_create', views.order_create, name='order_create'),
    path('order/<int:pk>/delete', views.OrderDeleteViews.as_view(), name='order_delete'),

    path('trainer', views.trainer, name='trainer'),
    path('trainer/<int:pk>/update', views.TrainerUpdateViews.as_view(), name='trainer_update'),
    path('trainer/trainer_create', views.trainer_create, name='trainer_create'),
    path('trainer/<int:pk>/delete', views.TrainerDeleteViews.as_view(), name='trainer_delete'),

    path('user', views.user, name='user'),
    path('user/<int:pk>/update', views.UserUpdateViews.as_view(), name='user_update'),
    path('user/<int:pk>/delete', views.UserDeleteViews.as_view(), name='user_delete'),
]

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path(route='simple', view=views.simple, name='simple'),

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for registration
    path(route='registration', view=views.registration_request, name='registration'),

    # path for login
    path(route='login', view=views.login_request, name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),


    path(route='', view=views.get_dealerships, name='index'),

    path(route='add_review/<int:dealer_id>', view=views.add_review, name='add_review'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='dealer/<int:dealer_id>/', view=views.add_review, name='dealer_details')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
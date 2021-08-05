from django.urls import path
from . import views

app_name = 'organization'
urlpatterns = [
    path('create/', views.OrganizationCreateView.as_view(), name="create-organ"),
    path('list/', views.OrganizationListView.as_view(), name='list-organ'),

    path('detail/<int:pk>', views.OrganizationDetailView.as_view(), name='detail-organ'),
    path('detail/edit/<int:pk>', views.OrganizationUpdateView.as_view(), name='update-organ'),

    path('followup/edtit/<int:pk>', views.FollowUpUpdateView.as_view(), name='update-followup'),
    path('followup/create/<int:pk>', views.FollowUpCreateView.as_view(), name='create-followup'),
]

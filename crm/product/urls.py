from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('company/create/', views.ProductCreateView.as_view(), name='create-product'),
    path('company/list/', views.ProductListView.as_view(), name='list-product'),
    path('compony/detail/<int:pk>',views.ProductDetailView.as_view(),name='detail-product'),
    path('compony/update/<int:pk>',views.ProductUpdateView.as_view(),name='update-product'),

    path('organization/create/', views.OrganizationProductCreateView.as_view(), name='create-orgproduct'),
    path('organization/list/', views.OrganizationProductListView.as_view(), name='list-org-product'),

]

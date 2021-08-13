from django.urls import path
from . import views

app_name = 'sale'
urlpatterns = [
    # path('create/', views.quote_create, name="create-quote"),
    path('create/', views.QuoteCreateView.as_view(), name='create-quote'),
    path('list/', views.QuoteListView.as_view(), name='list-quote'),
    path('detail/<int:pk>', views.QuoteDetailView.as_view(), name='detail-quote'),
    path('detail/pdf/<int:pk>', views.PrintQuoteDetailView.as_view(), name='detail-pdf-quote'),
    path('send/email/<int:pk>', views.send_email_view, name='send-email'),
    path('update/<int:pk>', views.QuoteUpdateView.as_view(), name='update-quote'),
    path('delete/<int:pk>', views.QuoteDeleteView.as_view(), name='delete-quote')

]

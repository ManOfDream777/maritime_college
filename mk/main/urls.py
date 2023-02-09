from django.urls import path
from .views import Index, About, Blog, Contact, Seniors, Faculties, ApiRankView, AuthView, ApiAuthView, ApiLogout,BlogListView, BlogDetailView,ApiFacultiesGroups, APIContactCreate

urlpatterns = [
    path('', Index.as_view(), name = 'index'),
    path('about/', About.as_view(), name = 'about'),
    path('blog/', Blog.as_view(), name = 'blog'),
    path('blog/<slug:slug>/', BlogListView.as_view(), name = 'blog_list'),
    path('blog/<slug:category_slug>/<slug:slug>/', BlogDetailView.as_view(), name = 'blog_detail'),
    path('contact/', Contact.as_view(), name = 'contact'),
    path('seniors/', Seniors.as_view(), name = 'seniors'),
    path('faculties/', Faculties.as_view(), name = 'faculties'),
    path('auth/', AuthView.as_view(), name = 'auth'),
    #api urls
    path('api/senior_staff/<int:id>/', ApiRankView.as_view(), name='display_seniors_by_rank'),
    path('api/auth/', ApiAuthView.as_view(), name='api_auth'),
    path('api/logout/', ApiLogout.as_view(), name='api_logout'),
    path('api/groups/<int:faculty>/', ApiFacultiesGroups.as_view(), name='api_groups'),
    path('api/contact_create/', APIContactCreate.as_view(), name='api_contact')
]

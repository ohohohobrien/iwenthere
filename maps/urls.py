from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [

    # API Routes
    path("geojson", views.geojson, name="geojson"),
    path("geojson/<str:map_id>", views.geojson_search, name="geojson_search"),
    path("maps/<str:country_name>", views.state_names, name="state_names"),
    path("delete/<str:map_id>", views.delete_map, name="delete"),
    path("save/<str:map_id>", views.save_map, name="save"),

    # Site routes
    path("", views.search, name="search"),
    path("search_results", views.search_results, name="search_results"),
    path("all", views.home_page, name="index"),
    path("create", views.test, name="test"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("error", views.not_found, name="not_found"),
    path("map/<str:map_id>", views.display_map, name="display_map"),
    path("edit/<str:map_id>", views.edit_map, name="edit"),
    path("<str:profile>", views.profile_page, name="profile"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
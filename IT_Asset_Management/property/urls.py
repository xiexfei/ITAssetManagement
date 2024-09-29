from django.urls import path
from property.views.asset_views import (
    add_asset,
    asset_list,
    asset_statistics,
    export_assets,
    import_assets,
    manage_asset,
)
from property.views.user_views import add_userinfo, export_userinfos, import_userinfos, manage_userinfo, adminuser_login, adminuser_logout, userinfo_list
from property.views.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("add_asset/", add_asset, name="add_asset"),
    path("asset_list/", asset_list, name="asset_list"),
    path("<int:id>/<str:action>/", manage_asset, name="manage_asset"),
    path("export_assets/", export_assets, name="export_assets"),
    path("import_assets/", import_assets, name="import_assets"),
    path("asset_statistics/", asset_statistics, name="asset_statistics"),
    path("login/", adminuser_login, name="adminuser_login"),
    path("logout/", adminuser_logout, name="adminuser_logout"),
    # path("register/", register, name="register"),
    path("userinfo_list", userinfo_list, name="userinfo_list"),
    path("add_userinfo", add_userinfo, name="add_userinfo"),
    path("userinfo/<int:id>/<str:action>/", manage_userinfo, name="manage_userinfo"),
    path('import_userinfos/', import_userinfos, name='import_userinfos'),
    path('export_userinfos/', export_userinfos, name='export_userinfos'),
]

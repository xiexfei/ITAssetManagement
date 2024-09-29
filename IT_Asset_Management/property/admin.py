from django.contrib import admin
from property.models import AssetInfo, AssetTypeList, Department, Software, UserInfo

admin.site.site_header = "我的资产管理系统"
admin.site.site_title = "资产管理系统后台"
admin.site.index_title = "资产管理系统管理"


class AssetInfoAdmin(admin.ModelAdmin):
    list_display = (
        "host_name",
        "service_tag",
        "host_type",
        "receive_date",
        "host_status",
        "host_user", 
    )
    list_filter = ("host_type", "host_status", "receive_date")
    search_fields = ("host_name", "service_tag", "host_user")
    ordering = ("-receive_date",)


admin.site.register(AssetInfo, AssetInfoAdmin)


@admin.register(AssetTypeList)
class AssetTypeListAdmin(admin.ModelAdmin):
    list_display = ("type_name",) 
    search_fields = ("type_name",)  


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("dept_name",)  
    search_fields = ("dept_name",) 


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("soft_name", "version", "license_key", "department") 
    search_fields = ("soft_name", "license_key") 


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user_name", "fullname", "email", "department")
    search_fields = ("user_name", "fullname", "email")
    list_filter = ("department",)

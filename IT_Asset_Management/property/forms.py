from django import forms
from .models import AssetInfo, UserInfo


class AssetForm(forms.ModelForm):
    class Meta:
        model = AssetInfo
        fields = [
            "host_name",
            "service_tag",
            "host_type",
            "host_model",
            "receive_date",
            "host_user", 
            "host_status",
            "remark",
        ]
        labels = {
            "host_name": "设备名称",
            "service_tag": "设备序列号",
            "host_type": "设备类别",
            "host_model": "设备型号",
            "receive_date": "采购日期",
            "host_user": "使用用户", 
            "host_status": "设备状态",
            "remark": "备注",
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ["user_name", "fullname", "email", "department"]
        labels = {
            "user_name": "账户名",
            "fullname": "姓名",
            "email": "邮箱",
            "department": "部门",
        }

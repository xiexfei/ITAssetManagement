from django.db import models
from django.utils import timezone


class AssetTypeList(models.Model):
    type_name = models.CharField(max_length=100, verbose_name="设备类别")

    class Meta:
        verbose_name = "类别"
        verbose_name_plural = "类别列表"

    def __str__(self):
        return self.type_name


class Department(models.Model):
    dept_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门列表"

    def __str__(self):
        return self.dept_name


class UserInfo(models.Model):
    user_name = models.CharField(max_length=100, unique=True, verbose_name="账户名")
    fullname = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="姓名"
    )
    email = models.EmailField(verbose_name="邮箱")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="所属部门",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "员工用户"
        verbose_name_plural = "员工用户列表"

    def __str__(self):
        return self.user_name


class AssetInfo(models.Model):
    STATUS_CHOICES = [
        ("闲置", "闲置"),
        ("使用中", "使用中"),
        ("等待报废", "等待报废"),
    ]

    host_name = models.CharField(max_length=200, verbose_name="设备名称")
    service_tag = models.CharField(
        max_length=100, unique=True, verbose_name="设备序列号"
    )
    host_type = models.ForeignKey(
        AssetTypeList, on_delete=models.CASCADE, verbose_name="设备类别"
    )
    host_model = models.CharField(max_length=100, verbose_name="设备型号")
    receive_date = models.DateField(default=timezone.now, verbose_name="采购日期")
    host_user = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="使用用户",
    )
    host_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="闲置", verbose_name="设备状态"
    )
    remark = models.TextField(blank=True, null=True, verbose_name="备注")

    @property
    def department(self):
        return self.host_user.department if self.host_user else None

    def purchase_duration(self):
        if not hasattr(self, "_purchase_duration"):
            duration = timezone.now().date() - self.receive_date
            years = duration.days // 365
            months = (duration.days % 365) // 30
            self._purchase_duration = f"{years}年{months}月"
        return self._purchase_duration

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = "设备列表"

    def __str__(self):
        return f"{self.host_name} - {self.host_model}"


class Software(models.Model):
    soft_name = models.CharField(max_length=100, verbose_name="名称")
    version = models.CharField(max_length=50, verbose_name="版本")
    license_key = models.CharField(max_length=100, unique=True, verbose_name="密钥")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="softwares",
        verbose_name="所属部门",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "软件"
        verbose_name_plural = "软件列表"

    def __str__(self):
        return self.soft_name

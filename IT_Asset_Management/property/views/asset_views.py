# views/asset_views.py
import csv
from django.utils import timezone
import pandas as pd
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from property.forms import AssetForm
from property.models import AssetInfo, AssetTypeList, UserInfo


@login_required
def asset_list(request):
    query = request.GET.get("search", "")
    assets = AssetInfo.objects.all()
    if query:
        assets = assets.filter(host_name__icontains=query)
    
    paginator = Paginator(assets, 10)  # 每页显示 10 条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, "property/asset_list.html", {"page_obj": page_obj, "assets": assets, "query": query}
    )


@login_required
def add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "资产添加成功！")
            return redirect("asset_list")
        else:
            messages.error(request, "表单验证失败！请检查输入的信息。")
            print(form.errors)
    else:
        form = AssetForm()
    return render(request, "property/add_asset.html", {"form": form})


def manage_asset(request, id, action):
    asset = get_object_or_404(AssetInfo, id=id)
    user_list = UserInfo.objects.all()
    host_type_list = AssetTypeList.objects.all()

    if action == "assetedit":
        if request.method == "POST":
            form = AssetForm(request.POST, instance=asset)
            if form.is_valid():
                form.save()
                messages.success(request, "资产信息已成功更新！")
                return redirect("asset_list")
        else:
            form = AssetForm(instance=asset)

        return render(
            request,
            "property/manage_asset.html",
            {
                "form": form,
                "asset": asset,
                "action": "assetedit",
                "host_type_list": host_type_list,
                "user_list": user_list,
                "status_choices": AssetInfo.STATUS_CHOICES,
            },
        )

    elif action == "scrap":
        if request.method == "POST":
            asset.delete()
            messages.success(request, "资产已成功报废删除！")
            return redirect("asset_list")

        return render(
            request,
            "property/manage_asset.html",
            {
                "asset": asset,
                "action": "scrap",
            },
        )

    elif action == "idle":
        if request.method == "POST":
            asset.host_status = "闲置"
            asset.host_user = None
            asset.save()
            messages.success(request, "资产已成功清空用户信息！")
            return redirect("asset_list")

        return render(
            request,
            "property/manage_asset.html",
            {
                "asset": asset,
                "action": "idle",
            },
        )

    messages.error(request, "不支持的操作。")
    return redirect("asset_list")


@login_required
def import_assets(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        if file.name.endswith(".csv"):
            try:
                data = pd.read_csv(file)

                def create_asset_info(row):
                    try:
                        # 验证必填字段
                        host_name = row.get("设备名称")
                        service_tag = row.get("设备序列号")

                        if not host_name:
                            raise ValueError("设备名称不能为空")
                        if not service_tag:
                            raise ValueError("设备序列号不能为空")

                        # 获取设备类别，处理异常
                        host_type_name = row.get("设备类别")
                        if host_type_name:
                            try:
                                host_type = AssetTypeList.objects.get(type_name=host_type_name)
                            except AssetTypeList.DoesNotExist:
                                
                                host_type = AssetTypeList.objects.get(type_name="未知设备")
                        
                        # 获取用户信息，处理异常
                        host_user_name = row.get("使用用户")
                        if host_user_name:
                            try:
                                host_user = UserInfo.objects.get(user_name=host_user_name)
                            except UserInfo.DoesNotExist:
                        
                                host_user = UserInfo.objects.get(user_name="Notuser")

                        # 自动填写采购日期和设备状态
                        receive_date = pd.to_datetime(row.get("采购日期"), errors='coerce') if row.get("采购日期") else timezone.now().date()
                        if pd.isna(receive_date):
                            receive_date = timezone.now().date()  # 如果无法解析日期，使用当前日期

                        host_status = row.get("设备状态")
                        if pd.isna(host_status) or (isinstance(host_status, str) and not host_status.strip()):
                            host_status = "闲置"


                        # 创建资产信息
                        AssetInfo.objects.create(
                            host_name=host_name,
                            service_tag=service_tag,
                            host_type=host_type,
                            host_model=row.get("设备型号", ""),
                            receive_date=receive_date,
                            host_user=host_user,
                            host_status=host_status,
                            remark=row.get("备注", ""),
                        )
                    except ValueError as e:
                        messages.error(request, f"导入失败: {str(e)}")
                        return False  # 表示导入失败
                    return True  # 表示导入成功

                # 批量创建资产信息
                success_count = 0
                for index, row in data.iterrows():
                    if create_asset_info(row):
                        success_count += 1

                messages.success(request, f"成功导入 {success_count} 条资产信息！")
            except Exception as e:
                messages.error(request, f"导入失败: {str(e)}")
        else:
            messages.error(request, "请上传有效的 CSV 文件。")
    return render(request, "property/import_assets.html")

@login_required
def export_assets(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="assets.csv"'

    writer = csv.writer(response)
    response.write("\ufeff".encode("utf-8"))

    # 写入 CSV 头
    writer.writerow(
        [
            "设备名称",
            "设备序列号",
            "设备类别",
            "设备型号",
            "采购日期",
            "已购时长",  # 新增字段
            "使用用户",
            "所属部门",
            "设备状态",
            "备注",
        ]
    )

    # 获取资产信息
    assets = AssetInfo.objects.all().values_list(
        "host_name",
        "service_tag",
        "host_type__type_name",
        "host_model",
        "receive_date",
        "host_user__user_name",
        "host_user__department__dept_name",
        "host_status",
        "remark",
    )

    # 当前日期
    current_date = timezone.now().date()

    # 写入资产信息到 CSV
    for asset in assets:
        purchase_date = asset[4]  # 采购日期
        if purchase_date:
            # 计算已购时长
            duration = current_date - purchase_date
            years, months = divmod(duration.days, 30)  # 简单处理为以30天为一个月
            purchased_duration = f"{years}年{months}月"
        else:
            purchased_duration = "N/A"

        # 将已购时长加入到资产信息中
        writer.writerow(list(asset)[:5] + [purchased_duration] + list(asset)[5:])

    return response


def asset_statistics(request):
    total_assets = AssetInfo.objects.count()
    asset_count_by_type = AssetInfo.objects.values(
        "host_type__type_name"
    ).annotate(  # 修改为 type_name
        count=Count("id")
    )

    context = {
        "total_assets": total_assets,
        "asset_count_by_type": asset_count_by_type,
    }
    return render(request, "property/asset_statistics.html", context)

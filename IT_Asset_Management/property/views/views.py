from django.contrib.auth.decorators import login_required
from django.shortcuts import  render
from django.db.models import Count
from property.models import AssetInfo


@login_required
def dashboard(request):
    total_assets = AssetInfo.objects.count()
    asset_status_counts = AssetInfo.objects.values("host_status").annotate(
        count=Count("id")
    )
    status_counts = {
        status["host_status"]: status["count"] for status in asset_status_counts
    }

    return render(
        request,
        "property/dashboard.html",
        {
            "total_assets": total_assets,
            "idle_assets": status_counts.get("闲置", 0),
            "in_use_assets": status_counts.get("使用中", 0),
            "discarded_assets": status_counts.get("等待报废", 0),
        },
    )

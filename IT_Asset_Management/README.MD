IT_ASSET_MANAGEMENT/
├── manage.py
├── db.sqlite3
├── property/                  # 应用程序文件夹
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/          # 数据库迁移文件
│   │   └── __init__.py
│   ├── models.py            # 数据模型定义
│   ├── urls.py              # URL 路由
│   ├── assetform.py         # 
│   ├── views.py             # 视图函数
│   ├── templates/           # 模板文件夹
│   │   └── property/
│   │       ├── base.html    # 基础模板
│   │       ├── asset_list.html  # 资产列表模板
│   │       ├── asset_statistics.html  # 资产统计模板
│   │       ├── manage_assets.html  # 资产管理操作模板
│   │       ├── add_asset.html    # 添加资产模板
│   │       ├── edit_asset.html   # 编辑资产模板
│   │       ├── import_assets.html # 导入资产模板
│   │       ├── login.html    # 登录模板
│   │       └── register.html  # 注册模板
│   └── static/              # 静态文件
│       └── property/
│           └── css/
│               └── style.css
└── IT_Asset_Management/              # 项目文件夹
    ├── __init__.py
    ├── settings.py          # 项目设置
    ├── urls.py              # 项目 URL 路由
    └── wsgi.py              # WSGI 配置文件




django-admin startproject asset_management
python manage.py startapp assets
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


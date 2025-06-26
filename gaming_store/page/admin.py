from django.contrib import admin

# Register your models here.
admin.site.site_header = "Gaming Store Admin"
admin.site.site_title = "Gaming Store Admin Portal"
admin.site.index_title = "Welcome to the Gaming Store Admin Portal"
# You can register your models here if you have any
# For example:
# from .models import YourModel
# admin.site.register(YourModel)
# If you have any custom admin views, you can add them here as well
# For example:
# from django.urls import path
# from .views import custom_admin_view
# admin.site.register_view('custom-view', view=custom_admin_view, name='Custom View')
# If you have any custom admin actions, you can define them here
# For example:
# from django.contrib import messages
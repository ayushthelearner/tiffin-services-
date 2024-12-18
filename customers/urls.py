from django.urls import path
from . import views



from django.contrib import admin

admin.site.site_header = 'Tiffin Treat Tiffin services ( Administration panel ) '                    # default: "Django Administration"
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'HTML title from adminsitration' # default: "Django site admin"



urlpatterns = [
  
   path("", views.PlanSelection, name="PlanSelect"),
   path("customerCredentials/",views.TwoWeekVegPlan,name="TwoWeekVeg"),
   path("thankyou/",views.LastPage,name="LastPage"),
   path("FreeTrials/",views.Free, name="Free"),
   path("OneMonthVeg/",views.OneMonthVeg, name="OneMonthVeg"),
   path("OneMonthVegNonVeg/",views.OneMonthVegNonVeg, name="OneMonthVegNonVeg"),
   path("ThreeMonthVeg/",views.ThreeMonthVeg, name="ThreeMonthVeg"),
   path("ThreeMonthVegNonveg/",views.ThreeMonthVegNonveg, name="ThreeMonthVegNonveg"),
   

]

from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path


from .views import (quotelog_create,QuoteLogListView,update_quotelogs,QuoteLogDetialView,\
    get_codes,QLManagement_DetialView,managementAnalytics,countsmanagement,\
    biztype_winratio_API
)

urlpatterns = [ 
    path('create_ql/', quotelog_create,name='create_ql'),  # create a quote log
    path('view_ql/', login_required(QuoteLogListView.as_view()),name='view_ql'),  # view all ql
    path('detialed_ql/<int:pk>', login_required(QuoteLogDetialView.as_view()),name='detialed_ql'),  # update a quote log by id
    path('mng/', login_required(QLManagement_DetialView.as_view()),name='mng'), 
    path('update_ql/<int:id>',update_quotelogs,name='update_ql'),  # update a quote log by id
    path('codes/<str:country>', get_codes,name='get_codes'),  # update a quote log by id
    path('countsmain',managementAnalytics,name='countsmain'),
    path('countsmng',countsmanagement,name='countsmng'),
    # winratios
    path('bizratioapi',biztype_winratio_API,name='bizratioapi'),
]
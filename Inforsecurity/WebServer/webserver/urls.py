from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webadmin.views.home', name='home'),
    # url(r'^webadmin/', include('webadmin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'engine.account.user_login'),
    url(r'^accounts/resetpwd/$', 'engine.account.reset_password'),
    url(r'^accounts/logout/$',  'django.contrib.auth.views.logout',
                                {'next_page': '/accounts/login/'}
                                ),
    url(r'^accounts/sendverifycode/', 'engine.account.sendverifycode'),
    url(r'^accounts/login_post/$', 'engine.account.user_login_post'),
    url(r'^accounts/fogetpwd/$', 'engine.account.fogetpwd'),
    url(r'^accounts/refindpwd/$', 'engine.account.refindpwd'),
    url(r'^accounts/register/$', 'engine.account.register'),
    url(r'^accounts/changeinfo/$', 'engine.account.changeinfo'),
    url(r'^accounts/get_user_userid/$', 'engine.account.get_user_userid'), 
    

    url(r'^$', 'engine.account.homepage'),
    url(r'^accounts/get_alarm_count/$', 'engine.account.get_alarm_count'),
    #url(r'^statistic/ip/$', 'engine.views.statistic_ip'),
    #url(r'^statistic/url/$', 'engine.views.statistic_url'),
    #url(r'^statistic/trojan/$', 'engine.views.statistic_trojan'),
    #by hyq
    url(r'^dashboard/general/', 'engine.dashboard.general'),
    url(r'^ajax/dashboard/general/', 'engine.dashboard.ajaxgeneral'),
    url(r'^dashboard/general_detail/', 'engine.dashboard.general_detail'),
    url(r'^ajax/dashboard/get_angular_data/', 'engine.dashboard.get_angular_data'),
    url(r'^ajax/dashboard/get_chart_data/', 'engine.dashboard.get_chart_data'),
    url(r'^ajax/dashboard/get_chartdt_data/', 'engine.dashboard.get_chartdt_data'),
    url(r'^ajax/dashboard/get_user_riskvalue/', 'engine.dashboard.get_user_riskvalue'),


    url(r'^ajax/dashboard/statistic_ip/', 'engine.dashboard.statistic_ip'),
    url(r'^ajax/dashboard/statistic_weekip/', 'engine.dashboard.statistic_weekip'),

#--------------------------------------------alarm_list----------------------------------------------------------------------------
    url(r'^alarmlist/get_user_alarmpre/', 'engine.alarmlist.get_user_alarmpre'),
    url(r'^ajax/get_user_alarmpre_list/', 'engine.alarmlist.get_user_alarmpre_list'),  
#--------------------------------------------xiaonan----------------------------------------------------------------------------
    url(r'^ajax/dashboard/statistic_url/', 'engine.dashboard.statistic_url'),
    url(r'^ajax/dashboard/statistic_weekurl/', 'engine.dashboard.statistic_weekurl'),
    url(r'^accounts/get_user_info/$', 'engine.account.get_user_info'),
#---------------------------------------------end-------------------------------------------------------------------------------

    
#by fengya
    url(r'^ajax/dashboard/statistic_email/', 'engine.dashboard.statistic_email'),
    url(r'^ajax/dashboard/statistic_weekemail/', 'engine.dashboard.statistic_weekemail'),

    url(r'^usersettings/alarm_list/$', 'engine.usersettings.alarm_list'),
    # url(r'^usersettings/get_user_alarm_list/$', 'engine.usersettings.get_user_alarm_list'),
    url(r'^usersettings/get_alarm_list/$', 'engine.usersettings.get_alarm_list'),

    url(r'^ajax/dashboard/userstatistic_url/', 'engine.dashboard.userstatistic_url'),
    url(r'^ajax/dashboard/userstatistic_weekurl/', 'engine.dashboard.userstatistic_weekurl'),

#-----------------------------------------------black_list----------------------------------------------------------------------
    #balck_IP
    url(r'^management/blackIP/$', 'engine.blacklistmanage.black_ip'),
    url(r'^ajax/get_blackip_list/$', 'engine.blacklistmanage.get_blackip_list'),
    url(r'^ajax/delete_blackip/$', 'engine.blacklistmanage.delete_blackip'),
    url(r'^ajax/edit_blackip/$', 'engine.blacklistmanage.edit_blackip'),
    url(r'^management/blackip_search/$', 'engine.blacklistmanage.blackip_search'),

    #balck_url
    url(r'^management/blackURL/$', 'engine.blacklistmanage.black_url'),
    url(r'^ajax/get_blackurl_list/$', 'engine.blacklistmanage.get_blackurl_list'),
    url(r'^ajax/delete_blackurl/$', 'engine.blacklistmanage.delete_blackurl'),
    url(r'^ajax/edit_blackurl/$', 'engine.blacklistmanage.edit_blackurl'),
    url(r'^management/blackurl_search/$', 'engine.blacklistmanage.blackurl_search'),

    #balck_email
    url(r'^management/blackemail/$', 'engine.blacklistmanage.black_email'),
    url(r'^ajax/get_blackemails_list/$', 'engine.blacklistmanage.get_blackemails_list'), 
    url(r'^ajax/delete_blackemail/$', 'engine.blacklistmanage.delete_blackemail'),
    url(r'^ajax/edit_blackemail/$', 'engine.blacklistmanage.edit_blackemail'),
    url(r'^management/email_search/$', 'engine.blacklistmanage.blackemail_search'),
    

#-----------------------------------------------statistic----------------------------------------------------------------------
    #statistic_email
    url(r'^statistic/email/$', 'engine.statistics.statistic_email'),
    url(r'^ajax/get_resemails_list/$', 'engine.statistics.get_resemails_list'), 
    url(r'^ajax/get_resemails_detail_list/$', 'engine.statistics.get_detail_resemails_list'),
    url(r'^statistic/email_search/$', 'engine.statistics.statistic_email_search'),

    #statistic_url
    url(r'^statistic/url/', 'engine.statistics.statistic_url'),
    url(r'^ajax/get_resurls_list/$', 'engine.statistics.get_resurls_list'),
    url(r'^ajax/get_resurls_detail_list/$', 'engine.statistics.get_detail_resurls_list'),
    url(r'^statistic/url_search/$', 'engine.statistics.statistic_url_search'),
    
    #statistic_ip
    url(r'^statistic/ip/', 'engine.statistics.statistic_ip'),
    url(r'^ajax/get_resips_list/$', 'engine.statistics.get_resips_list'),
    url(r'^ajax/get_resips_detail_list/$', 'engine.statistics.get_detail_resips_list'),
    url(r'^statistic/ip_search/$', 'engine.statistics.statistic_ip_search'),

#-----------------------------------------------userstatistic----------------------------------------------------------------------
    #user_statistic_email
    url(r'^user_statistic/email/$', 'engine.userstatistic.user_statistic_email'),
    url(r'^ajax/get_user_resemails_list/$', 'engine.userstatistic.get_user_resemails_list'), 
    url(r'^ajax/get_user_resemails_detail_list/$', 'engine.userstatistic.get_user_detail_resemails_list'),
    url(r'^user_statistic/email_search/$', 'engine.userstatistic.user_statistic_email_search'),
    url(r'^ajax/add_white_email/$', 'engine.userstatistic.add_white_email'),
    url(r'^ajax/dashboard/user_statistic_email/$', 'engine.dashboard.user_statistic_email'),
    url(r'^ajax/dashboard/user_statistic_weekemail/$', 'engine.dashboard.user_statistic_weekemail'),


    #user_statistic_url
    url(r'^user_statistic/url/', 'engine.userstatistic.user_statistic_url'),
    url(r'^ajax/get_user_resurls_list/$', 'engine.userstatistic.get_user_resurls_list'),
    url(r'^ajax/get_user_resurls_detail_list/$', 'engine.userstatistic.get_user_detail_resurls_list'),
    url(r'^user_statistic/url_search/$', 'engine.userstatistic.user_statistic_url_search'),
    url(r'^ajax/add_white_url/$', 'engine.userstatistic.add_white_url'),
    
    #user_statistic_ip
    url(r'^user_statistic/ip/', 'engine.userstatistic.user_statistic_ip'),
    url(r'^ajax/get_user_resips_list/$', 'engine.userstatistic.get_user_resips_list'),
    url(r'^ajax/get_user_resips_detail_list/$', 'engine.userstatistic.get_user_detail_resips_list'),

    url(r'^user_statistic/ip_search/$', 'engine.userstatistic.user_statistic_ip_search'),
    url(r'^ajax/add_white_ip/$', 'engine.userstatistic.add_white_ip'),
    url(r'^ajax/dashboard/user_statistic_ip/$', 'engine.dashboard.user_statistic_ip'),
    url(r'^ajax/dashboard/user_statistic_weekip/$', 'engine.dashboard.user_statistic_weekip'),
   
    #user_statistic_net
    url(r'^user_statistic/net/', 'engine.userstatistic.user_statistic_net'),
    url(r'^ajax/get_net_behaviour_list/$', 'engine.userstatistic.get_net_behaviour_list'),
    url(r'^userstatistic/net_behaviour_search/$', 'engine.userstatistic.net_behaviour_search'),

    #user_statistic_driver
    url(r'^user_statistic/driver/', 'engine.userstatistic.user_statistic_driver'),
    url(r'^ajax/get_driver_behaviour_list/$', 'engine.userstatistic.get_driver_behaviour_list'),

    #user_statistic_driver_compare
    url(r'^user_statistic/driver_compare/', 'engine.userstatistic.user_statistic_driver_compare'),
    url(r'^ajax/userstatistic/get_driver_compare_data/$', 'engine.userstatistic.get_driver_compare_data_list'),

    #user_statistic_net_compare
    url(r'^user_statistic/net_compare/', 'engine.userstatistic.user_statistic_net_compare'),
    url(r'^ajax/userstatistic/get_net_compare_data/$', 'engine.userstatistic.get_net_compare_data_list'),


#-----------------------------------------------whitelistmanage----------------------------------------------------------------------
    #white_email
    url(r'^usersettings/white_email/$', 'engine.usersettings.white_email'),
    url(r'^ajax/get_white_email_list/$', 'engine.usersettings.get_white_email_list'),
    url(r'^ajax/delete_white_email/$', 'engine.usersettings.delete_white_email'),
    
    #white_ip
    url(r'^usersettings/white_ip/$', 'engine.usersettings.white_ip'),
    url(r'^ajax/get_white_ip_list/$', 'engine.usersettings.get_white_ip_list'),
    url(r'^ajax/delete_white_ip/$', 'engine.usersettings.delete_white_ip'),
        
    #white_url
    url(r'^usersettings/white_url/$', 'engine.usersettings.white_url'),
    url(r'^ajax/get_white_url_list/$', 'engine.usersettings.get_white_url_list'),
    url(r'^ajax/delete_white_url/$', 'engine.usersettings.delete_white_url'),
    
    #risk_manage
    url(r'^usersettings/risk_manage/$', 'engine.usersettings.risk_manage'),
    url(r'^usersettings/risk_manage_post/', 'engine.usersettings.risk_manage_post'),
#-----------------------------------------------systemmanage----------------------------------------------------------------------
    
    #jobmanage
    url(r'^systemmanage/job_manage/', 'engine.sysmanage.job_manage'),
    #processmange
    url(r'^systemmanage/process_manage/', 'engine.sysmanage.process_manage'),

    # url(r'^management/blackemail/$', 'engine.blacklistmanage.black_email'),
    url(r'^ajax/get_whiteprocess_list/$', 'engine.sysmanage.get_whiteprocess_list'), 
    url(r'^ajax/delete_whiteprocess/$', 'engine.sysmanage.delete_whiteprocess'),
    url(r'^ajax/edit_whiteprocess/$', 'engine.sysmanage.edit_whiteprocess'),
    url(r'^systemmanage/whiteprocess_search/$', 'engine.sysmanage.whiteprocess_search'),
    url(r'^systemmanage/client_download/$', 'engine.sysmanage.client_download'),

#-----------------------------------------------sysmanage----------------------------------------------------------------------

    url(r'^sysmanage/get_register/$', 'engine.sysmanage.get_register'),
    url(r'^ajax/get_register_list/$', 'engine.sysmanage.get_register_list'),
    
    url(r'^sysmanage/get_user/$', 'engine.sysmanage.get_user'),
    url(r'^ajax/get_user_list/$', 'engine.sysmanage.get_user_list'),
    url(r'^ajax/prove_user/$', 'engine.sysmanage.prove_user'),


    
    #end hyq
    # url(r'^captcha/', include('captcha.urls')),
    #url(r'^test/ajax/stock/$','engine.ajax.stockajax'),
#    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),
#    url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
#    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^templates/form_elements', 'engine.tests.test_form_elements'),
    url(r'^templates/form_layouts', 'engine.tests.test_form_layouts'),
    url(r'^templates/form_wizard', 'engine.tests.test_form_wizard'),


    # url(r'^dashboard/general/', 'engine.dashboard.general'),    
    url(r'^register/job/$', 'engine.account.job'),    
    url(r'^captcha/', include('captcha.urls')),

)

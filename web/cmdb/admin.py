from django.contrib import admin
from .models import *

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','device_type', 'name',
                    'hostname','businessunit',
                    'admin','idc','cabinet_num','status')
    list_filter = ('idc','businessunit','status','device_type')
    search_fields = ['hostname','id']
class ServerAdmin(admin.ModelAdmin):
    readonly_fields = ('update_at',)
    # list_display=('asset','from_idc','sn','cpu_count','cpu_model','ram_size','manufactory','model','update_at')
    list_display = (
    'asset', 'sn', 'from_idc', 'cpu_count', 'cpu_model', 'ram_size', 'manufactory', 'model', 'update_time', 'update_at')
    search_fields = ['sn', 'asset__hostname']
    # list_filter = ('manufactory','update_at','asset__idc')
    list_filter = ('manufactory', ('update_at'), 'asset__idc')
    filter_horizontal = ('nic', 'physical_disk_driver', 'ram', 'raid_adaptor', 'software')

    # date_hierarchy = 'update_at'
    def from_idc(self, obj):
        return '%s' % obj.asset.idc

    from_idc.short_description = 'IDC'

    def update_time(self, obj):
        return obj.update_at.strftime('%Y-%m-%d %H:%M:%S')

    update_time.short_description = u'更新时间'
class NICAdmin(admin.ModelAdmin):
    search_fields = ['sn', 'mac']
    list_display=('sn','model','name','ip','mac')
class RAMAdmin(admin.ModelAdmin):
    list_display=('sn','model','slot','manufactory')
class NetworkAdmin(admin.ModelAdmin):
    list_display=('sn','manufactory', 'model','firmware','port_num','device_detail')
class SoftwareAdmin(admin.ModelAdmin):
    list_display=('version','types')
'''
class ContractAdmin(admin.ModelAdmin):
    list_display=('sn','name','cost','start_date','end_date','license_num')
'''
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('user','name','department','email',
                  'phone','mobile','back_name','leader')
class MaintainenceAdmin(admin.ModelAdmin):
    list_display=('name','maintain_type','device_sn','description','applicant','event_start','event_end','performer')
    list_filter = ('name','maintain_type','applicant','event_start')
    #date_hierarchy = 'event_start'
    search_fields = ('device_sn',)
class RaidAdaptorAdmin(admin.ModelAdmin):
    list_display=('name','sn','model','comment')
class DiskAdmin(admin.ModelAdmin):
    search_fields = ['sn']
    list_display=('slot','sn','model','iface_type')
class CPUAdmin(admin.ModelAdmin):
    search_fields = ['sn']
    list_display=('sn','model')
class EventLogAdmin(admin.ModelAdmin):
    search_fields = ['uuid','detail','post_data']
    list_display=('id','uuid','detail','create_at')
    list_filter = ('create_at',)
    #date_hierarchy = 'create_at'
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id','os_installed','puppet_installed','zabbix_configured','auditing_configured','approved')

class ApiAuthAdmin(admin.ModelAdmin):
    list_display = ('url', 'method_type','description')

admin.site.register(Idc)
admin.site.register(Assets, AssetAdmin)
admin.site.register(Manufactures)
admin.site.register(Server,ServerAdmin)
admin.site.register(ApiAuth, ApiAuthAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(NetworkDevice,NetworkAdmin)
admin.site.register(Software,SoftwareAdmin)
admin.site.register(Disk,DiskAdmin)
admin.site.register(CPU,CPUAdmin)
admin.site.register(NIC,NICAdmin)
admin.site.register(ProductVersion)
admin.site.register(BusinessUnit)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Maintainence,MaintainenceAdmin)
admin.site.register(Mem, RAMAdmin)
admin.site.register(Monitor)
admin.site.register(RaidAdaptor,RaidAdaptorAdmin)
admin.site.register(EventLog,EventLogAdmin)


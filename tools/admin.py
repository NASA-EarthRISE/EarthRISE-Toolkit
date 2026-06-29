from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import resources

from .models import (
    Application, Like, Organization,
    Log, Feedback, DeploymentEnvironment, Dataset,
    ApplicationComponent, Developer, Scientist, Link, ExternalApp,
)

admin.site.site_header = "EarthRISE Toolkit Admin"
admin.site.site_title = "EarthRISE Toolkit"
admin.site.index_title = "Tool Management"


# ---------------------------------------------------------------------------
# ApplicationComponent
# ---------------------------------------------------------------------------
class ApplicationComponentResource(resources.ModelResource):
    class Meta:
        model = ApplicationComponent


class ApplicationComponentAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = ApplicationComponentResource
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)


admin.site.register(ApplicationComponent, ApplicationComponentAdmin)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class LogInline(admin.TabularInline):
    model = Log
    extra = 1


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 1


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


class ApplicationResource(resources.ModelResource):
    class Meta:
        model = Application


class ApplicationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = ApplicationResource
    list_display = ('name', 'organization', 'active', 'shown', 'display_priority', 'incomplete_info', 'total_likes')
    list_filter = ('active', 'shown', 'ast_round', 'organization')
    search_fields = ('name', 'description', 'organization__name')
    filter_horizontal = (
        'datasets', 'scientists', 'developers',
        'deployment_environment', 'application_components',
    )
    ordering = ('display_priority', 'name')
    inlines = [LinkInline, LogInline, FeedbackInline]
    readonly_fields = ('total_likes',)
    fieldsets = (
        ('Identification', {
            'fields': ('name', 'description', 'total_likes', 'url', 'hero', 'organization'),
        }),
        ('Infrastructure', {
            'fields': (
                'deployment_environment', 'deployment_env_further_details',
                'application_components', 'datasets',
            ),
        }),
        ('AST Involvement', {
            'fields': ('ast_pi', 'ast_round'),
        }),
        ('Teams', {
            'fields': ('developers', 'scientists'),
        }),
        ('Repository & Documentation', {
            'fields': ('code_repo_url', 'design_documentation_url'),
        }),
        ('Status', {
            'fields': (
                'date_released', 'active', 'date_decommissioned',
                'shown', 'display_priority', 'incomplete_info',
            ),
        }),
        ('Platform', {
            'fields': ('platform_description',),
        }),
    )

    def total_likes(self, obj):
        return obj.like_count()

    total_likes.short_description = 'Total Likes'


admin.site.register(Application, ApplicationAdmin)


# ---------------------------------------------------------------------------
# Link
# ---------------------------------------------------------------------------
class LinkResource(resources.ModelResource):
    class Meta:
        model = Link


class LinkAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = LinkResource
    list_display = ('application', 'url', 'description')
    list_filter = ('application',)
    search_fields = ('application__name', 'description', 'url')
    ordering = ('application',)


admin.site.register(Link, LinkAdmin)


# ---------------------------------------------------------------------------
# Organization
# ---------------------------------------------------------------------------
class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization


class OrganizationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = OrganizationResource
    list_display = ('name', 'description', 'url', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)


admin.site.register(Organization, OrganizationAdmin)


# ---------------------------------------------------------------------------
# Developer
# ---------------------------------------------------------------------------
class DeveloperResource(resources.ModelResource):
    class Meta:
        model = Developer


class DeveloperAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = DeveloperResource
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)


admin.site.register(Developer, DeveloperAdmin)


# ---------------------------------------------------------------------------
# Scientist
# ---------------------------------------------------------------------------
class ScientistResource(resources.ModelResource):
    class Meta:
        model = Scientist


class ScientistAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = ScientistResource
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)


admin.site.register(Scientist, ScientistAdmin)


# ---------------------------------------------------------------------------
# Log
# ---------------------------------------------------------------------------
class LogResource(resources.ModelResource):
    class Meta:
        model = Log


class LogAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = LogResource
    list_display = ('application', 'date_modified', 'log_entry', 'user')
    list_filter = ('application',)
    search_fields = ('application__name', 'log_entry', 'user__username')
    ordering = ('application',)
    date_hierarchy = 'date_added'


admin.site.register(Log, LogAdmin)


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------
class FeedbackAdminForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['application'].required = False


class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback


class FeedbackAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    form = FeedbackAdminForm
    resource_class = FeedbackResource
    list_display = ('application', 'date_modified', 'feedback_entry', 'user', 'resolved')
    list_filter = ('application', 'resolved')
    search_fields = ('application__name', 'feedback_entry', 'user__username')
    ordering = ('application',)
    date_hierarchy = 'date_added'


admin.site.register(Feedback, FeedbackAdmin)


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------
class DatasetResource(resources.ModelResource):
    class Meta:
        model = Dataset


class DatasetAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = DatasetResource
    list_display = ('name', 'description', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)


admin.site.register(Dataset, DatasetAdmin)


# ---------------------------------------------------------------------------
# DeploymentEnvironment
# ---------------------------------------------------------------------------
class DeploymentEnvironmentResource(resources.ModelResource):
    class Meta:
        model = DeploymentEnvironment


class DeploymentEnvironmentAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = DeploymentEnvironmentResource
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)


admin.site.register(DeploymentEnvironment, DeploymentEnvironmentAdmin)


# ---------------------------------------------------------------------------
# Like
# ---------------------------------------------------------------------------
admin.site.register(Like)


# ---------------------------------------------------------------------------
# ExternalApp
# ---------------------------------------------------------------------------
class ExternalAppResource(resources.ModelResource):
    class Meta:
        model = ExternalApp


class ExternalAppAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = ExternalAppResource
    list_display = ('name', 'description', 'url', 'user', 'date_added')
    search_fields = ('name', 'description', 'url')
    ordering = ('name',)
    date_hierarchy = 'date_added'


admin.site.register(ExternalApp, ExternalAppAdmin)

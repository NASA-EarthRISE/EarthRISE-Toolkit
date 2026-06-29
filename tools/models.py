from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


# ---------------------------------------------------------------------------
# Application (Tool) model — main model
# ---------------------------------------------------------------------------
class Application(models.Model):
    name = models.CharField(help_text="Application name", max_length=250)
    description = models.TextField(help_text="Brief application description", blank=True)
    url = models.URLField(max_length=200, blank=True)
    hero = models.ImageField(upload_to='heroes/', blank=True)
    organization = models.ForeignKey(
        'Organization', on_delete=models.CASCADE,
        help_text="Organization that developed the application", blank=True, null=True
    )
    datasets = models.ManyToManyField('Dataset', blank=True)
    active = models.BooleanField(default=True, help_text="Is this application active?")
    shown = models.BooleanField(default=False, help_text="Is this application visible?")
    developers = models.ManyToManyField('Developer', blank=True, related_name='developers')
    scientists = models.ManyToManyField('Scientist', blank=True)
    code_repo_url = models.URLField(max_length=250, blank=True, help_text="Code repository location")
    design_documentation_url = models.URLField(max_length=250, blank=True, help_text="Design documentation location")
    application_components = models.ManyToManyField('ApplicationComponent', blank=True)
    platform_description = models.TextField(help_text="Brief description of platform used", blank=True)
    deployment_environment = models.ManyToManyField('DeploymentEnvironment', blank=True)
    deployment_env_further_details = models.TextField(
        help_text="Further details about the deployment environment", blank=True
    )
    date_released = models.DateField(
        default=timezone.now, help_text="Approximate date the application was released"
    )
    date_decommissioned = models.DateField(
        blank=True, null=True, help_text="Approximate date the application was decommissioned"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    display_priority = models.IntegerField(
        help_text="Display priority (lower numbers shown at the top)", default=10, blank=True
    )
    incomplete_info = models.BooleanField(default=True, help_text="Application needs more information?")
    ast_pi = models.ForeignKey(
        'Scientist', on_delete=models.SET_NULL, related_name="PI_Scientist",
        help_text="PI Scientist when the application was developed",
        blank=True, default=None, null=True
    )
    ast_round = models.IntegerField(
        help_text="AST round involved with when the app was created",
        default=None, blank=True, null=True
    )

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tool_detail', kwargs={'pk': self.pk})

    def like_count(self):
        return self.like_set.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_priority', 'name']


# ---------------------------------------------------------------------------
# Like model
# ---------------------------------------------------------------------------
class Like(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, default=None, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user.username} likes {self.application.name}"

    class Meta:
        unique_together = ('user', 'application')


# ---------------------------------------------------------------------------
# Organization model
# ---------------------------------------------------------------------------
class Organization(models.Model):
    name = models.CharField(help_text="Name of the organization", max_length=250)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=200, blank=True)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Log model
# ---------------------------------------------------------------------------
class Log(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    log_entry = models.TextField()
    date = models.DateField(help_text="Date issue or milestone happened", blank=True, default=date.today)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')

    def __str__(self):
        return self.application.name


# ---------------------------------------------------------------------------
# Feedback model
# ---------------------------------------------------------------------------
class Feedback(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, default=None, null=True)
    feedback_entry = models.TextField()
    date = models.DateField(help_text="Date feedback reported", blank=True, default=date.today)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


# ---------------------------------------------------------------------------
# DeploymentEnvironment model
# ---------------------------------------------------------------------------
class DeploymentEnvironment(models.Model):
    name = models.CharField(help_text="Name of the deployment environment", max_length=250)
    description = models.TextField(help_text="Brief description of the deployment environment", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField(
        'Application', through=Application.deployment_environment.through, blank=True
    )

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Dataset model
# ---------------------------------------------------------------------------
class Dataset(models.Model):
    name = models.CharField(help_text="Name of the dataset", max_length=250)
    description = models.TextField(help_text="Brief description of the dataset", blank=True)
    url = models.URLField(max_length=200, blank=True, help_text="Dataset location")
    credentials = models.TextField(help_text="Credentials for accessing the dataset", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField(
        'Application', through=Application.datasets.through, blank=True
    )

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# ApplicationComponent model
# ---------------------------------------------------------------------------
class ApplicationComponent(models.Model):
    name = models.CharField(
        help_text="Name of the application component (include version if relevant)", max_length=250
    )
    description = models.TextField(help_text="Further details for the application component", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField(
        'Application', through=Application.application_components.through, blank=True
    )

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Developer model
# ---------------------------------------------------------------------------
class Developer(models.Model):
    name = models.CharField(help_text="Name of the developer", max_length=250)
    photo = models.ImageField(
        upload_to='icons/', blank=True, null=True,
        help_text="Square image, minimum 150px × 150px"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    active = models.BooleanField(default=True, help_text="Is the developer active?")
    applications = models.ManyToManyField(
        'Application', through=Application.developers.through, blank=True
    )

    @property
    def image_url(self):
        if self.photo:
            return self.photo.url
        return "/static/tools/img/no_profile.png"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Scientist model
# ---------------------------------------------------------------------------
class Scientist(models.Model):
    name = models.CharField(help_text="Name of the scientist", max_length=250)
    photo = models.ImageField(
        upload_to='icons/', blank=True, null=True,
        help_text="Square image, minimum 150px × 150px"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    active = models.BooleanField(default=True, help_text="Is the scientist active?")
    applications = models.ManyToManyField(
        'Application', through=Application.scientists.through, blank=True
    )

    @property
    def image_url(self):
        if self.photo:
            return self.photo.url
        return "/static/tools/img/no_profile.png"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Link model
# ---------------------------------------------------------------------------
class Link(models.Model):
    url = models.URLField(max_length=200, blank=True, help_text="Link location")
    description = models.CharField(help_text="Link description", max_length=250, blank=True)
    additional_description = models.TextField(help_text="Further details for the link", blank=True)
    application = models.ForeignKey('Application', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.url


# ---------------------------------------------------------------------------
# ExternalApp model
# ---------------------------------------------------------------------------
class ExternalApp(models.Model):
    url = models.URLField(max_length=255, help_text="Primary URL of the application", blank=True)
    name = models.CharField(help_text="Application name", max_length=250)
    description = models.TextField(help_text="Brief description. Why is the app relevant for SERVIR?", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ExternalApps')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

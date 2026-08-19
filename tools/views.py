import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import (
    Application, Scientist, Developer,
    DeploymentEnvironment, Organization,
    Dataset, ApplicationComponent,
)


# ---------------------------------------------------------------------------
# Quick-create AJAX endpoint (staff only)
# ---------------------------------------------------------------------------
_QC_MODELS = {
    'deployment_environment': (DeploymentEnvironment, ['name', 'description']),
    'dataset':                (Dataset,                ['name', 'description', 'url']),
    'application_component':  (ApplicationComponent,  ['name', 'description']),
    'scientist':              (Scientist,              ['name', 'organization']),
    'developer':              (Developer,              ['name', 'organization']),
}


@staff_member_required
@require_POST
def quick_create(request, model_type):
    config = _QC_MODELS.get(model_type)
    if not config:
        return JsonResponse({'success': False, 'error': 'Unknown type'}, status=400)

    model_cls, fields = config
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'errors': {'name': ['Name is required.']}}, status=400)

    kwargs = {'name': name}

    if 'description' in fields:
        kwargs['description'] = request.POST.get('description', '').strip()
    if 'url' in fields:
        kwargs['url'] = request.POST.get('url', '').strip()
    if 'organization' in fields:
        org_name = request.POST.get('organization', '').strip()
        org = Organization.objects.filter(name=org_name).first()
        if not org:
            return JsonResponse(
                {'success': False, 'errors': {'organization': ['Please select a valid organization.']}},
                status=400,
            )
        kwargs['organization'] = org

    obj = model_cls.objects.create(**kwargs)
    return JsonResponse({'success': True, 'name': obj.name})


def _form_options():
    return {
        'deployment_environment': list(
            DeploymentEnvironment.objects.values_list('name', flat=True).order_by('name')
        ),
        'organization': list(Organization.objects.values_list('name', flat=True).order_by('name')),
        'scientists': list(Scientist.objects.values_list('name', flat=True).order_by('name')),
        'developers': list(Developer.objects.values_list('name', flat=True).order_by('name')),
        'datasets': list(Dataset.objects.values_list('name', flat=True).order_by('name')),
        'application_components': list(
            ApplicationComponent.objects.values_list('name', flat=True).order_by('name')
        ),
    }


# ---------------------------------------------------------------------------
# Home — filterable, searchable, pageable tool thumbnail grid
# ---------------------------------------------------------------------------
def home(request):
    qs = (
        Application.objects
        .filter(active=True)
        .select_related('organization')
    )

    # Non-staff only see tools marked as shown
    if not (request.user.is_authenticated and request.user.is_staff):
        qs = qs.filter(shown=True)

    # Search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        qs = qs.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        ).distinct()

    # Organisation filter
    org_filter = request.GET.get('org', '').strip()
    if org_filter:
        qs = qs.filter(organization__name=org_filter)

    # Pagination — 12 cards per page
    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    organizations = Organization.objects.order_by('name')

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'org_filter': org_filter,
        'organizations': organizations,
        'total_count': paginator.count,
    })


# ---------------------------------------------------------------------------
# Tool Detail (staff only)
# ---------------------------------------------------------------------------
@staff_member_required
def tool_detail(request, pk):
    app = get_object_or_404(
        Application.objects
        .select_related('organization', 'ast_pi')
        .prefetch_related(
            'deployment_environment',
            'scientists__organization', 'developers__organization',
            'datasets', 'application_components',
            'link_set',
        ),
        pk=pk,
    )
    return render(request, 'tool_detail.html', {
        'app': app,
        'scientists': app.scientists.select_related('organization'),
        'developers': app.developers.select_related('organization'),
        'links': app.link_set.all(),
    })


# ---------------------------------------------------------------------------
# Add Tool (staff only)
# ---------------------------------------------------------------------------
@staff_member_required
def add_tool(request):
    if request.method == 'POST':
        org = None
        org_name = request.POST.get('organization', '').strip()
        if org_name:
            org = Organization.objects.filter(name=org_name).first()

        app = Application.objects.create(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            url=request.POST.get('url', ''),
            organization=org,
            code_repo_url=request.POST.get('code_repo_url', ''),
            design_documentation_url=request.POST.get('design_documentation_url', ''),
            platform_description=request.POST.get('platform_description', ''),
            deployment_env_further_details=request.POST.get('deployment_env_further_details', ''),
            shown=False,
        )

        hero_file = request.FILES.get('hero')
        if hero_file:
            app.hero.save(hero_file.name, hero_file, save=True)

        def _set_m2m_create(field_name, model_cls):
            names = [
                n.strip()
                for n in request.POST.get(field_name, '').split(',')
                if n.strip()
            ]
            objs = [model_cls.objects.get_or_create(name=n)[0] for n in names]
            getattr(app, field_name).set(objs)

        def _set_m2m_existing(field_name, model_cls):
            names = [
                n.strip()
                for n in request.POST.get(field_name, '').split(',')
                if n.strip()
            ]
            objs = list(model_cls.objects.filter(name__in=names))
            getattr(app, field_name).set(objs)

        _set_m2m_create('deployment_environment', DeploymentEnvironment)
        _set_m2m_existing('scientists', Scientist)
        _set_m2m_existing('developers', Developer)
        _set_m2m_existing('datasets', Dataset)
        _set_m2m_existing('application_components', ApplicationComponent)

        return redirect('tool_detail', pk=app.pk)

    options = _form_options()
    return render(request, 'add_tool.html', {
        'form_options': options,
        'form_options_json': json.dumps(options),
    })
def hds_preview(request):
    return render(request, 'hds/hds_home.html')

# EarthRISE Toolkit

[![Python: 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![EarthRISE: Development](https://img.shields.io/badge/EarthRISE-Development-b50000?labelColor=191f4c)](https://science.nasa.gov/earth-science/earth-action/earthrise/)

A Django-based catalog for Earth observation and geospatial decision-support tools developed by EarthRISE. The application provides a filterable, searchable, and pageable grid of tool thumbnails built with Bootstrap 5, jQuery, and the [NASA Horizon Design System](https://website.nasa.gov/horizon-design-system/).

---

## Features

- **Public tool catalog** — responsive thumbnail grid of active tools
- **Search** — full-text search across tool name and description (server-side, debounced client-side)
- **Filters** — filter by Service Area, Region, and Organization
- **Pagination** — 12 tools per page
- **Staff-only detail view** — full metadata, QR code, team roster, links & resources
- **Staff-only add tool form** — multi-section form with MultiSelect widgets and AJAX quick-create for related objects
- **Role-based behavior**:
  - Public users: clicking a thumbnail navigates directly to the tool URL
  - Staff users: clicking a thumbnail opens the internal detail page
- **WCAG 2.0 / Section 508 compliant** — semantic HTML, skip links, ARIA roles, sufficient contrast, keyboard-navigable components
- **Horizon Design System** — consistent color tokens, typography (Inter + Public Sans), spacing, and component styles

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 6.0.6 |
| Database | SQLite (development) |
| Frontend | Bootstrap 5.3, jQuery 3.7, Bootstrap Icons 1.11 |
| Fonts | Google Fonts — Inter (headings) + Public Sans (body) |
| Admin | Django Admin + django-import-export |
| Images | Pillow |

---

## Project Structure

```
EarthRISE_Toolkit/
├── earthrise_toolkit/          # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tools/                      # Main application
│   ├── migrations/
│   ├── models.py               # 14 models (Application, Organization, etc.)
│   ├── views.py                # home, tool_detail, add_tool, quick_create
│   ├── urls.py
│   └── admin.py                # Full admin with import/export
├── templates/
│   ├── base.html               # Horizon header/footer, Bootstrap/jQuery
│   ├── home.html               # Filterable, searchable, pageable grid
│   ├── tool_detail.html        # Staff-only detail view
│   └── add_tool.html           # Staff-only add form
├── static/
│   └── tools/
│       ├── css/
│       │   └── horizon.css     # Horizon Design System stylesheet
│       ├── js/
│       │   └── main.js         # MultiSelect widget, quick-create, utilities
│       └── img/
│           └── no_profile.png  # Default profile placeholder (add manually)
├── media/                      # User-uploaded content (auto-created)
│   ├── heroes/
│   └── icons/
├── horizon-design-system.md    # Horizon DS reference
├── manage.py
├── environment.yml
└── README.md
```

---

## Data Models

| Model | Description |
|-------|-------------|
| `Application` | Core tool record — name, description, URL, hero image, all metadata |
| `Organization` | Developing organization |
| `Service` | Individual service within a service area |
| `Dataset` | Datasets used by the tool |
| `ApplicationComponent` | Tech stack components |
| `DeploymentEnvironment` | Where the tool is deployed |
| `Developer` | Engineering team members |
| `Scientist` | Research team members |
| `Link` | Additional resource links |
| `Like` | Per-user likes (unique constraint) |
| `Log` | Change log entries |
| `Feedback` | User feedback submissions |
| `ExternalApp` | Third-party tools of interest |

---

## Setup

### Prerequisites

- [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Git (optional)

### 1. Create and activate the conda environment

```bash
conda env create -f environment.yml
conda activate earthrise-toolkit
```

### 2. Apply database migrations

```bash
python manage.py migrate
```

### 3. Create a superuser (staff account)

```bash
python manage.py createsuperuser
```

### 4. Add the no_profile placeholder image (optional)

Place a 150×150 px JPEG or PNG at:

```
static/tools/img/no_profile.png
```

This is shown as a fallback for team members without a photo.

### 5. Collect static files (production only)

```bash
python manage.py collectstatic
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Usage

### Public users

- Browse the tool catalog at `/`
- Use the search box, Service Area, Region, and Organization dropdowns to filter
- Click any tool card to navigate directly to the tool's registered URL

### Staff users

Sign in via the **Staff Sign In** button in the header (uses Django admin auth at `/admin/login/`).

After signing in:

- All active tools are visible, including those pending review
- Tool cards link to the internal **detail page** instead of the external URL
- The **Add Tool** button in the header and navigation opens the add form
- The **Edit** button on the detail page opens the Django admin change form

### Admin

Full CRUD and import/export via the Django admin panel at `/admin/`.

All models support CSV import/export via `django-import-export`.

---

## Accessibility

This application targets **WCAG 2.0 Level AA** and **Section 508** compliance:

| Feature | Implementation |
|---------|---------------|
| Skip navigation | `.hz-skip-link` — visible on focus, jumps to `#main-content` |
| ARIA landmarks | `<header role="banner">`, `<nav aria-label>`, `<main>`, `<footer role="contentinfo">` |
| ARIA live regions | Filter results count, form status messages |
| Focus management | Dotted `2px` focus ring (`#444447`) on all interactive elements |
| Color contrast | Body text `#3a3a3a` on `#F5F5F5` bg (≥ 7:1); white on `#2e2e32` (≥ 10:1) |
| Keyboard navigation | All controls (dropdowns, modals, pagination) usable via keyboard |
| Semantic HTML | `<article>`, `<section>`, `<aside>`, `<h1>`–`<h2>` hierarchy per page |
| Alternative text | All images have descriptive `alt` attributes; decorative icons use `aria-hidden` |
| Form labels | All inputs have associated `<label>` or `aria-label` attributes |

---

## Design System

Styles follow the **NASA Horizon Design System**. Key tokens defined in `static/tools/css/horizon.css`:

```css
--color-primary:   #0170B9;   /* links, badges, accents */
--color-hover:     #f64137;   /* button hover, CTA */
--color-dark:      #2e2e32;   /* header, modal headers */
--color-text:      #3a3a3a;   /* body copy */
--color-bg:        #F5F5F5;   /* page background */
--color-surface:   #FFFFFF;   /* cards, panels */
--color-border:    #dddddd;   /* dividers, input borders */
--font-body:       'Public Sans', sans-serif;
--font-heading:    'Inter', sans-serif;
```

See `horizon-design-system.md` for the full reference.

---

## Environment Variables

For production, override these settings (via environment variables or a `.env` file):

| Setting | Purpose |
|---------|---------|
| `SECRET_KEY` | Django secret key (rotate from default) |
| `DEBUG` | Set to `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `DATABASE_URL` | Switch to PostgreSQL or another production database |

---

## License

The EarthRISE Toolkit is distributed by EarthRISE under the terms of the GPLv3 License. See
[LICENSE](https://github.com/NASA-EarthRISE/EarthRISE-Toolkit/blob/main/LICENSE) in this directory for more information.

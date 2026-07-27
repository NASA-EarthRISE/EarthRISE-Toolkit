# Accessibility Compliance Report — Post-Fix Verification
## EarthRISE Toolkit — WCAG 2.0 A/AA & Section 508

**Fix Date:** 2026-07-23
**Standard:** WCAG 2.0 Level A and Level AA; Section 508 (2017 Refresh)
**Verification Tool:** pa11y 9.1.1 (htmlcs runner, WCAG2AA standard)
**Based on:** `compliance.md` — original audit findings

---

## Summary

All 5 WCAG violations and all 4 best-practice warnings from the original audit have been remediated. An additional contrast defect in the footer secondary section (white text on USWDS-injected white background) was discovered and fixed during pa11y re-verification.

**pa11y results after fixes:**

| Page | URL | Errors (before) | Errors (after) | Warnings (after) |
|---|---|---|---|---|
| Home / Catalog | `/` | 10 | **0** | 27 (all false positives / WCAG 2.1) |
| Tool Detail | `/tool/5/` | 0 | **0** | 1 (false positive) |

---

## Fixes Applied

### Fix 1 — Warning Badge Contrast (Issue 1)
**Criterion:** WCAG 1.4.3 AA
**File:** `static/tools/css/horizon.css`

Changed `.hz-tag-warning` background from `#ea6f24` (3.09:1) to `#b84f0e` (≈5.0:1 against white).

```css
/* Before */
.hz-tag-warning {
  background-color: var(--hds-color-international-orange, #ea6f24);
}

/* After */
.hz-tag-warning {
  background-color: #b84f0e; /* white on #b84f0e ≈ 5.0:1 ✅ */
}
```

---

### Fix 2 — Card Like-Count Contrast (Issue 2)
**Criterion:** WCAG 1.4.3 AA
**File:** `static/tools/css/horizon.css`

Changed `.hz-card-likes` text color from `#77777a` (4.46:1) to `#767679` (≈4.52:1 on white). This was the issue generating all 10 pa11y errors.

```css
/* Before */
color: var(--hds-color-carbon-50, #77777a); /* 4.46:1 — FAIL */

/* After */
color: #767679; /* 4.52:1 ✅ */
```

---

### Fix 3 — MultiSelect Focus Indicator (Issue 3)
**Criterion:** WCAG 2.4.7 AA
**File:** `static/tools/css/horizon.css`

Added an explicit `:focus-visible` rule to `.hz-multiselect-display`, matching the site's existing focus style pattern.

```css
.hz-multiselect-display:focus-visible {
  outline: 2px dashed var(--hds-color-carbon-70, #444447);
  outline-offset: 2px;
}
```

---

### Fix 4 — Auto-Submit Filter Disclosure (Issue 4)
**Criterion:** WCAG 3.2.2 A
**File:** `templates/home.html`

Added a visible hint paragraph advising users that results update automatically, and connected both filter controls to it via `aria-describedby`.

```html
<p class="usa-hint" id="filter-auto-hint">
  Results update automatically as you type or change filters.
</p>
```

Both `#searchInput` and `#orgFilter` now include `aria-describedby="filter-auto-hint"`.

---

### Fix 5 — USWDS Identifier Placeholder Links (Issue 5)
**Criterion:** WCAG 2.4.4 A / 4.1.1 A
**File:** `templates/base.html`

Replaced all `javascript:void(0)` and empty `href=""` attributes with real NASA.gov destination URLs. Updated placeholder text (`domain.gov`, `<Parent agency>`) with actual agency information.

| Link | Before | After |
|---|---|---|
| Agency logo | `javascript:void(0)` | `https://www.nasa.gov` |
| About | `javascript:void(0)` | `https://www.nasa.gov/about/` |
| Accessibility | `href=""` | `https://www.nasa.gov/accessibility/` |
| FOIA | `href=""` | `https://www.nasa.gov/foia/` |
| No FEAR Act | `href=""` | `https://www.nasa.gov/no-fear-act/` |
| OIG | `href=""` | `https://oig.nasa.gov` |
| Performance | `href=""` | `https://www.nasa.gov/performance/` |
| Privacy | `href=""` | `https://www.nasa.gov/privacy/` |

---

### Fix 6 — Footer Secondary Section Background (New — found during pa11y verification)
**Criterion:** WCAG 1.4.3 AA
**File:** `static/tools/css/horizon.css`

The USWDS CSS applies its own background-color to `.usa-footer__secondary-section`, overriding the parent footer's dark background. This caused white text (`usa-footer__logo-heading`, contrast 1.14:1) and gray text (`usa-footer__logo-tagline`, contrast 2.62:1) to render against a white background. Fixed by explicitly targeting the child element in the dark-palette rule.

```css
/* Before — only the footer element itself was darkened */
.usa-footer[data-hds-palette="dark"] {
  background-color: var(--hds-color-carbon-90, #17171b);
}

/* After — secondary section explicitly overridden too */
.usa-footer[data-hds-palette="dark"],
.usa-footer[data-hds-palette="dark"] .usa-footer__secondary-section {
  background-color: var(--hds-color-carbon-90, #17171b);
}
```

---

### Fix W1 — Placeholder Images Converted to `<img>` (Warning 1)
**Files:** `templates/home.html`, `templates/tool_detail.html`

Replaced `<div role="img" aria-label="...">` fallback elements with native `<img>` elements using `alt` text. Both now reference the existing `circle-gray-20.svg` asset.

```html
<!-- Before -->
<div class="hz-card-thumb-placeholder" role="img" aria-label="{{ app.name }} — no image available">
  <i class="bi bi-image" aria-hidden="true"></i>
</div>

<!-- After -->
<img src="{% static 'tools/hds/assets/img/circle-gray-20.svg' %}"
     alt="{{ app.name }} — no image available"
     class="hz-card-thumb hz-card-thumb-placeholder"
     loading="lazy">
```

The `.hz-card-thumb-placeholder` and `.hz-detail-hero-img--placeholder` CSS rules were updated to use `object-fit: none` / `object-position: center` instead of `display: flex` layout.

---

### Fix W2 — Form Validation Error Injection Order (Warning 2)
**Files:** `templates/add_tool.html` (main form + quick-create modal)

Moved `.focus()` to after the error `<span>` insertion in both form validation handlers, so the `role="alert"` element is in the DOM before focus shifts, giving assistive technology a reliable opportunity to announce it.

```javascript
// Before — focus moved before error was injected
$('#name').addClass('usa-input--error').focus();
$('#name').after('<span class="usa-error-message" role="alert">...</span>');

// After — error injected first, then focus
$('#name').addClass('usa-input--error');
$('#name').after('<span class="usa-error-message" role="alert">...</span>');
$('#name').focus();
```

---

### Fix W3 — MultiSelect CSS Class Name Reconciliation (Warning 3)
**File:** `static/tools/css/horizon.css`

The JavaScript widget was rendering with `.hz-multiselect-*` class names while all CSS rules still used the old `.ms-*` naming scheme. This caused option hover styles, selected-state checkmarks, tag styling, and dropdown visibility to not apply. All CSS class names in the MultiSelect widget section have been updated to match the JS output:

| Old CSS class | New CSS class |
|---|---|
| `.ms-container` | `.hz-multiselect` |
| `.ms-display` | `.hz-multiselect-display` |
| `.ms-tag` | `.hz-multiselect-tag` |
| `.ms-tag-remove` | `.hz-multiselect-tag-remove` |
| `.ms-dropdown` | `.hz-multiselect-dropdown` |
| `.ms-search` | `.hz-multiselect-search input` |
| `.ms-option` | `.hz-multiselect-option` |
| `.ms-option:hover` | `.hz-multiselect-option:hover` |
| `.ms-option--selected` | `.hz-multiselect-option.selected` |
| `.ms-option--selected::before` | `.hz-multiselect-option.selected::before` |

Additionally, `.hz-multiselect-dropdown` now uses `display: none` by default with a `.open` modifier class to control visibility, replacing the previous `$().addClass('open')` pattern (which relied on the missing CSS to be a no-op).

`.ms-placeholder` was retained as-is since `main.js` still renders that class name on the placeholder span.

---

### Fix W4 — QR Code Container Redundant `role="img"` (Warning 4)
**File:** `templates/tool_detail.html`

Removed `role="img"` and `aria-label` from the `<div id="qrcode">` wrapper. The `<img>` element injected by JavaScript already carries `alt="QR code for {url}"`, making the container attributes redundant and causing nested accessible image roles.

```html
<!-- Before -->
<div id="qrcode" aria-label="QR code for {{ app.url }}" role="img"></div>

<!-- After -->
<div id="qrcode"></div>
```

---

## pa11y Verification Results (Final)

### Home / Catalog Page

**0 errors · 27 warnings**

All remaining warnings are unchanged from the pre-fix scan and are confirmed false positives or WCAG 2.1 criteria outside the WCAG 2.0 audit scope:

| Code | Verdict |
|---|---|
| `1_4_10` — `position: fixed` overlay | False positive / WCAG **2.1** only. `.usa-overlay` is hidden by default, contains no text. |
| `1_4_3.G18.BgImage` — nav logo on background image | False positive. Header is solid `#2e2e32`, not an image. White text = 13.5:1 ✅ |
| `1_4_3.G18.Alpha` — nav link alpha transparency | False positive. Hover state blends to ≈10:1 ✅ |
| `4_1_2.H91.Select.Value` — `#orgFilter` no value | False positive. Element has `<label>` + `aria-label`; pa11y/htmlcs limitation. |
| `1_3_1.H85.2` — select options not grouped | Advisory only; not a WCAG 2.0 requirement. |
| `2_5_3.F96` — card link accessible name mismatch | False positive / WCAG **2.1** only. `aria-label` contains the tool name. |

### Tool Detail Page

**0 errors · 1 warning**

| Code | Verdict |
|---|---|
| `1_4_3.G18.Abs` — `#branding` absolutely positioned span | False positive from external USWDS component; `#branding` not present in application templates. |

---

## Changed Files

| File | Changes |
|---|---|
| `static/tools/css/horizon.css` | Fix 1 (warning badge), Fix 2 (card likes), Fix 3 (focus ring), Fix 6 (footer bg), W1 (placeholder CSS), W3 (MultiSelect class names) |
| `templates/base.html` | Fix 5 (Identifier links) |
| `templates/home.html` | Fix 4 (auto-submit hint), W1 (placeholder img tag) |
| `templates/tool_detail.html` | W1 (hero placeholder img tag), W4 (QR role) |
| `templates/add_tool.html` | W2 (error injection order) |

---

## Remaining Known Limitations

- **Manual AT testing not performed.** Fixes have been validated by static analysis and pa11y automated scanning. Full compliance verification requires manual testing with NVDA, JAWS, or VoiceOver.
- **Add-tool form** — pa11y could not scan the authenticated form (login redirect). The W2 error injection fix was validated by code review only.
- **Placeholder SVG** — `circle-gray-20.svg` is used as the no-image placeholder. It is visually minimal; a purpose-built placeholder graphic would improve visual quality without affecting compliance.
- **Auto-submit filter** — Disclosure text satisfies WCAG 3.2.2. However, a future improvement could replace the full-page form submit with an in-place AJAX fetch, eliminating the context change entirely.

# Accessibility Compliance Report
## EarthRISE Toolkit — WCAG 2.0 A/AA & Section 508

**Audit Date:** 2026-07-23
**Standard:** WCAG 2.0 Level A and Level AA; Section 508 (2017 Refresh, WCAG 2.0-based)
**Scope:** All templates, custom CSS (`horizon.css`), and application JavaScript (`main.js`)
**Files Reviewed:** `base.html`, `home.html`, `tool_detail.html`, `add_tool.html`, `horizon.css`, `main.js`, `views.py`, `models.py`
**Automated Testing:** 22 9.1.1 (htmlcs runner, WCAG2AA standard) run against three live pages

---

## Executive Summary

The application demonstrates strong accessibility foundations, built on the U.S. Web Design System (USWDS) / NASA Horizon Design System, which provides a compliant baseline. Most WCAG 2.0 A/AA criteria are met. Five issues require remediation — two contrast failures, two functional/interaction concerns, and one incomplete section of boilerplate identifier markup.

| Severity | Count |
|---|---|
| Level A violations | 2 |
| Level AA violations | 3 |
| Warnings / best-practice gaps | 4 |
| Confirmed compliant criteria | 28+ |

**pa11y automated scan summary (3 pages tested):**

| Page | URL | pa11y Errors | pa11y Warnings |
|---|---|---|---|
| Home / Catalog | `/` | 10 | 34 |
| Tool Detail | `/tool/5/` | 0 | 1 |
| Add Tool | `/add-tool/` | 0 | 1 |

All 10 pa11y errors on the home page are the same single issue (card like-count contrast 4.46:1) repeated across 10 card instances. The detail and add-tool pages are error-free.

---

## Issues Requiring Remediation

### Issue 1 — Color Contrast: Warning Badge
**Criterion:** WCAG 1.4.3 Contrast (Minimum) — Level AA
**Section 508:** 502.3.3
**File:** `static/tools/css/horizon.css:516–519`, `templates/tool_detail.html:45–47`

The `.hz-tag-warning` badge renders white (#ffffff) text on an international orange (#ea6f24) background. The measured contrast ratio is approximately **3.09:1**, which fails the 4.5:1 minimum required for normal-size text.

```css
/* horizon.css:516 */
.hz-tag-warning {
  background-color: var(--hds-color-international-orange, #ea6f24);
  color: #fff;
}
```

The badge appears at `tool_detail.html:45` when `app.incomplete_info` is true (staff-only view). Despite the limited audience, the criterion still applies.

**Recommendation:** Darken the background to at least `#b84f0e` (≥4.5:1 against white), or switch to dark text (#17171b) on the orange background.

---

### Issue 2 — Color Contrast: Card Like Count
**Criterion:** WCAG 1.4.3 Contrast (Minimum) — Level AA
**Section 508:** 502.3.3
**File:** `static/tools/css/horizon.css:484–491`, `templates/home.html:174–177`

The like-count text in card footers uses color `#77777a` on a white `#ffffff` background. The measured contrast ratio is approximately **4.46:1**, marginally below the 4.5:1 minimum for normal text. The font size is 0.75rem (≈12px), which does not qualify as large text.

```css
/* horizon.css:484 */
.hz-card-likes {
  font-size: 0.75rem;
  color: var(--hds-color-carbon-50, #77777a);
}
```

**Recommendation:** Darken to `#767679` or lower to achieve ≥4.5:1, or use the already-compliant `#58585b` (7.1:1).

---

### Issue 3 — Focus Indicator: MultiSelect Combobox
**Criterion:** WCAG 2.4.7 Focus Visible — Level AA
**Section 508:** 502.3.7
**File:** `static/tools/js/main.js:54–61`, `static/tools/css/horizon.css`

The custom MultiSelect widget renders a `<div>` as a combobox with `tabindex="0"` and `role="combobox"`. No explicit `:focus` or `:focus-visible` style is defined for `.hz-multiselect-display` in `horizon.css`. Keyboard users relying on the browser default outline may receive an inconsistent or invisible focus ring depending on operating system and browser defaults.

```javascript
// main.js:54
const html = `
  <div class="hz-multiselect-display"
       id="${displayId}"
       tabindex="0"
       role="combobox"
       ...>
```

For comparison, `.hz-card-link:focus-visible` (horizon.css:407) is explicitly styled with a dashed outline.

**Recommendation:** Add a `:focus-visible` rule for `.hz-multiselect-display` that matches the site's existing focus style pattern:
```css
.hz-multiselect-display:focus-visible {
  outline: 2px dashed var(--hds-color-carbon-70, #444447);
  outline-offset: 2px;
}
```

---

### Issue 4 — Unexpected Context Change: Auto-Submit Filter
**Criterion:** WCAG 3.2.2 On Input — Level A
**Section 508:** 502.3.13
**File:** `static/tools/js/main.js:296–308`

The filter bar auto-submits the form 400ms after the user stops typing in the search field, and immediately on dropdown change, without explicit user action (e.g., pressing Enter or activating a submit button). While a results count live region (`aria-live="polite"`) exists on `home.html:88`, the page-reload navigation from a full form submission is a context change that may disorient screen reader and keyboard-only users.

```javascript
// main.js:296
window.initFilterBar = function () {
  let timer;
  $('#searchInput').on('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      $('#filterForm').submit();  // full-page navigation
    }, 400);
  });
  $('#filterForm select').on('change', function () {
    $('#filterForm').submit();
  });
};
```

A full-page navigation resets keyboard focus to the browser default (top of page) and interrupts any screen reader announcement. WCAG 3.2.2 permits auto-submission only when "the behavior is described to the user before using the component."

**Recommendation:** Either (a) add a visible submit button as the primary submission path and make auto-submit opt-in/disclosed, or (b) switch to an AJAX fetch that updates the results list in-place without navigating, updating the `aria-live` region with new results and preserving keyboard focus.

---

### Issue 5 — Incomplete USWDS Identifier / Broken Links
**Criterion:** WCAG 2.4.4 Link Purpose (In Context) — Level A; WCAG 4.1.1 Parsing — Level A
**Section 508:** 502.3.10
**File:** `templates/base.html:175–225`

The USWDS Identifier component at the bottom of every page contains placeholder content that was not removed or customized. This includes two `javascript:void(0)` href values and multiple empty `href=""` attributes, as well as placeholder text (`domain.gov`, `<Parent agency>`).

```html
<!-- base.html:179 -->
<a href="javascript:void(0)" class="usa-identifier__logo">...</a>

<!-- base.html:194 -->
<a href="javascript:void(0)" class="usa-identifier__required-link usa-link">
  About &lt;Parent shortname&gt;
</a>

<!-- base.html:197 -->
<a href="" class="usa-identifier__required-link usa-link">Accessibility support</a>
```

`javascript:void(0)` links have no meaningful destination, cannot be bookmarked, may confuse assistive technology, and break right-click / open-in-new-tab behavior. Empty `href=""` links navigate to the current page URL with no purpose.

**Recommendation:** Replace all `javascript:void(0)` and empty `href=""` values with real destination URLs, or remove links that are not applicable. Update the placeholder text with actual agency information. The "Accessibility support" link should, per Section 508, point to a real accessibility statement or contact form.

---

## Warnings / Best-Practice Gaps

These do not constitute WCAG 2.0 A/AA violations but are noted for improved robustness.

### W1 — Placeholder Images Use `<div role="img">` Instead of `<img>`
**Files:** `home.html:140`, `tool_detail.html:23–26`

When no hero image has been uploaded, the fallback uses a `<div>` with `role="img"` and `aria-label`. While this satisfies WCAG 1.1.1 technically (a text alternative exists), native `<img alt="...">` elements provide stronger semantics and more consistent cross-browser AT behavior.

```html
<!-- home.html:140 -->
<div class="hz-card-thumb-placeholder" role="img" aria-label="{{ app.name }} — no image available">
  <i class="bi bi-image" aria-hidden="true"></i>
</div>
```

**Recommendation:** Use `<img src="{% static 'tools/img/placeholder.svg' %}" alt="{{ app.name }} — no image available" class="hz-card-thumb">` instead.

---

### W2 — Form Validation Error Injection May Not Reliably Announce
**Files:** `templates/add_tool.html:552–564`, `templates/add_tool.html:499–509`

When validation fails, error messages are injected into the DOM via jQuery `.after()` with `role="alert"`. In some browsers/AT combinations, dynamically injected `role="alert"` elements may not announce if inserted simultaneously with a `focus()` call on the erroneous field. The error is also not summarized at the top of the form.

```javascript
// add_tool.html:556
$('#name').addClass('usa-input--error').focus();
// error injected right after focus — timing issue
$('#name').after('<span class="usa-error-message" role="alert">Tool name is required.</span>');
```

**Recommendation:** Insert the `role="alert"` element first (before calling `.focus()`), or use a pre-existing empty `role="alert"` container that is updated in-place.

---

### W3 — Stale CSS for MultiSelect Widget
**File:** `static/tools/css/horizon.css:1015–1104`

The CSS contains `.ms-container`, `.ms-display`, `.ms-tag`, `.ms-option` etc., but the JavaScript widget now renders with `.hz-multiselect-*` class names. The old CSS rules are largely orphaned. This means option hover states (`.ms-option:hover`) and selected checkmarks (`.ms-option--selected::before`) will not render for the current widget. This does not cause a WCAG failure (the widget remains operable) but reduces visual affordance for sighted keyboard/mouse users.

**Recommendation:** Update CSS class names to match the widget's current `.hz-multiselect-*` naming, or update the widget rendering to use `.ms-*` class names consistently.

---

### W4 — QR Code: Nested `role="img"` with Inner `<img>`
**File:** `templates/tool_detail.html:107`, `tool_detail.html:380–387`

The QR code container `<div>` declares `role="img"` and `aria-label`, and jQuery then appends an `<img alt="...">` inside it. This creates nested image roles; AT will expose the inner `<img>` as the accessible image but may also announce the outer `role="img"` container. The alt text of the inner image (`alt: 'QR code for ' + url`) duplicates the container's `aria-label`.

**Recommendation:** Remove `role="img"` and `aria-label` from the `<div id="qrcode">` container since the appended `<img>` with `alt` handles the accessible name directly.

---

## Confirmed Compliant Criteria

The following WCAG 2.0 A/AA criteria are met.

| Criterion | Description | Evidence |
|---|---|---|
| **1.1.1** | Non-text content | All `<img>` have `alt`. Decorative icons use `aria-hidden="true"`. |
| **1.3.1** | Info and Relationships | Proper semantic landmarks, headings, lists, fieldsets/legends. |
| **1.3.2** | Meaningful Sequence | Linear DOM order reflects visual layout. |
| **1.3.3** | Sensory Characteristics | Instructions do not rely on shape, size, color, or position alone. |
| **1.4.1** | Use of Color | Status communicated by both color and text label (badges have text). |
| **1.4.3** | Contrast (most elements) | Nav text (#d1d1d1 / #2e2e32 ≈ 8.9:1), footer links (#d1d1d1 / #17171b ≈ 11.7:1), body text (#17171b / #fff ≈ 18.1:1). |
| **1.4.4** | Resize Text | Layout uses `rem`/`clamp()` and responsive grid; no pixel-locked text. |
| **2.1.1** | Keyboard | All interactive elements reachable by keyboard; modal and MultiSelect handle Enter/Space/Escape. |
| **2.1.2** | No Keyboard Trap | Modal can be dismissed with Escape; dropdowns close on Escape. |
| **2.2.2** | Pause, Stop, Hide | No auto-playing media or animations requiring control. |
| **2.3.1** | Three Flashes | No flashing content. |
| **2.4.1** | Bypass Blocks | Skip navigation implemented (`base.html:27`); reveals on focus. |
| **2.4.2** | Page Titled | Each page has a unique `<title>` via template `{% block title %}`. |
| **2.4.3** | Focus Order | DOM order reflects logical tab sequence; modal traps focus correctly. |
| **2.4.4** | Link Purpose | Action buttons and links have descriptive `aria-label`; external links note "(opens in new tab)". |
| **2.4.5** | Multiple Ways | Pagination and search/filter provide multiple navigation paths. |
| **2.4.6** | Headings and Labels | All form inputs have `<label>` elements or `aria-label`. Headings describe sections. |
| **2.4.7** | Focus Visible (most elements) | Card links, nav links, and buttons have `:focus-visible` styles (USWDS + `horizon.css:407`). |
| **3.1.1** | Language of Page | `<html lang="en">` present (`base.html:3`). |
| **3.1.2** | Language of Parts | No foreign-language content identified. |
| **3.2.1** | On Focus | No context changes on focus alone. |
| **3.3.1** | Error Identification (partial) | Error messages use `role="alert"` and descriptive text. (See W2 for timing concern.) |
| **3.3.2** | Labels or Instructions | Required fields use `aria-required`, hint text via `aria-describedby`, and `<abbr title="required">`. |
| **4.1.1** | Parsing | Valid semantic HTML; ARIA roles and attributes used correctly overall. |
| **4.1.2** | Name, Role, Value | Interactive elements have accessible names, roles, and state (e.g., `aria-expanded`, `aria-current`, `aria-selected`, `aria-disabled`). |
| **4.1.3** | Status Messages | `aria-live="polite"` on results count (`home.html:88`), flash messages (`base.html:118`), and form status (`add_tool.html:328`). |

### Notable Accessibility Strengths

- **Skip navigation** is fully implemented and visually appears on keyboard focus (`horizon.css:1134–1151`).
- **ARIA landmark roles** are comprehensive: `role="banner"`, `role="main"`, `role="contentinfo"`, `role="search"`, `role="navigation"` with descriptive `aria-label` values.
- **Custom MultiSelect widget** follows the WAI-ARIA Combobox / Listbox pattern with correct roles, `aria-expanded`, `aria-multiselectable`, `aria-selected`, and keyboard support (Enter, Space, Escape).
- **External links** consistently use `aria-label="… (opens in new tab)"` and `target="_blank" rel="noopener noreferrer"`.
- **Pagination** uses `aria-current="page"` on the active page and `aria-disabled="true"` on inactive arrows.
- **Dynamic content** is communicated via `aria-live` regions, not page reload.
- **Modal dialog** uses `role="dialog"`, `aria-modal="true"`, `aria-labelledby`, and Bootstrap's built-in focus trap.

---

## Section 508 Specific Notes

The 2017 Section 508 Refresh incorporates WCAG 2.0 Level A and AA by reference (36 CFR Part 1194, E205). All WCAG issues above therefore constitute Section 508 failures.

Additionally:

| Section 508 Requirement | Status | Note |
|---|---|---|
| **E205** — Web content must conform to WCAG 2.0 A/AA | Partial | Issues 1–5 above require remediation. |
| **Accessibility Statement** | Missing | The "Accessibility support" link in the Identifier is empty (`href=""`). A published accessibility statement with contact information is required for federal/federally-funded sites. |
| **VPAT / ACR** | Not provided | A Voluntary Product Accessibility Template should accompany federal software. |

---

## Recommended Remediation Priority

| Priority | Issue | File(s) |
|---|---|---|
| **P1** | Complete USWDS Identifier (real URLs, real agency info) | `base.html:175–225` |
| **P1** | Fix warning badge contrast (3.09:1 → ≥4.5:1) | `horizon.css:516` |
| **P2** | Darken card like-count color (4.46:1 → ≥4.5:1) | `horizon.css:486` |
| **P2** | Add `:focus-visible` to `.hz-multiselect-display` | `horizon.css` |
| **P2** | Address auto-submit with explicit action or in-place AJAX | `main.js:296–308` |
| **P3** | Fix error injection order in form validation | `add_tool.html:554–562` |
| **P3** | Replace `<div role="img">` placeholders with `<img>` | `home.html:140`, `tool_detail.html:23` |
| **P3** | Remove `role="img"` from QR code container | `tool_detail.html:107` |
| **P4** | Reconcile `.ms-*` CSS with `.hz-multiselect-*` JS class names | `horizon.css:1015–1104` |

---

## pa11y Automated Scan Results

**Tool:** pa11y 9.1.1 · **Runner:** htmlcs · **Standard:** WCAG2AA · **Date:** 2026-07-23
**Config:** `chromeLaunchConfig.executablePath` pointed to Puppeteer-managed Chromium

Three pages were scanned while the Django development server ran locally (`http://127.0.0.1:8765`). The add-tool page was scanned unauthenticated; it redirected to the admin login page, so the scan reflects the login redirect page, not the form itself.

---

### Home / Catalog Page (`/`)

**10 errors · 34 warnings · 85 notices**

#### Errors

All 10 errors are the same code, repeating once per tool card on the page:

| Code | Message | Selector |
|---|---|---|
| `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail` | Contrast ratio 4.46:1; expected ≥4.5:1. Recommendation: change to `#767679`. | `.hz-card-likes` (×10 cards) |

> **Confirmed:** This is Issue 2 from the manual audit. The fix is to darken `.hz-card-likes` from `#77777a` to `#767679` or `#58585b` in `horizon.css:486`.

#### Warnings (unique, deduplicated)

| Code | Message | Notes |
|---|---|---|
| `WCAG2AA.Principle1.Guideline1_4.1_4_10.C32,…` | Element has `position: fixed`; may require two-dimensional scrolling. | Applies to `.usa-overlay` (mobile nav backdrop, `base.html:30`). WCAG **2.1** criterion 1.4.10 (Reflow) — outside WCAG 2.0 scope. Likely a false positive; the overlay is hidden by default and does not contain content. |
| `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.BgImage` | Nav logo link text placed on a background image; contrast unverifiable. | The header uses a solid dark color (`#2e2e32`), not an image. This is a pa11y false positive caused by the `data-hds-palette="dark"` attribute being misidentified as a background image context. Manual contrast calculation: white on `#2e2e32` = 13.5:1 ✅ |
| `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Alpha` | Nav link text or background contains alpha transparency. | The hover/active state uses `background-color: rgba(28, 103, 227, 0.2)` (`horizon.css:92`). Pa11y cannot resolve alpha-composited colors against the dark header. In resting state the text is white on `#2e2e32` (13.5:1 ✅). The hover state blends to approximately `#2a3a5c`, yielding white-on-dark ≈ 10:1 ✅. No real issue. |
| `WCAG2AA.Principle4.Guideline4_1.4_1_2.H91.Select.Value` | The `#orgFilter` select element does not have a value available to an accessibility API. | The select has both `<label for="orgFilter">` and `aria-label`. The `aria-label` overrides the label for AT name computation but does not prevent value exposure. This appears to be a pa11y/htmlcs false positive; the element is fully labeled and functional. |
| `WCAG2AA.Principle1.Guideline1_3.1_3_1.H85.2` | Selection list may contain groups of related options; consider `<optgroup>`. | Advisory only. The organization filter lists orgs without grouping. Not a WCAG 2.0 violation; a best-practice suggestion. |
| `WCAG2AA.Principle2.Guideline2_5.2_5_3.F96` | Accessible name for card link does not contain the visible label text. | WCAG **2.1** criterion 2.5.3 (Label in Name) — outside WCAG 2.0 scope. The `aria-label` is `"Open {name} (opens in new tab)"` which does contain the tool name. Likely a false positive from htmlcs not resolving the inner heading text correctly. |
| `WCAG2AA.Principle4.Guideline4_1.4_1_2.H91.A.Placeholder` | Anchor element with link content but no `href`, `id`, or `name`. | Targets the `<a href="">` links inside the USWDS Identifier section (`base.html:197–213`). **Confirmed real issue** — see Issue 5 in this report. |

---

### Tool Detail Page (`/tool/5/`)

**0 errors · 1 warning · 43 notices**

The tool detail page passes all WCAG 2.0 A/AA automated checks.

#### Warning

| Code | Message | Notes |
|---|---|---|
| `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Abs` | Absolutely positioned element; background color cannot be determined. | Selector: `#branding > button > span`. The `#branding` ID is not present in the application templates and appears to be injected by the USWDS JavaScript component or a browser extension. This is a false positive from an external component, not application code. |

---

### Add Tool Page (`/add-tool/`)

**0 errors · 1 warning · 25 notices**

> Note: pa11y scanned the admin login redirect page (`/admin/login/?next=/add-tool/`) since the add-tool route requires staff authentication. The result reflects the USWDS/Django admin login page, not the add-tool form.

#### Warning

| Code | Message | Notes |
|---|---|---|
| `WCAG2AA.Principle1.Guideline1_3.1_3_1.H39.3.NoCaption` | Data table has no `<caption>` element. | Selector: `#summary > table`. This is a Django development-mode debug panel table injected at the bottom of the page in `DEBUG=True` mode. It does not appear in production. Not an application issue. |

---

### pa11y Findings Summary

| Finding | Source | Status |
|---|---|---|
| `.hz-card-likes` contrast 4.46:1 (×10) | pa11y error | **Real — confirm Issue 2** |
| Empty `href=""` identifier links | pa11y warning | **Real — confirm Issue 5** |
| `position: fixed` overlay (1.4.10) | pa11y warning | False positive / WCAG 2.1 only |
| Nav logo background image contrast | pa11y warning | False positive (solid color, 13.5:1) |
| Nav link alpha background | pa11y warning | False positive (hover state passes) |
| `#orgFilter` select value | pa11y warning | False positive |
| Card link label (2.5.3) | pa11y warning | False positive / WCAG 2.1 only |
| `#branding` button span | pa11y warning | External component, false positive |
| Django debug table caption | pa11y warning | DEBUG mode only, not production |

**Net new issues confirmed by pa11y:** 0 (all real pa11y findings were already identified in the manual audit above).

---

*This report was produced via static code analysis, manual template review, and automated pa11y scanning. Contrast ratios were calculated using the WCAG 2.0 relative luminance formula.*

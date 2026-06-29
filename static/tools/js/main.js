/**
 * EarthRISE Toolkit — Main JavaScript
 * Bootstrap 5 + jQuery
 * WCAG 2.0 / Section 508 compliant
 */

(function ($) {
  'use strict';

  /* ============================================================
     MultiSelect Widget
     ============================================================ */
  /**
   * MultiSelect — wraps a hidden text input and renders a
   * tag-based multi-select dropdown with keyboard support.
   *
   * Usage:
   *   new MultiSelect({
   *     containerId: 'ms-serviceareas',
   *     hiddenInputId: 'id_serviceareas_hidden',
   *     options: ['Agriculture', 'Disasters', ...],
   *     label: 'Service Areas',
   *     allowNew: false,          // allow user-created items
   *     quickCreateType: null,    // 'scientist' etc for AJAX create
   *     csrfToken: '...',
   *   })
   */
  class MultiSelect {
    constructor(opts) {
      this.containerId   = opts.containerId;
      this.hiddenInputId = opts.hiddenInputId;
      this.options       = opts.options || [];
      this.label         = opts.label || '';
      this.allowNew      = opts.allowNew || false;
      this.quickCreateType = opts.quickCreateType || null;
      this.csrfToken     = opts.csrfToken || '';
      this.selected      = [];
      this._filteredOpts = [...this.options];

      this.$container = $('#' + this.containerId);
      this.$hidden    = $('#' + this.hiddenInputId);

      this._render();
      this._bindEvents();
    }

    _render() {
      const displayId  = this.hiddenInputId + '_display';
      const dropdownId = this.hiddenInputId + '_dropdown';
      const searchId   = this.hiddenInputId + '_search';

      const html = `
        <div class="hz-multiselect" data-ms="${this.hiddenInputId}">
          <div class="hz-multiselect-display"
               id="${displayId}"
               tabindex="0"
               role="combobox"
               aria-expanded="false"
               aria-haspopup="listbox"
               aria-label="${this.label}"
               aria-controls="${dropdownId}">
            <span class="ms-placeholder text-meta" aria-hidden="true">Select or search…</span>
          </div>
          <div class="hz-multiselect-dropdown" id="${dropdownId}" role="listbox" aria-multiselectable="true">
            <div class="hz-multiselect-search">
              <input type="text" id="${searchId}" placeholder="Search…"
                     aria-label="Search ${this.label}" autocomplete="off">
            </div>
            <div class="ms-options-list"></div>
          </div>
        </div>`;

      this.$container.html(html);
      this.$display  = this.$container.find('.hz-multiselect-display');
      this.$dropdown = this.$container.find('.hz-multiselect-dropdown');
      this.$search   = this.$container.find('input[type=text]');
      this.$list     = this.$container.find('.ms-options-list');

      this._renderOptions(this.options);
    }

    _renderOptions(opts) {
      const self = this;
      this.$list.empty();
      opts.forEach(function (opt) {
        const isSel = self.selected.includes(opt);
        const $opt  = $(`<div class="hz-multiselect-option${isSel ? ' selected' : ''}"
                              role="option"
                              aria-selected="${isSel}"
                              tabindex="-1"
                              data-value="${self._esc(opt)}">${self._esc(opt)}</div>`);
        self.$list.append($opt);
      });
    }

    _updateDisplay() {
      this.$display.empty();
      if (this.selected.length === 0) {
        this.$display.append('<span class="ms-placeholder text-meta" aria-hidden="true">Select or search…</span>');
      } else {
        const self = this;
        this.selected.forEach(function (val) {
          const $tag = $(`<span class="hz-multiselect-tag">
                            ${self._esc(val)}
                            <button type="button" class="hz-multiselect-tag-remove"
                                    aria-label="Remove ${self._esc(val)}">×</button>
                          </span>`);
          $tag.find('.hz-multiselect-tag-remove').on('click', function (e) {
            e.stopPropagation();
            self._removeItem(val);
          });
          self.$display.append($tag);
        });
      }
      this.$hidden.val(this.selected.join(','));
      // Re-render options to reflect selection state
      this._renderOptions(this._filteredOpts);
    }

    _removeItem(val) {
      this.selected = this.selected.filter(function (v) { return v !== val; });
      this._updateDisplay();
    }

    _toggleDropdown(open) {
      if (open) {
        this.$dropdown.addClass('open');
        this.$display.attr('aria-expanded', 'true');
        this.$search.val('').focus();
        this._filteredOpts = [...this.options];
        this._renderOptions(this._filteredOpts);
      } else {
        this.$dropdown.removeClass('open');
        this.$display.attr('aria-expanded', 'false');
      }
    }

    _bindEvents() {
      const self = this;

      // Toggle dropdown on click / Enter / Space
      this.$display.on('click keydown', function (e) {
        if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') {
          return;
        }
        e.preventDefault();
        const isOpen = self.$dropdown.hasClass('open');
        self._toggleDropdown(!isOpen);
      });

      // Filter options on search
      this.$search.on('input', function () {
        const q = $(this).val().toLowerCase();
        self._filteredOpts = self.options.filter(function (o) {
          return o.toLowerCase().includes(q);
        });
        self._renderOptions(self._filteredOpts);
      });

      // Select option
      this.$list.on('click keydown', '.hz-multiselect-option', function (e) {
        if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') {
          return;
        }
        const val = $(this).data('value');
        if (self.selected.includes(val)) {
          self._removeItem(val);
        } else {
          self.selected.push(val);
          self._updateDisplay();
        }
      });

      // Close on outside click
      $(document).on('click.ms_' + this.hiddenInputId, function (e) {
        if (!self.$container.find('.hz-multiselect').is(e.target) &&
            !self.$container.find('.hz-multiselect').has(e.target).length) {
          self._toggleDropdown(false);
        }
      });

      // Escape key closes
      this.$container.on('keydown', function (e) {
        if (e.key === 'Escape') {
          self._toggleDropdown(false);
          self.$display.focus();
        }
      });
    }

    _esc(str) {
      return $('<div>').text(str).html();
    }

    destroy() {
      $(document).off('click.ms_' + this.hiddenInputId);
    }
  }

  /* ============================================================
     Quick-Create Modal
     ============================================================ */
  window.initQuickCreate = function (csrfToken, organizations) {
    $('#quickCreateSave').on('click', function () {
      const type  = $('#quickCreateType').val();
      const name  = $('#quickCreateName').val().trim();
      const desc  = $('#quickCreateDesc').val().trim();
      const url   = $('#quickCreateUrl').val().trim();
      const org   = $('#quickCreateOrg').val().trim();

      if (!name) {
        showFieldError('#quickCreateName', 'Name is required.');
        return;
      }

      const data = { csrfmiddlewaretoken: csrfToken, name: name };
      if (desc)     data.description  = desc;
      if (url)      data.url          = url;
      if (org)      data.organization = org;

      $.post('/quick-create/' + type + '/', data)
        .done(function (resp) {
          if (resp.success) {
            // Add to the corresponding multiselect and auto-select
            const $ms = $('[data-ms-type="' + type + '"]').closest('.hz-multiselect').data('ms-instance');
            if ($ms) {
              $ms.options.push(resp.name);
              $ms.selected.push(resp.name);
              $ms._filteredOpts = [...$ms.options];
              $ms._updateDisplay();
            }
            bootstrap.Modal.getInstance(document.getElementById('quickCreateModal')).hide();
            $('#quickCreateForm')[0].reset();
          } else {
            showFieldError('#quickCreateName', Object.values(resp.errors || {}).flat().join(' '));
          }
        })
        .fail(function () {
          showFieldError('#quickCreateName', 'Server error. Please try again.');
        });
    });

    // Reset errors on input
    $('#quickCreateModal').on('input', function () {
      clearFieldErrors();
    });

    // Populate org dropdown
    if (organizations && organizations.length) {
      const $orgGroup = $('#quickCreateOrgGroup');
      const $sel = $('<select id="quickCreateOrg" class="hz-form-control"></select>');
      $sel.append('<option value="">— Select organization —</option>');
      organizations.forEach(function (o) {
        $sel.append($('<option></option>').val(o).text(o));
      });
      $orgGroup.find('input').replaceWith($sel);
    }
  };

  function showFieldError(selector, msg) {
    clearFieldErrors();
    const $el = $(selector);
    $el.addClass('is-invalid');
    $el.after('<div class="invalid-feedback d-block">' + $('<div>').text(msg).html() + '</div>');
  }

  function clearFieldErrors() {
    $('.is-invalid').removeClass('is-invalid');
    $('.invalid-feedback').remove();
  }

  /* ============================================================
     Hero image preview
     ============================================================ */
  window.initHeroPreview = function (inputId, previewId) {
    $('#' + inputId).on('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          $('#' + previewId)
            .attr('src', e.target.result)
            .show();
        };
        reader.readAsDataURL(file);
      }
    });
  };

  /* ============================================================
     Live search / filter on home page (client-side debounce)
     The server does the actual filtering; this just auto-submits
     the form after a short debounce so the user doesn't have
     to press Enter.
     ============================================================ */
  window.initFilterBar = function () {
    let timer;
    $('#searchInput').on('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        $('#filterForm').submit();
      }, 400);
    });

    // Auto-submit on select changes
    $('#filterForm select').on('change', function () {
      $('#filterForm').submit();
    });
  };

  /* ============================================================
     Export MultiSelect to global for template use
     ============================================================ */
  window.MultiSelect = MultiSelect;

})(jQuery);

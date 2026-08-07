/* ============================================================
   PMO EPC — Script principal
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sidebar Toggle ────────────────────────────────────────
  const sidebarToggle = document.getElementById('sidebarToggle');
  const body          = document.body;

  const COLLAPSED_KEY = 'pmo_sidebar_collapsed';

  // Restaurer état persisté
  if (localStorage.getItem(COLLAPSED_KEY) === '1') {
    body.classList.add('sidebar-collapsed');
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
      body.classList.toggle('sidebar-collapsed');
      localStorage.setItem(
        COLLAPSED_KEY,
        body.classList.contains('sidebar-collapsed') ? '1' : '0'
      );
    });
  }

  // ── Auto-dismiss alerts ───────────────────────────────────
  document.querySelectorAll('.alert.alert-success').forEach(el => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert?.close();
    }, 4000);
  });

  // ── Tooltips Bootstrap ────────────────────────────────────
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
    new bootstrap.Tooltip(el, { trigger: 'hover' });
  });

  // ── Sortable tables (tri colonne) ────────────────────────
  document.querySelectorAll('.sortable-col').forEach(th => {
    th.addEventListener('click', () => {
      const field   = th.dataset.sort;
      const url     = new URL(window.location.href);
      const current = url.searchParams.get('sort') || '';
      url.searchParams.set(
        'sort',
        current === field ? `-${field}` : field
      );
      url.searchParams.delete('page');
      window.location.href = url.toString();
    });
  });

  // ── Filtre — Soumission sur changement select ─────────────
  document.querySelectorAll('.pmo-auto-submit').forEach(el => {
    el.addEventListener('change', () => {
      el.closest('form')?.submit();
    });
  });

  // ── Sélection masse tableau ───────────────────────────────
  const selectAll = document.getElementById('selectAll');
  if (selectAll) {
    selectAll.addEventListener('change', () => {
      document.querySelectorAll('.row-checkbox').forEach(cb => {
        cb.checked = selectAll.checked;
      });
      updateBulkActions();
    });
    document.querySelectorAll('.row-checkbox').forEach(cb => {
      cb.addEventListener('change', updateBulkActions);
    });
  }

  function updateBulkActions() {
    const checked = document.querySelectorAll('.row-checkbox:checked').length;
    const bar     = document.getElementById('bulkActionsBar');
    if (bar) {
      bar.style.display = checked > 0 ? 'flex' : 'none';
      const counter = bar.querySelector('.bulk-counter');
      if (counter) counter.textContent = `${checked} sélectionné(s)`;
    }
  }

  // ── Progress bars animées ─────────────────────────────────
  document.querySelectorAll('.pmo-progress-bar[data-width]').forEach(bar => {
    const w = bar.dataset.width;
    setTimeout(() => { bar.style.width = w + '%'; }, 100);
  });

  // ── Couleur SPI/CPI automatique ───────────────────────────
  document.querySelectorAll('.pmo-spi-value').forEach(el => {
    const val = parseFloat(el.textContent);
    if (!isNaN(val)) {
      if (val >= 0.95) el.classList.add('pmo-spi-good');
      else if (val >= 0.80) el.classList.add('pmo-spi-warn');
      else el.classList.add('pmo-spi-bad');
    }
  });

  // ── Drag & drop fichiers (dropzone) ──────────────────────
  document.querySelectorAll('.pmo-dropzone').forEach(zone => {
    zone.addEventListener('dragover', e => {
      e.preventDefault();
      zone.classList.add('dragover');
    });
    zone.addEventListener('dragleave', () => {
      zone.classList.remove('dragover');
    });
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('dragover');
      const files = e.dataTransfer.files;
      const input = zone.querySelector('input[type="file"]');
      if (input && files.length) {
        // DataTransfer API
        const dt = new DataTransfer();
        Array.from(files).forEach(f => dt.items.add(f));
        input.files = dt.files;
        // Feedback visuel
        const label = zone.querySelector('.pmo-dropzone-label');
        if (label) {
          label.textContent = `${files.length} fichier(s) sélectionné(s)`;
        }
      }
    });
  });

  // ── Confirmation modale avant suppression ─────────────────
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm || 'Confirmer cette action ?')) {
        e.preventDefault();
      }
    });
  });

  // ── Chart.js : helpers globaux ────────────────────────────
  window.PMO = window.PMO || {};

  /**
   * Courbe en S standard
   * @param {string} canvasId
   * @param {string[]} labels  dates
   * @param {number[]} pv      Planned Value
   * @param {number[]} ev      Earned Value
   * @param {number[]} ac      Actual Cost
   */
  window.PMO.drawSCurve = function(canvasId, labels, pv, ev, ac) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label:           'PV — Valeur Planifiée',
            data:            pv,
            borderColor:     '#1E6FD9',
            backgroundColor: 'rgba(30,111,217,0.08)',
            borderWidth:     2,
            pointRadius:     3,
            fill:            true,
            tension:         0.4,
          },
          {
            label:           'EV — Valeur Acquise',
            data:            ev,
            borderColor:     '#16A34A',
            backgroundColor: 'rgba(22,163,74,0.08)',
            borderWidth:     2,
            pointRadius:     3,
            fill:            true,
            tension:         0.4,
          },
          {
            label:           'AC — Coût Réel',
            data:            ac,
            borderColor:     '#E53935',
            backgroundColor: 'rgba(229,57,53,0.06)',
            borderWidth:     2,
            pointRadius:     3,
            borderDash:      [5,3],
            fill:            false,
            tension:         0.4,
          },
        ],
      },
      options: {
        responsive:         true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            position: 'bottom',
            labels:   { font: { size: 11 }, boxWidth: 12 },
          },
          tooltip: {
            callbacks: {
              label: ctx => {
                const v = ctx.parsed.y;
                return ` ${ctx.dataset.label}: ${
                  new Intl.NumberFormat('fr-FR',
                    {style:'currency', currency:'EUR',
                     maximumFractionDigits:0}).format(v)
                }`;
              }
            }
          }
        },
        scales: {
          x: {
            grid:  { color: 'rgba(0,0,0,0.05)' },
            ticks: { font: { size: 11 } },
          },
          y: {
            grid:  { color: 'rgba(0,0,0,0.05)' },
            ticks: {
              font: { size: 11 },
              callback: v => {
                if (v >= 1e6) return `${(v/1e6).toFixed(1)}M€`;
                if (v >= 1e3) return `${(v/1e3).toFixed(0)}k€`;
                return `${v}€`;
              }
            }
          }
        }
      }
    });
  };

  /**
   * Graphique EVM barres SPI/CPI
   */
  window.PMO.drawEVMBar = function(canvasId, labels, spi, cpi) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label:           'SPI (Schedule)',
            data:            spi,
            backgroundColor: spi.map(v =>
              v >= 0.95 ? '#16A34A' :
              v >= 0.80 ? '#F59E0B' : '#E53935'),
            borderRadius:    4,
          },
          {
            label:           'CPI (Cost)',
            data:            cpi,
            backgroundColor: cpi.map(v =>
              v >= 0.95 ? '#1E6FD9' :
              v >= 0.80 ? '#00C2A8' : '#E53935'),
            borderRadius:    4,
          },
        ],
      },
      options: {
        responsive:          true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels:   { font: { size: 11 }, boxWidth: 12 },
          },
        },
        scales: {
          y: {
            min:  0,
            max:  1.5,
            grid: { color: 'rgba(0,0,0,0.05)' },
            ticks: { font: { size: 11 } },
          },
          x: {
            grid:  { display: false },
            ticks: { font: { size: 11 } },
          }
        }
      }
    });
  };

  /**
   * Donut chart simple
   */
  window.PMO.drawDonut = function(canvasId, labels, values, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data:            values,
          backgroundColor: colors || ['#1E6FD9','#16A34A','#F59E0B','#E53935'],
          borderWidth:     2,
          borderColor:     '#fff',
        }]
      },
      options: {
        responsive:          true,
        maintainAspectRatio: false,
        cutout:              '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels:   { font: { size: 11 }, boxWidth: 10 },
          },
        }
      }
    });
  };

});
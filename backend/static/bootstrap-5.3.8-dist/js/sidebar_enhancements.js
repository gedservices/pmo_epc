/**
 * ============================================
 * SIDEBAR ENHANCEMENTS - Bootstrap 5
 * ============================================
 * Gestion des accordéons avec mémorisation d'état
 */

(function () {
  'use strict';

  // ============================================
  // CONSTANTES
  // ============================================
  const STORAGE_KEY = 'pmo_sidebar_accordion_state';
  const SIDEBAR_COLLAPSED_KEY = 'pmo_sidebar_collapsed';

  // ============================================
  // GESTION DU TOGGLE SIDEBAR
  // ============================================
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('pmoSidebar');

  if (sidebarToggle && sidebar) {
    // Restaurer l'état au chargement
    const isCollapsed = localStorage.getItem(SIDEBAR_COLLAPSED_KEY) === 'true';
    if (isCollapsed) {
      sidebar.classList.add('collapsed');
    }

    // Toggle au clic
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('collapsed');
      const collapsed = sidebar.classList.contains('collapsed');
      localStorage.setItem(SIDEBAR_COLLAPSED_KEY, collapsed);

      // Initialiser les tooltips en mode réduit
      if (collapsed) {
        initTooltips();
      } else {
        disposeTooltips();
      }
    });
  }

  // ============================================
  // MÉMORISATION DE L'ÉTAT DES ACCORDÉONS
  // ============================================

  /**
   * Sauvegarder l'état des accordéons ouverts
   */
  function saveAccordionState() {
    const openAccordions = [];
    document.querySelectorAll('.accordion-collapse.show').forEach(collapse => {
      openAccordions.push(collapse.id);
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(openAccordions));
  }

  /**
   * Restaurer l'état des accordéons au chargement
   */
  function restoreAccordionState() {
    try {
      const savedState = localStorage.getItem(STORAGE_KEY);
      if (!savedState) return;

      const openAccordions = JSON.parse(savedState);
      openAccordions.forEach(id => {
        const collapseEl = document.getElementById(id);
        if (collapseEl && !collapseEl.classList.contains('show')) {
          // Ouvrir uniquement si pas déjà ouvert par Django
          const hasActiveChild = collapseEl.querySelector('.pmo-nav-subitem.active');
          if (!hasActiveChild) {
            const bsCollapse = new bootstrap.Collapse(collapseEl, { toggle: false });
            bsCollapse.show();
          }
        }
      });
    } catch (e) {
      console.warn('Impossible de restaurer l\'état des accordéons:', e);
    }
  }

  /**
   * Écouter les changements d'état des accordéons
   */
  function initAccordionListeners() {
    const accordionElement = document.getElementById('sidebarAccordion');
    if (!accordionElement) return;

    accordionElement.addEventListener('shown.bs.collapse', saveAccordionState);
    accordionElement.addEventListener('hidden.bs.collapse', saveAccordionState);
  }

  // ============================================
  // TOOLTIPS EN MODE RÉDUIT
  // ============================================
  let tooltipList = [];

  function initTooltips() {
    if (!sidebar.classList.contains('collapsed')) return;

    const tooltipTriggerList = [].slice.call(
      sidebar.querySelectorAll('[data-bs-toggle="tooltip"]')
    );

    tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl, {
        placement: 'right',
        trigger: 'hover'
      });
    });
  }

  function disposeTooltips() {
    tooltipList.forEach(tooltip => tooltip.dispose());
    tooltipList = [];
  }

  // ============================================
  // HIGHLIGHT ACTIF AU SCROLL
  // ============================================

  /**
   * Ajouter une classe au scroll pour feedback visuel
   */
  function initScrollIndicator() {
    const navElement = document.querySelector('.pmo-nav');
    if (!navElement) return;

    navElement.addEventListener('scroll', function () {
      if (this.scrollTop > 10) {
        sidebar.classList.add('is-scrolled');
      } else {
        sidebar.classList.remove('is-scrolled');
      }
    });
  }

  // ============================================
  // FERMETURE AUTO SUR MOBILE
  // ============================================

  function initMobileAutoClose() {
    if (window.innerWidth < 768) {
      const navLinks = sidebar.querySelectorAll('.pmo-nav-subitem, .pmo-nav-item');
      navLinks.forEach(link => {
        link.addEventListener('click', function () {
          // Fermer le sidebar sur mobile après clic
          if (sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
          }
        });
      });
    }
  }

  // ============================================
  // NAVIGATION AU CLAVIER
  // ============================================

  function initKeyboardNavigation() {
    sidebar.addEventListener('keydown', function (e) {
      const focused = document.activeElement;

      // Flèche haut/bas pour naviguer entre items
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        const items = Array.from(
          sidebar.querySelectorAll('.pmo-nav-item, .pmo-nav-subitem, .pmo-accordion-button')
        );
        const currentIndex = items.indexOf(focused);

        if (currentIndex !== -1) {
          const nextIndex = e.key === 'ArrowDown'
            ? Math.min(currentIndex + 1, items.length - 1)
            : Math.max(currentIndex - 1, 0);
          items[nextIndex].focus();
        }
      }
    });
  }

  // ============================================
  // INDICATEUR DE CHARGEMENT (optionnel)
  // ============================================

  /**
   * Ajouter une classe loading sur le lien cliqué
   */
  function initLoadingIndicator() {
    const navLinks = sidebar.querySelectorAll('.pmo-nav-subitem, .pmo-nav-item');
    navLinks.forEach(link => {
      link.addEventListener('click', function () {
        if (this.href && this.href !== '#') {
          this.classList.add('loading');
        }
      });
    });
  }

  // ============================================
  // INITIALISATION
  // ============================================

  document.addEventListener('DOMContentLoaded', function () {
    // Restaurer l'état des accordéons (mais respecter Django actif)
    // restoreAccordionState(); // Commenté car Django gère déjà l'ouverture

    // Écouter les changements pour mémorisation future
    initAccordionListeners();

    // Initialiser tooltips si sidebar collapsed
    if (sidebar && sidebar.classList.contains('collapsed')) {
      initTooltips();
    }

    // Autres initialisations
    initScrollIndicator();
    initMobileAutoClose();
    initKeyboardNavigation();
    initLoadingIndicator();

    console.log('✅ Sidebar enhancements initialized');
  });

  // ============================================
  // EXPOSITION GLOBALE (optionnel)
  // ============================================

  window.PMOSidebar = {
    saveState: saveAccordionState,
    restoreState: restoreAccordionState,
    initTooltips: initTooltips,
    disposeTooltips: disposeTooltips
  };

})();
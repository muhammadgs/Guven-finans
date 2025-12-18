(function () {
  const headerOffset = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-offset')) || 0;

  function hideLoader() {
    const loader = document.getElementById('loader-overlay');
    if (!loader) return;
    loader.classList.add('hidden');
    setTimeout(() => loader.remove(), 400);
  }

  function setupLoader() {
    const loader = document.getElementById('loader-overlay');
    if (!loader) return;

    const navigationEntry = performance.getEntriesByType('navigation')[0];
    const navType = navigationEntry?.type || (performance.navigation?.type === 1 ? 'reload' : 'navigate');
    const alreadyShown = sessionStorage.getItem('gtiLoaderShown') === '1';
    const shouldShow = navType === 'reload' || !alreadyShown;
    const start = performance.now();
    const MIN_DURATION = 1200;

    if (shouldShow) {
      sessionStorage.setItem('gtiLoaderShown', '1');
      const tick = () => {
        const elapsed = performance.now() - start;
        if (elapsed >= MIN_DURATION) {
          hideLoader();
        } else {
          requestAnimationFrame(tick);
        }
      };
      tick();
    } else {
      hideLoader();
    }
  }

  function mountHeader() {
    const target = document.getElementById('site-header');
    if (!target) return;
    target.innerHTML = `
      <div class="top-bar">
        <div class="top-links">
          <a href="mailto:info@guvenfinans.az"><i class="fas fa-envelope"></i> info@guvenfinans.az</a>
          <a href="tel:+994557636993" id="header-phone-link"><i class="fas fa-phone-alt"></i> +994 55 763 69 93</a>
        </div>
        <div class="social-links">
          <a class="social-button" href="#" aria-label="Whatsapp"><i class="fa-brands fa-whatsapp"></i></a>
          <a class="social-button" href="#" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
          <a class="social-button" href="#" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
          <a class="social-button" href="#" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
        </div>
      </div>
      <nav class="nav-bar">
        <a class="brand" href="index.html">
          <h1 class="brand-title">Güvən Finans</h1>
          <p class="brand-tagline">İnnovativ maliyyə həlləri</p>
        </a>
        <div class="nav-links" aria-label="Primary">
          <a class="nav-link" data-scroll-target="hero" href="index.html#hero">Ana səhifə</a>
          <a class="nav-link" data-scroll-target="about" href="index.html#about">Biz kimik</a>
          <a class="nav-link" data-scroll-target="why" href="index.html#why">Niyə biz?</a>
          <a class="nav-link" data-scroll-target="services" href="index.html#services">Xidmətlər</a>
          <a class="nav-link" data-scroll-target="projects" href="index.html#projects">Layihələr</a>
          <a class="nav-link" data-scroll-target="partners" href="index.html#partners">Partnyorlar</a>
          <a class="nav-link" data-scroll-target="consult" href="index.html#consult">Konsultasiya</a>
        </div>
        <div class="nav-actions">
          <a class="btn btn-outline" href="register-choice.html">Qeydiyyat</a>
          <a class="btn btn-primary" href="login.html">Giriş et</a>
        </div>
      </nav>
    `;
  }

  function mountFooter() {
    const target = document.getElementById('site-footer');
    if (!target) return;
    target.innerHTML = `
      <div class="container footer-grid">
        <div>
          <a href="index.html" class="brand">
            <img src="../financeApp/staticfiles/images/logo.png" alt="Güvən Finans" style="height:80px; width:auto; padding-left:12px;">
            <h3 class="brand-title" style="color:#fff; margin:0.5rem 0 0;">Güvən Finans</h3>
            <p class="brand-tagline" style="color:#cbd5f5;">İnnovativ maliyyə həlləri</p>
          </a>
          <div class="social-links" style="margin-top:1rem;">
            <a class="social-button" href="#" aria-label="Whatsapp"><i class="fa-brands fa-whatsapp"></i></a>
            <a class="social-button" href="#" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
            <a class="social-button" href="#" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a>
            <a class="social-button" href="#" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
          </div>
        </div>
        <div>
          <h3>Əlaqə</h3>
          <ul style="list-style:none; padding:0; margin:0; display:grid; gap:0.5rem;">
            <li><a href="mailto:info@guvenfinans.az"><i class="fas fa-envelope"></i> info@guvenfinans.az</a></li>
            <li><a href="tel:+994513210989"><i class="fas fa-phone-alt"></i> (+994) 51 321 0989</a></li>
            <li><span><i class="fas fa-map-marker-alt"></i> Əhməd Rəcəbli 33, Esra Plaza, B bloku, 4-cü mərtəbə Azərbaycan/Bakı</span></li>
          </ul>
        </div>
        <div>
          <h3>Xidmətlərimiz</h3>
          <ul style="list-style:none; padding:0; margin:0; display:grid; gap:0.4rem;">
            <li><a href="index.html#services">Proqram təminatı xidməti</a></li>
            <li><a href="index.html#services">Mühasibatlıq xidməti</a></li>
            <li><a href="index.html#services">Hüquq xidməti</a></li>
            <li><a href="index.html#services">Vergi xidməti</a></li>
            <li><a href="index.html#services">İnsan resursları xidməti</a></li>
          </ul>
        </div>
        <div>
          <h3>Səhifələr</h3>
          <ul style="list-style:none; padding:0; margin:0; display:grid; gap:0.35rem;">
            <li><a href="index.html#hero">Ana səhifə</a></li>
            <li><a href="index.html#consult">Konsultasiya</a></li>
            <li><a href="index.html#partners">Partnyorlarımız</a></li>
            <li><a href="index.html#services">Xidmətlər</a></li>
            <li><a href="index.html#about">Haqqımızda</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">Copyright &copy; 2023 Bütün Hüquqları Güvən Finans tərəfindən qorunur.</div>
    `;
  }

  function setupScroll() {
    const header = document.querySelector('.header-shell');
    const phoneLink = document.getElementById('header-phone-link');

    const updateHeader = () => {
      if (!header) return;
      if (window.scrollY > 10) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });

    if (phoneLink) {
      phoneLink.addEventListener('click', (e) => {
        if (!confirm('Hörmətli istifadəçi, bu nömrəyə zəng etmək istəyirsiniz?')) {
          e.preventDefault();
        }
      });
    }

    const scrollLinks = document.querySelectorAll('[data-scroll-target]');
    scrollLinks.forEach((link) => {
      link.addEventListener('click', (event) => {
        const targetId = link.getAttribute('data-scroll-target');
        const target = document.getElementById(targetId);
        if (!target) return;
        event.preventDefault();
        const position = target.getBoundingClientRect().top + window.scrollY - headerOffset();
        window.scrollTo({ top: position, behavior: 'smooth' });
      });
    });
  }

  function setupProjects() {
    const slider = document.querySelector('[data-project-slider]');
    const prev = document.querySelector('[data-project-prev]');
    const next = document.querySelector('[data-project-next]');
    if (!slider || !prev || !next) return;

    const updateButtons = () => {
      const maxScroll = slider.scrollWidth - slider.clientWidth;
      prev.style.display = slider.scrollLeft <= 4 ? 'none' : 'grid';
      next.style.display = slider.scrollLeft >= maxScroll - 4 ? 'none' : 'grid';
    };

    prev.addEventListener('click', () => {
      slider.scrollBy({ left: -(slider.clientWidth * 0.6), behavior: 'smooth' });
    });
    next.addEventListener('click', () => {
      slider.scrollBy({ left: slider.clientWidth * 0.6, behavior: 'smooth' });
    });

    slider.addEventListener('scroll', updateButtons, { passive: true });
    window.addEventListener('resize', updateButtons);
    updateButtons();
  }

  function setupConsultationForm() {
    const form = document.querySelector('[data-consult-form]');
    if (!form) return;
    const statusBox = document.querySelector('[data-consult-status]');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());
      try {
        await API.request('/consultations', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
        if (statusBox) {
          statusBox.textContent = 'Müraciətiniz uğurla göndərildi. Tezliklə əlaqə saxlayacağıq.';
          statusBox.className = 'alert success';
        }
        form.reset();
      } catch (error) {
        if (statusBox) {
          statusBox.textContent = error.message || 'Xəta baş verdi. Yenidən cəhd edin.';
          statusBox.className = 'alert error';
        }
      }
    });
  }

  function setupLoginForm() {
    const form = document.querySelector('[data-login-form]');
    if (!form) return;
    const status = document.querySelector('[data-login-status]');

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const credentials = Object.fromEntries(formData.entries());
      try {
        await Auth.login(credentials);
        status.textContent = 'Giriş uğurludur. İstifadəçi məlumatları yüklənir...';
        status.className = 'alert success';
        setTimeout(() => {
          window.location.href = 'owner-dashboard.html';
        }, 800);
      } catch (error) {
        status.textContent = error.message || 'Giriş zamanı xəta baş verdi';
        status.className = 'alert error';
      }
    });

    const meBtn = document.querySelector('[data-api-me-btn]');
    const refreshBtn = document.querySelector('[data-api-refresh-btn]');
    const apiStatus = document.querySelector('[data-api-status]');

    if (meBtn) {
      meBtn.addEventListener('click', async () => {
        try {
          const me = await Auth.getMe();
          apiStatus.textContent = JSON.stringify(me, null, 2);
          apiStatus.className = 'alert success';
        } catch (error) {
          apiStatus.textContent = error.message;
          apiStatus.className = 'alert error';
        }
      });
    }

    if (refreshBtn) {
      refreshBtn.addEventListener('click', async () => {
        try {
          const token = Auth.getToken();
          const refreshed = await API.request('/auth/refresh', {
            method: 'POST',
            headers: { Authorization: `Bearer ${token}` },
          });
          Auth.saveToken(refreshed?.access_token);
          apiStatus.textContent = 'Token yeniləndi';
          apiStatus.className = 'alert success';
        } catch (error) {
          apiStatus.textContent = error.message;
          apiStatus.className = 'alert error';
        }
      });
    }
  }

  function setupRegisterForm(selector, endpoint, successRedirect) {
    const form = document.querySelector(selector);
    if (!form) return;
    const status = document.querySelector('[data-register-status]');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const payload = Object.fromEntries(new FormData(form).entries());
      try {
        await API.request(endpoint, { method: 'POST', body: JSON.stringify(payload) });
        status.textContent = 'Məlumatlar göndərildi. Qısa zamanda geri dönüş ediləcək.';
        status.className = 'alert success';
        setTimeout(() => { window.location.href = successRedirect; }, 900);
      } catch (error) {
        status.textContent = error.message || 'Xəta baş verdi';
        status.className = 'alert error';
      }
    });
  }

  async function guardProtectedPages() {
    const protectedArea = document.querySelector('[data-protected]');
    if (!protectedArea) return;
    const status = document.querySelector('[data-api-status]');
    try {
      const me = await Auth.getMe();
      const userName = document.querySelector('[data-user-name]');
      if (userName) userName.textContent = me?.name || 'İstifadəçi';
      if (status) {
        status.textContent = 'Profil məlumatları yeniləndi.';
        status.className = 'alert success';
      }
    } catch (error) {
      if (status) {
        status.textContent = 'Sessiya tapılmadı, giriş səhifəsinə yönləndirilirsiniz';
        status.className = 'alert error';
      }
      setTimeout(() => { window.location.href = 'login.html'; }, 900);
    }
  }

  function setupDashboardLogout() {
    const logoutBtn = document.querySelector('[data-dashboard-logout]');
    if (!logoutBtn) return;
    logoutBtn.addEventListener('click', async (event) => {
      event.preventDefault();
      await Auth.logout();
      window.location.href = 'login.html';
    });
  }

  function initHomeData() {
    const stats = document.querySelector('[data-stats]');
    if (!stats) return;
    const statData = [
      { label: 'Aktiv layihə', count: '120+' },
      { label: 'Məmnun müştəri', count: '300+' },
      { label: 'Peşəkar əməkdaş', count: '25+' },
      { label: 'İllik təcrübə', count: '10 il' },
    ];
    stats.innerHTML = statData.map((item) => `
      <div class="stat-card">
        <p class="stat-number">${item.count}</p>
        <p class="stat-label">${item.label}</p>
      </div>
    `).join('');

    const projects = document.querySelector('[data-project-slider]');
    if (projects) {
      const projectData = [
        { title: 'FinTech mobil tətbiqi', desc: 'Real-time ödəniş izləmə və hesabat modulu.', image: '../financeApp/staticfiles/images/office.png' },
        { title: 'ERP inteqrasiyası', desc: 'Mühasibat və HR sistemlərinin vahid paneldə birləşdirilməsi.', image: '../financeApp/staticfiles/images/workerman.png' },
        { title: 'Bulud hesabat mərkəzi', desc: 'CEO-lar üçün ətraflı analitik göstəricilərin olduğu platforma.', image: '../financeApp/staticfiles/images/SVG.svg' },
      ];
      projects.innerHTML = projectData.map((project) => `
        <article class="project-card">
          <div class="project-image"><img src="${project.image}" alt="${project.title}"></div>
          <div class="project-body">
            <h3>${project.title}</h3>
            <p style="color:var(--gray-600);">${project.desc}</p>
            <a class="btn btn-primary" href="#consult">Bax</a>
          </div>
        </article>
      `).join('');
    }

    const partners = document.querySelector('[data-partner-track]');
    if (partners) {
      const partnerData = [
        { name: 'Partner One', desc: 'Regional texnologiya şirkəti', image: '../financeApp/staticfiles/images/workerman.png' },
        { name: 'Partner Two', desc: 'İstehsalat sektorunda lider', image: '../financeApp/staticfiles/images/office.png' },
        { name: 'Partner Three', desc: 'Bulud infrastrukturu mütəxəssisi', image: '../financeApp/staticfiles/images/SVG 2(mobile).svg' },
      ];
      partners.innerHTML = partnerData.map((partner) => `
        <article class="partner-card">
          <div class="project-image">${partner.image ? `<img src="${partner.image}" alt="${partner.name}">` : ''}</div>
          <div class="partner-body">
            <h3>${partner.name}</h3>
            <p style="color:var(--gray-600);">${partner.desc}</p>
            <a class="btn btn-primary" href="#" target="_blank" rel="noopener">Bax</a>
          </div>
        </article>
      `).join('');
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    mountHeader();
    mountFooter();
    setupLoader();
    setupScroll();
    setupProjects();
    setupConsultationForm();
    setupLoginForm();
    setupRegisterForm('[data-owner-register]', '/accounts/owner', 'owner-thanks.html');
    setupRegisterForm('[data-worker-register]', '/accounts/worker', 'worker-thanks.html');
    guardProtectedPages();
    setupDashboardLogout();
    initHomeData();
  });
})();

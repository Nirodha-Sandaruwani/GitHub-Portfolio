/* ===================================================
   MINI CARNOVA LOADER — ULTRA FAST VERSION
=================================================== */
document.addEventListener("DOMContentLoaded", () => {
  let percent = 0;

  const loader = document.getElementById("loader-wrapper");
  const percentEl = document.getElementById("loader-count");
  const rings = document.querySelectorAll(".ring");

  const interval = setInterval(() => {
    percent += 6; // ⚡ EVEN FASTER
    if (percent > 100) percent = 100;

    if (percentEl) percentEl.textContent = percent;

    // faster ring expansion sync
    const scale = 1 + percent / 550;
    rings.forEach(r => r.style.setProperty("--scale", scale));

    if (percent >= 100) {
      clearInterval(interval);

      // quick burst
      rings.forEach(r => r.style.setProperty("--scale", 1.22));

      setTimeout(() => {
        loader.classList.add("hide");
      }, 260); // faster fade-out
    }
  }, 12); // very fast interval
});


// CarNova Interactions + Hero Rotator + Swiper + Owl + Counters + Tabs + Particles

document.addEventListener("DOMContentLoaded", () => {

/* -------------------------------------------
  YEAR IN FOOTER
------------------------------------------- */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

/* -------------------------------------------
   MOBILE NAV — SLIDE MENU
------------------------------------------- */
const menuToggle = document.getElementById("menuToggle");
const mobileNav = document.getElementById("mobileNav");

if (menuToggle && mobileNav) {
  menuToggle.addEventListener("click", () => {
    menuToggle.classList.toggle("active");
    mobileNav.classList.toggle("open");
  });
}

// Close menu when clicking any link
document.querySelectorAll(".mobile-menu a").forEach(link => {
  link.addEventListener("click", () => {
    mobileNav.classList.remove("open");
    menuToggle.classList.remove("active");
  });
});

// Pages submenu toggle
document.querySelectorAll(".mobile-has-sub").forEach(sub => {
  const btn = sub.querySelector(".sub-toggle-btn");
  const icon = sub.querySelector(".toggle-icon");

  btn.addEventListener("click", () => {
    sub.classList.toggle("open");

    // Change icon
    if (sub.classList.contains("open")) {
      icon.textContent = "–";  // minus sign
    } else {
      icon.textContent = "+"; // X symbol
    }
  });
});

/* CLOSE MOBILE MENU WHEN CLICKING OUTSIDE */
const mobileOverlay = document.getElementById("mobileOverlay");

if (mobileOverlay) {
  mobileOverlay.addEventListener("click", () => {
    // Close slide menu
    mobileNav.classList.remove("open");
    
    // Reset hamburger
    menuToggle.classList.remove("active");

    // Hide overlay
    mobileOverlay.classList.remove("show");
  });
}

/* SHOW OVERLAY WHEN MENU OPENS */
menuToggle.addEventListener("click", () => {
  if (mobileNav.classList.contains("open")) {
    mobileOverlay.classList.add("show");
  } else {
    mobileOverlay.classList.remove("show");
  }
});

  /* -------------------------------------------
     ABOUT-CARDS Entrance Fix
  ------------------------------------------- */
  const cardsContainer = document.querySelector(".anime-cards");
  if (cardsContainer) {
    setTimeout(() => {
      cardsContainer.classList.add("cards-loaded");
    }, 100);
  }

  /* -------------------------------------------
     PARTICLES BACKGROUND
  ------------------------------------------- */
  function createParticles() {
    const container = document.getElementById("particles");
    if (!container) return;

    const count = 30;
    for (let i = 0; i < count; i++) {
      const p = document.createElement("div");
      p.className = "particle";
      p.style.left = Math.random() * 100 + "%";
      p.style.animationDelay = Math.random() * 15 + "s";
      p.style.animationDuration = Math.random() * 10 + 15 + "s";
      p.style.background = Math.random() > 0.5 ? "#00B2FF" : "#FF5E00";
      container.appendChild(p);
    }
  }
  createParticles();

  /* -------------------------------------------
     HERO TEXT ROTATOR + BACKGROUND SWIPE
  ------------------------------------------- */
  const textSets = Array.from(document.querySelectorAll(".text-rotator .text-set"));
  const heroCar = document.getElementById("heroCar");
  const heroBgCurrent = document.querySelector(".hero-bg-current");
  const heroBgNext = document.querySelector(".hero-bg-next");
  const prevBtn = document.querySelector(".hero-prev");
  const nextBtn = document.querySelector(".hero-next");
  const heroSection = document.querySelector(".hero");

  let currentIndex = 0;
  let isAnimating = false;
  let activeBg = heroBgCurrent;
  let idleBg = heroBgNext;
  let autoTimer = null;

  function wrapTitleChars(textSet) {
    if (!textSet) return;
    const titleEl = textSet.querySelector(".glitch-text");
    if (!titleEl) return;

    const baseText = titleEl.getAttribute("data-text") || titleEl.textContent.trim();
    titleEl.setAttribute("data-text", baseText);

    titleEl.innerHTML = "";
    Array.from(baseText).forEach((char, i) => {
      const span = document.createElement("span");
      span.className = "char";
      span.textContent = char === " " ? "\u00A0" : char;
      span.style.animationDelay = `${i * 0.05}s`;
      titleEl.appendChild(span);
    });
  }

  function applyBackgroundFromSet(textSet, instant = false) {
    if (!activeBg || !idleBg || !textSet) return;

    const bgType = textSet.dataset.bgType || "image";
    const bgUrl = textSet.dataset.bg || "";
    const carUrl = textSet.dataset.car || "";

    if (heroSection) {
      if (bgType === "plain") heroSection.classList.add("no-overlay");
      else heroSection.classList.remove("no-overlay");
    }

    if (heroCar && carUrl) {
      heroCar.classList.remove("car-enter");
      heroCar.src = carUrl;
      void heroCar.offsetWidth;
      heroCar.classList.add("car-enter");
    }

    idleBg.style.transition = "none";
    activeBg.style.transition = "none";

    if (bgType === "image" && bgUrl) {
      idleBg.style.backgroundImage = `url('${bgUrl}')`;
      idleBg.classList.remove("hero-bg-plain");
    } else {
      idleBg.style.backgroundImage = "none";
      idleBg.classList.add("hero-bg-plain");
    }

    idleBg.style.transform = "translateX(-100%)";

    if (instant) {
      idleBg.style.transform = "translateX(0)";
      activeBg.style.transform = "translateX(100%)";
      const tmp = activeBg;
      activeBg = idleBg;
      idleBg = tmp;
      return;
    }

    void idleBg.offsetWidth;

    idleBg.style.transition = "transform .85s ease";
    activeBg.style.transition = "transform .85s ease";

    idleBg.style.transform = "translateX(0)";
    activeBg.style.transform = "translateX(100%)";

    setTimeout(() => {
      const tmp = activeBg;
      activeBg = idleBg;
      idleBg = tmp;
    }, 900);
  }

  function showSet(index, animate = true) {
    if (!textSets.length) return;

    index = (index + textSets.length) % textSets.length;
    const newSet = textSets[index];
    const oldSet = textSets[currentIndex];

    if (!animate) {
      textSets.forEach((set, i) => {
        set.classList.toggle("active", i === index);
        const subtitle = set.querySelector(".subtitle");
        if (subtitle) subtitle.classList.toggle("visible", i === index);
      });

      wrapTitleChars(newSet);
      applyBackgroundFromSet(newSet, true);

      currentIndex = index;
      return;
    }

    if (isAnimating) return;
    isAnimating = true;

    if (oldSet) {
      const oldTitle = oldSet.querySelector(".glitch-text");
      if (oldTitle) {
        oldTitle.querySelectorAll(".char").forEach((c, i) => {
          c.classList.add("out");
          c.style.animationDelay = `${i * 0.02}s`;
        });
      }
      const oldSubtitle = oldSet.querySelector(".subtitle");
      if (oldSubtitle) oldSubtitle.classList.remove("visible");
    }

    setTimeout(() => {
      textSets.forEach((set, i) => set.classList.toggle("active", i === index));
      wrapTitleChars(newSet);

      const newSubtitle = newSet.querySelector(".subtitle");
      if (newSubtitle) {
        setTimeout(() => newSubtitle.classList.add("visible"), 450);
      }

      applyBackgroundFromSet(newSet, false);

      currentIndex = index;

      setTimeout(() => {
        isAnimating = false;
      }, 700);
    }, 280);
  }

  if (textSets.length) {
    textSets.forEach((set) => {
      const h1 = set.querySelector(".glitch-text");
      if (h1) {
        const t = h1.getAttribute("data-text") || h1.textContent.trim();
        h1.setAttribute("data-text", t);
      }
    });

    showSet(0, false);
  }

  function nextSlide() {
    showSet(currentIndex + 1, true);
    resetAuto();
  }
  function prevSlide() {
    showSet(currentIndex - 1, true);
    resetAuto();
  }

  if (nextBtn) nextBtn.addEventListener("click", nextSlide);
  if (prevBtn) prevBtn.addEventListener("click", prevSlide);

  function startAuto() {
    autoTimer = setInterval(() => {
      showSet(currentIndex + 1, true);
    }, 6500);
  }
  function resetAuto() {
    if (autoTimer) clearInterval(autoTimer);
    startAuto();
  }
  if (textSets.length) startAuto();

  /* -------------------------------------------
     COUNTERS
  ------------------------------------------- */
  const counters = document.querySelectorAll(".fact-number");
  const speed = 100;

  const startCounting = () => {
    counters.forEach(counter => {
      const updateCount = () => {
        const target = +counter.getAttribute("data-count");
        const count = +counter.innerText;
        const increment = Math.ceil(target / speed);

        if (count < target) {
          counter.innerText = count + increment;
          setTimeout(updateCount, 30);
        } else {
          counter.innerText = target;
        }
      };
      updateCount();
    });
  };

  const factSection = document.querySelector(".facts");
  if (factSection) {
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        startCounting();
        observer.unobserve(factSection);
      }
    }, { threshold: 0.4 });

    observer.observe(factSection);
  }

  /* -------------------------------------------
     SERVICE TABS
  ------------------------------------------- */
  const serviceTabs = document.querySelectorAll(".service-tab");
  const servicePanes = document.querySelectorAll(".service-pane");

  serviceTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      serviceTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const target = tab.getAttribute("data-tab");

      servicePanes.forEach(pane => {
        pane.classList.remove("active");
        if (pane.id === target) pane.classList.add("active");
      });

      // flash effect
      const targetPane = document.getElementById(target);
      const layout = targetPane ? targetPane.querySelector(".service-layout") : null;

      if (layout) {
        layout.classList.add("flash-active");
        setTimeout(() => layout.classList.remove("flash-active"), 80);
      }
    });
  });


  /* -------------------------------------------
     GSAP ENTRANCES
  ------------------------------------------- */
  if (window.gsap) {
    gsap.from(".hero-text", { opacity: 0, x: -40, duration: 1, ease: "power3.out" });
    gsap.from(".hero-car-img", { opacity: 0, x: 50, duration: 1.1, delay: 0.2, ease: "power3.out" });
  }

/* -------------------------------------------
     TESTIMONIALS CAROUSEL (OwlCarousel)
  ------------------------------------------- */
  function initTestimonialCarousel() {
    if (!window.jQuery || !window.jQuery.fn || typeof window.jQuery.fn.owlCarousel !== "function") {
      setTimeout(initTestimonialCarousel, 100);
      return;
    }

    $(".testimonial-carousel").owlCarousel({
      autoplay: true,
      smartSpeed: 900,
      center: true,
      margin: 25,
      dots: true,
      dotsEach: true,
      loop: true,
      nav: false,
      URLhashListener: false,
      startPosition: 0,
      responsive: {
        0:   { items: 1 },
        768: { items: 2 },
        992: { items: 3 }
      }
    });
  }

  initTestimonialCarousel(); 
  
  /* -------------------------------------------
   PACKAGES SWIPER (Auto-forward Carousel)
------------------------------------------- */

const packageSwiper = new Swiper('.packages-swiper', {
  slidesPerView: 3,
  spaceBetween: 60,
  slidesPerGroup: 3,
  loop: true,
  grabCursor: true,
  speed: 1200,

  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },

  breakpoints: {
    0: { slidesPerView: 1, slidesPerGroup: 1 },
    768: { slidesPerView: 2, slidesPerGroup: 2 },
    1024: { slidesPerView: 3, slidesPerGroup: 3 },
  },
});

// 🔁 continuous autoplay (manual control)
setInterval(() => {
  packageSwiper.slideNext();
}, 3500);


  /* -------------------------------------------
   FLATPICKR DATE + CUSTOM TIME SELECTOR
------------------------------------------- */
flatpickr("#datetime", {
  enableTime: false,
  dateFormat: "Y-m-d H:i",
  altInput: true,
  altFormat: "F j, Y — h:i K",
  minDate: "today",
  disableMobile: true,

  onReady: function(selectedDates, dateStr, instance) {
    instance.calendarContainer.classList.add("fp-ready");
  },

  onDayCreate: function(_, __, ___, dayElem) {
    if (dayElem.dateObj.getDay() === 0 || dayElem.dateObj.getDay() === 6) {
      dayElem.classList.add("weekend");
    }
  },

  onOpen: function(selectedDates, dateStr, instance) {
    setTimeout(() => {
      let fp = instance;

      const oldTime = fp.calendarContainer.querySelector(".flatpickr-time");
      if (oldTime) oldTime.remove();

      if (!fp.calendarContainer.querySelector(".flatpickr-session")) {
        const sessionDiv = document.createElement("div");
        sessionDiv.className = "flatpickr-session";

        sessionDiv.innerHTML = `
          <label style="font-weight:600; margin-bottom:6px; display:block;">
            Select Time
          </label>

          <select id="sessionSelect">
            <option value="">-- Choose a Time --</option>
            <option>09:00 AM</option>
            <option>10:00 AM</option>
            <option>11:00 AM</option>
            <option>12:00 PM</option>
            <option>01:00 PM</option>
            <option>02:00 PM</option>
            <option>03:00 PM</option>
            <option>04:00 PM</option>
            <option>05:00 PM</option>
          </select>

          <button type="button" class="flatpickr-clear-btn">Clear</button>
        `;

        fp.calendarContainer.appendChild(sessionDiv);

        const sessionSelect = sessionDiv.querySelector("#sessionSelect");

        sessionSelect.addEventListener("change", () => {
          if (!sessionSelect.value) return;

          const datePart =
            fp.selectedDates[0]
              ? fp.formatDate(fp.selectedDates[0], "Y-m-d")
              : fp.formatDate(new Date(), "Y-m-d");

          fp.setDate(`${datePart} ${sessionSelect.value}`);
        });

        sessionDiv.querySelector(".flatpickr-clear-btn").onclick = () => {
          fp.clear();
          sessionSelect.value = "";
        };
      }
    }, 10);
  }
});


/* -------------------------------------------
   SERVICE OPTIONS DATABASE
------------------------------------------- */
const serviceOptions = {
  all: [
    "Basic Cleaning",
    "Premium Cleaning",
    "Full Diagnostic",
    "Engine Servicing",
    "Detailing Package",
    "Tire Replacement",
    "Interior Shampoo"
  ],

  sedan: [
    "Sedan Basic Wash",
    "Sedan Full Diagnostic",
    "Sedan Oil Change",
    "Sedan Interior Detailing"
  ],

  suv: [
    "SUV Deep Wash",
    "SUV Engine Servicing",
    "4x4 Suspension Check",
    "SUV Off-Road Cleaning"
  ],

  luxury: [
    "Luxury Ceramic Coating",
    "Luxury Premium Engine Care",
    "Luxury Leather Conditioning",
    "Showroom Detailing"
  ]
};


/* -------------------------------------------
   UPDATE SERVICE DROPDOWN
------------------------------------------- */
function updateServiceList(type) {
  const select = document.getElementById("serviceSelect");
  if (!select) return;

  select.innerHTML = `<option value="">Select A Service</option>`;

  serviceOptions[type].forEach(service => {
    const opt = document.createElement("option");
    opt.textContent = service;
    opt.value = service;
    select.appendChild(opt);
  });
}

updateServiceList("all");


/* -------------------------------------------
   SERVICE TYPE BUTTON GROUP
------------------------------------------- */
const buttons = document.querySelectorAll("#serviceTypeButtons .bbtn");

buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    buttons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    const selectedType = btn.dataset.type;
    updateServiceList(selectedType);
  });
});


/* -------------------------------------------
   TECH CARD MOBILE BEHAVIOR
------------------------------------------- */
const isMobile = window.innerWidth < 768;

document.querySelectorAll('.tech-card').forEach(card => {
  card.addEventListener('click', (e) => {
    if (e.target.closest('.social-icons')) return;
    if (isMobile) card.classList.toggle('show-social');
  });
});

/* -------------------------------------------
   FOOTER PHONE NUMBER ROLLER
------------------------------------------- */
const footerContainer = document.getElementById("footer-phone-roller");
const PHONE_NUMBER = "(406) 555-0120";

function footerSplitRoller(textVal) {
  if (!footerContainer) return;

  footerContainer.innerHTML = "";
  const chars = textVal.split("");

  chars.forEach((ch, index) => {
    const wrap = document.createElement("span");
    wrap.className = "letter-wrap";
    wrap.style.setProperty("--i", index);

    const rail = document.createElement("span");
    rail.className = "letter-rail";

    const main = document.createElement("span");
    main.className = "letter";
    main.textContent = ch === " " ? "\u00A0" : ch;

    const dup = document.createElement("span");
    dup.className = "letter letter-duplicate";
    dup.textContent = ch === " " ? "\u00A0" : ch;

    rail.appendChild(main);
    rail.appendChild(dup);
    wrap.appendChild(rail);
    footerContainer.appendChild(wrap);
  });
}

if (footerContainer) {
  footerContainer.addEventListener("touchstart", e => {
    e.preventDefault();
    footerContainer.classList.toggle("hovered");
  });

  footerSplitRoller(PHONE_NUMBER);
}

// ================================
// PRINT BROCHURE BUTTON
// ================================
const printBtn = document.getElementById("printQuote");
if (printBtn) {
  printBtn.addEventListener("click", () => {
    window.print(); // Opens print dialog
  });
}

// ================================
// PRINT BOOKING CONFIRMATION
// ================================
const form = document.querySelector(".booking-right form");

if (form) {
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Fill print confirmation
    document.getElementById("printName").textContent =
      form.querySelector('input[type="text"]').value;

    document.getElementById("printEmail").textContent =
      form.querySelector('input[type="email"]').value;

    document.getElementById("printService").textContent =
      form.querySelector("#serviceSelect").value;

    document.getElementById("printDateTime").textContent =
      form.querySelector("#datetime").value;

    document.getElementById("printMessage").textContent =
      form.querySelector("textarea").value || "—";

    // Print
    setTimeout(() => {
      window.print();
    }, 400);
  });

  // 🔥 CLEAR FORM AFTER PRINT
  window.onafterprint = () => {
    form.reset();

    // Optional: reset service list back to "All"
    updateServiceList("all");

    // Optional: reset active button
    document.querySelectorAll("#serviceTypeButtons .bbtn").forEach(btn =>
      btn.classList.remove("active")
    );
    document.querySelector('#serviceTypeButtons .bbtn[data-type="all"]')
      ?.classList.add("active");
  };
}

});

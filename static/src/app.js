import './app.css';

const setupHomeScrollEffects = () => {
  const root = document.querySelector('[data-parallax-root]');
  if (!root) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealNodes = document.querySelectorAll('[data-reveal]');
  const parallaxNodes = document.querySelectorAll('[data-parallax]');

  revealNodes.forEach((node) => {
    node.classList.add('sf-reveal');
  });

  if (!reducedMotion && revealNodes.length) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: '0px 0px -12% 0px', threshold: 0.12 }
    );

    revealNodes.forEach((node) => revealObserver.observe(node));
  } else {
    revealNodes.forEach((node) => node.classList.add('is-visible'));
  }

  if (reducedMotion || !parallaxNodes.length) return;

  let rafId = null;
  const runParallax = () => {
    const scrollY = window.scrollY || window.pageYOffset;
    parallaxNodes.forEach((node) => {
      const speed = Number(node.getAttribute('data-speed') || '0.15');
      const offset = scrollY * speed;
      node.style.transform = `translate3d(0, ${offset.toFixed(2)}px, 0)`;
    });
    rafId = null;
  };

  const requestTick = () => {
    if (rafId !== null) return;
    rafId = requestAnimationFrame(runParallax);
  };

  runParallax();
  window.addEventListener('scroll', requestTick, { passive: true });
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupHomeScrollEffects);
} else {
  setupHomeScrollEffects();
}

document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.querySelector('.navbar');
  const header = document.querySelector('header');
  const headerHeight = header.offsetHeight;
  const scrollTopBtn = document.createElement('div');

  scrollTopBtn.innerHTML = '&#8679;';
  scrollTopBtn.classList.add('scroll-to-top');
  document.body.appendChild(scrollTopBtn);

  scrollTopBtn.style.display = 'none';

  navbar.style.top = `${headerHeight}px`;

  window.addEventListener('scroll', () => {
    if (window.scrollY > headerHeight) {
      navbar.style.position = 'fixed';
      navbar.style.top = '0';
      scrollTopBtn.style.display = 'flex';
    } else {
      navbar.style.position = 'absolute';
      navbar.style.top = `${headerHeight}px`;
      scrollTopBtn.style.display = 'none';
    }
  });

  scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});

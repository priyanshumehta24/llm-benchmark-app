import { useEffect } from 'react';
import anime from 'animejs';

export const useStaggerFadeUp = (selector, deps = []) => {
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    const elements = document.querySelectorAll(selector);
    if (!elements.length) return;

    // Reset initial state before animating
    anime.set(elements, { opacity: 0, translateY: 20 });

    anime({
      targets: elements,
      opacity: [0, 1],
      translateY: [20, 0],
      duration: 800,
      delay: anime.stagger(80),
      easing: 'easeOutExpo'
    });
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps
};

export const useCountUp = (selector, targetValue, deps = []) => {
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    const elements = document.querySelectorAll(selector);
    if (!elements.length) return;
    
    elements.forEach(el => {
      // Use targetValue if provided, otherwise parse the DOM content
      const finalValue = (targetValue !== undefined && targetValue !== null) 
        ? targetValue 
        : (Number(el.textContent.replace(/,/g, '')) || 0);
        
      if (finalValue === 0 && el.textContent.trim() !== '0') return;

      const obj = { val: 0 };
      anime({
        targets: obj,
        val: finalValue,
        round: 1,
        duration: 1200,
        easing: 'easeOutExpo',
        update: () => {
          el.innerHTML = obj.val;
        }
      });
    });
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps
};

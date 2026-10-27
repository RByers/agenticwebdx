const classes = el.className.split(' ');
if (classes.includes('open')) {
  el.className = classes.filter(c => c !== 'open').join(' ');
} else {
  el.className += ' open';
}

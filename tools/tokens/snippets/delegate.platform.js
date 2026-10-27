document.addEventListener('click', event => {
  const button = event.target.closest('.delete');
  if (button) removeItem(button.dataset.id);
});

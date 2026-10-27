const xhr = new XMLHttpRequest();
xhr.open('GET', '/api/user');
xhr.responseType = 'json';
xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    render(xhr.response);
  } else {
    showError(xhr.status);
  }
};
xhr.onerror = () => showError(0);
xhr.send();

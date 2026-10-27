try {
  const res = await fetch('/api/user');
  if (!res.ok) throw res.status;
  render(await res.json());
} catch (e) {
  showError(e);
}

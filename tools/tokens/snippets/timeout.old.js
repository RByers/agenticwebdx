const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 5000);
const res = await fetch(url, { signal: controller.signal });
clearTimeout(timer);

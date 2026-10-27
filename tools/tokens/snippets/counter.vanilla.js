class ClickCounter extends HTMLElement {
  #count = 0;
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = '<button></button>';
    this.button = this.shadowRoot.querySelector('button');
    this.button.addEventListener('click', () => {
      this.#count++;
      this.render();
    });
  }
  connectedCallback() {
    this.render();
  }
  render() {
    this.button.textContent = `Clicked ${this.#count} times`;
  }
}
customElements.define('click-counter', ClickCounter);

import { LitElement, html } from 'lit';

class ClickCounter extends LitElement {
  static properties = { count: { state: true } };
  constructor() {
    super();
    this.count = 0;
  }
  render() {
    return html`<button @click=${() => this.count++}>Clicked ${this.count} times</button>`;
  }
}
customElements.define('click-counter', ClickCounter);

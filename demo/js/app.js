/* Bookstore App - Frontend JavaScript */

const BookstoreApp = {
  getToken() { return localStorage.getItem('token'); },
  setToken(t) { localStorage.setItem('token', t); },
  clearToken() { localStorage.removeItem('token'); },

  requireAuth() {
    if (!this.getToken()) {
      window.location.href = '/login.html';
    }
  },

  async api(path, options = {}) {
    const headers = { 'Content-Type': 'application/json' };
    const token = this.getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(path, {
      ...options,
      headers: { ...headers, ...(options.headers || {}) },
    });
    if (res.status === 401 && token) {
      this.clearToken();
      window.location.href = '/login.html';
      return;
    }
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: res.statusText }));
      throw new Error(err.detail || err.error || res.statusText);
    }
    if (res.status === 204) return null;
    return res.json();
  },

  async refreshCartCounter() {
    const token = this.getToken();
    if (!token) return;
    try {
      const data = await this.api('/api/cart');
      const count = data?.items?.length ?? 0;
      document.querySelectorAll('[data-testid="cart-counter"]').forEach(el => {
        el.textContent = count;
      });
    } catch (_) {
      // ignore cart counter refresh errors
    }
  },
};

/* ------------------------------------------------------------------ */
/* Login page                                                           */
/* ------------------------------------------------------------------ */
async function initLoginPage() {
  // Already logged in? go to catalog
  if (BookstoreApp.getToken()) {
    window.location.href = '/catalog.html';
    return;
  }

  const form = document.getElementById('login-form');
  const emailInput = document.querySelector('[data-testid="email-input"]');
  const passwordInput = document.querySelector('[data-testid="password-input"]');
  const errorEl = document.querySelector('[data-testid="login-error"]');
  const emailValidation = document.querySelector('[data-testid="email-validation"]');
  const passwordValidation = document.querySelector('[data-testid="password-validation"]');

  function hideValidation() {
    if (emailValidation) emailValidation.classList.add('hidden');
    if (passwordValidation) passwordValidation.classList.add('hidden');
    if (errorEl) errorEl.classList.add('hidden');
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideValidation();

      const email = emailInput?.value.trim() || '';
      const password = passwordInput?.value || '';

      let hasError = false;
      if (!email) {
        if (emailValidation) emailValidation.classList.remove('hidden');
        hasError = true;
      }
      if (!password) {
        if (passwordValidation) passwordValidation.classList.remove('hidden');
        hasError = true;
      }
      if (hasError) return;

      try {
        const data = await BookstoreApp.api('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        });
        BookstoreApp.setToken(data.token);
        window.location.href = '/catalog.html';
      } catch (err) {
        if (errorEl) {
          errorEl.textContent = err.message || 'Login failed';
          errorEl.classList.remove('hidden');
        }
      }
    });
  }
}

/* ------------------------------------------------------------------ */
/* Catalog page                                                         */
/* ------------------------------------------------------------------ */
async function initCatalogPage() {
  BookstoreApp.requireAuth();

  const searchInput = document.querySelector('[data-testid="search-input"]');
  const categoryFilter = document.querySelector('[data-testid="category-filter"]');
  const sortSelect = document.querySelector('[data-testid="sort-select"]');
  const searchSubmit = document.querySelector('[data-testid="search-submit"]');
  const bookListEl = document.querySelector('[data-testid="book-list"]');
  const noResultsEl = document.querySelector('[data-testid="no-results-message"]');

  await BookstoreApp.refreshCartCounter();

  async function loadBooks() {
    const params = new URLSearchParams();
    const search = searchInput?.value.trim();
    const category = categoryFilter?.value;
    const sort = sortSelect?.value;
    if (search) params.set('search', search);
    if (category) params.set('category', category);
    if (sort) params.set('sort', sort);
    params.set('limit', '20');

    try {
      const data = await BookstoreApp.api(`/api/books?${params}`);
      renderBooks(data.items);
    } catch (err) {
      console.error('Failed to load books', err);
    }
  }

  function renderBooks(books) {
    if (!bookListEl) return;
    bookListEl.innerHTML = '';

    if (books.length === 0) {
      if (noResultsEl) noResultsEl.classList.remove('hidden');
      return;
    }
    if (noResultsEl) noResultsEl.classList.add('hidden');

    books.forEach(book => {
      const li = document.createElement('li');
      li.setAttribute('data-testid', `book-item-${book.id}`);
      li.innerHTML = `
        <span class="book-title" data-testid="book-title">${escapeHtml(book.title)}</span>
        <span class="book-author" data-testid="book-author">${escapeHtml(book.author)}</span>
        <span class="book-category" data-testid="book-category">${escapeHtml(book.category)}</span>
        <span class="book-price" data-testid="book-price">$${book.price.toFixed(2)}</span>
        <button data-testid="add-to-cart-${book.id}" ${book.stock === 0 ? 'disabled' : ''}>
          ${book.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
        </button>
      `;
      const btn = li.querySelector(`[data-testid="add-to-cart-${book.id}"]`);
      if (btn && book.stock > 0) {
        btn.addEventListener('click', () => addToCart(book.id));
      }
      bookListEl.appendChild(li);
    });
  }

  async function addToCart(bookId) {
    try {
      await BookstoreApp.api('/api/cart/items', {
        method: 'POST',
        body: JSON.stringify({ bookId, quantity: 1 }),
      });
      await BookstoreApp.refreshCartCounter();
    } catch (err) {
      alert(err.message || 'Failed to add to cart');
    }
  }

  if (searchSubmit) {
    searchSubmit.addEventListener('click', loadBooks);
  }
  if (searchInput) {
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') loadBooks();
    });
  }

  await loadBooks();
}

/* ------------------------------------------------------------------ */
/* Cart page                                                            */
/* ------------------------------------------------------------------ */
async function initCartPage() {
  BookstoreApp.requireAuth();

  const cartItemsEl = document.querySelector('[data-testid="cart-items"]');
  const emptyMsgEl = document.querySelector('[data-testid="empty-cart-message"]');
  const subtotalEl = document.querySelector('[data-testid="cart-subtotal"]');

  await BookstoreApp.refreshCartCounter();

  async function loadCart() {
    try {
      const data = await BookstoreApp.api('/api/cart');
      renderCart(data);
    } catch (err) {
      console.error('Failed to load cart', err);
    }
  }

  function renderCart(data) {
    if (!cartItemsEl) return;
    cartItemsEl.innerHTML = '';

    if (!data.items || data.items.length === 0) {
      if (emptyMsgEl) emptyMsgEl.classList.remove('hidden');
      if (subtotalEl) subtotalEl.textContent = '$0.00';
      return;
    }
    if (emptyMsgEl) emptyMsgEl.classList.add('hidden');

    data.items.forEach(item => {
      const row = document.createElement('tr');
      row.setAttribute('data-testid', `cart-item-${item.bookId}`);
      row.innerHTML = `
        <td>${escapeHtml(item.title)}</td>
        <td>$${item.price.toFixed(2)}</td>
        <td>
          <input type="number" data-testid="qty-${item.bookId}" value="${item.quantity}" min="1" style="width:60px">
        </td>
        <td>$${item.lineTotal.toFixed(2)}</td>
        <td>
          <button class="danger" data-testid="remove-${item.bookId}">Remove</button>
        </td>
      `;

      const qtyInput = row.querySelector(`[data-testid="qty-${item.bookId}"]`);
      if (qtyInput) {
        qtyInput.addEventListener('change', async () => {
          const qty = parseInt(qtyInput.value);
          try {
            await BookstoreApp.api(`/api/cart/items/${item.bookId}`, {
              method: 'PATCH',
              body: JSON.stringify({ quantity: qty }),
            });
            await loadCart();
            await BookstoreApp.refreshCartCounter();
          } catch (err) {
            alert(err.message || 'Failed to update quantity');
          }
        });
      }

      const removeBtn = row.querySelector(`[data-testid="remove-${item.bookId}"]`);
      if (removeBtn) {
        removeBtn.addEventListener('click', async () => {
          try {
            await BookstoreApp.api(`/api/cart/items/${item.bookId}`, { method: 'DELETE' });
            await loadCart();
            await BookstoreApp.refreshCartCounter();
          } catch (err) {
            alert(err.message || 'Failed to remove item');
          }
        });
      }

      cartItemsEl.appendChild(row);
    });

    if (subtotalEl) subtotalEl.textContent = `$${data.subtotal.toFixed(2)}`;
  }

  await loadCart();
}

/* ------------------------------------------------------------------ */
/* Checkout page                                                        */
/* ------------------------------------------------------------------ */
function initCheckoutPage() {
  BookstoreApp.requireAuth();

  const shippingSection = document.querySelector('[data-testid="shipping-section"]');
  const paymentSection = document.querySelector('[data-testid="payment-section"]');
  const reviewSection = document.querySelector('[data-testid="review-section"]');

  const stepShipping = document.querySelector('[data-testid="step-shipping"]');
  const stepPayment = document.querySelector('[data-testid="step-payment"]');
  const stepReview = document.querySelector('[data-testid="step-review"]');

  let shippingData = {};
  let paymentData = {};

  function showSection(section) {
    [shippingSection, paymentSection, reviewSection].forEach(s => s?.classList.add('hidden'));
    section?.classList.remove('hidden');
  }

  function setActiveStep(step) {
    [stepShipping, stepPayment, stepReview].forEach(s => s?.classList.remove('active'));
    step?.classList.add('active');
  }

  // Shipping next
  const shippingNext = document.querySelector('[data-testid="shipping-next"]');
  if (shippingNext) {
    shippingNext.addEventListener('click', () => {
      shippingData = {
        name: document.querySelector('[data-testid="ship-name"]')?.value || '',
        address: document.querySelector('[data-testid="ship-address"]')?.value || '',
        city: document.querySelector('[data-testid="ship-city"]')?.value || '',
        zip: document.querySelector('[data-testid="ship-zip"]')?.value || '',
      };
      showSection(paymentSection);
      setActiveStep(stepPayment);
    });
  }

  // Payment next
  const paymentNext = document.querySelector('[data-testid="payment-next"]');
  if (paymentNext) {
    paymentNext.addEventListener('click', async () => {
      const cardNumber = document.querySelector('[data-testid="card-number"]')?.value || '';
      const cardLast4 = document.querySelector('[data-testid="card-last4"]')?.value || cardNumber.slice(-4);
      paymentData = { cardLast4 };

      // Populate review summary
      const summaryEl = document.querySelector('[data-testid="order-summary"]');
      if (summaryEl) {
        try {
          const cart = await BookstoreApp.api('/api/cart');
          let html = '<table class="order-summary-table"><tbody>';
          cart.items.forEach(item => {
            html += `<tr><td>${escapeHtml(item.title)} x${item.quantity}</td><td>$${item.lineTotal.toFixed(2)}</td></tr>`;
          });
          html += `</tbody><tfoot><tr><td><strong>Total</strong></td><td><strong>$${cart.subtotal.toFixed(2)}</strong></td></tr></tfoot></table>`;
          html += `<p><strong>Ship to:</strong> ${escapeHtml(shippingData.name)}, ${escapeHtml(shippingData.address)}, ${escapeHtml(shippingData.city)} ${escapeHtml(shippingData.zip)}</p>`;
          html += `<p><strong>Card ending:</strong> ${escapeHtml(cardLast4)}</p>`;
          summaryEl.innerHTML = html;
        } catch (_) {}
      }

      showSection(reviewSection);
      setActiveStep(stepReview);
    });
  }

  // Confirm order
  const confirmBtn = document.querySelector('[data-testid="confirm-order"]');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', async () => {
      try {
        const order = await BookstoreApp.api('/api/orders', {
          method: 'POST',
          body: JSON.stringify({
            shipping: shippingData,
            payment: { cardLast4: paymentData.cardLast4 },
          }),
        });
        window.location.href = `/order-success.html?orderId=${order.id}`;
      } catch (err) {
        alert(err.message || 'Failed to place order');
      }
    });
  }

  showSection(shippingSection);
  setActiveStep(stepShipping);
}

/* ------------------------------------------------------------------ */
/* Order success page                                                   */
/* ------------------------------------------------------------------ */
function initOrderSuccessPage() {
  const params = new URLSearchParams(window.location.search);
  const orderId = params.get('orderId') || 'Unknown';
  const el = document.getElementById('order-id');
  if (el) el.textContent = orderId;
}

/* ------------------------------------------------------------------ */
/* Orders list page                                                     */
/* ------------------------------------------------------------------ */
async function initOrdersPage() {
  BookstoreApp.requireAuth();

  const listEl = document.getElementById('orders-list');

  try {
    const data = await BookstoreApp.api('/api/orders?limit=50');
    if (!listEl) return;

    if (!data.items || data.items.length === 0) {
      listEl.innerHTML = '<li>No orders found.</li>';
      return;
    }

    listEl.innerHTML = '';
    data.items.forEach(order => {
      const li = document.createElement('li');
      const date = new Date(order.createdAt).toLocaleDateString();
      li.innerHTML = `
        <div>
          <strong>${escapeHtml(order.id)}</strong>
          <span style="color:#666;font-size:0.85rem;margin-left:0.5rem">${date}</span>
        </div>
        <div>
          <span>$${order.total.toFixed(2)}</span>
          <span class="order-status ${order.status}" style="margin-left:1rem">${order.status}</span>
        </div>
      `;
      listEl.appendChild(li);
    });
  } catch (err) {
    if (listEl) listEl.innerHTML = `<li>Error: ${escapeHtml(err.message)}</li>`;
  }
}

/* ------------------------------------------------------------------ */
/* Utility                                                              */
/* ------------------------------------------------------------------ */
function escapeHtml(str) {
  if (typeof str !== 'string') return String(str);
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// إدارة سلة المشتريات
const MobileMenuManager = {
    toggle: () => {
        const menu = document.getElementById('mobile-menu');
        if (menu) {
            menu.classList.toggle('hidden');
        }
    }
};

const ThemeManager = {
    init: () => {
        const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
        toggleBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                document.documentElement.classList.toggle('dark');
                if (document.documentElement.classList.contains('dark')) {
                    localStorage.setItem('theme', 'dark');
                } else {
                    localStorage.setItem('theme', 'light');
                }
            });
        });
    }
};

const ScrollToTopManager = {
    init: () => {
        const buttonHTML = `
            <button id="scroll-to-top" class="hidden fixed bottom-24 left-6 z-40 bg-brand-800/80 dark:bg-brand-500/80 text-white p-3 rounded-full shadow-2xl hover:bg-brand-700 dark:hover:bg-brand-600 transition-all duration-300 transform hover:scale-110 backdrop-blur-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                </svg>
            </button>
        `;
        document.body.insertAdjacentHTML('beforeend', buttonHTML);

        const btn = document.getElementById('scroll-to-top');
        if (!btn) return;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                btn.classList.remove('hidden');
            } else {
                btn.classList.add('hidden');
            }
        });

        btn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
};

const AnimationManager = {
    init: () => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        const targets = document.querySelectorAll('.fade-in-on-scroll');
        targets.forEach(target => observer.observe(target));
    }
};

const CartManager = {
    isDrawerOpen: false,

    getCart: () => {
        return JSON.parse(localStorage.getItem('kuwait_store_cart')) || [];
    },

    saveCart: (cart) => {
        localStorage.setItem('kuwait_store_cart', JSON.stringify(cart));
        CartManager.updateCartCount();
        CartManager.renderDrawerCart();
    },

    addToCart: (product, quantity = 1) => {
        let cart = CartManager.getCart();
        const existingItem = cart.find(item => item.id === product.id);

        if (existingItem) {
            existingItem.quantity += parseInt(quantity);
        } else {
            cart.push({
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image,
                currency: product.currency,
                quantity: parseInt(quantity)
            });
        }

        CartManager.saveCart(cart);
        CartManager.openDrawer(); // فتح السلة تلقائياً عند الإضافة
    },

    removeFromCart: (productId) => {
        let cart = CartManager.getCart();
        cart = cart.filter(item => item.id !== productId);
        CartManager.saveCart(cart);
        CartManager.renderDrawerCart();
    },

    updateQuantity: (productId, newQty) => {
        let cart = CartManager.getCart();
        const item = cart.find(item => item.id === productId);
        if (item) {
            item.quantity = parseInt(newQty);
            if (item.quantity <= 0) {
                CartManager.removeFromCart(productId);
            } else {
                CartManager.saveCart(cart);
                CartManager.renderDrawerCart();
            }
        }
    },

    clearCart: () => {
        localStorage.removeItem('kuwait_store_cart');
        CartManager.updateCartCount();
        CartManager.renderDrawerCart();
    },

    updateCartCount: () => {
        const cart = CartManager.getCart();
        const count = cart.reduce((total, item) => total + item.quantity, 0);
        const badges = document.querySelectorAll('.cart-count-badge');
        badges.forEach(badge => {
            badge.innerText = count;
            badge.classList.toggle('hidden', count === 0);
        });
    },

    // --- وظائف السلة الجانبية (Drawer) ---

    initDrawer: () => {
        // حقن HTML السلة الجانبية والزر العائم
        const drawerHTML = `
            <!-- زر السلة العائم -->
            <button onclick="CartManager.toggleDrawer()" class="fixed bottom-6 left-6 z-40 bg-brand-600 text-white p-4 rounded-full shadow-2xl hover:bg-brand-700 transition transform hover:scale-110 flex items-center justify-center border-2 border-gold-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="cart-count-badge absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center border-2 border-white">0</span>
            </button>

            <!-- خلفية التعتيم -->
            <div id="cart-overlay" onclick="CartManager.closeDrawer()" class="fixed inset-0 bg-black bg-opacity-50 z-40 hidden transition-opacity duration-300 opacity-0 backdrop-blur-sm"></div>

            <!-- السلة الجانبية -->
            <div id="cart-drawer" class="fixed top-0 left-0 h-full w-full sm:w-96 bg-sand-50 shadow-2xl z-50 transform -translate-x-full transition-transform duration-300 ease-in-out flex flex-col border-r-4 border-gold-500">
                <div class="p-5 bg-brand-600 text-white flex justify-between items-center shadow-md">
                    <h2 class="text-xl font-bold flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gold-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                        سلة المشتريات
                    </h2>
                    <button onclick="CartManager.closeDrawer()" class="text-gray-200 hover:text-white hover:rotate-90 transition duration-300">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>

                <div id="drawer-items" class="flex-1 overflow-y-auto p-4 space-y-4">
                    <!-- المنتجات ستظهر هنا -->
                </div>

                <div class="p-5 bg-white border-t border-gray-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)]">
                    <div class="flex justify-between items-center mb-4 text-lg font-bold">
                        <span class="text-gray-700">المجموع:</span>
                        <span id="drawer-total" class="text-brand-600">0.000 KWD</span>
                    </div>
                    <a href="checkout.html" class="block w-full bg-brand-600 text-white text-center py-3 rounded-xl font-bold hover:bg-brand-700 transition shadow-lg border-b-4 border-brand-800 active:border-0 active:translate-y-1">
                        إتمام الطلب
                    </a>
                    <a href="cart.html" class="block text-center text-gray-500 text-sm mt-3 hover:text-brand-600 underline">عرض السلة كاملة</a>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', drawerHTML);
        CartManager.renderDrawerCart();
    },

    toggleDrawer: () => {
        if (CartManager.isDrawerOpen) CartManager.closeDrawer();
        else CartManager.openDrawer();
    },

    openDrawer: () => {
        CartManager.isDrawerOpen = true;
        const drawer = document.getElementById('cart-drawer');
        const overlay = document.getElementById('cart-overlay');
        
        drawer.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
        setTimeout(() => overlay.classList.remove('opacity-0'), 10); // تفعيل الأنيميشن
    },

    closeDrawer: () => {
        CartManager.isDrawerOpen = false;
        const drawer = document.getElementById('cart-drawer');
        const overlay = document.getElementById('cart-overlay');
        
        drawer.classList.add('-translate-x-full');
        overlay.classList.add('opacity-0');
        setTimeout(() => overlay.classList.add('hidden'), 300);
    },

    renderDrawerCart: () => {
        const cart = CartManager.getCart();
        const container = document.getElementById('drawer-items');
        const totalEl = document.getElementById('drawer-total');
        
        if (!container) return;

        if (cart.length === 0) {
            container.innerHTML = `
                <div class="text-center py-10 opacity-60">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                    <p>السلة فارغة</p>
                </div>`;
            totalEl.innerText = '0.000 KWD';
            return;
        }

        container.innerHTML = '';
        let total = 0;

        cart.forEach(item => {
            total += parseFloat(item.price) * item.quantity;
            container.innerHTML += `
                <div class="flex gap-3 bg-white p-3 rounded-xl shadow-sm border border-gray-100 relative group">
                    <img src="${item.image}" class="w-16 h-16 object-cover rounded-lg border border-gray-200">
                    <div class="flex-1">
                        <h4 class="text-sm font-bold text-gray-800 line-clamp-1">${item.name}</h4>
                        <div class="flex justify-between items-center mt-2">
                            <span class="text-brand-600 font-bold text-sm">${item.price} ${item.currency}</span>
                            <div class="flex items-center gap-2 bg-gray-50 rounded-lg px-2 py-1">
                                <button onclick="CartManager.updateQuantity('${item.id}', ${item.quantity - 1})" class="text-gray-500 hover:text-red-500 font-bold">-</button>
                                <span class="text-xs font-bold w-4 text-center">${item.quantity}</span>
                                <button onclick="CartManager.updateQuantity('${item.id}', ${item.quantity + 1})" class="text-gray-500 hover:text-green-500 font-bold">+</button>
                            </div>
                        </div>
                    </div>
                    <button onclick="CartManager.removeFromCart('${item.id}')" class="absolute top-2 left-2 text-gray-300 hover:text-red-500"><svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg></button>
                </div>
            `;
        });
        totalEl.innerText = total.toFixed(3) + ' KWD';
    }
};

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    CartManager.initDrawer();
    CartManager.updateCartCount();
    ThemeManager.init();
    ScrollToTopManager.init();
    AnimationManager.init();

    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});
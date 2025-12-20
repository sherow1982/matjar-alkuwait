import os
import json

# --- إعدادات المسار (المسار الذي طلبته) ---
base_path = r"C:\Users\shero\OneDrive\Desktop\متاجر الكويت على جيت هب"

# --- محتوى الملفات ---

# 1. محتوى ملف البيانات التجريبي (products.json)
products_data = [
    {
        "id": "101",
        "name": "عطر العود الكويتي الملكي",
        "description": "عطر فاخر مستخلص من أجود أنواع العود، ثبات عالي ورائحة فواحة تعكس التراث الكويتي الأصيل.",
        "price": "25.000",
        "currency": "KWD",
        "image": "https://images.unsplash.com/photo-1594035910387-fea4779426e9?auto=format&fit=crop&w=800&q=80",
        "category": "عطور",
        "sku": "KW-OUD-01",
        "availability": "InStock"
    },
    {
        "id": "102",
        "name": "دراعة استقبال مطرزة",
        "description": "دراعة كويتية بتصميم عصري وتطريز يدوي فاخر، خامة باردة ومريحة للصيف.",
        "price": "45.500",
        "currency": "KWD",
        "image": "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?auto=format&fit=crop&w=800&q=80",
        "category": "ملابس نسائية",
        "sku": "KW-DR-02",
        "availability": "InStock"
    },
    {
        "id": "103",
        "name": "مبخرة خشبية فاخرة",
        "description": "مبخرة بتصميم إسلامي هندسي، مصنوعة من الخشب الطبيعي مع تطعيمات ذهبية.",
        "price": "12.000",
        "currency": "KWD",
        "image": "https://images.unsplash.com/photo-1615634260167-c8cdede054de?auto=format&fit=crop&w=800&q=80",
        "category": "ديكور منزلي",
        "sku": "KW-DEC-03",
        "availability": "InStock"
    }
]

# 2. محتوى الصفحة الرئيسية (index.html)
index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر الكويت | الرئيسية</title>
    <meta name="description" content="تسوق أفضل المنتجات الكويتية أونلاين">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Cairo', 'sans-serif'] },
                    colors: { brand: { 500: '#1a4d2e', 600: '#143d24' }, gold: { 500: '#d4af37' } }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-50 font-sans text-gray-800">
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold text-brand-500">متجر الكويت</h1>
            <div class="hidden md:flex space-x-6 space-x-reverse text-gray-600">
                <a href="#" class="hover:text-brand-500">الرئيسية</a>
                <a href="#" class="hover:text-brand-500">الأقسام</a>
            </div>
        </div>
    </nav>

    <header class="bg-brand-500 text-white py-16 text-center relative overflow-hidden">
        <div class="relative z-10 container mx-auto px-4">
            <h2 class="text-4xl md:text-5xl font-bold mb-4">أفخم المنتجات الكويتية</h2>
            <p class="text-xl opacity-90 mb-8">جودة عالية، تراث أصيل، وتوصيل سريع</p>
            <input type="text" id="search" placeholder="ابحث عن منتج..." class="w-full max-w-md px-6 py-3 rounded-full text-gray-800 focus:outline-none shadow-lg">
        </div>
    </header>

    <main class="container mx-auto px-4 py-12">
        <div id="loading" class="text-center py-10 text-xl text-gray-500">جاري تحميل المنتجات...</div>
        <div id="products-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8"></div>
    </main>

    <footer class="bg-gray-900 text-white py-8 mt-12 text-center">
        <p>&copy; 2023 متجر الكويت. جميع الحقوق محفوظة.</p>
    </footer>

    <script>
        let allProducts = [];
        async function fetchProducts() {
            try {
                const response = await fetch('products.json');
                allProducts = await response.json();
                renderProducts(allProducts);
                document.getElementById('loading').style.display = 'none';
            } catch (error) {
                document.getElementById('loading').innerText = 'حدث خطأ في التحميل.';
            }
        }

        function renderProducts(products) {
            const grid = document.getElementById('products-grid');
            grid.innerHTML = '';
            products.forEach(p => {
                grid.innerHTML += `
                    <a href="product.html?id=${p.id}" class="group bg-white rounded-2xl shadow-sm hover:shadow-xl transition duration-300 overflow-hidden border border-gray-100 flex flex-col">
                        <div class="relative h-64 overflow-hidden bg-gray-100">
                            <img src="${p.image}" alt="${p.name}" class="w-full h-full object-cover transform group-hover:scale-110 transition duration-500">
                        </div>
                        <div class="p-5 flex-1 flex flex-col">
                            <span class="text-xs text-gold-500 font-bold uppercase mb-1">${p.category}</span>
                            <h3 class="font-bold text-lg text-gray-900 mb-2 group-hover:text-brand-500 transition">${p.name}</h3>
                            <div class="mt-auto flex justify-between items-center">
                                <span class="text-brand-500 font-bold text-xl">${p.price} ${p.currency}</span>
                                <span class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm group-hover:bg-brand-500 group-hover:text-white transition">شراء</span>
                            </div>
                        </div>
                    </a>
                `;
            });
        }

        document.getElementById('search').addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = allProducts.filter(p => p.name.toLowerCase().includes(term));
            renderProducts(filtered);
        });

        fetchProducts();
    </script>
</body>
</html>
"""

# 3. محتوى صفحة المنتج (product.html)
product_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر الكويت | تفاصيل المنتج</title>
    <meta name="description" content="تفاصيل المنتج">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Cairo', 'sans-serif'] },
                    colors: { brand: { 500: '#1a4d2e', 600: '#143d24' }, gold: { 500: '#d4af37' } }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-50 font-sans text-gray-800">
    <nav class="bg-white shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex items-center gap-4">
            <a href="index.html" class="text-gray-500 hover:text-brand-500 transition flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                العودة
            </a>
        </div>
    </nav>

    <main class="container mx-auto px-4 py-10 min-h-screen flex items-center justify-center">
        <div id="loading" class="text-center text-xl text-gray-500">جاري تحميل التفاصيل...</div>
        
        <div id="product-card" class="hidden bg-white rounded-3xl shadow-2xl overflow-hidden w-full max-w-6xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-2">
                <div class="bg-gray-100 relative h-96 md:h-auto flex items-center justify-center p-8 group">
                    <img id="p-image" src="" alt="" class="max-h-[500px] w-auto object-contain drop-shadow-xl transition transform group-hover:scale-105 duration-500">
                </div>
                <div class="p-8 md:p-16 flex flex-col justify-center bg-white">
                    <span id="p-category" class="text-sm text-gold-500 font-bold uppercase tracking-wider mb-3"></span>
                    <h1 id="p-name" class="text-3xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight"></h1>
                    <div class="flex items-center gap-4 mb-8">
                        <div class="text-4xl font-bold text-brand-500"><span id="p-price"></span> <span id="p-currency" class="text-xl text-gray-500"></span></div>
                        <span class="bg-green-100 text-green-800 text-xs font-bold px-3 py-1 rounded-full">متوفر</span>
                    </div>
                    <div class="prose prose-lg text-gray-600 mb-10">
                        <p id="p-desc" class="leading-relaxed"></p>
                    </div>
                    <div class="mt-auto">
                        <a id="whatsapp-btn" href="#" target="_blank" class="w-full flex items-center justify-center gap-3 bg-[#25D366] text-white font-bold py-4 rounded-xl hover:bg-[#128C7E] transition shadow-lg hover:shadow-xl transform hover:-translate-y-1">
                            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
                            اطلب الآن عبر واتساب
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        const STORE_PHONE = "96512345678"; // ضع رقمك هنا

        function getQueryParam(param) { return new URLSearchParams(window.location.search).get(param); }

        function updateSchema(product) {
            const schema = {
                "@context": "https://schema.org/", "@type": "Product",
                "name": product.name, "image": [product.image], "description": product.description,
                "sku": product.sku || product.id,
                "offers": { "@type": "Offer", "priceCurrency": product.currency, "price": product.price, "availability": "https://schema.org/InStock" }
            };
            const s = document.createElement('script'); s.type = "application/ld+json"; s.text = JSON.stringify(schema); document.head.appendChild(s);
        }

        async function loadProduct() {
            const id = getQueryParam('id');
            if (!id) { window.location.href = 'index.html'; return; }
            try {
                const res = await fetch('products.json');
                const products = await res.json();
                const product = products.find(p => p.id == id);
                if (product) {
                    document.getElementById('p-image').src = product.image;
                    document.getElementById('p-category').innerText = product.category;
                    document.getElementById('p-name').innerText = product.name;
                    document.getElementById('p-price').innerText = product.price;
                    document.getElementById('p-currency').innerText = product.currency;
                    document.getElementById('p-desc').innerText = product.description;
                    document.title = `${product.name} | متجر الكويت`;
                    document.querySelector('meta[name="description"]').setAttribute("content", product.description);
                    updateSchema(product);
                    const msg = `مرحباً، أرغب بطلب المنتج: ${product.name} (كود: ${product.id})`;
                    document.getElementById('whatsapp-btn').href = `https://wa.me/${STORE_PHONE}?text=${encodeURIComponent(msg)}`;
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('product-card').classList.remove('hidden');
                } else { document.getElementById('loading').innerText = 'المنتج غير موجود'; }
            } catch (e) { document.getElementById('loading').innerText = 'خطأ في الاتصال'; }
        }
        loadProduct();
    </script>
</body>
</html>
"""

# 4. محتوى سكريبت التحويل (convert_data.py)
convert_py = """import pandas as pd
import json
import os

excel_file = 'منتجات الكويت بالكامل.xlsx'
output_file = 'products.json'

def convert():
    if not os.path.exists(excel_file):
        print(f"خطأ: الملف '{excel_file}' غير موجود في هذا المجلد.")
        return

    try:
        df = pd.read_excel(excel_file)
        df = df.fillna('')
        
        column_mapping = {
            'الرقم': 'id', 'كود': 'id', 'id': 'id',
            'اسم المنتج': 'name', 'الاسم': 'name',
            'الوصف': 'description', 'التفاصيل': 'description',
            'السعر': 'price',
            'العملة': 'currency',
            'القسم': 'category', 'التصنيف': 'category',
            'رابط الصورة': 'image', 'الصورة': 'image',
            'SKU': 'sku'
        }
        
        df = df.rename(columns=column_mapping)
        
        required = ['id', 'name', 'description', 'price', 'image']
        for col in required:
            if col not in df.columns:
                df[col] = ''

        products = df.to_dict(orient='records')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        print(f"تم إنشاء {output_file} بنجاح!")
        
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    convert()
"""

# --- دالة التنفيذ ---
def create_project():
    # 1. إنشاء المجلد
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path)
            print(f"✅ تم إنشاء المجلد: {base_path}")
        except Exception as e:
            print(f"❌ فشل إنشاء المجلد: {e}")
            return
    else:
        print(f"ℹ️ المجلد موجود بالفعل: {base_path}")

    # 2. كتابة الملفات
    files = {
        "products.json": json.dumps(products_data, ensure_ascii=False, indent=4),
        "index.html": index_html,
        "product.html": product_html,
        "convert_data.py": convert_py
    }

    for filename, content in files.items():
        full_path = os.path.join(base_path, filename)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ تم إنشاء الملف: {filename}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء {filename}: {e}")

    print("\n🎉 تم الانتهاء! يمكنك الآن الذهاب للمجلد وفتح index.html")

if __name__ == "__main__":
    create_project()

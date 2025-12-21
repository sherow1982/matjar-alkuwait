import pandas as pd
import json
import os
import re

excel_file = r"C:\Users\shero\OneDrive\Desktop\متاجر الكويت على جيت هب\منتجات الكويت بالكامل.xlsx"
output_file = r"C:\Users\shero\OneDrive\Desktop\متاجر الكويت على جيت هب\products.json"

def deduce_category(title):
    title = str(title).lower()
    keywords = {
        'عطور وبخور': ['عطر', 'perfume', 'parfum', 'fragrance', 'cologne', 'عود', 'oud', 'aoud', 'بخور', 'bakhoor', 'bukhoor', 'طيب', 'مسك', 'musk', 'رشوش', 'amber', 'عنبر', 'mamoul', 'معمول', 'مبخر', 'mabkhara', 'دهن', 'dehn', 'ward', 'rose', 'patchouli', 'sandalwood'],
        'ساعات ومجوهرات': ['ساعة', 'watch', 'سوار', 'bracelet', 'bangle', 'خاتم', 'ring', 'قلادة', 'necklace', 'pendant', 'chain', 'ذهب', 'gold', 'فضة', 'silver', 'الماس', 'diamond', 'طقم', 'set', 'jewelry', 'jewellery', 'earring', 'حلق', 'brooch', 'بروش', 'سبحة', 'rosary'],
        'أزياء نسائية': ['فستان', 'dress', 'عباية', 'abaya', 'جلابية', 'jalabiya', 'دراعة', 'daraa', 'kaftan', 'قفطان', 'تنورة', 'skirt', 'بلوزة', 'blouse', 'طرحة', 'tarha', 'نقاب', 'niqab', 'حجاب', 'hijab', 'شال', 'shawl', 'وشاح', 'scarf', 'leggings', 'ليقنز', 'top', 'توب'],
        'أزياء رجالية': ['دشداشة', 'dishdasha', 'thobe', 'ثوب', 'بشت', 'bisht', 'غترة', 'ghutra', 'شماغ', 'shemagh', 'عقال', 'agal', 'iqal', 'wizar', 'وزار', 'fanila', 'فانيلة', 'miksar', 'مكسر'],
        'ملابس عامة': ['قميص', 'shirt', 't-shirt', 'تيشيرت', 'بنطلون', 'pants', 'trousers', 'jeans', 'جينز', 'short', 'شورت', 'jacket', 'جاكيت', 'coat', 'معطف', 'hoodie', 'هودي', 'pyjama', 'بيجامة', 'ملابس', 'clothes', 'wear', 'outfit', 'socks', 'جوارب'],
        'أحذية': ['حذاء', 'shoes', 'shoe', 'footwear', 'نعال', 'slipper', 'flip flop', 'صندل', 'sandal', 'جوتي', 'sneaker', 'trainer', 'boot', 'بوت', 'كعب', 'heel', 'wedge', 'moccasin', 'loafer'],
        'حقائب ومحافظ': ['حقيبة', 'bag', 'handbag', 'tote', 'shoulder bag', 'crossbody', 'شنطة', 'purse', 'wallet', 'محفظة', 'clutch', 'backpack', 'حقيبة ظهر', 'luggage', 'travel bag', 'حقيبة سفر'],
        'إلكترونيات': ['موبايل', 'phone', 'iphone', 'samsung', 'galaxy', 'huawei', 'xiaomi', 'شاحن', 'charger', 'adapter', 'سماعة', 'headphone', 'earphone', 'airpods', 'buds', 'كفر', 'case', 'cover', 'screen protector', 'حماية شاشة', 'كيبل', 'cable', 'usb', 'power bank', 'بطارية', 'battery', 'laptop', 'لابتوب', 'ipad', 'tablet', 'تابلت', 'smart watch', 'ساعة ذكية'],
        'أجهزة منزلية': ['خلاط', 'blender', 'mixer', 'مكواة', 'iron', 'غسالة', 'washing machine', 'thallaja', 'ثلاجة', 'fridge', 'oven', 'فرن', 'microwave', 'ميكروويف', 'vacuum', 'مكنسة', 'air fryer', 'قلاية', 'heater', 'دفاية', 'fan', 'مروحة'],
        'عناية وجمال': ['كريم', 'cream', 'لوشن', 'lotion', 'moisturizer', 'مرطب', 'صابون', 'soap', 'wash', 'غسول', 'ماسك', 'mask', 'scrub', 'مقشر', 'مكياج', 'makeup', 'foundation', 'lipstick', 'روج', 'mascara', 'eyeliner', 'shadow', 'عدسات', 'lenses', 'lens', 'رموش', 'lashes', 'serum', 'سيروم', 'shampoo', 'شامبو', 'conditioner', 'oil', 'زيت', 'hair', 'شعر', 'skin', 'بشرة', 'nail', 'أظافر', 'perfumed', 'معطر'],
        'منزل وديكور': ['أثاث', 'furniture', 'طاولة', 'table', 'كرسي', 'chair', 'sofa', 'كنبة', 'تحفة', 'ديكور', 'decor', 'vase', 'فازة', 'إضاءة', 'light', 'lamp', 'سجاد', 'carpet', 'rug', 'مفرش', 'bedsheet', 'bed', 'سرير', 'pillow', 'وسادة', 'cushion', 'blanket', 'بطانية', 'towel', 'منشفة', 'kitchen', 'مطبخ', 'cookware', 'pot', 'pan', 'mug', 'cup', 'كوب'],
        'أغذية ومشروبات': ['قهوة', 'coffee', 'espresso', 'capsule', 'كبسولة', 'شاي', 'tea', 'حلوى', 'sweet', 'candy', 'chocolate', 'شوكولاتة', 'تمر', 'dates', 'maamoul', 'عسل', 'honey', 'مكسرات', 'nuts', 'زعفران', 'saffron', 'spice', 'بهارات', 'water', 'ماء', 'juice', 'عصير'],
        'إكسسوارات': ['نظارة', 'sunglasses', 'glasses', 'حزام', 'belt', 'cufflink', 'كبك', 'محفظة بطاقات', 'card holder', 'tie', 'cravat', 'كرفتة'],
        'ألعاب أطفال': ['لعبة', 'toy', 'game', 'doll', 'دمية', 'car', 'سيارة', 'puzzle', 'lego', 'board game', 'educational', 'تعليمية', 'scooter', 'سكوتر'],
        'قرطاسية': ['قلم', 'pen', 'pencil', 'notebook', 'دفتر', 'paper', 'ورق', 'file', 'ملف', 'stationery', 'قرطاسية'],
        'معدات رياضية': ['رياضة', 'sport', 'gym', 'fitness', 'yoga', 'mat', 'ball', 'كرة', 'racket', 'مضرب'],
        'سيارات': ['car accessory', 'إكسسوار سيارة', 'car care', 'عناية بالسيارة', 'car perfume', 'عطر سيارة']
    }
    
    for category, tags in keywords.items():
        for tag in tags:
            if tag in title:
                return category
    return "منتجات متنوعة"

def convert():
    if not os.path.exists(excel_file):
        print(f"خطأ: الملف غير موجود في المسار:\n{excel_file}")
        return

    try:
        df = pd.read_excel(excel_file)
        df = df.fillna('')
        
        # تنظيف أسماء الأعمدة
        df.columns = [str(c).strip() for c in df.columns]

        products = []

        for index, row in df.iterrows():
            # دالة مساعدة لاستخراج القيم وتنظيفها لتقليل التكرار
            def get_val(key):
                val = row.get(key)
                return str(val).strip() if val is not None else ""

            # توليد Slug عربي
            name = get_val('Title')
            # استبدال المسافات بشرط، وإزالة الرموز غير المرغوبة مع الحفاظ على الأحرف العربية
            slug = re.sub(r'[^\w\s\u0600-\u06FF-]', '', name).strip().replace(' ', '-').replace('--', '-')
            slug = re.sub(r'-+', '-', slug) # منع تكرار الشرطات
            if not slug: # إذا كان الاسم فارغاً أو يحتوي رموزاً فقط
                slug = str(row.get('id', 'product'))

            # استخراج الصور
            images = []
            for img_col in ['Images', 'Variant Image2', 'Variant Image3', 'Variant Image4']:
                img_val = get_val(img_col)
                if img_val:
                    images.append(img_val)

            # تحديد السعر
            regular_price = get_val('Regular Price')
            sale_price = get_val('Sale Price')
            
            # استخدام سعر الخصم إذا وجد
            price = sale_price if sale_price and sale_price != '0' else regular_price

            # تحديد التصنيف (Category) - استنتاج من الاسم أولاً
            category = deduce_category(name)
            
            # إذا لم يتم العثور على تصنيف من الاسم، نحاول البحث في الأعمدة
            if category == "منتجات متنوعة":
                for col in ['Google Product Category', 'Product Category', 'Category', 'Type', 'التصنيف', 'القسم']:
                    val = get_val(col)
                    if val:
                        category = val
                        break

            # تحديد التوفر بناءً على قيمة رقمية حقيقية لتجنب أخطاء النصوص (مثل "0.0")
            qty_str = get_val('Quantity')
            try:
                is_in_stock = float(qty_str) > 0 if qty_str else False
            except ValueError:
                is_in_stock = False

            product = {
                "id": get_val('id'),
                "name": get_val('Title'),
                "slug": slug,
                "description": get_val('Description'),
                "seo_title": get_val('SEO Title'),
                "seo_description": get_val('SEO Description'),
                "quantity": qty_str,
                "regular_price": regular_price,
                "sale_price": sale_price,
                "price": price,
                "currency": "KWD",
                "image": images[0] if images else "",
                "images": images,
                "category": category,
                "availability": "InStock" if is_in_stock else "OutOfStock"
            }
            products.append(product)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        print(f"تم التحويل بنجاح! تم استخراج {len(products)} منتج.")
        
    except Exception as e:
        print(f"حدث خطأ أثناء التحويل: {e}")
        print("تأكد من وجود الأعمدة: id, Title, Description, SEO Title, SEO Description, Quantity, Regular Price, Sale Price, Images...")

if __name__ == "__main__":
    convert()

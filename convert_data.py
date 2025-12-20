import pandas as pd
import json
import os

excel_file = r"C:\Users\shero\OneDrive\Desktop\متاجر الكويت على جيت هب\منتجات الكويت بالكامل.xlsx"
output_file = r"C:\Users\shero\OneDrive\Desktop\متاجر الكويت على جيت هب\products.json"

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
            # استخراج الصور
            images = []
            if row.get('Images'): images.append(str(row.get('Images')).strip())
            if row.get('Variant Image2'): images.append(str(row.get('Variant Image2')).strip())
            if row.get('Variant Image3'): images.append(str(row.get('Variant Image3')).strip())
            if row.get('Variant Image4'): images.append(str(row.get('Variant Image4')).strip())

            # تحديد السعر
            regular_price = str(row.get('Regular Price', '')).strip()
            sale_price = str(row.get('Sale Price', '')).strip()
            
            # استخدام سعر الخصم إذا وجد
            price = sale_price if sale_price and sale_price != '0' else regular_price

            product = {
                "id": str(row.get('id', '')).strip(),
                "name": str(row.get('Title', '')).strip(),
                "description": str(row.get('Description', '')).strip(),
                "seo_title": str(row.get('SEO Title', '')).strip(),
                "seo_description": str(row.get('SEO Description', '')).strip(),
                "quantity": str(row.get('Quantity', '')).strip(),
                "regular_price": regular_price,
                "sale_price": sale_price,
                "price": price,
                "currency": "KWD",
                "image": images[0] if images else "",
                "images": images,
                "category": "عام",
                "availability": "InStock" if str(row.get('Quantity', '0')) != '0' else "OutOfStock"
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

import sqlite3
import xml.etree.ElementTree as ET

dbconnection= sqlite3.connect("data.sqlite")
cursor = dbconnection.cursor()

cursor.execute("""
    SELECT 
        pro.product_id,
        pro.name,
        pro_des.description,
        pro.quantity,
        pro.price,
        man.name as brand
    FROM product pro
    JOIN manufacturer man ON pro.manufacturer_id = man.manufacturer_id
    JOIN product_description pro_des ON pro.product_id = pro_des.product_id
    WHERE pro.status != 0
""")

products = cursor.fetchall()

#  XML root
rss = ET.Element('rss', version="2.0", attrib={'xmlns:g': "http://base.google.com/ns/1.0"})
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = "Butopea Product Feed"
ET.SubElement(channel, 'link').text = "https://butopea.com"
ET.SubElement(channel, 'description').text = "Product feed for Butopea.com"

# Helper to get additional images
def get_additional_images(product_id):
    cursor.execute("""
        SELECT image 
        FROM product_image 
        WHERE product_id = ? 
        ORDER BY sort_order
    """, (product_id,))
    images = cursor.fetchall()
    return [f"https://butopea.com/image/catalog/{img[0]}" for img in images]

for prod in products:
    product_id = prod[0]
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'g:id').text = str(product_id)
    ET.SubElement(item, 'g:title').text = prod[1]
    ET.SubElement(item, 'g:description').text = prod[2]
    ET.SubElement(item, 'g:link').text = f"https://butopea.com/p/{product_id}"
    
    # Images
    all_images = get_additional_images(product_id)
    if all_images:
        ET.SubElement(item, 'g:image_link').text = all_images[0]
        if len(all_images) > 1:
            ET.SubElement(item, 'g:additional_image_link').text = ", ".join(all_images[1:])
    else:
        ET.SubElement(item, 'g:image_link').text = ""
    ET.SubElement(item, 'g:availability').text = "in stock" if int(prod[3]) > 0 else "out of stock"
    ET.SubElement(item, 'g:price').text = f"{float(prod[4]):.2f} HUF"
    ET.SubElement(item, 'g:brand').text = prod[5]
    ET.SubElement(item, 'g:condition').text = "new"

# Writing XML to file
tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
print("feed.xml has been generated successfully!")

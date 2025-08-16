import sqlite3
import xml.etree.ElementTree as ET

dbconnection= sqlite3.connect("data.sqlite")
cursor = dbconnection.cursor()

cursor.execute("""
SELECT 
    pro.product_id AS ID,
    pro_des.name AS Title,
    pro_des.description AS Description,
    pro.image AS Image_Link,
    pro.quantity AS Availability,
    pro.price AS Price,
    man.name AS Brand
FROM product pro
JOIN manufacturer man 
    ON pro.manufacturer_id = man.manufacturer_id
JOIN product_description pro_des 
    ON pro.product_id = pro_des.product_id
JOIN product_image pro_image 
    ON pro_image.product_id = pro.product_id
WHERE pro.quantity >= 1;
""")

products = cursor.fetchall()

rss = ET.Element('rss', version="2.0", attrib={"xmlns:g":"http://base.google.com/ns/1.0"})
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = "Butopea Product Feed"
ET.SubElement(channel, 'link').text = "https://butopea.com"
ET.SubElement(channel, 'description').text = "Product feed for Google Merchant"

for prod in products:
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'g:id').text = str(prod[0])
    ET.SubElement(item, 'g:title').text = prod[1]
    ET.SubElement(item, 'g:description').text = prod[2]
    ET.SubElement(item, 'g:link').text = f"https://butopea.com/product/{prod[0]}"
    ET.SubElement(item, 'g:image_link').text = prod[3]
    ET.SubElement(item, 'g:availability').text = "in stock" if prod[4] > 0 else "out of stock"
    ET.SubElement(item, 'g:price').text = f"{prod[5]:.2f} HUF"
    ET.SubElement(item, 'g:brand').text = prod[6]
#saving the xml file
tree = ET.ElementTree(rss)
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

print("XML product feed created successfully!")
dbconnection.close()

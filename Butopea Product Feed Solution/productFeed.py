import sqlite3

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

rows = cursor.fetchall()
for row in rows:
    print(row)

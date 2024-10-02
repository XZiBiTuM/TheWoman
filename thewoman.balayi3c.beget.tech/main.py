# import mysql.connector

# # Подключение к базе данных MySQL
# conn = mysql.connector.connect(
#     host="bipipikub.beget.app",
#     user="default-db",
#     password="N8cq%13YLh3L",
#     database="default-db"
# )
# print('SUCCESS')
# # Создание курсора
# cursor = conn.cursor()

# count = 417

# i = 0

# for i in range(count):
#     count_element = count - i

#     sql_query = """
#     SELECT last_in_stock_change
#     FROM catalog_product
#     ORDER BY last_in_stock_change DESC
#     LIMIT 1 OFFSET %s;
#     """

#     cursor.execute(sql_query, (count_element,))

#     max_id_lisc = cursor.fetchone()[0]
    
#     sql_query = """
#     SELECT id
#     FROM catalog_product
#     ORDER BY last_in_stock_change ASC
#     LIMIT 1 OFFSET %s
#     """
    
#     cursor.execute(sql_query, (count_element,))
    
#     max_id = cursor.fetchone()[0]
    
#     sql_query = """
#     UPDATE catalog_product
#     SET last_in_stock_change = %s
#     WHERE id = %s; 
#     """
    
#     cursor.execute(sql_query, (max_id_lisc, max_id,))

# # Сохранение изменений и закрытие соединения
# conn.commit()
# conn.close()
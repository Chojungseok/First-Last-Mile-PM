import psycopg2


try:
    connection = psycopg2.connect(
        dbname="sejong",
        user="chojungseok",
        password="jungseok0324!",
        host="localhost",
        port="5432"
    )
    
    cursor = connection.cursor()

    

except Exception as error:
    print('error 발생', error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection closed.")
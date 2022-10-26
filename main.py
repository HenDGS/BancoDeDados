import mysql.connector
import numpy as np
from mysql.connector import Error
import PySimpleGUI as sg


# Function to read from mysql database
'''def read_from_mysql():
    global cursor
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='employees',
                                             user='root',
                                             password='')  # Adicionar a sua senha
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
        sql_select_query = "select * from departments"
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        print("Total number of rows in departments is: ", cursor.rowcount)
        cursor = connection.cursor()

    except Error as e:
        print("Error while connecting to MySQL", e)'''

# Function to search csv data by column
def search_by_column(data, column, value):
    return data[data[:, column] == value]


# Function to read from csv file
def read_from_csv():
    data = np.genfromtxt('data.csv', delimiter=',')
    print(data)
    return data


# Main function
def main():
    data = read_from_csv()

    # Query data


# Run main function
if __name__ == "__main__":
    main()

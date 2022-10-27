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

# Function to read from csv file
def read_from_csv():
    data = np.genfromtxt('employees1000.csv', delimiter=',', dtype=None, encoding=None)
    # data = np.genfromtxt('data.csv', delimiter=',')
    return data

# Function to recive an input with projection, where and order by; then search in the data
def search(data):
    # Layout
    layout = [
        [sg.Text('Enter the projection: '), sg.Input(key='projection')],
        [sg.Text('Enter the where: '), sg.Input(key='where')],
        [sg.Text('Enter the order by: '), sg.Input(key='order')],
        [sg.Button('Search')]
    ]
    # Create window
    window = sg.Window('Search', layout)
    # Read values
    event, values = window.read()
    # Close window
    window.close()
    # Get values
    projection = values['projection']
    where = values['where']
    order = values['order']
    # Search in the data
    if where == '':
        if order == '':
            if projection == '':
                print(data)
            else:
                print(data[projection])
        else:
            if projection == '':
                print(data[np.argsort(data[order])])
            else:
                print(data[projection][np.argsort(data[order])])
    else:
        if order == '':
            if projection == '':
                print(data[data[where]])
            else:
                print(data[projection][data[where]])
        else:
            if projection == '':
                print(data[data[where]][np.argsort(data[order])])
            else:
                print(data[projection][data[where]][np.argsort(data[order])])


# Function to search by


# Main function
def main():
    data = read_from_csv()
    # Print columns in data
    print(data.dtype.names)
    # Search in data
    search(data)

    print(data[0])


# Run main function
if __name__ == "__main__":
    main()

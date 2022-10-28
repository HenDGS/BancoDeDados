import mysql.connector
import numpy as np
from mysql.connector import Error
import PySimpleGUI as sg
import glob
import os
import csv

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


# Function to receive a input query string in gui
def read_from_csv():
    # Layout
    layout = [
        [sg.Text('Enter the query: '), sg.Input(key='query')],
        [sg.Button('Search')]
    ]
    # Create window
    window = sg.Window('Search', layout)
    # Read values
    event, values = window.read()
    # Close window
    window.close()
    # Get values
    query = values['query']
    # Get all files in the folder
    files = glob.glob('*.csv')
    # Create a list to save the data
    data = []
    # Read all files
    for file in files:
        # Read file
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Save data in a list
            data.append(np.array(list(csv_reader)))

    # Split query into select, from and where
    query = query.split(' ')
    # Use the from query to choose the csv from files
    sql_from = query[query.index('from') + 1]
    if sql_from in files:
        array = data[files.index(sql_from)]
    else:
        print('Table not found')

    # Use the where query to filter by condition
    # Dele rows that don't match the condition from the numpy array
    if 'where' in query:
        # Get the index of where
        where_index = query.index('where')
        # Get the column name
        column_name = query[where_index + 1]
        # Get the condition
        condition = query[where_index + 2]
        # Get the value
        value = query[where_index + 3]
        # Get the index of the column
        column_index = np.where(array[0] == column_name)[0][0]
        # Get the index of the rows that match the condition
        if condition == '=':
            rows_index = np.where(array[:, column_index] == value)[0]
        elif condition == '>':
            rows_index = np.where(array[:, column_index] > value)[0]
        elif condition == '<':
            rows_index = np.where(array[:, column_index] < value)[0]
        elif condition == '>=':
            rows_index = np.where(array[:, column_index] >= value)[0]
        elif condition == '<=':
            rows_index = np.where(array[:, column_index] <= value)[0]
        elif condition == '!=':
            rows_index = np.where(array[:, column_index] != value)[0]
        elif condition == 'between':
            # Get the second value
            value2 = query[where_index + 4]
            rows_index = np.where((array[:, column_index] >= value) & (array[:, column_index] <= value2))[0]
        elif condition == 'like':
            rows_index = np.where(array[:, column_index] == value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))

        else:
            print('Condition not found')
        # Delete rows that don't match the condition
        # array = np.delete(array, rows_index, axis=0)

    # Use the select query to choose the column
    sql_select = query[query.index('select') + 1]
    if sql_select == '*':
        print(array)
    else:
        i = array[0].tolist().index(sql_select)
        print(array[:,i])
        new_array = array[:,i]


    '''# Import libraries
    import glob
    import os
    import csv
    import numpy as np
    # Get all files in the folder
    files = glob.glob('*.csv')
    # Create a list to save the data
    data = []
    # Read all files
    for file in files:
        # Read file
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Save data in a list
            data.append(np.array(list(csv_reader)))
    # Use gui to choose wich file to return
    # Layout
    layout = [
        [sg.Text('Choose the file to return:')],
        [sg.Listbox(values=files, size=(30, 6), key='files')],
        [sg.Button('Ok')]
    ]
    # Create window
    window = sg.Window('Choose file', layout)
    # Read values
    event, values = window.read()
    # Close window
    window.close()
    # Return data
    return data[files.index(values['files'][0])]'''


# Function to recive an input with projection, where and order by; then search in the data
def search(data):
    # Extract columns from data
    columns = data[0]
    # Create a list with the columns
    columns_list = []
    for column in columns:
        columns_list.append(column)
    columns_list.append('*')
    # Create a list with conditions
    conditions_list = ['=!', '>', '<', '>=', '<=', '!=', 'between', 'like']
    # Where is a list of
    # Layout
    # Projection is a dropdown with all the columns
    # Where is a input text
    # Order by is a dropdown with all the columns
    layout = [
        [sg.Text('Projection:'), sg.Combo(columns_list, size=(20, 1), key='projection')],
        [sg.Text('Enter the where: '), sg.Input(key='where')],
        [sg.Text('Condition:'), sg.Combo(conditions_list, size=(20, 1), key='condition')],
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
    condition = values['condition']
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




# Main function
def main():
    # Read all csvs files in the folder and save in a list
    data = read_from_csv()
    # Search in data
    # search(data)
    print('a')

    # print(data[0])


# Run main function
if __name__ == "__main__":
    main()

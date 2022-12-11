#AUTORES: HENRIQUE DA GAMA SACZKWOSKI e IVAN BAUER JUNIOR
#AUTHORS: HENRIQUE DA GAMA SACZKWOSKI and IVAN BAUER JUNIOR

#Trabalho 2, Introducao a Banco de Dados, UTFPR, 2022/2
#Este trabalho inclui a implementacao de 'joins' no codigo do trabalho 1

#Assignment 2, Introduction to Databases, UTFPR, 2022/2
#This assignment includes the implementation of 'joins' in the code of assignment 1

import csv
import glob

import PySimpleGUI as sg
import numpy as np

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
    sql_from2 = "null"
    
    # Verify if there are two tables
    if sql_from.find(",") >= 0:
        sql_from = sql_from.replace(',', '')
        sql_from2 = query[query.index('from') + 2]
        # Verify if the table2 exists
        if sql_from2 not in files:
            print('Table2 not found')


    # Verify if the table exists
    if sql_from in files:
        array = data[files.index(sql_from)]
    else:
        print('Table not found')


    if 'join' in query:
        sql_from2 = query[query.index('join') + 1]
        # Verify if the table2 exists
        if sql_from2 != "null":
            if sql_from2 in files:
                array_table2 = data[files.index(sql_from2)]
            else:
                print('Table2 not found')
        if 'on' in query:
            on_index = query.index('on')
            on_column_name1 = query[on_index + 1]
            if on_column_name1.find(".") >= 0: #if it is in the format of table.column
                    aux = on_column_name1.split('.')
                    on_column_name1 = aux[1] #on_column_name1 is now the column name
            try: 
                on_condition = query[on_index + 2]
            except IndexError:
                 on_condition = "indexerror"
            try : 
                on_column_name2 = query[on_index + 3]
                if on_column_name2.find(".") >= 0: #if it is in the format of table.column
                    aux = on_column_name2.split('.')
                    on_column_name2 = aux[1] #on_column_name1 is now the column name
            except IndexError:
                 on_column_name2 = "indexerror"
        if on_condition == '=':
            column_index = np.where(array[0] == on_column_name1)[0][0]
            column_index2 = np.where(array_table2[0] == on_column_name2)[0][0]
            #nested loop join using np.where
            #doesn't work
            #rows_index = np.where(array[:, column_index] == array_table2[:, column_index2]
            #rows_index2 = np.where(array_table2[:, column_index2] == array[:, column_index])

            #nested loop join using for
            rows_index = []
            rows_index2 = []
            for i in range(len(array)):
                for j in range(len(array_table2)):
                    if array[i, column_index] == array_table2[j, column_index2]:
                        rows_index.append(i)
                        rows_index2.append(j)
            # Make a new array with the rows that match the join condition
            array = np.vstack((array[rows_index]))
            # Make a new array with the rows that match the join conditions
            array_table2 = np.vstack((array_table2[rows_index2]))

        columns_count = 1
        sql_select = query[query.index('select') + columns_count]

        if sql_select == '*':
            print(array)
            print(array_table2)
        else:
            while sql_select.find(",") >= 0: #if there are more than one column
                if sql_select.find(".") >= 0: #if it is in the format of table.column
                    aux = sql_select.split('.')
                    aux[0] = aux[0]+'.csv'
                    sql_select = aux[1] #sql_select is now the column name
                    if aux[0] == sql_from: #checks from which table the column is
                        sql_select = sql_select.replace(',', '')
                        i = array[0].tolist().index(sql_select)
                        # print(array[:,i])
                        new_array = array[:, i]
                        print(new_array)
                        columns_count += 1
                        sql_select = query[query.index('select') + columns_count]
                    elif aux[0] == sql_from2: #checks from which table the column is
                            sql_select = sql_select.replace(',', '')
                            i = array_table2[0].tolist().index(sql_select)
                            # print(array[:,i])
                            new_array = array_table2[:, i]
                            print(new_array)
                            columns_count += 1
                            sql_select = query[query.index('select') + columns_count]

            #does the procedure one last time for the last column
            aux = sql_select.split('.')
            aux[0] = aux[0]+'.csv'
            sql_select = aux[1] #sql_select is now the column name
            if aux[0] == sql_from: #checks from which table the column is
                i = array[0].tolist().index(sql_select)
                new_array = array[:, i]

            elif aux[0] == sql_from2: #checks from which table the column is
                i = array_table2[0].tolist().index(sql_select)
                new_array = array_table2[:, i]
            
            print(new_array)
            return()



    elif sql_from2 != "null":
        if sql_from2 in files:
            array_table2 = data[files.index(sql_from2)]
        else:
            print('Table2 not found')
        if 'where' in query:
            where_index = query.index('where')
            # Get the column name
            column_name = query[where_index + 1]
            # Get the condition
            condition = query[where_index + 2]
            column_name2 = query[where_index + 3]
            if column_name.find(".") >= 0: #if it is in the format of table.column
                aux = column_name.split('.')
                column_name = aux[1] #column_name1 is now the column name
            if column_name2.find(".") >= 0: #if it is in the format of table.column
                aux = column_name2.split('.')
                column_name2 = aux[1] #column_name2 is now the column name
            if condition == '=':
                column_index = np.where(array[0] == column_name)[0][0]
                column_index2 = np.where(array_table2[0] == column_name2)[0][0]
                #nested loop join
                rows_index = []
                rows_index2 = []
                for i in range(len(array)):
                    for j in range(len(array_table2)):
                        if array[i, column_index] == array_table2[j, column_index2]:
                            rows_index.append(i)
                            rows_index2.append(j)
                # Make a new array with the rows that match the join condition
                array = np.vstack((array[rows_index]))
                # Make a new array with the rows that match the join conditions
                array_table2 = np.vstack((array_table2[rows_index2]))

        columns_count = 1
        sql_select = query[query.index('select') + columns_count]

        if sql_select == '*':
            print(array)
            print(array_table2)
        else:
            while sql_select.find(",") >= 0: #if there are more than one column
                if sql_select.find(".") >= 0: #if it is in the format of table.column
                    aux = sql_select.split('.')
                    aux[0] = aux[0]+'.csv'
                    sql_select = aux[1] #sql_select is now the column name
                    if aux[0] == sql_from: #checks from which table the column is
                        sql_select = sql_select.replace(',', '')
                        i = array[0].tolist().index(sql_select)
                        # print(array[:,i])
                        new_array = array[:, i]
                        print(new_array)
                        columns_count += 1
                        sql_select = query[query.index('select') + columns_count]
                    elif aux[0] == sql_from2: #checks from which table the column is
                            sql_select = sql_select.replace(',', '')
                            i = array_table2[0].tolist().index(sql_select)
                            # print(array[:,i])
                            new_array = array_table2[:, i]
                            print(new_array)
                            columns_count += 1
                            sql_select = query[query.index('select') + columns_count]

            #does the procedure one last time for the last column
            if sql_select.find(".") >= 0:
                aux = sql_select.split('.')
                aux[0] = aux[0]+'.csv'
                sql_select = aux[1] #sql_select is now the column name
                if aux[0] == sql_from: #checks from which table the column is
                    i = array[0].tolist().index(sql_select)
                    new_array = array[:, i]

                elif aux[0] == sql_from2: #checks from which table the column is
                    i = array_table2[0].tolist().index(sql_select)
                    new_array = array_table2[:, i]

            else:
                i = array[0].tolist().index(sql_select)
                new_array = array[:, i]
            
            print(new_array)
            return()



        

    # Use the where query to filter by condition
    # Delete rows that don't match the condition from the numpy array
    
    elif 'where' in query:
        # Get the index of where
        where_index = query.index('where')
        # Get the column name
        column_name = query[where_index + 1]
        # Get the condition
        condition = query[where_index + 2]
        # Get the value
        value = query[where_index + 3]
        # Verify if there are two conditions with an "and" or "or"
        try:
            andor = query[where_index + 4]
        except IndexError:
            andor = "indexerror"
        # Get the index of the column
        column_index = np.where(array[0] == column_name)[0][0]
        # Get the index of the rows that match the condition
        if condition == 'like':
            rows_index = np.where(array[:, column_index] == value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == '=':
            rows_index = np.where(array[:, column_index] == value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == '>':
            rows_index = np.where(array[:, column_index] > value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == '<':
            rows_index = np.where(array[:, column_index] < value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == '>=':
            rows_index = np.where(array[:, column_index] >= value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == '<=':
            rows_index = np.where(array[:, column_index] <= value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == '<>':
            rows_index = np.where(array[:, column_index] != value)
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))
        elif condition == 'between':
            # Get the second value
            value2 = query[where_index + 5]
            rows_index = np.where((array[:, column_index] > value) & (array[:, column_index] < value2))
            # Make a new array with the rows that match the condition, keeping column names
            array = np.vstack((array[0], array[rows_index]))

        else:
            print('Condition not found')

        if andor == 'and':
            # Get the column name
            column_name2 = query[where_index + 5]
            # Get the condition
            condition2 = query[where_index + 6]
            # Get the value
            value2 = query[where_index + 7]
            # Get the index of the column
            column_index2 = np.where(array[0] == column_name2)[0][0]
            # Get the index of the rows that match the condition
            if condition2 == 'like':
                rows_index2 = np.where(array[:, column_index2] == value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            elif condition2 == '=':
                rows_index2 = np.where(array[:, column_index2] == value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            elif condition2 == '>':
                rows_index2 = np.where(array[:, column_index2] > value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            elif condition2 == '<':
                rows_index2 = np.where(array[:, column_index2] < value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            elif condition == '<>':
                rows_index2 = np.where(array[:, column_index2] != value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            elif condition2 == '>=':
                rows_index2 = np.where(array[:, column_index2] >= value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            elif condition2 == '<=':
                rows_index2 = np.where(array[:, column_index2] <= value2)
                # Make a new array with the rows that match the condition, keeping column names
                array = np.vstack((array[0], array[rows_index2]))
            else:
                print('Condition not found')

        elif andor == 'or':
            column_name2 = query[where_index + 5]
            condition2 = query[where_index + 6]
            value2 = query[where_index + 7]
            array2 = data[files.index(sql_from)]
            column_index2 = np.where(array2[0] == column_name2)[0][0]
            # Get the index of the rows that match the condition
            if condition2 == 'like':
                rows_index = np.where(array2[:, column_index2] == value2)
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))
            elif condition2 == '=':
                rows_index = np.where(array2[:, column_index2] == value2)
                # Make a new array with the rows that match the condition
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))
            elif condition2 == '>':
                rows_index = np.where(array2[:, column_index2] > value2)
                # Make a new array with the rows that match the condition
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))
            elif condition2 == '<':
                rows_index = np.where(array2[:, column_index2] < value2)
                # Make a new array with the rows that match the condition
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))
            elif condition2 == '>=':
                rows_index = np.where(array2[:, column_index2] >= value2)
                # Make a new array with the rows that match the condition
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))
            elif condition2 == '<=':
                rows_index = np.where(array2[:, column_index2] <= value2)
                # Make a new array with the rows that match the condition
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))
            elif condition2 == 'between':
                # Get the second value
                value3 = query[where_index + 9]
                rows_index = np.where((array2[:, column_index2] > value2) & (array2[:, column_index2] < value3))
                # Make a new array with the rows that match the condition
                array2 = array2[rows_index]
                array2 = array2[1:]
                array = np.vstack((array, array2))

        # Delete rows that don't match the condition
        # array = np.delete(array, rows_index, axis=0)

    # Use the select query to choose the column(s)
    columns_count = 1
    sql_select = query[query.index('select') + columns_count]

    if sql_select == '*':
        print(array)
    else:
        
        while sql_select.find(",") >= 0: #if there are more than one column
            if sql_select.find(".") >= 0: #if it is in the format of table.column
                aux = sql_select.split('.')
                sql_select = aux[1] #sql_select is now the column name
            sql_select = sql_select.replace(',', '')
            i = array[0].tolist().index(sql_select)
            # print(array[:,i])
            new_array = array[:, i]
            print(new_array)
            columns_count += 1
            sql_select = query[query.index('select') + columns_count]
            
        #does the procedure one last time for the last column
        if sql_select.find(".") >= 0: #if it is in the format of table.column
            aux = sql_select.split('.')
            sql_select = aux[1] #sql_select is now the column name
        i = array[0].tolist().index(sql_select)
        # print(array[:,i])
        new_array = array[:, i]

        #if sql_from2 != "null":

    if 'order' in query:
        order_index = query.index('order')
        order_column = query[order_index + 2]
        order_column_index = np.where(array[0] == order_column)[0][0]
        if 'desc' in query:
            array = array[np.argsort(array[:, order_column_index])[::-1]]
        else:
            array = array[np.argsort(array[:, order_column_index])]
        print(array)
            

#   print(new_array)


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
    read_from_csv()
    # Search in data
    # search(data)
    print('')

    # print(data[0])


# Run main function
if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import sqlite3
import time

def sql_connection(db_path):
    try:
        con = sqlite3.connect(db_path)
        return con
    except Error:
        print(Error)

def sql_create(con, cursorObj, sql_statement):
    for statement in sql_statement:
        cursorObj.execute(statement)
        con.commit()

def sql_table(con, df, table_name):
    df.astype(str).to_sql(table_name, con, if_exists='append', index=False)

def sql_select(con, cursorObj, sql_statement):
    cursorObj.execute(sql_statement)

def sql_fetch(con, cursorObj, sql_statement):
    cursorObj.execute(sql_statement)
    rows = cursorObj.fetchall()

    [print(row) for row in cursorObj.fetchall()]

def sql_insert(con, cursorObj, sql_statement, data):
    cursorObj = con.cursor()
    cursorObj.execute(sql_statement, data)
    con.commit()

def check_type(row):
    error_detected = False
    for r in row:
        try:
            int(r)
        except ValueError:
            print("Invalid data type(s) detected: " + str(type(r)))
            error_detected = True
            break

    if error_detected == True:
        print(str(error_detected))
        return False        

def fizzbuzz(file_dir, file_name, con, run_type, run_id):
    df = pd.read_csv(file_dir + file_name, header=None)
    new_list = []
    error_dict = {'RunId': [],'RowNumber': [], 'ErrorCode': []}
    row_list = [list(row) for row in df.values]
    count = 1

    for row in row_list:
        valid_type = check_type(row)
        if valid_type == False and len(row) == 20:
            error_dict['RunId'].append(run_id)
            error_dict['RowNumber'].append(count)
            error_dict['ErrorCode'].append('Invalid data type and invalid number of columns detected.')
        elif valid_type == False and len(row) != 20:
            error_dict['RunId'].append(run_id)
            error_dict['RowNumber'].append(count)
            error_dict['ErrorCode'].append('Invalid data type detected.')
        elif valid_type != False and len(row) != 20:
            error_dict['RunId'].append(run_id)
            error_dict['RowNumber'].append(count)
            error_dict['ErrorCode'].append('Invalid number of columns detected.')
        else:
            if run_type == 'FizzBuzz':
                row = ['fizzbuzz' if (x % 3 == 0 and x % 5 == 0) else 'fizz' if (x % 3 == 0) else 'buzz' if (x % 5 == 0) else x for x in row]
                new_list.append(row)
            else: 
                row = ['fizzbuzz' if (x % 3 == 0 and x % 5 == 0) else 'fizz' if (x % 3 == 0) else 'buzz' if (x % 5 == 0) else 'lucky' if ('3' in str(x))  else x for x in row]
                new_list.append(row)
        count += 1

    new_df = pd.DataFrame(new_list)
    sql_table(con, new_df, run_type)
    run_info = {"ValidRows": len(new_list), "InvalidRows": len(error_dict['RunId']), "TotalRows": len(row_list)}
    return run_info, error_dict, new_list

def word_count_report(lucky_list):
    word_list = ['fizz', 'buzz', 'fizzbuzz', 'lucky']
    word_count_dict = {"Word": [], "Count": []}
    for l in lucky_list:
        for word in word_list:
            word_count = l.count(word)
            print(word + ' ' + str(word_count))
            word_count_dict['Word'].append(word)
            word_count_dict['Count'].append(word_count)
    
    word_count_df = pd.DataFrame(word_count_dict)
    word_count_df = word_count_df.groupby(['Word'], as_index=False)['Count'].sum()
    sql_table(con, word_count_df, 'WordCounts')

file_dir = './InputFiles/'

# Establish DB Connection
con = sql_connection('./Database/FizzBuzz.db')
con.row_factory = sqlite3.Row
cursorObj = con.cursor()

# Create Tables
createTables = ['CREATE TABLE IF NOT EXISTS RunInformation(RunId integer PRIMARY KEY AUTOINCREMENT, FileName text, ValidRows integer, InvalidRows integer, TotalRows integer, ProcessingTime float, ProcessingStart timestamp, ProcessingEnd timestamp)','CREATE TABLE IF NOT EXISTS RunErrors(RunId integer, RowNumber integer, ErrorCode text)']
sql_create(con, cursorObj, createTables)

# Run information
run_info_insert = 'INSERT INTO RunInformation (FileName, ValidRows, InvalidRows, TotalRows, ProcessingTime, ProcessingStart, ProcessingEnd) VALUES(?, ?, ?, ?, ?, ?, ?)'
run_error_insert = 'INSERT INTO RunErrors (RunId, RowNumber, ErrorCode) VALUES(?, ?, ?)'
cursorObj.execute('SELECT RunId FROM RunInformation ORDER BY RunId DESC LIMIT 1')
row = cursorObj.fetchone()
if row is None:
    last_id = 1
else:
    last_id = row[0]

# Read CSV
csv_list = ['RandomIntegers.csv', 'RandomIntegers_Invalid.csv']

for csv in csv_list:
    # FizzBuzz Tranformations
    start_time = time.time()
    fizzbuzz_df = fizzbuzz(file_dir, csv, con, 'FizzBuzz', last_id)
    lucky_fizzbuzz_df = fizzbuzz(file_dir, csv, con, 'LuckyFizzBuzz', last_id)
    end_time = time.time()
    processing_time = float(end_time - start_time)

    # Log Run Information
    run_info = [csv, lucky_fizzbuzz_df[0]['ValidRows'], lucky_fizzbuzz_df[0]['InvalidRows'], lucky_fizzbuzz_df[0]['TotalRows'], processing_time, start_time, end_time]
    sql_insert(con, cursorObj, run_info_insert, run_info)

    error_df = pd.DataFrame(lucky_fizzbuzz_df[1])
    sql_table(con, error_df, 'RunErrors')
    
    # Create Word Count Report
    word_count_report(lucky_fizzbuzz_df[2])
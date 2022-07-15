import os
import sys
import math
import pymysql.cursors
from bokeh.plotting import figure, output_file, show

def get_db_connection():
  connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'hassan123',
    db = 'schema_1',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
  )

  return connection

def dump_exp1_in_sql(file_path):
  Connection = get_db_connection()
  File = open('{}'.format(file_path), 'r')
  contents = File.readlines()

  try:
    with Connection.cursor() as cursor:
      for content in contents:
        if 'Temperature' not in content:
          values = content.replace(',', '.').split()
          sql_query = "insert into experiment_1 (temperature, strain) values('{}', '{}')".format(values[0], values[1])
          print(sql_query)
          cursor.execute(sql_query)

    Connection.commit()
  except Exception as e:
    # Uncomment below line to see complete error stack trace
    # raise e
    print("Error Class: ", sys.exc_info()[0])
  finally:
    Connection.close()

def dump_exp2_in_sql(file_path):
  Connection = get_db_connection()
  File = open('{}'.format(file_path), 'rb')
  contents = File.readlines()

  try:
    with Connection.cursor() as cursor:
      for lines in range(21, len(contents)):
        x = contents[lines].split()
        sql_query = "insert into experiment_2 (zeit, temperature, dl, kraft) values('{}', '{}', '{}', '{}')"
        sql_query = sql_query.format(x[0].decode(), x[1].decode(), x[2].decode(), x[3].decode())
        print(sql_query)
        cursor.execute(sql_query)

    Connection.commit()
  except Exception as e:
    print("Error Class: ", sys.exc_info()[0])
    # Uncomment below line to see complete error stack trace
    # raise e
  finally:
    Connection.close()

def generate_line_graph(x_data, y_data, x_label, y_label, output_filename, graph_name):
  output_file(output_filename)
  graph = figure(title = graph_name, x_axis_label = x_label, y_axis_label = y_label)
  graph.line(x_data, y_data, line_width = 2)
  show(graph)

def plot_experiment_1():
  Connection = get_db_connection()

  try:
    with Connection.cursor() as cursor:
      sql = "select temperature, strain as updated_strain from hassan.experiment_1 order by updated_strain desc, temperature desc";
      cursor.execute(sql)
      result = cursor.fetchall()
      temperature = []
      strain = []
      for item in result:
        # temperature.append(math.log(item['temperature'])) if item['temperature'] > 0 else temperature.append(0)
        temperature.append(item['temperature'])
        strain.append(item['updated_strain'])
      generate_line_graph(temperature, strain, 'strain', 'temperature', 'exp1.html', 'Experiment 1 graph')

  except Exception as e:
    print("Error Class: ", sys.exc_info()[0])
    # Uncomment below line to see complete error stack trace
    raise e
  finally:
    Connection.close()

if __name__ == "__main__":
  FOLDER_1 = '/Experiment1_rawdata'
  FOLDER_2 = '/Experiment2_rawdata'
  # dump_exp1_in_sql('{}/Prestrain04_1.txt'.format(ROOT_PATH + FOLDER_1))
  # dump_exp2_in_sql('{}/14_22MnB5_950_700_phip1,0_40ks-1_VD0,15_02.11.17.txt'.format(ROOT_PATH + FOLDER_2))
  plot_experiment_1()

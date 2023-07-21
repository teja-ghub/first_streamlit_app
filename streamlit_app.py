import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 omega 3 & Blueberry oatmeal')
streamlit.text('🥗 kale, Spinach & Rocket Smoothie ')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
Fruits_selected = streamlit.multiselect("pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[Fruits_selected]
streamlit.dataframe(fruits_to_show)
#function
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

#new function for api respnose
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:                                   
      back_from_function =get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLerror as e:
    streamlit.error()

streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
#add a button to load fruit
if streamlit.button('Get Fruit Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
   
#function for end user
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values('guava')")
         return "Thanks for adding"+ new_fruit
       
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function =insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)













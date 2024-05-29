# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(" :cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose your fruits and
    **make a custom smoothie!**"""
)
name = st.text_input("Name on smoothie")

if name:
    st.write("Hello",name)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

fruit_list = st.multiselect(
'Choose your PRUUUUTTT',my_dataframe,max_selections = 5
)
if fruit_list:
    #st.write(fruit_list)
    #st.text(fruit_list)
    fruit_string = ''
    for x in fruit_list:
        fruit_string += x + ' '
        st.subheader(x + 'Nurtition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + x)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER,ORDER_FILLED)
            values ('""" + fruit_string + """', '""" + name + """','""" + 'False' + """')"""

    #st.write(my_insert_stmt)
    Button = st.button('Place order')
    if Button:
        session.sql(my_insert_stmt).collect()
        st.success(""" Your Smoothie is ordered, """ + name + """! """,icon="✅")
        


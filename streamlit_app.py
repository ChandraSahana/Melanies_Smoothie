# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
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
    
session = get_active_session()
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
    #st.write(fruit_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER,ORDER_FILLED)
            values ('""" + fruit_string + """', '""" + name + """','""" + 'False' + """')"""

    #st.write(my_insert_stmt)
    Button = st.button('Place order')
    if Button:
        session.sql(my_insert_stmt).collect()
        st.success(""" Your Smoothie is ordered, """ + name + """! """,icon="✅")

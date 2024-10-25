# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """choose a fruit you want in your custom smoothie!
    """
)

# adding name input field and label
name_on_order = st.text_input("Name on Smoothie: ")
st.write('Name on your smoothie will be: ',name_on_order)

# session  = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe,use_container_width=True);
ingredient_list = st.multiselect(
    'choose upto 5 ingredients',
    my_dataframe,
    max_selections=5
)

ingredient_string='' 
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)
    # st.write(ingredient_string)
    ingredient_string = " ".join(ingredient_list)


order_insert_smt = """insert into smoothies.public.orders(ingredients,name_on_order) values('"""+ingredient_string+"""','"""+name_on_order+"""')"""
# st.write(order_insert_smt)

time_to_insert = st.button('submit order')

if ingredient_string and time_to_insert:
    session.sql(order_insert_smt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")



# added some change 

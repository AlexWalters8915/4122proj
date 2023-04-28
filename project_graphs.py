import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import altair as alt
import plotly.express as px
warnings.filterwarnings("ignore")
showErrorDetails = False

@st.cache
def load_data():
    df = pd.read_csv('Crash_Reporting.csv')
    return df
#John
df = load_data()
df1 = df
#dfi = df.drop(df[df['Injury Severity'] == 'NO APPARENT INJURY'].index, inplace = True)
#if st.sidebar.checkbox('Severity of Injuries'):
#    fig, ax = plt.subplots()
#    df.filter(['Injury Severity']).value_counts().plot.bar(ax=ax)
#    st.write(fig)

if st.sidebar.checkbox('Collision Type Count'):
    fig, ax = plt.subplots()
    df1.filter(['Collision Type']).value_counts().plot.bar(ax=ax)
    st.write(fig)
    


# Define the available speed limits and sort them in ascending order
speed_limits = sorted(df1['Speed Limit'].unique())
speed_limits.remove(70)

# Create a container for the dropdown, checkbox, and graph
container = st.container()

# Create a dropdown selection widget for speed limits inside the container
with container:
    selected_speed_limit = st.selectbox('Select a speed limit', speed_limits)

# Create a checkbox to exclude "NO APPARENT INJURY" injuries inside the container
with container:
    exclude_no_injury = st.checkbox('Exclude "NO APPARENT INJURY" values', value = True)

# Filter the data based on the selected speed limit and the checkbox value
filtered_data = df1[df1['Speed Limit'] == selected_speed_limit].copy()
if exclude_no_injury:
    filtered_data = filtered_data[filtered_data['Injury Severity'] != 'NO APPARENT INJURY']
    
# Create a bar chart of injury severity counts for the selected speed limit
with container:
    fig, ax = plt.subplots()
    filtered_data['Injury Severity'].value_counts().plot.bar(ax=ax)
    ax.set_title('Distribution of Injuries by Severity at {} Miles Per Hour'.format(selected_speed_limit))
    st.write(fig)
    
    
    
    #--------------------------------------------------------------------------------------------------------
    df2 = df
    #test to make sure data frame made it
    #print(df2)
#Alex w
#drops null values and any duplicates from chart
counties = df2['Agency Name'].dropna().unique()



#pick police depatment they want to look at (built in a similair way to the types of eletric power activity we did 
#https://discuss.streamlit.io/t/newb-to-streamlit-easy-selectbox-question-i-am-sure/21758/5
counties = ['Rockville Police Departme', 'Montgomery County Police', 'Rockville Police Departme','Gaithersburg Police Depar','Takoma Park Police Depart']
option = st.sidebar.selectbox('Which department do you want to display?', counties)

# filter the data to reduce size but also make sure only the correctselection is shown
#https://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
#data frame county is equal to df2 where Agency Name is equal to option(ie selection by use)
county_data = df2[df2['Agency Name'] == option]


# create pie chart basics 
#https://altair-viz.github.io/gallery/pie_chart_with_labels.html basics to creating a pie chart in altair
#https://stackoverflow.com/questions/62547160/altair-data-aggregation
pie_chart = alt.Chart(county_data).transform_aggregate(
 #counts number of occurence
    count='count()',
    #the groupiongs for the pie chart
    groupby=['Collision Type']
).mark_arc().encode(
    color='Collision Type:N',
    theta='count:Q'
).properties(
    width=800,
    height=800,
    title='Collision types by department'
)

#display chart
st.write(pie_chart)



#---------------------------------------------------------------------------------
#Sreehitha
df3 =df

if st.sidebar.checkbox('Collision Type/Date'):
    # Extract the month from the 'Crash Date/Time' column and create a new column with it
    df3['Period'] = pd.to_datetime(df3['Crash Date/Time']).dt.to_period('M')

    df3 = df3.head(5000)

    # Convert the 'month' column to a string format
    df3['Period'] = df3['Period'].astype(str)

# Create an interactive scatter plot using plotly express
    fig = px.scatter(df3, x='Period', y='Speed Limit', color='Collision Type',
                     title='Crash Rate by Period and Collision Type')

# Display the chart in a web browser
    fig.show()

#------------------------------------------
#Luai

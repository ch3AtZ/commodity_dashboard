import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV file with low_memory=False to suppress the DtypeWarning
file_path = '/Users/dhruvbharara/Downloads/upto29.csv'
df = pd.read_csv(file_path, low_memory=False)

# Preprocess data (e.g., converting date, handling missing values)
df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], format='%d/%m/%y')

# Convert price columns to numeric, forcing errors to NaN
df['Modal_x0020_Price'] = pd.to_numeric(df['Modal_x0020_Price'], errors='coerce')
df['Max_x0020_Price'] = pd.to_numeric(df['Max_x0020_Price'], errors='coerce')

# Streamlit App
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Modal Price Analysis", "Max Price Analysis","Min Price Analysis" , 'Commodity Wise'])

if page == "Modal Price Analysis":
    st.title("Commodity Price Analysis Dashboard")
    
    # Creating filters
    state = st.selectbox('Select State:', df['State'].unique())
    district = st.selectbox('Select District:', df[df['State'] == state]['District'].unique())
    market = st.selectbox('Select Market:', df[(df['State'] == state) & (df['District'] == district)]['Market'].unique())
    commodity = st.selectbox('Select Commodity:', df[(df['State'] == state) & (df['District'] == district) & (df['Market'] == market)]['Commodity'].unique())

    # Filter the DataFrame
    filtered_df = df[(df['State'] == state) &
                     (df['District'] == district) &
                     (df['Market'] == market) &
                     (df['Commodity'] == commodity)]

    # Drop any rows with NaN values in 'Modal_x0020_Price'
    filtered_df = filtered_df.dropna(subset=['Modal_x0020_Price'])

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
    else:
        # Calculate the average modal price
        average_price = filtered_df['Modal_x0020_Price'].mean()

        # Display the results
        st.write(f"### Average Modal Price for {commodity} in {market}, {district}, {state}: ₹{average_price:.2f}")

        # Create a Plotly visualization
        fig = px.line(filtered_df, x='Arrival_Date', y='Modal_x0020_Price', title=f'Modal Price Over Time for {commodity}')
        
        # Add markers to the line for better visibility
        fig.update_traces(mode='lines+markers')
        
        # Display the plot
        st.plotly_chart(fig)

elif page == "Max Price Analysis":
    st.title("Maximum Price Analysis")

    # Creating filters
    state = st.selectbox('Select State:', df['State'].unique())
    district = st.selectbox('Select District:', df[df['State'] == state]['District'].unique())
    market = st.selectbox('Select Market:', df[(df['State'] == state) & (df['District'] == district)]['Market'].unique())
    
    # Filter the DataFrame
    filtered_df = df[(df['State'] == state) &
                     (df['District'] == district) &
                     (df['Market'] == market)]

    # Drop any rows with NaN values in 'Max_x0020_Price'
    filtered_df = filtered_df.dropna(subset=['Max_x0020_Price'])

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
    else:
        # Find the row with the maximum price
        max_price_row = filtered_df.loc[filtered_df['Max_x0020_Price'].idxmax()]

        # Display the results
        st.write(f"### Highest Price Commodity in {market}, {district}, {state}")
        st.write(f"**Commodity:** {max_price_row['Commodity']}")
        st.write(f"**Variety:** {max_price_row['Variety']}")
        st.write(f"**Maximum Price:** ₹{max_price_row['Max_x0020_Price']:.2f}")
        st.write(f"**Arrival Date:** {max_price_row['Arrival_Date'].strftime('%d/%m/%Y')}")
        
        # Create a Plotly visualization
        fig = px.line(filtered_df[filtered_df['Commodity'] == max_price_row['Commodity']],
                      x='Arrival_Date', y='Max_x0020_Price',
                      title=f'Max Price Over Time for {max_price_row["Commodity"]}')
        
        # Add markers to the line for better visibility
        fig.update_traces(mode='lines+markers')
        
        # Display the plot
        st.plotly_chart(fig)
elif page == "Min Price Analysis":
    st.title("Minimum Price Analysis")

    # Creating filters
    state = st.selectbox('Select State:', df['State'].unique())
    district = st.selectbox('Select District:', df[df['State'] == state]['District'].unique())
    market = st.selectbox('Select Market:', df[(df['State'] == state) & (df['District'] == district)]['Market'].unique())
    
    # Filter the DataFrame
    filtered_df = df[(df['State'] == state) &
                     (df['District'] == district) &
                     (df['Market'] == market)]

    # Drop any rows with NaN values in 'Min_x0020_Price'
    filtered_df = filtered_df.dropna(subset=['Min_x0020_Price'])

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
    else:
        # Find the row with the minimum price
        min_price_row = filtered_df.loc[filtered_df['Min_x0020_Price'].idxmin()]

        # Display the results
        st.write(f"### Lowest Price Commodity in {market}, {district}, {state}")
        st.write(f"**Commodity:** {min_price_row['Commodity']}")
        st.write(f"**Variety:** {min_price_row['Variety']}")
        st.write(f"**Minimum Price:** ₹{min_price_row['Min_x0020_Price']:.2f}")
        st.write(f"**Arrival Date:** {min_price_row['Arrival_Date'].strftime('%d/%m/%Y')}")
        
        # Create a Plotly visualization
        fig = px.line(filtered_df[filtered_df['Commodity'] == min_price_row['Commodity']],
                      x='Arrival_Date', y='Min_x0020_Price',
                      title=f'Min Price Over Time for {min_price_row["Commodity"]}')
        
        # Add markers to the line for better visibility
        fig.update_traces(mode='lines+markers')
        
        # Display the plot
        st.plotly_chart(fig)

elif page == "Commodity Wise":
    st.title("Commodity Wise Analysis")

    # Create filter for commodity
    commodity = st.selectbox('Select Commodity:', df['Commodity'].unique())

    # Filter the DataFrame
    filtered_df = df[df['Commodity'] == commodity]

    # Drop any rows with NaN values in price columns
    filtered_df = filtered_df.dropna(subset=['Modal_x0020_Price', 'Max_x0020_Price', 'Min_x0020_Price'])

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        st.write("No data available for the selected commodity.")
    else:
        # Display summary statistics
        st.write(f"### Summary for {commodity}")
        st.write(f"**Number of Records:** {filtered_df.shape[0]}")
        st.write(f"**Average Modal Price:** ₹{filtered_df['Modal_x0020_Price'].mean():.2f}")
        st.write(f"**Highest Price:** ₹{filtered_df['Max_x0020_Price'].max():.2f}")
        st.write(f"**Lowest Price:** ₹{filtered_df['Min_x0020_Price'].min():.2f}")

        # Create Plotly visualization for Modal Price
        fig_modal = px.line(filtered_df, x='Arrival_Date', y='Modal_x0020_Price', title=f'Modal Price Over Time for {commodity}')
        fig_modal.update_traces(mode='lines+markers')
        st.plotly_chart(fig_modal)

        # Create Plotly visualization for Max Price
        fig_max = px.line(filtered_df, x='Arrival_Date', y='Max_x0020_Price', title=f'Max Price Over Time for {commodity}')
        fig_max.update_traces(mode='lines+markers')
        st.plotly_chart(fig_max)

        # Create Plotly visualization for Min Price
        fig_min = px.line(filtered_df, x='Arrival_Date', y='Min_x0020_Price', title=f'Min Price Over Time for {commodity}')
        fig_min.update_traces(mode='lines+markers')
        st.plotly_chart(fig_min)
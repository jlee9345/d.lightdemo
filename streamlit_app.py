import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Sidebar header
st.sidebar.header('d.light Solar Demo')

# Load the custom CSS
def load_css():
    css = """
    .card {
        background-color: #f0f0f0;
        padding: 15px;
        margin: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .card p {
        margin: 0;
    }
    .metric {
        font-size: 2em;
        font-weight: bold;
    }
    .metric-name {
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 5px;
    }
    .logic {
        font-size: 0.9em;
        color: #555;
        margin-top: 10px;
    }
    .section {
        margin-top: 20px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.8em;
    }
    th, td {
        text-align: left;
        padding: 8px;
    }
    th {
        font-weight: bold;
        background-color: #f0f0f0;
    }
    .dropdown {
        margin-bottom: 5px;
    }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

load_css()

# Function to determine the color of the metric based on its value
def get_metric_color(value):
    if value > 0:
        return "green"
    elif value < 0:
        return "red"
    else:
        return "black"

# Appliance Unit Wattage Assumptions
APPLIANCE_WATTAGE = {
    'tv': 45,
    'light': 5,
    'fan': 75,
    'phone': 20,
    'home_theater': 50,
    'laptop': 65
}

def calculate_wattage(appliances):
    return sum(APPLIANCE_WATTAGE[appliance] * quantity for appliance, quantity in appliances.items())

# Sidebar tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.sidebar.tabs(["Product Type", "Appliance Usage", "Monthly Energy Costs", "Other Energy Needs", "Assumptions", "Generator Assumptions"])

# Product Type Inputs
with tab1:
    st.subheader('Product Type')
    product_selection = st.selectbox("Select your product", ["iMax 10 w/ 1 x 200W panel", "iMax 10 w/ 2 x 200W panels"], key="product_selection")

    if product_selection == "iMax 10 w/ 1 x 200W panel":
        product_info = {
            "Deposit": "₦75,200",
            "Weekly Repayment": "₦12,600",
            "Tenor (weeks)": "93",
            "Total PAYGO Price": "₦1,247,000",
            "Outright CASH Price": "₦826,000",
            "Total solar panels wattage": "200W",
            "Inverter": "500W",
            "Battery Capacity": "538W"
        }
        total_solar_panels_wattage = 200
        battery_capacity = 538
        weekly_repayment = 12600
        paygo_price = 1247000
        cash_price = 826000
    else:
        product_info = {
            "Deposit": "₦88,000",
            "Weekly Repayment": "₦14,000",
            "Tenor (weeks)": "93",
            "Total PAYGO Price": "₦1,390,000",
            "Outright CASH Price": "₦946,000",
            "Total solar panels wattage": "400W",
            "Inverter": "500W",
            "Battery Capacity": "538W"
        }
        total_solar_panels_wattage = 400
        battery_capacity = 538
        weekly_repayment = 14000
        paygo_price = 1390000
        cash_price = 946000

    st.markdown(f"""
    <div class="card">
        <table>
            <tr><th>Deposit</th><td>{product_info['Deposit']}</td></tr>
            <tr><th>Weekly Repayment</th><td>{product_info['Weekly Repayment']}</td></tr>
            <tr><th>Tenor (weeks)</th><td>{product_info['Tenor (weeks)']}</td></tr>
            <tr><th>Total PAYGO Price</th><td>{product_info['Total PAYGO Price']}</td></tr>
            <tr><th>Outright CASH Price</th><td>{product_info['Outright CASH Price']}</td></tr>
            <tr><th>Total solar panels wattage</th><td>{product_info['Total solar panels wattage']}</td></tr>
            <tr><th>Inverter</th><td>{product_info['Inverter']}</td></tr>
            <tr><th>Battery Capacity</th><td>{product_info['Battery Capacity']}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    payment_type = st.selectbox("Select Payment Type", ["PAYGO", "CASH"], key="payment_type")
    if payment_type == "PAYGO":
        st.write(f"Price: ₦{paygo_price:,.2f}")
    else:
        st.write(f"Price: ₦{cash_price:,.2f}")

# Appliance Usage Inputs
with tab2:
    st.subheader('Appliance Selector')
    appliances = {
        'tv': st.slider("How many TVs will you power?", 0, 5, 0),
        'light': st.slider("How many lights will you power?", 0, 20, 0),
        'fan': st.slider("How many fans will you power?", 0, 10, 0),
        'phone': st.slider("How many phones will you charge?", 0, 10, 0),
        'home_theater': st.slider("How many home theaters will you power?", 0, 3, 0),
        'laptop': st.slider("How many laptops will you charge?", 0, 5, 0)
    }
    other_watts = st.slider("What is the total number of watts to power your other appliances", 0, 500, 0)
    st.write("TV(s): ", appliances['tv'], " Light(s): ", appliances['light'], " Fan(s): ", appliances['fan'], " Phone(s): ", appliances['phone'], " Home Theater(s): ", appliances['home_theater'], " Laptop(s): ", appliances['laptop'], " Other Appliance Watts: ", other_watts)

    total_watts = calculate_wattage(appliances) + other_watts

# Monthly Energy Cost Inputs
with tab3:
    st.subheader('Your Monthly Grid Energy & Gasoline Costs')

    # List of states
    states = ["Abia", "Abuja", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nassarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"]

    # User selects their state
    state = st.selectbox("Select your state", states)

    # Upload file
    uploaded_file = st.file_uploader("Upload the Excel file with fuel prices", type="xlsx")

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Uploaded Data")
            st.write(df)
            st.write("Columns:", df.columns)

            # Find the most recent price data for the selected state
            state_column_name = df.columns[0]  # Assuming the first column is the state column
            latest_price_row = df[df[state_column_name] == state].iloc[:, 1:].dropna(axis=1, how='all').iloc[:, -1]
            latest_price = latest_price_row.values[0]
            average_price = df.iloc[:, 1:].mean().mean()
            
            st.write(f"Most recent fuel price: ₦{latest_price:,.2f} per liter")
            st.write(f"Average fuel price: ₦{average_price:,.2f} per liter")
        except Exception as e:
            st.write(f"Error processing the data: {e}")
    else:
        latest_price = 650

    # Input for yearly growth rate
    yearly_growth_rate = st.number_input("Enter the yearly growth rate of petrol prices (%)", value=15.0, step=0.1, key="yearly_growth_rate")

    # Calculate the monthly growth rate
    monthly_growth_rate = ((1 + yearly_growth_rate / 100) ** (1 / 12)) - 1

    # Display the monthly growth rate
    st.write(f"Monthly Growth Rate: {monthly_growth_rate * 100:.2f}%")
    
    # User input for liters of fuel used per month
    fuel_usage = st.number_input("How many liters of fuel do you use per month?", value=150.0, step=0.1, key="fuel_usage")

    # Calculate fuel cost if the price is available
    fuel_cost = fuel_usage * latest_price

    grid_cost = st.number_input("How much do you spend per month on grid energy?", value=0, step=1, key="grid_cost")
    total_cost = fuel_cost + grid_cost

    st.write(f"Monthly cost for fuel: ₦{fuel_cost:,.2f}")
    st.write(f"Monthly cost for grid energy: ₦{grid_cost:,.2f}")
    st.write(f"Total energy cost per month: ₦{total_cost:,.2f}")

# Other Energy Needs Inputs 
with tab4:
    st.subheader('Other Energy Needs')
    hours_electricity = st.number_input("How many hours of continuous electricity do you need daily?", min_value=0, max_value=24, value=0, step=1, key="hours_electricity")
    day_usage_percentage = st.slider("Percentage of electricity usage during the day", 0, 100, 50, key="day_usage_percentage")
    night_usage_percentage = 100 - day_usage_percentage
    solar_replacement = st.slider("Estimate the percentage of energy needs you expect to replace with solar", 0, 100, 50, key="solar_replacement")

    st.write(f"You need {hours_electricity} hours of continuous electricity daily.")
    st.write(f"Percentage of electricity usage: {day_usage_percentage}% during the day, {night_usage_percentage}% at night.")
    st.write(f"Estimated percentage of energy needs to be replaced with solar: {solar_replacement}%")    

# Assumptions tab
with tab5:
    st.subheader('Assumptions')
    sunny_weather_percentage = st.slider("Percentage of sunny weather per day", 0, 100, 70, key="sunny_weather_percentage")
    daylight_hours = st.slider("Hours of daylight per day", 0, 24, 12, key="daylight_hours")
    night_hours = 24 - daylight_hours

    st.write(f"Hours of night time per day: {night_hours}")

# Generator Assumptions tab
with tab6:
    st.subheader('Generator Assumptions')
    initial_generator_cost = st.number_input("Initial Generator Cost (₦)", value=55000, step=1000, key="initial_generator_cost")
    monthly_maintenance_cost = st.number_input("Monthly Generator Maintenance Cost (₦)", value=3500, step=100, key="monthly_maintenance_cost")

# Main section with tabs
tabs = st.tabs(["Cost Savings", "Load", "Advanced Metrics"])

with tabs[0]:
    st.subheader('Cost Savings')

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # Creating the data
    generator_grid_costs = []
    solar_costs = []

    for month in range(36):
        if month == 0:
            generator_cost = initial_generator_cost + fuel_cost + grid_cost + monthly_maintenance_cost
            fuel_monthly_cost = fuel_cost
            grid_monthly_cost = grid_cost
        else:
            fuel_monthly_cost *= (1 + monthly_growth_rate)
            grid_monthly_cost *= (1 + monthly_growth_rate)
            generator_cost = fuel_monthly_cost + grid_monthly_cost + monthly_maintenance_cost

        if payment_type == "PAYGO":
            if month == 0:
                solar_cost = float(product_info["Deposit"].replace("₦", "").replace(",", "")) + (weekly_repayment * 4)
            else:
                solar_cost = weekly_repayment * 4
        else:
            solar_cost = cash_price if month == 0 else 0

        generator_grid_costs.append(generator_cost)
        solar_costs.append(solar_cost)

    chart_data = pd.DataFrame({
        "Month": list(range(1, 37)),
        "Generator Grid Cost": generator_grid_costs,
        "Solar Cost": solar_costs
    })

    # Melt the dataframe for easier plotting
    melted_chart_data = chart_data.melt('Month', var_name='Cost Type', value_name='Cost')

    # Creating the layered area chart with Altair
    combined_chart = alt.Chart(melted_chart_data).mark_area().encode(
        x=alt.X('Month:O', axis=alt.Axis(title='Month')),
        y=alt.Y('Cost:Q', stack=None, axis=alt.Axis(title='Cost (₦)')),  # Disable stacking
        color=alt.Color('Cost Type:N', legend=alt.Legend(title="Cost Type", orient="bottom")),
        tooltip=[
            alt.Tooltip('Month:O', title='Month'),
            alt.Tooltip('Cost:Q', title='Cost (₦)', format=',.2f'),
            alt.Tooltip('Cost Type:N', title='Cost Type')
        ]
    ).properties(
        title='Cost Savings'
    )

    # Solar Cost Savings bar chart
    chart_data['Cost Savings'] = chart_data['Generator Grid Cost'] - chart_data['Solar Cost']
    chart_data['Color'] = chart_data['Cost Savings'].apply(lambda x: 'green' if x > 0 else 'red')

    savings_chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Month:O', axis=alt.Axis(title='Month')),
        y=alt.Y('Cost Savings:Q', axis=alt.Axis(title='Cost Savings (₦)')),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=[
            alt.Tooltip('Month:O', title='Month'),
            alt.Tooltip('Cost Savings:Q', title='Cost Savings (₦)', format=',.2f')
        ]
    ).properties(
        title='Solar Cost Savings'
    )

    # Display the charts
    st.altair_chart(combined_chart, use_container_width=True)
    st.altair_chart(savings_chart, use_container_width=True)

    # DataFrame configuration
    cost_type_selection = st.selectbox("Select Cost Type", ["Generator Grid Cost", "Solar Cost"], key="cost_type_selection")

    if cost_type_selection == "Generator Grid Cost":
        df_data = {
            "Month": list(range(1, 37)),
            "Total Cost": [f"₦{cost:,.2f}" for cost in generator_grid_costs],
            "Initial Cost": [f"₦{initial_generator_cost:,}"] + ["₦0"] * 35,
            "Monthly Fuel Cost": [f"₦{fuel_cost:,.2f}"] + [f"₦{fuel_cost * (1 + monthly_growth_rate) ** month:,.2f}" for month in range(1, 36)],
            "Monthly Grid Cost": [f"₦{grid_cost:,.2f}"] + [f"₦{grid_cost * (1 + monthly_growth_rate) ** month:,.2f}" for month in range(1, 36)],
            "Maintenance Cost": [f"₦{monthly_maintenance_cost:,.2f}"] * 36
        }
    else:
        df_data = {
            "Month": list(range(1, 37)),
            "Total Cost": [f"₦{cost:,.2f}" for cost in solar_costs],
            "Deposit": ["₦0"] + ["₦0"] * 35 if payment_type == "CASH" else [f"₦{float(product_info['Deposit'].replace('₦', '').replace(',', '')):,.2f}"] + ["₦0"] * 35,
            "Weekly Repayment": [f"₦{weekly_repayment * 4:,}"] * 36 if payment_type == "PAYGO" else ["₦0"] * 36
        }

    df = pd.DataFrame(df_data)

    st.dataframe(df, use_container_width=True)

with tabs[1]:
    st.subheader('Load')

    # Stacked bar chart for total appliance load
    appliance_data = pd.DataFrame({
        'Appliance': ['TV', 'Light', 'Fan', 'Phone', 'Home Theater', 'Laptop', 'Other'],
        'Wattage': [appliances['tv'] * APPLIANCE_WATTAGE['tv'], appliances['light'] * APPLIANCE_WATTAGE['light'],
                    appliances['fan'] * APPLIANCE_WATTAGE['fan'], appliances['phone'] * APPLIANCE_WATTAGE['phone'],
                    appliances['home_theater'] * APPLIANCE_WATTAGE['home_theater'], appliances['laptop'] * APPLIANCE_WATTAGE['laptop'],
                    other_watts],
        'Count': [appliances['tv'], appliances['light'], appliances['fan'], appliances['phone'], appliances['home_theater'], appliances['laptop'], other_watts]
    })

    # Updated chart with total appliance load in watts and tooltip for number of appliances
    load_chart = alt.Chart(appliance_data).mark_bar().encode(
        x=alt.X('Appliance:N', axis=alt.Axis(title='Appliance')),
        y=alt.Y('Wattage:Q', axis=alt.Axis(title='Total Appliance Load (W)')),
        color=alt.Color('Appliance:N'),
        tooltip=[
            alt.Tooltip('Appliance:N', title='Appliance'),
            alt.Tooltip('Wattage:Q', title='Wattage (W)'),
            alt.Tooltip('Count:Q', title='# of Appliances')
        ]
    ).properties(
        title='Total Appliance Load'
    )

    st.altair_chart(load_chart, use_container_width=True)

    # Total Load and Metrics
    st.markdown('### Total Load')
    col1, col2 = st.columns(2)
    col1.metric("Total Appliance Watts", total_watts)
    col2.metric("Cost of running generator & grid energy", total_cost)

    # Runtime Metrics
    if total_watts != 0:
        runtime_without_panels = battery_capacity / total_watts
    else:
        runtime_without_panels = float('inf')

    watts_generated_per_hour_daytime = (sunny_weather_percentage / 100) * total_solar_panels_wattage
    if total_watts - watts_generated_per_hour_daytime > 0:
        runtime_with_panels = battery_capacity / (total_watts - watts_generated_per_hour_daytime)
    else:
        runtime_with_panels = float('inf')

    if runtime_with_panels == float('inf'):
        runtime_with_panels_text = "inf"
        runtime_with_panels_color = "off"
    else:
        runtime_with_panels_text = f"{runtime_with_panels:.2f} hours"
        runtime_with_panels_color = "normal"

    col1, col2 = st.columns(2)
    col1.metric("Runtime without panels", f"{runtime_without_panels:.2f} hours")
    col2.metric("Runtime with panels", f"{runtime_with_panels_text} hours", delta_color=runtime_with_panels_color)

with tabs[2]:
    st.subheader('Advanced Metrics')

    sunny_weather_fraction = sunny_weather_percentage / 100
    total_max_watts_generated_per_day = sunny_weather_fraction * daylight_hours * total_solar_panels_wattage

    st.markdown(f"""
    <div class="card">
        <p class="metric" style="color: {get_metric_color(total_max_watts_generated_per_day)};">{total_max_watts_generated_per_day:,.2f} W</p>
        <p class="metric-name">Total Maximum Watts Generated per Day</p>
        <p class="logic">Total Maximum Watts Generated per day = Percentage of sunny weather per day * Hours of daylight per day * Total solar panels wattage</p>
        <p class="logic">Total Maximum Watts Generated per day = {sunny_weather_percentage}% * {daylight_hours} hours * {total_solar_panels_wattage}W</p>
    </div>
    """, unsafe_allow_html=True)

    watts_generated_per_hour_daytime = sunny_weather_fraction * total_solar_panels_wattage
    appliance_watt_usage_daytime_per_hour = watts_generated_per_hour_daytime - total_watts
    appliance_watt_usage_nighttime_per_hour = total_watts
    battery_charge_time_hours = battery_capacity / watts_generated_per_hour_daytime

    st.markdown(f"""
    <div class="card">
        <p class="metric" style="color: {get_metric_color(appliance_watt_usage_daytime_per_hour)};">{appliance_watt_usage_daytime_per_hour:,.2f} W</p>
        <p class="metric-name">Total Appliance Wattage needed while charging in the daytime per Hour</p>
        <p class="logic">Total appliance wattage needed while charging in the daytime per hour = (Percentage of sunny weather per day * Total solar panels wattage of product selected) - Total appliance watts</p>
        <p class="logic">Total appliance wattage needed while charging in the daytime per hour = ({sunny_weather_fraction} * {total_solar_panels_wattage}) - {total_watts:,}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <p class="metric" style="color: {get_metric_color(appliance_watt_usage_nighttime_per_hour)};">{appliance_watt_usage_nighttime_per_hour:,.2f} W</p>
        <p class="metric-name">Total Appliance Watt Usage during the Nighttime per Hour</p>
        <p class="logic">Total appliance watt usage during the nighttime per hour = Total appliance watts</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <p class="metric" style="color: {get_metric_color(watts_generated_per_hour_daytime)};">{watts_generated_per_hour_daytime:,.2f} W</p>
        <p class="metric-name">Watts Generated per Hour during Daytime</p>
        <p class="logic">Watts generated per hour during daytime = Percentage of sunny weather per day * Total solar panels wattage of product selected</p>
        <p class="logic">Watts generated per hour during daytime = {sunny_weather_fraction} * {total_solar_panels_wattage}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <p class="metric" style="color: {get_metric_color(battery_charge_time_hours)};">{battery_charge_time_hours:,.2f} hours</p>
        <p class="metric-name">0-100% Battery Charge Time in Hours</p>
        <p class="logic">0-100% Battery Charge Time in hours = Battery Capacity / Watts generated per hour during daytime</p>
        <p class="logic">0-100% Battery Charge Time in hours = {battery_capacity} / {watts_generated_per_hour_daytime}</p>
    </div>
    """, unsafe_allow_html=True)

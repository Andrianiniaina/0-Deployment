# Import useful libraries
import streamlit as st

# Data manipulation
import pandas as pd
import plotly.graph_objects as go

# Data visualization
import plotly.express as px

# Requests
import requests

import os

# Page configuration
st.set_page_config(
    page_title="Getaround Space",
    page_icon="👩‍💻",
    layout="wide"
  )

# Create a title for the app
st.title('👩‍💻 Dashboard with streamlit')

# Create a sidebar
st.sidebar.image("Getaround_(Europe).png")

# Create checkboxes on the sidebar
data = st.sidebar.checkbox("Show data", key="raw_data_checkbox")
data_analysis = st.sidebar.checkbox("Data Analysis", key="data_analysis_checkbox")
machine_learning = st.sidebar.checkbox("Machine Learning", key="machine_learning_checkbox")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("get_around_delay_analysis.xlsx")
    return df

if data :
    # If data show raw data and some visualizations
    st.markdown("<h3 style='color: #00DDD1; font-weight: bold;'>Data</h3>",unsafe_allow_html=True)
    st.subheader("Loading data...")
    data = load_data()

    # Display the data
    if st.checkbox("Show raw data") :
        st.write(data)

    # Visualizations
    with st.expander("See visualizations") :
        tab1, tab2, tab3, tab4 = st.tabs([
            "Checkout delays",
            "Time distribution between two rentals",
            "Check-in types",
            "Rental statuses"
            ])
        
        # Tab 1 : Visualization of the distribution of checkout delays
        with tab1 :
            st.subheader("Distribution of checkout delays")
            fig1 = px.histogram(
                data, 
                x="delay_at_checkout_in_minutes", 
                histfunc="count",
                nbins=100
            )
            fig1.update_layout(
                xaxis_title="Delay (minutes)",
                yaxis_title="Frequency",
                bargap=0.1
            )
            st.plotly_chart(fig1)

        # Tab 2 : Visualization of the time distribution between two rentals
        with tab2:
            st.subheader("Time distribution between two rentals")
            fig2 = px.histogram(
                data, 
                x="time_delta_with_previous_rental_in_minutes", 
                nbins=30, 
                color_discrete_sequence=["#00DDD1"]  
            )
            fig2.update_layout(
                xaxis_title="Time (minutes)",
                yaxis_title="Frequency",
                bargap=0.1, 
                showlegend=False
            )
            st.plotly_chart(fig2)

        # Tab 3 : Visualization of the distribution of check-in types
        with tab3:
            st.subheader("Distribution of check-in types")
            fig3 = px.histogram(
                data,
                x="checkin_type",
                nbins=30,
                color_discrete_sequence=["#93D7C5"]
            )
            fig3.update_layout(
                xaxis_title="Check-in type",
                yaxis_title="Frequency",
                bargap=0.1,
                showlegend=False
            )
            st.plotly_chart(fig3)
            
        # Tab 4 : Visualization of the rental statuses
        with tab4:
            st.subheader("Distribution of rental statuses")
            state_counts = data["state"].value_counts(normalize=True) * 100
            color_mapping = {
                "ended": "#00DDD1",
                "cancelled": "#93D7C5"
            }
            colors = [color_mapping.get(state) for state in state_counts.index] 
            fig4 = go.Figure()
            fig4.add_trace(go.Pie(
                labels=state_counts.index,
                values=state_counts.values,
                marker=dict(colors=colors), 
                textinfo="percent+label", 
                pull=[0.2] * len(state_counts)
            ))
            st.plotly_chart(fig4)
    st.divider()

if data_analysis :
    # If data analysis show data analysis
    st.markdown("<h3 style='color: #00DDD1; font-weight: bold;'>Data Analysis</h3>",unsafe_allow_html=True)

    st.markdown("""
        To avoid unsatisfied customers, we need to understand the impact of checkout delays in the rental process.
        To do this, we will answer the following questions:
    """)

    # st.write("The following graphs can help us answer these questions:")
    st.write("To answer these following questions, let's initiallize the thershold for the delay at checkout.")

    data = load_data()
    threshold1 = st.number_input("Thershold for delay at checkout (minutes)", min_value=0, max_value=720, value=0, step=30, key="threshold1")

    # Function to analyze rentals based on a threshold
    def analyze_rentals_threshold(data, threshold):
        """
        Analyzes the impact of an arbitrary threshold on rentals.

        Parameters:
        - data: DataFrame containing the rentals
        - threshold: Threshold in minutes to filter rentals

        Returns:
        - Percentage of rentals affected for each check-in type
        - Number of problem cases resolved
        """
        # Filter rentals based on the given threshold
        affected_rentals = data[data['time_delta_with_previous_rental_in_minutes'] < threshold]
                
        # Calculation of rentals affected by check-in type
        affected_rentals_connect = affected_rentals[affected_rentals['checkin_type'] == 'connect']
        affected_rentals_mobile = affected_rentals[affected_rentals['checkin_type'] == 'mobile']
        
        # Calculation of the percentage of rentals affected by check-in type
        total_rentals_connect = (data['checkin_type'] == 'connect').sum()
        total_rentals_mobile = (data['checkin_type'] == 'mobile').sum()
        
        percentage_affected_connect = (len(affected_rentals_connect) / total_rentals_connect * 100) if total_rentals_connect > 0 else 0
        percentage_affected_mobile = (len(affected_rentals_mobile) / total_rentals_mobile * 100) if total_rentals_mobile > 0 else 0
        
        # Calculation of resolved problem cases for each check-in type
        problem_cases_resolved_connect = affected_rentals_connect[affected_rentals_connect['delay_at_checkout_in_minutes'] > 0]
        problem_cases_resolved_mobile = affected_rentals_mobile[affected_rentals_mobile['delay_at_checkout_in_minutes'] > 0]
        
        return percentage_affected_connect, percentage_affected_mobile, problem_cases_resolved_connect, problem_cases_resolved_mobile, affected_rentals_connect, affected_rentals_mobile, affected_rentals, total_rentals_connect, total_rentals_mobile

    # Call function to analyze rentals based on the threshold
    percentage_affected_connect, percentage_affected_mobile, problem_cases_resolved_connect, problem_cases_resolved_mobile, affected_rentals, affected_rentals_connect, affected_rentals_mobile, total_rentals_connect, total_rentals_mobile = analyze_rentals_threshold(data, threshold1)

    col1, col2, col3 = st.columns([2, 2, 4])

    with col1:
        st.metric(
            "Rentals with a delay (Connect)", 
            len(affected_rentals_connect),
            delta=len(affected_rentals_connect) - len(affected_rentals_mobile)
        )
        st.metric(
            "Rentals with a delay (Mobile)", 
            len(affected_rentals_mobile),
            delta=len(affected_rentals_mobile) - len(affected_rentals_connect)
        )
    with col2:
        st.metric(
            "Percentage of rentals with a delay (Connect)",
            f"{percentage_affected_connect:.2f}%",
            delta=f"{percentage_affected_connect - percentage_affected_mobile:.2f}%"
        )
        st.metric(
            "Percentage of rentals with a delay (Mobile)",
            f"{percentage_affected_mobile:.2f}%",
            delta=f"{percentage_affected_mobile - percentage_affected_connect:.2f}%"
        )
    with col3:
        # Graph showing the percentage of rentals affected by check-in type
        fig_affected = px.bar(
            pd.DataFrame({
                "Check-in Type": ["Connect", "Mobile"],
                "Percentage Affected": [percentage_affected_connect, percentage_affected_mobile]
            }),
            x="Check-in Type",
            y="Percentage Affected",
            color="Check-in Type",
            color_discrete_sequence=["#00DDD1", "#93D7C5"],
            title="Percentage of Rentals Affected by Check-in Type"
        )
        st.plotly_chart(fig_affected)
    st.divider()

    # Question 1       
    with st.expander("1- Which share of our owner’s revenue would potentially be affected by the feature?") :
        st.write("Depending on the threshold chosen, we can see the different revenue shares that could be affected by the threshold's implementation.")
        col1, col2 = st.columns(2)
        with col1 :
            st.write("By defining the thresholds above, we can see the different revenue shares that could be affected by the threshold's implementation, depending on the check-in type used.")
            st.write("Part of owner's revenue impacted by threshold")
            col2.metric(
                "With connect check-in type",
                f"{percentage_affected_connect:.2f}%",
            )
            col2.metric(
                "With mobile check-in type",
                f"{percentage_affected_mobile:.2f}%",
            )

    # Question 2
    with st.expander("2- How many rentals would be affected by the feature depending on the threshold and scope we choose?"):
        col1, col2 = st.columns(2)
        col1.metric(
            "Rentals with a delay (Connect)", 
            int(len(affected_rentals_connect)), 
            delta=int(len(affected_rentals_connect) - len(affected_rentals_mobile))
        )
        col2.metric(
            "Rentals with a delay (Mobile)", 
            int(len(affected_rentals_mobile)), 
            delta=int(len(affected_rentals_mobile) - len(affected_rentals_connect))
        )
    
    # Question 3
    with st.expander("3- How often are drivers late for the next check-in? ") :
        
        def impacted_next_rentals():
            # Select only the rentals with a delay at checkout
            delayed_checkouts = data[['delay_at_checkout_in_minutes', 'checkin_type']].dropna()
            positive_delays = delayed_checkouts[delayed_checkouts['delay_at_checkout_in_minutes'] > 0]
            
            # Total of rentals with a delay
            total_delayed_rentals = len(positive_delays)
            
            # Select only the rentals with a delay at checkout and a check-in type
            delayed_connect = positive_delays[positive_delays['checkin_type'] == 'connect']
            delayed_mobile = positive_delays[positive_delays['checkin_type'] == 'mobile']

            # Compute the percentage of delayed rentals
            percentage_delayed = (total_delayed_rentals / len(delayed_checkouts)) * 100

            # Compute the percentage of delayed rentals for each check-in type
            percentage_delayed_connect = (len(delayed_connect) / total_delayed_rentals * 100) if total_delayed_rentals > 0 else 0
            percentage_delayed_mobile = (len(delayed_mobile) / total_delayed_rentals * 100) if total_delayed_rentals > 0 else 0

            return percentage_delayed, percentage_delayed_connect, percentage_delayed_mobile
        # Retrieve values
        percentage_delayed, percentage_delayed_connect, percentage_delayed_mobile = impacted_next_rentals()

        # Display the results
        col1, col2 = st.columns(2)
        col1.write("We must not forget the overall percentage of rentals returned late.")
        with col2 :
            st.metric(
                "Percentatge of rentals with a delay at checkout",
                f"{percentage_delayed:.2f}%",
            )
        st.write(f"Approximatevely {percentage_delayed:.2f}% of rentals are a positive delay at checkout.")
        st.divider()
        
        st.write("We can divide this percentage by type of check-in :")
        col1, col2 = st.columns(2)
        with col1 :
            st.metric(
                "Percentatge of rentals with a delay at checkout (Connect)",
                f"{percentage_delayed_connect:.2f}%",
            )
            st.metric(
                    "Percentatge of rentals with a delay at checkout (Mobile)",
                    f"{percentage_delayed_mobile:.2f}%",
            )
        with col2 :
            fig = px.pie(
                names=["Connect", "Mobile"],
                values=[percentage_delayed_connect, percentage_delayed_mobile],
                title="Percentage of Rentals with Delay by Check-In Type",
                color_discrete_sequence=["#00DDD1", "#93D7C5"]
                )
            st.plotly_chart(fig)

    # Question 4
    with st.expander("4- How does it impact the next driver?") :
        st.markdown("""
            Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day.
            \n Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental
        """)

        # Select only the rentals with a delay at checkout and a check-in type
        impacted_next_rentals = data[data['time_delta_with_previous_rental_in_minutes'].notna() & (data['time_delta_with_previous_rental_in_minutes'] < 0)]
        percentage_impacted = len(impacted_next_rentals) / len(data) * 100
        
        col1, col2 = st.columns(2)
        with col1 :
            st.markdown("""
            Currently, the impact on the next driver is simply dissatisfaction.
            \n Considering cancellations, canceled rentals either result in no subsequent rentals or the next rental is more than 12 hours after the previous rental.
            """)
        with col2:
            st.metric(
                "Percentage of cancelled rentals with a delay at checkout",
                f"{percentage_impacted:.2f}%"
            )
        
        nb_cancelled_rentals = data[(data['state'] == 'cancelled') &
                            (data['delay_at_checkout_in_minutes'] > 0) &
                            (data['previous_ended_rental_id'].notna())]
        st.markdown(
            f"<span style='color: blue;'>According to our data, for any rental with a 'cancelled' status with a previous completed rental recorded is: {len(nb_cancelled_rentals)}</span>",
            unsafe_allow_html=True
        )
    
    # Question 5
    with st.expander("5- How many problematic cases will it solve depending on the chosen threshold and scope?"):
        st.markdown("""
            Let's repeat our calculation:
            \n Depending on the threshold and check-in type, here are the number of problem cases that will be resolved:
        """)
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Threshold for delay at checkout (minutes): {threshold1}")
        with col2:
            checkin_type = st.radio(
                "Check-in type",
                [":rainbow[Connect]", ":rainbow[Mobile]"],
                key="checkin_type2",
            )

        # Display the results based on the selected check-in type
        st.write(f"Number of problematic cases resolved")
        if checkin_type == ":rainbow[Connect]":
            resolved_case = len(problem_cases_resolved_connect)
            st.write(f"With threshold of {threshold1} minutes and checkin type Connect")
            st.metric(
                "Number of problem cases resolved (Connect)",
                f"{resolved_case}",
            )
        elif checkin_type == ":rainbow[Mobile]":
            resolved_case = len(problem_cases_resolved_mobile)
            st.write(f"With threshold of {threshold1} minutes and checkin type Mobile")
            st.metric(
                "Number of problem cases resolved (Mobile)",
                f"{resolved_case}",
            )

    # Conclusion
    with st.expander("Conclusion") :
        st.markdown("""
            Analyzing checkout delays reveals significant impacts on the rental process, affecting both revenue and guest satisfaction. 
            \n By setting an appropriate threshold, we can reduce the number of problematic cases, thus improving the overall user experience. 
            \n Visualizations and calculations show that check-in types (connected and mobile) have different impacts, requiring tailored strategies for each case. 
            \n By optimizing these aspects, we can not only increase operational efficiency but also increase guest loyalty by minimizing frustrations related to delays.
            """)
    st.divider()
    
if machine_learning :
    st.markdown("<h3 style='color: #00DDD1; font-weight: bold;'>Pricing Prediction</h3>",unsafe_allow_html=True)

    # Space of API
    URL_BASE = "https://andrianiniaina-api-space-1f33d3f.hf.space/"      

    # API
    def get_prediction(data):
        response = requests.post(f"{URL_BASE}/predict", json=data)
        # st.write("Raw API response:", response.text)
        if response.status_code == 200:
            result = response.json()
            return result["predicted_price"]
        else:
            return None

    # Layout
    row1 = st.columns(1)
    row2_left, row2_center, row2_right = st.columns(3)
    row3 = st.columns(1)

    # Features
    features = {}

    # ---------------- ENUM MAPPINGS ----------------
    model_key_map = {
        "Citroën": "Citroën",
        "Peugeot": "Peugeot",
        "PGO": "PGO",
        "Renault": "Renault",
        "Audi": "Audi",
        "BMW": "BMW",
        "Ford": "Ford",
        "Mercedes": "Mercedes",
        "Opel": "Opel",
        "Porsche": "Porsche",
        "Volkswagen": "Volkswagen",
        "KIA Motors": "KIA Motors",
        "Alfa Romeo": "Alfa Romeo",
        "Ferrari": "Ferrari",
        "Fiat": "Fiat",
        "Lamborghini": "Lamborghini",
        "Maserati": "Maserati",
        "Lexus": "Lexus",
        "Honda": "Honda",
        "Mazda": "Mazda",
        "Mini": "Mini",
        "Mitsubishi": "Mitsubishi",
        "Nissan": "Nissan",
        "SEAT": "SEAT",
        "Subaru": "Subaru",
        "Suzuki": "Suzuki",
        "Toyota": "Toyota",
        "Yamaha": "Yamaha"
    }

    fuel_type_map = {
        "Diesel": "diesel",
        "Petrol": "petrol",
        "Hybrid Petrol": "hybrid_petrol",
        "Electro": "electro"
    }

    paint_color_map = {
        "Black": "black",
        "Grey": "grey",
        "White": "white",
        "Red": "red",
        "Silver": "silver",
        "Blue": "blue",
        "Orange": "orange",
        "Beige": "beige",
        "Brown": "brown",
        "Green": "green"
    }

    car_type_map = {
        "Convertible": "convertible",
        "Coupe": "coupe",
        "Estate": "estate",
        "Hatchback": "hatchback",
        "Sedan": "sedan",
        "Subcompact": "subcompact",
        "SUV": "suv",
        "Van": "van"
    }


    with row1[0]:
        st.markdown("""
            Please select in the following features the characteristics of the car you want to rent.
        """)

    # Initialize default values ​​for selectboxes (if not already defined)
    if "model_label" not in st.session_state:
        st.session_state.model_label = ""
    if "fuel_label" not in st.session_state:
        st.session_state.fuel_label = ""
    if "color_label" not in st.session_state:
        st.session_state.color_label = ""
    if "car_type_label" not in st.session_state:
        st.session_state.car_type_label = ""

    with row2_left:
        model_options = [""] + list(model_key_map.keys())
        model_label = st.selectbox(
            "Model of the car",
            model_options,
            format_func=lambda x: "Select a model of car" if x == "" else x,
            key="model_label",
            )
        
        fuel_options = [""] + list(fuel_type_map.keys())
        fuel_label = st.selectbox(
            "Fuel type", 
            fuel_options,
            format_func=lambda x: "Select a fuel type" if x == "" else x,
            key="fuel_label",
            )
        
        color_options = [""] + list(paint_color_map.keys())
        color_label = st.selectbox(
            "Paint color", 
            color_options,
            format_func=lambda x: "Select a paint color" if x == "" else x,
            key="color_label",
            )
        
        car_type_options = [""] + list(car_type_map.keys())
        car_type_label = st.selectbox(
            "Car type", 
            car_type_options,
            format_func=lambda x: "Select a car type" if x == "" else x,
            key="car_type_label",
            )

    with row2_center:
        with st.container(border=True): 

            st.write("Select numerical features...")
            #  ------------- Mileage ---------------
            mileage = st.number_input(
                "Mileage",
                min_value=0,
                max_value=500000,
                step=1,
                placeholder="Enter the mileage",
                key="mileage",
            )
            #  ------------- Engine Power ---------------
            engine_power = st.number_input(
                "Engine power",
                min_value=0,
                max_value=1000,
                step=1,
                placeholder="Enter the engine power",
                key="engine_power",
            )            
            
            st.write("Select boolean features...")
            #  ------------- Private parking available ---------------
            private_parking_available = st.checkbox(
                "Private parking available",
                value=False,
                key="private_parking_available",
            )
            #  ------------- Has GPS ---------------
            has_gps = st.checkbox(
                "Has GPS",
                value=False,
                key="has_gps",
            )
            #  ------------- Has air conditioning ---------------
            has_air_conditioning = st.checkbox(
                "Has air conditioning",
                value=False,
                key="has_air_conditioning",
            )
            #  ------------- Automatic car ---------------
            automatic_car = st.checkbox(
                "Automatic car",
                value=False,
                key="automatic_car",
            )
            #  ------------- Has Getaround Connect---------------
            has_getaround_connect = st.checkbox(
                "Has Getaround Connect",
                value=False,
                key="has_getaround_connect",
            )
            #  ------------- Has speed regulator ---------------
            has_speed_regulator = st.checkbox(
                "Has speed regulator",
                value=False,
                key="has_speed_regulator",
            )
            #  ------------- Winter tires ---------------
            winter_tires = st.checkbox(
                "Has winter tires",
                value=False,
                key="winter_tires",
            )
           
    with row2_right:
        with st.container(border=True):
            features = {
                "model_key": model_key_map.get(model_label, None),
                "fuel": fuel_type_map.get(fuel_label, None),
                "paint_color": paint_color_map.get(color_label, None),
                "car_type": car_type_map.get(car_type_label, None),
                "mileage": mileage,
                "engine_power": engine_power,
                "private_parking_available": private_parking_available,
                "has_gps": has_gps,
                "has_air_conditioning": has_air_conditioning,
                "automatic_car": automatic_car,
                "has_getaround_connect": has_getaround_connect,
                "has_speed_regulator": has_speed_regulator,
                "winter_tires": winter_tires,
            }

            st.write(features)

    # ------------- Click manage ---------------
    if "prediction_price" not in st.session_state:
        st.session_state.prediction_price = None
    
    def predict_action():
        prediction = get_prediction(features)
        # st.write("DEBUG prediction:", prediction)
        if prediction is not None:
            st.session_state.prediction_price = prediction
        else:
            st.session_state.prediction_price = "Not specified"


    ML_KEYS = {
        "model_key": None,
        "fuel": "",
        "paint_color": "",
        "car_type": "",
        "mileage": 0,
        "engine_power": 0,
        "private_parking_available": False,
        "has_gps": False,
        "has_air_conditioning": False,
        "automatic_car": False,
        "has_getaround_connect": False,
        "has_speed_regulator": False,
        "winter_tires": False,
        "prediction_price": None
    }

    def reset_ml_form():
        for key, default in ML_KEYS.items():
            st.session_state[key] = default
        st.session_state.model_label = ""
        st.session_state.fuel_label = ""
        st.session_state.color_label = ""
        st.session_state.car_type_label = ""
        
    with row3[0] :
        with st.container(border=True):
            st.write("Make prediction")

            # ------------- Make prediction ---------------
            st.button("Predict price", on_click=predict_action)
            st.button("Reset", on_click=reset_ml_form)

            if st.session_state.prediction_price is not None:
                if isinstance(st.session_state.prediction_price, (int, float)):
                    st.success(f"The predicted price is: {st.session_state.prediction_price:.2f} €")
                    # st.write(st.session_state)
                else:
                    st.error(f"Prediction failed: {st.session_state.prediction_price}")
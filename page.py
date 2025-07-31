import streamlit as st 

#THIS PAGE IS THE CODE FOR THE METHODOLOGY AND CREDITS BUT IT IS LATER IMPORTED IN THE ORIGINAL FILE (APP.PY)

###METHODOLOGY PAGE 
#JUSTIFICATION OF TEXT TO MAKE IT LOOK NEATER
def justified(text):
    st.markdown(f"<div style='text-align: justify'>{text}</div>", unsafe_allow_html=True)

##ENERGY USAGE
#THIS IS THE TEXT FOR THE METHODS
def methods():
    justified("The dashboard has been designed to illustrate the energy usage and carbon dioxide equivalent (CO₂e) emissions of a computing lab. Ultimately, the dashboard will ingest live energy (or power) data for a given lab, look up live CO₂e emissions, and calculate the CO₂e emissions due to that energy usage. ")
    st.markdown(" ")
    justified("In this prototype, due to the unavailability of live energy data, an example CSV file was used to provide a sample dataset relating to energy used by the computing lab. To calculate CO₂e emissions, carbon intensity (CI) data was retrieved from <a href='https://carbonintensity.org.uk/' target='_blank'>Carbon Intensity API</a> and stored in a separate CSV file. In practice, these files will be replaced by actual data inputs.")
    st.markdown(" ")
    justified("The example computing lab CSV file contains power data for the period between January 1st, 2025, and June 30th, 2025, at 30-minute intervals, and this is used to estimate energy usage (see below). The source code is currently configured to demonstrate graphs for this specific date range. However, it can be easily adjusted to support different timeframes depending on data availability.")
    st.markdown(" ")
    justified("Similarly, the CI file includes data for the period between January 1st, 2025 and June 30th, 2025, at the same 30-minute intervals. Due to limitations with the Carbon Intensity API, this dataset was created by combining data from several downloads from the CI website.")
    st.markdown(" ")
    justified("In terms of missing data, if the user selects dates with no energy and/or CO₂e emissions data, those dates will be displayed, but with values set to zero. Similarly, if some periods have no data (e.g. an hour out of a day), then a default value of zero is used for that period, leading to under-estimates of energy and carbon consumption.")
    st.markdown("<br>", unsafe_allow_html=True) 

#DATA DESIGN SECTION
    st.markdown("<h3 style='font-size: 20px;'>Energy Usage</h3>",unsafe_allow_html=True)
    st.markdown("""1. Date Format of Computing Lab CSV """)   
    st.markdown(" The data format that is necessary for this dashboard is an excel spreadsheet (CSV file). This spreadsheet needs to consist of two main columns:")
    st.markdown("""         
- Datetime, which records timestamps at 30-minute intervals for the period between January 1st, 2025 and June 30th, 2025. 

- Power at T which was the instantaneous power reading (in kW) at time T. 
   """ )


#DATA IMPLEMENTATION SECTION
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("2. Data Implementation")   
    justified("This data was implemented on <a href='https://streamlit.io/' target='_blank'>Streamlit</a>, an open-source Python framework for creating interactive applications. The dashboards were created using various programming languages, including Python, HTML, and CSS, to process the data and design the layout. ")
    st.markdown(" ")
    justified("The Pandas library was useful for various functions such as reading the energy CSV file and filtering the dataset based on selected timeframes including daily, weekly, monthly, and yearly. This further includes building the following DataFrames columns: Datetime, Power at T (kW), Power at T+30min (kW), and Energy Used (kWh). ")
    st.markdown(" ")
    justified("The process starts with the system reading the Datetime column and filtering the data to cover only the period from January to June 2025. For each timestamp, the Power at T (kW) is retrieved from the spreadsheet. The system shifts the power values forward by one time interval (30 minutes ahead) to generate a new column, Power at T+30min (kW). Next, hardcoded summations are performed to average power readings (Power at T and Power at T+30min). Following this, the result is multiplied by 0.5 hours, as per the energy calculation formula below, producing the new column Energy Used (kWh). This is because the assumed dataset is recorded at half-hour (0.5-hour) intervals, indicating that each row represents energy usage over a 30-minute period. Furthermore, NumPy was used to structure the time intervals, with Matplotlib visualizing an image of energy consumption. ")

#THIS IS FOR THE ENERGY FORMULA
    st.latex(r"Energy = (\frac{P_1 + P_2}{2}) \times \Delta t")

    justified("The calculations for the different timeframes are calculated as follows: the daily plot displays the half-hourly energy data (Energy Used (kWh) column) for a single day. For the weekly plot, the half-hourly values are summed for each day to show total daily usage across all seven days of the week. The monthly plot follows a similar approach but spans a 30 or 31-day period instead of seven days. Lastly, the yearly plot aggregates the energy usage over each 30 or 31-day period (calendar month) to represent the total monthly usage. ")







#CO2e Emissions Section
#Data Design
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("<h3 style='font-size: 20px;'>CO₂e Emissions</h3>",unsafe_allow_html=True)
    st.markdown("1. Data Format of Carbon Intensity CSV")
    st.markdown("This section requires the previously energy CSV file along with a new excel spreadsheet (CSV file) which includes the following columns: ")
    st.markdown("""
    - Datetime, T, which records timestamps at 30-minute intervals for the period between January 1st, 2025 and June 30th, 2025. 
    - Carbon Intensity (in gCO₂e/kWh) at time, T. 
 """)
#Data Implementation
    st.markdown("<br>", unsafe_allow_html=True) 
    st.markdown("2. Data Implementation")   
    justified("As a continuation of the energy script implemented in Streamlit, the CO₂e-related section differs as it processes two separate files instead: the energy CSV and the carbon intensity CSV.  First, the Datetime column in both files was converted to a standard format and aligned to merge the two datasets together. Following this, energy usage was recalculated using the previous hardcoded formula from the energy CSV file. Finally, the Emissions DataFrame column was newly generated by multiplying the calculated energy values by the corresponding carbon intensity values for a given time period.")
    st.markdown(" ")
    justified("As a result, Matplotlib managed to provide a visualization of the CO₂e emissions (in gCO₂e) of a computing lab on a daily, weekly, monthly, and yearly basis. Similarly to energy, CO₂e emissions undergo the same timeframe-based calculations. The main difference is that the figures display the CO₂e emissions (Emissions column) instead.  ")
    st.latex(r"CO₂e = \text{Energy} \times \text{Carbon Intensity}")



























###CREDITS PAGE 

def acknowledge():
    st.markdown("This dashboard has been created as part of the Green Software Internship at Manchester Metropolitan University, funded by Jobs 4 Students.")
    st.markdown("<h3 style='font-size: 20px;'>Development</h3>",unsafe_allow_html=True)
    st.markdown("Designed and developed by Raghad Sandid, BSc Environmental Science Undergraduate & Green Software Intern.")
    st.markdown("Email: raghadsandid5@gmail.com | LinkedIn: www.linkedin.com/in/raghad-sandid")
    st.markdown("<h3 style='font-size: 20px;'>Supervision</h3>",unsafe_allow_html=True)
    st.markdown("With special thanks to Dr. Michael Bane, Senior Lecturer in Green Software Engineering & Performance Computing, for his continuous support, feedback, and guidance throughout this internship.")
    st.markdown("Email: m.bane@mmu.ac.uk | LinkedIn: www.linkedin.com/in/mkbane/")
    st.markdown("<h3 style='font-size: 20px;'>Further Information</h3>",unsafe_allow_html=True)
    st.markdown("For further information, please contact Michael on m.bane@mmu.ac.uk or visit https://GreenCompute.UK.")
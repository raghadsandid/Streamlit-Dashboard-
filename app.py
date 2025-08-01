import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
from datetime import date, timedelta
from page import methods
from page import acknowledge

#NOTES
#I LIKE TO LEAVE A LOT OF SPACE BETWEEN SECTIONS JUST SO I DON'T GET CONFUSED
#I WROTE THE NOTES IN CAPITAL LETTERS, IT CAN BE EITHER WITH A # OR /* 
#THE CODE CAN EITHER BE SOURCED FROM  STREAMLIT TUTORIALS, DISCUSSION CHATS, OR CHATGPT IF IT IS SPECIFIC 
#SOMETIMES THE ELEMENT REQUIRES A LABEL EVEN THOUGH I WOULD NOT WANT ONE SO THAT IS WHY YOU MIGHT SEE "T" AND THEN COLLAPSED



#CREATING THE NAVIGATION SIDEBAR WHICH WILL SHOW THE 4 DIFFERENT PAGES
with st.sidebar:
    st.title("Navigation")
    page = st.sidebar.radio("T", ["Energy Usage", "CO₂e Emissions", "Methodology", "Credits"], label_visibility="collapsed")

#SHOWING THE WORD "DASHBOARD" IF THE PAGE IS ENERGY USAGE OR CARBON EMISSIONS 
if page in ["Energy Usage", "CO₂e Emissions"]:
    st.subheader("Dashboard")
   
#DIFFERENT TITLES FOR THE 4 DIFFERENT PAGES 
if page == "Energy Usage":
    st.markdown("Energy Usage in a Computing Lab")
elif page == "CO₂e Emissions":
    st.markdown("CO₂e Emissions Statistics")
elif page == "Methodology":
    st.subheader("Methodology")
elif page == "Credits":
    st.subheader("Credits")


st.markdown("""
    <style>
    /*PULLS THE MAIN CONTENT UP*/
    .block-container {
    padding-top: 3rem;
}

/* FORCES THE BACKGROUND AND APP COLOR TO BE BLACK + TEXT COLOR TO BE WHITE + ADDS THE FONT */
    header {background-color: #00000 !important;}
    .stApp {
        background-color: #000000;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
/* CREATING THE 4 RADIO BUTTONS (DAILY, WEEKLY, MONTHLY, YEARLY) (AND NAVIGATION SIDEBAR) + FLEX FOR HORIZONTAL LAYOUT SIDE BY SIDE + BACKGROUND COLOR FOR THE RADIO BUTTONS + BORDER RADIUS TO ROUND THE CORNERS + PADDING TO CREATE INNER SPACE FROM ALL SIDES AND THE EDGES + MARGINS TO GIVE VERTICAL SPACE FOR THE RADIO BUTTONS */
    div[role="radiogroup"] {
        display: flex;
        justify-content: flex-start;
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 6px 10px;
        width: fit-content;
        margin-left: -19px;
        margin-bottom: 50px;
        margin-top: 10px;      
        margin-bottom: 50px;
    }

/* THIS IS FOR EACH SPECIFIC BUTTON IN THE RADIO BUTTONS (AND NAVIGATION SIDEBAR) SO FOR DAILY, FOR MONTHLY.. */
  div[role="radiogroup"] > label {
        padding: 6px 28px;
        margin: 0 4px;
        font-size: 13px;
        font-weight: 500;
        background-color: transparent;
        border-radius: 24px;
        transition: all 0.25s ease;
        cursor: pointer;
        min-height: 40px;
    }

/* THIS CODE ADDS AN EMPTY FAKE BOX BEFORE EACH OPTION IN THE NAVIGATION SIDEBAR + THE CONTENT: '' MEANS THE BOX IS EMPTY FOR NOW, BUT I WILL FILL IT WITH AN ICON IMAGE LATER + DISPLAY: INLINE-BLOCK TO MAKE THE BOX BEHAVE LIKE AN ELEMENT THAT CAN HAVE WIDTH AND HEIGHT FOR SIZE + MARGIN-RIGHT CREATES SPACE BETWEEN THE ICON AND THE TEXT, SO THEY DON’T TOUCH. */
section[data-testid="stSidebar"] div[role="radiogroup"] > label::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    background-size: contain;
    margin-right: 10px;
}


/* THIS IS THE LINK FOR THE ICONS IN THE NAVIGATION SIDEBAR FOR THE DIFFERENT OPTIONS (PAGES) */


section[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(1)::before {
    background-image: url('https://img.icons8.com/?size=100&id=dycyAkR52Xah&format=png&color=3490EC');
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(2)::before {
    background-image: url('https://img.icons8.com/?size=100&id=rbeD1p7PbOib&format=png&color=3490ec');
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(3)::before {
    background-image: url('https://img.icons8.com/?size=100&id=NC7hjV0bhWcl&format=png&color=3490ec');
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:nth-of-type(4)::before {
    background-image: url('https://img.icons8.com/?size=100&id=80eweJGFK1F4&format=png&color=3490ec');
}


/* GLOWING DESIGN FOR THE NAVIGATION SIDEBAR WHICH CONSISTS OF THE COLOR, GLOW BORDERS, AND ROUNDING CORNERS */
section[data-testid="stSidebar"] {
    padding-left: 2rem !important;}
 {
    border: 2px solid #00b4ff;
    box-shadow: 0 0 5px #00b4ff;
    border-radius: 28px;
    padding: 10px;
}

/* GLOWING DESIGN FOR THE 4 RADIO BUTTONS (DAILY... ETC) */
div[role="radiogroup"] {
    border: 2px solid #00b4ff;
    box-shadow: 0 0 5px #00b4ff;
    border-radius: 28px;
}

/* GLOWING DESIGN FOR THE TIME CONTROL NEXT TO THE 4 RADIO BUTTONS */
div[data-testid="stDateInput"],
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"] {
    border: 2px solid #00b4ff;
    box-shadow: 0 0 5px #00b4ff;
    border-radius: 10px;
    padding: 4px;

}
/* TO REMOVE THE AUTOMATIC CIRCLE ICONS THAT APPEAR FROM THE NAVIGATION SIDEBAR */
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    display: none !important;


}
section[data-testid="stSidebar"] div[role="radiogroup"] > label *::before {
  content: none !important;
}

/* ensure the icon on the label itself doesn’t tile */
section[data-testid="stSidebar"] div[role="radiogroup"] > label::before {
  background-repeat: no-repeat;
  background-position: center;
}

section[data-testid="stSidebar"] {
  min-width: 300px !important;   
  
       </style>
""", unsafe_allow_html=True)






#DEFINING MONTH NAMES 
month_names = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

#SPLITS THE PAGE INTO TWO COLUMNS: 4 RADIO BUTTON= 83% WIDTH & TIME CONTROL=24% WIDTH
col1, col2 = st.columns([0.83, 0.24])

#RADIO BUTTON ONLY SHOWS IN ENERGY USAGE AND CARBON EMISSIONS PAGE
#VIEW BUTTON LABEL SHOWS "" BECAUSE STREAMLIT REQUIRES IT BUT IT IS HIDDEN IN THE LABEL VISIBILITY 
#KEY FEATURE TO IDENTIFY THE BUTTON 
with col1:
    if page in ["Energy Usage", "CO₂e Emissions"]:
        view_button = st.radio("T", ["Daily", "Weekly", "Monthly", "Yearly"], horizontal=True, label_visibility="collapsed", key="view_selector")
    else:
        view_button = None  #BUTTON DOESNT SHOW IF IT IS OTHER PAGES BUT DOESNT BREAK

#TIME CONTROL BUTTON ONLY SHOWS IN ENERGY USAGE AND CARBON EMISSIONS PAGE 
#PREPARING TO PUT THE INPUTS LATER THATS WHY ITS STILL NONE 
with col2:
    if page in ["Energy Usage", "CO₂e Emissions"]:
        selected_date = None
        selected_week_label = None
        selected_week_start = None
        year = int(2025)

#THIS IS SETTING UP THE DIFFERENT TIME CONTROLS FOR THE 4 RADIO BUTTON OPTIONS

#DAILY 
#SELECTED DATE IS USED HERE FOR SELECTING A DATE FOR THE DAILY PERSPECTIVE. THE MINIMUM YEAR THAT USERS CAN CHOOSE IS 2020 AND THE MAXIMUM YEAR IS 2050
#KEY FEATURE TO IDENTIFY DAILY 
if page in ["Energy Usage", "CO₂e Emissions"] and view_button == "Daily":
    with col2:
        st.markdown("<div style='margin-top: 5px;'>", unsafe_allow_html=True)
        selected_date = st.date_input("Select a date:", value=date(2025, 1, 1), min_value=date(2020, 1, 1), max_value=date(2050, 12, 31), key="daily_date")
        st.markdown("</div>", unsafe_allow_html=True)

#WEEKLY
#CHATGPT HELPED WITH THIS 
elif page in ["Energy Usage", "CO₂e Emissions"] and view_button == "Weekly":
    with col2:
        def get_weeks(year):
            jan_1 = date(year, 1, 1) #JANUARY 1ST OF THE PICKED YEAR
            start = jan_1 - timedelta(days=jan_1.weekday())  #JAN_1.WEEKDAY() DEFINES A NUMBER WHERE MONDAY = 0, TUESDAY = 1, WEDNESDAY = 2.  IF JANUARY 1ST IS A WEDNESDAY (WHICH IS 2), IT SUBTRACTS TIMEDELTA(DAYS=2) TO GO BACK 2 DAYS, ENDING UP ON MONDAY. THIS MAKES SURE EVERY WEEK STARTS ON A MONDAY, EVEN IF JANUARY 1ST ISN’T.

            weeks = [] #LIST
            for i in range(52): #DO THIS LOOP 52 TIMES 
                week_start = start + timedelta(weeks=i) #STARTS FROM THE FIRST MONDAY AND MOVES FORWARD ONE WEEK EACH LOOP. SO EXAMPLE OF FIRST LOOP i=0 IS "WEEK_START = START + 0 WEEKS" SO IT STAYS DEC 30. EXAMPLE OF SECOND LOOP i=1 IS "WEEK_START = START + 1 WEEKS" SO IT WOULD BE A WEEK LATER JAN 06
                week_end = week_start + timedelta(days=6) #ADD TO THE MONDAY 6 DAYS SO IT WOULD SHOW ALL 7 DAYS OF THE WEEK 

                if week_end.year < year: #IF THE WEEK ENDS IN A YEAR BEFORE 2025, SKIP IT.
                    continue
                if week_start.year > year: #IF THE WEEK STARTS IN A YEAR AFTER 2025, (EXAMPLE 2026) BREAK THE LOOP.
                    break

                label = f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d')}" #CREATES A LABEL SO WEEK STARTS - WEEK ENDS (EXAMPLE: JAN06-JAN12). %b SHORTENS THE MONTH NAME %d SHOWS THE DAY
                weeks.append((label, week_start))
            return weeks #THIS RETURNS A LIST TO USE LATER ON FOR THE DROPDOWN


        week_options = get_weeks(year) #GETS THE GET_WEEKS FUNCTION THAT WAS JUST CREATED. EXAMPLE WEEK_OPTIONS = [("Jan 01 – Jan 07", datetime.date(2025, 1, 1)]
        labels = [label for label, _ in week_options] #THIS JUST MAKES IT APPEAR LABELS AND IGNORE THE SECOND PART (DATETIME)
        selected_week_label = st.selectbox("Select a week:", labels, key="weekly_week") #THIS IS INSERTING THE INPUT FOR THE TIME CONTROL FOR WEEKLY 
        selected_week_start = dict(week_options)[selected_week_label] #THIS IS INSERTING THE INPUT TO MATCH THE LABEL WITH THE WEEK OPTION THE USER HAS SELECTED
        
        year = st.number_input("Select a year:", min_value=2020, max_value=2050, value=2025, key="weekly_year") #SELECTING A YEAR BUTTON 

#MONTHLY
elif page in ["Energy Usage", "CO₂e Emissions"] and view_button == "Monthly":
    with col2:
        month = st.selectbox("Select a month:", month_names, key="Monthly_month")
        year = st.number_input("Select a year:", min_value=2020, max_value=2050, value=2025, key="Monthly_year")

#YEARLY
elif page in ["Energy Usage", "CO₂e Emissions"] and view_button == "Yearly":
    with col2:
     year = st.number_input("Select a year:", min_value=2020, max_value=2050, value=2025, key="Yearly_year")


#LOAD DATA AND READ THE DATE IN A CERTAIN FORMAT AS DAY MONTH YEAR HOURS:MINUTES
#THE INPUT DATA IS HALF HOURLY: 1:00..1:30..2:00
df = pd.read_csv("Power_Energy_Data.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"], format="%d/%m/%Y %H:%M")

# THIS IS TO ACTUALLY TO DO THE MATHEMTICAL CALUCLATIONS BASED ON THE ENERGY FORMULA INSTEAD OF JUST READING THE COLUMN IN THE EXCEL SHEET AS THE ONLY REASON WHY I ADDED THAT COLUMN IS TO SEE IF THE VALUES MATCHED AND IT DID THE CORRECT CALULATIONS

df["Power at T+30min (kW)"] = df["Power at T (kW)"].shift(-1)
df["Energy Used (kWh)"] = ((df["Power at T (kW)"] + df["Power at T+30min (kW)"]) / 2) * 0.5






#####DAILY
if page == "Energy Usage" and view_button == "Daily" and selected_date is not None:

    #ALLOW ONLY JAN TO JUNE, IF NOT SHOW THIS WARNING
    if not (selected_date.year == 2025 and 1 <= selected_date.month <= 6):
     st.warning("Please select a date between January 1st, 2025 and June 30th, 2025.")

    
    else:
        daily_data = df[df["Datetime"].dt.date == selected_date] #GET THE ROWS FOR THE SELECTED DATE
        daily_data = daily_data[~((daily_data["Datetime"].dt.hour == 23) & (daily_data["Datetime"].dt.minute == 30))] #REMOVE THE LAST ROW OF 23:30 AS THE ENERGY VALUE IS FOR THE NEXT DAY AND NOT FOR THE SELECTED DATE

        daily_data["start_time"] = daily_data["Datetime"].dt.hour + daily_data["Datetime"].dt.minute / 60 #EXTRACTS THE HOUR AND MINUTE FROM DATETIME COLUMN AND CONVERTS IT INTO A DECIMAL NUMBER AS IT IS EASIER TO PLOT 
        bar_positions = daily_data["start_time"] #THE EXACT TIME OF DAY FOR THE BAR CHART 
        bar_heights = daily_data["Energy Used (kWh)"] #THE BAR'S HEIGHT FOR THE ENERGY USED VALUES
        bar_widths = [0.5] * len(bar_positions) #THIS IS FOR THE BAR TO BE 0.5 INSTEAD OF 1 SO IT WOULD SHOW THE VALUE FROM 00:00 TO 00:30 INSTEAD OF ONE VALUE FOR EACH BAR 

        xticks = np.arange(0, 24, 0.5) #CREATES A LIST OF NUMBERS FROM 0 TO 23.5, IN STEPS OF 0.5
        xtick_labels = [f"{int(h):02}:00" if h % 1 == 0 else f"{int(h):02}:30" for h in xticks] #IF H IS A WHOLE NUMBER (DECIMAL WOULD BE 1.0) IT WILL SHOW 01:00 + IF H IS HALF NUMBER (DECIMAL WOULD BE 0.5), IT WILL SHOW 01:30

    #PLOT
        fig, ax = plt.subplots(figsize=(20, 8)) #FIGURE SIZE
        ax.set_axisbelow(True)  #CONTROLS THE LAYERING OF THE GRID LINES SO THEY GO UNDER THE BARS
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='white')  #GRID LINES CUSTOMISATION, DASHED STYLE AND WHITE

        ax.bar(bar_positions, bar_heights, width=bar_widths, align='edge', edgecolor='black', color="#1f77b4")  #BAR POSITION, BAR HEIGHTS, BAR WIDTH FROM EARLIER, ALIGN EDGE WHICH ARE THE BLACK LINES THAT ARE THE BORDERS OF THE BAR CHART 
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, rotation=90, fontsize=13, color="white") #CUSTOMIZE THE APPEARANCE FOR THE X-AXIS LABELS BY ROTATION, FONT SIZE, AND COLOR.
        ax.set_xlim(-0.5, 24.5) #GIVES PADDING TO THE RIGHT AND LEFT SIDE SO IT WOULDN'T CUT OFF

        ax.set_title(f"Energy Usage on {selected_date.strftime('%A %d %B %Y')}", fontsize=24, color='white', pad=20) #TITLE OF BAR CHART
        ax.set_xlabel("Time Intervals (30 minutes)", fontsize=18, color='white', labelpad=10) #X-AXIS TITLE
        ax.set_ylabel("Energy (kWh)", fontsize=18, color='white', labelpad=10) #Y-AXIS TITLE
        ax.tick_params(axis='y', colors='white', labelsize=13) #CUSTOMIZE THE APPEARANCE FOR THE Y-AXIS LABELS 

        for spine in ["bottom", "left"]: 
         ax.spines[spine].set_color('white') #BOTTOM AND LEFT SPINE WHICH IS X-AXIS AND Y-AXIS TO BE SET TO COLOR WHITE 
        ax.set_facecolor("none") #PUTS NO SOLID BACKGROUND COLOR 
        fig.patch.set_alpha(0.0) #MAKES THE FIGURE TRANSPARENT

        st.pyplot(fig, use_container_width=True)









#####WEEKLY  

if page == "Energy Usage" and view_button == "Weekly":
    if year != 2025:
        st.warning("Please select a week starting between January 1st, 2025 and June 30th, 2025.") #IF YEAR IS NOT 2025, IT WILL SHOW A WARNING
    
    elif selected_week_start is not None:
        week_end = selected_week_start + timedelta(days=6)
        if not (week_end >= date(2025, 1, 1) and selected_week_start <= date(2025, 6, 30)):
            st.warning("Please select a week starting between January 1st, 2025 and June 30th, 2025.") #ONLY ACCEPT WEEKS THAT END ON OR AFTER JAN 1ST, 2025 + WEEKS THAT START ON OR BEFORE JUNE 30TH, 2025. IF NOT SHOW WARNING
        
        else:
            week_start = selected_week_start
            week_end = week_start + timedelta(days=6)
            #IF THE DATE GREATER THAN OR EQUAL TO THE WEEK'S START DATE + IF THE DATE IS LOWER THAN OR EQUAL TO THE WEEK'S END DATE, THEN GET THAT SPECIFIC WEEK DATA
            mask = (df["Datetime"].dt.date >= week_start) & (df["Datetime"].dt.date <= week_end)
            weekly_data = df[mask]
            weekly_data = weekly_data[weekly_data["Datetime"].dt.date <= date(2025, 6, 30)] #AFTER JUNE 30TH CUT OFF THE DATA 

            #REMOVES THE 23:30 ROW DATA
            weekly_data = weekly_data[~(
                (weekly_data["Datetime"].dt.hour == 23) & 
                (weekly_data["Datetime"].dt.minute == 30)
            )]

            #FORMAT DATE LABELS LIKE "Tuesday 04 January"
            weekly_data["date"] = weekly_data["Datetime"].dt.date
            weekly_data["FullLabel"] = weekly_data["Datetime"].dt.strftime("%A %d %B")

            #SUM TOTAL ENERGY PER DAY
            total_energy_by_day = weekly_data.groupby("FullLabel")["Energy Used (kWh)"].sum()

            #THE FULL WEEK DATES CONSISTS OF ALL THE 7 DATES OF THE SELCTED WEEK FROM MONDAY THROUGH SUNDAY. REGARDING RANGE(7) FOR 0,1,2,3.. (EXAMPLE:week_start:0, week_start + 1 day:1)
            full_week_dates = [week_start + timedelta(days=i) for i in range(7)]
            full_labels = [d.strftime("%A %d %B") for d in full_week_dates]

            #CREATES INITIAL VALUE OF 0 FOR ALL 7 DAYS
            full_week_series = pd.Series(0, index=full_labels)

            #IF REAL DATA EXISTS, MERGE THE full_week_series AND THE total_energy_by_day TOGHETHER TO SHOW THE VALUES. WHERE THERE IS NO DATA AVAILABLE TREAT IT AS ZERO
            total_energy_ordered = full_week_series.add(total_energy_by_day, fill_value=0)

            #DEFINE WEEKDAY ORDER AS THE READABLE FORMAT
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            label_map = {label.split()[0]: label for label in total_energy_ordered.index} #BUILDING DICTIONARY TO MATCH THE LABELS SUCH AS MONDAY 30 JANUARY 2025 TO MONDAY
            ordered_labels = [label_map[day] for day in weekday_order if day in label_map] #AFTER MATCHING, GO THROUGH MONDAY TO SUNDAY AND IF THERE IS DATA FOR THE DAY THEN INCLUDE IT 
            total_energy_ordered = total_energy_ordered.reindex(ordered_labels) #ORDER THEM IN THE CORRECT ORDER OF MON, TUES...

            #PLOT
            fig, ax = plt.subplots(figsize=(18, 6))
            ax.set_axisbelow(True)
            ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")
            
            #CREATE NUMERIC POSITIONS FOR EACH BAR
            x_positions = np.arange(len(total_energy_ordered.index))

            #PLOT USING NUMERIC POSITIONS
            ax.bar(x_positions, total_energy_ordered.values, color="#1f77b4", width=0.6)

            #SET TICKS AND THEIR LABELS
            ax.set_xticks(x_positions)
            ax.set_xticklabels(total_energy_ordered.index, rotation=45, ha="right", fontsize=13, color="white")

            ax.set_title(f"Total Energy Usage: {week_start.strftime('%d %B')} to {week_end.strftime('%d %B')}",fontsize=22, color='white', pad=20)
            ax.set_xlabel("Day of the Week", fontsize=16, color='white', labelpad=10)
            ax.set_ylabel("Total Energy (kWh)", fontsize=16, color='white', labelpad=10)
            ax.tick_params(axis='y', labelsize=13, colors='white')

            for spine in ["bottom", "left"]:
             ax.spines[spine].set_color('white')
            ax.set_facecolor("none")
            fig.patch.set_alpha(0.0)
            
            st.pyplot(fig, use_container_width=True)








#####MONTHLY  

if page == "Energy Usage" and view_button == "Monthly" and month is not None:

    #CONVERTS A MONTH LIKE JANUARY INTO THE NUMBER 1 
    month_number = month_names.index(month) + 1  

    #CHECK IF MONTH IS BETWEEN JANUARY AND JUNE, IF NOT SHOW WARNING
    if not (1 <= month_number <= 6 and year == 2025):
        st.warning("Please select a month between January 1st, 2025 and June 30th 2025.")
    
    else:
        #MONTH_START IS THE FIRST DAY OF MONTH , MONTH_END IS THE LAST DAY OF THE MONTH BASED ON CALENDER SO 30 OR 31 
        month_start = date(year, month_number, 1)
        last_day = calendar.monthrange(year, month_number)[1] #PYTHON BUILT IN CALENDAR
        month_end = date(year, month_number, last_day)

        #KEEPS ONLY ROWS WHERE THE TIMESTAMP IS BETWEEN THE START AND END OF THAT MONTH 
        mask = (df["Datetime"].dt.date >= month_start) & (df["Datetime"].dt.date <= month_end)
        monthly_data = df[mask]

        #REMOVES THE 23:30 ROW DATA
        monthly_data = monthly_data[~(
            (monthly_data["Datetime"].dt.hour == 23) &
            (monthly_data["Datetime"].dt.minute == 30)
        )]

        #CREATE A NEW COLUMN "DATE" FROM THE TIMESTAMP AND SUM ALL 48 READINGS FOR THE SAME DAY
        monthly_data["date"] = monthly_data["Datetime"].dt.date
        total_energy_by_kindamonth = monthly_data.groupby("date")["Energy Used (kWh)"].sum()

        #PLOT
        fig, ax = plt.subplots(figsize=(18, 6))
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")

        ax.bar(total_energy_by_kindamonth.index, total_energy_by_kindamonth.values, color="#1f77b4",width=0.6)
        ax.set_xticks(total_energy_by_kindamonth.index)
        ax.set_xticklabels([date.strftime("%d %b") for date in total_energy_by_kindamonth.index], rotation=45, ha="right", fontsize=13, color="white")

        ax.set_title(f"Total Energy Usage: {month} {year}", fontsize=22, color='white', pad=20)
        ax.set_xlabel("Day of the Month", fontsize=16, color='white', labelpad=10)
        ax.set_ylabel("Total Energy (kWh)", fontsize=16, color='white', labelpad=10)
        ax.tick_params(axis='y', labelsize=13, colors='white')

        for spine in ["bottom", "left"]:
         ax.spines[spine].set_color('white')
        ax.set_facecolor("none")
        fig.patch.set_alpha(0.0)

        st.pyplot(fig, use_container_width=True)









#####YEARLY 
if page == "Energy Usage" and view_button == "Yearly" and year is not None:
    
    #DEFINING THE START AND END OF THE YEAR, IF YEAR IS NOT 2025 IT WILL SHOW WARNING
    year = int(year)
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)

    if not (year == 2025):
        st.warning("Please select the year 2025.")

    else:
        mask = (df["Datetime"].dt.date >= year_start) & (df["Datetime"].dt.date <= year_end)
        yearly_data = df[mask]
        yearly_data = yearly_data[~(
            (yearly_data["Datetime"].dt.hour == 23) & 
            (yearly_data["Datetime"].dt.minute == 30)
        )]

        yearly_data["month"] = yearly_data["Datetime"].dt.month
        total_energy_by_kindayear = yearly_data.groupby("month")["Energy Used (kWh)"].sum()

        #REMOVE REAL VALUES FOR ALL MONTHS THAT ARE GREATER THAN 6 = JULY–DECEMBER (MONTHS 7–12)
        total_energy_by_kindayear = total_energy_by_kindayear[total_energy_by_kindayear.index <= 6]

        all_months = list(range(1, 13))  #MONTH NUMBERS FROM 1 TO 12, THE REASON WHY ITS 13 BECAUSE RANGE DOESNT INCLUDE THE LAST NUMBER 
        month_labels = [calendar.month_name[m] for m in all_months] #LABELING THE CALENDAR MONTH NAMES 

        #REINDEX TO SHOW ALL MONTHS REGARDLESS + FILL MISSING MONTHS (INCLUDING JUL–DEC) WITH 0
        total_energy_by_kindayear = total_energy_by_kindayear.reindex(all_months, fill_value=0)

        #PLOT
        fig, ax = plt.subplots(figsize=(18, 6))
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")

        ax.bar(all_months, total_energy_by_kindayear.values, color="#1f77b4", width=0.6)
        ax.set_xticks(all_months)
        ax.set_xticklabels(month_labels, rotation=45, fontsize=13, color="white")

        ax.set_title(f"Total Energy Usage: {year}", fontsize=22, color='white', pad=20)
        ax.set_xlabel("Month", fontsize=16, color="white", labelpad=10)
        ax.set_ylabel("Total Energy (kWh)", fontsize=16, color="white", labelpad=10)
        ax.tick_params(axis='y', labelsize=13, colors='white')
       
        for spine in ["bottom", "left"]:
         ax.spines[spine].set_color('white')
        ax.set_facecolor("none")
        fig.patch.set_alpha(0.0)

        st.pyplot(fig, use_container_width=True)


#THIS IMPORTS METHODOLOGY AND CREDITS FROM THE OTHER FILE 
elif page == "Methodology":
    methods()

elif page == "Credits":
    acknowledge()

























#####CARBON

#LOAD DATA FROM THE TWO DIFFERENT FILES 
energy_df = pd.read_csv("Power_Energy_Data.csv")
carbon_df = pd.read_csv("Carbon_Data.csv")

#CONVERT DATETIME COLUMN 
energy_df["Datetime"] = pd.to_datetime(energy_df["Datetime"], format="%d/%m/%Y %H:%M")
carbon_df["Datetime"] = pd.to_datetime(carbon_df["Datetime"], format="%d/%m/%Y %H:%M")

#MERGE THE DATETIME COLUMN FROM BOTH FILES 
df = pd.merge(energy_df, carbon_df, on="Datetime", how="inner")

#CALCULATE THE ENERGY USAGE CALCULATIONS
df["Power at T+30min (kW)"] = df["Power at T (kW)"].shift(-1)
df["Energy Used (kWh)"] = ((df["Power at T (kW)"] + df["Power at T+30min (kW)"]) / 2) * 0.5

#CALCULATE THE CO2 EMISSIONS IN gCO2e
df["Emissions"] = df["Energy Used (kWh)"] * df["CI"]







####DAILY
if page == "CO₂e Emissions" and view_button == "Daily" and selected_date is not None:
 
 #ALLOW ONLY JAN TO JUNE, IF NOT SHOW THIS WARNING
 if not(selected_date.year == 2025 and 1 <= selected_date.month <=6):
    st.warning("Please select a date between between January 1st, 2025 and June 30th, 2025.")
 else:
    daily_data = df[df["Datetime"].dt.date == selected_date]
    daily_data = daily_data[~((daily_data["Datetime"].dt.hour == 23) & (daily_data["Datetime"].dt.minute == 30))]

    daily_data = daily_data.copy()
    daily_data["start_time"] = daily_data["Datetime"].dt.hour + daily_data["Datetime"].dt.minute / 60
    bar_positions = daily_data["start_time"]
    bar_heights = daily_data["Emissions"]
    bar_widths = [0.5] * len(bar_positions)

    xticks = np.arange(0, 24, 0.5)
    xtick_labels = [f"{int(h):02}:00" if h % 1 == 0 else f"{int(h):02}:30" for h in xticks]

    #PLOT 
    fig, ax = plt.subplots(figsize=(20, 8))
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='white')

    ax.bar(bar_positions, bar_heights, width=bar_widths, align='edge', edgecolor='black', color="#e63946")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation=90, fontsize=13, color="white")
    ax.set_xlim(-0.5, 24.5)

    ax.set_title(f"CO₂e Emissions on {selected_date.strftime('%A %d %B %Y')}", fontsize=24, color='white', pad=20)
    ax.set_xlabel("Time Intervals (30 minutes)", fontsize=18, color='white', labelpad=10)
    ax.set_ylabel("CO₂e Emissions (gCO₂e)", fontsize=18, color='white', labelpad=10)
    ax.tick_params(axis='y', colors='white', labelsize=13)

    for spine in ["bottom", "left"]:
      ax.spines[spine].set_color('white')
    ax.set_facecolor("none")
    fig.patch.set_alpha(0.0)

    st.pyplot(fig, use_container_width=True)








####WEEKLY
if page == "CO₂e Emissions" and view_button == "Weekly":
     if year != 2025:
        st.warning("Please select a week starting between January 1st, 2025 and June 30th, 2025.")
    
     elif selected_week_start is not None:
        week_end = selected_week_start + timedelta(days=6)
        if not (week_end >= date(2025, 1, 1) and selected_week_start <= date(2025, 6, 30)):
            st.warning("Please select a week starting between January 1st, 2025 and June 30th, 2025.")
        
        else:
            week_start = selected_week_start
            week_end = week_start + timedelta(days=6)

            mask = (df["Datetime"].dt.date >= week_start) & (df["Datetime"].dt.date <= week_end)
            weekly_data = df[mask]
            weekly_data = weekly_data[weekly_data["Datetime"].dt.date <= date(2025, 6, 30)]
            weekly_data = weekly_data[~((weekly_data["Datetime"].dt.hour == 23) & (weekly_data["Datetime"].dt.minute == 30))]

            weekly_data["date"] = weekly_data["Datetime"].dt.date
            weekly_data["FullLabel"] = weekly_data["Datetime"].dt.strftime("%A %d %B")

            #SUM THE EMISSIONS BY DAY TO SHOW FOR A WEEK 
            total_emissions_by_carbonday = weekly_data.groupby("FullLabel")["Emissions"].sum()

            full_week_dates = [week_start + timedelta(days=i) for i in range(7)]
            full_labels = [d.strftime("%A %d %B") for d in full_week_dates]
            full_week_series = pd.Series(0, index=full_labels)

            total_emissions_ordered = full_week_series.add(total_emissions_by_carbonday, fill_value=0)

            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            label_map = {label.split()[0]: label for label in total_emissions_ordered.index}
            ordered_labels = [label_map[day] for day in weekday_order if day in label_map]
            total_emissions_ordered = total_emissions_ordered.reindex(ordered_labels)

            #PLOT
            fig, ax = plt.subplots(figsize=(18, 6))
            ax.set_axisbelow(True)
            ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")

            x_positions = np.arange(len(total_emissions_ordered.index))
            ax.bar(x_positions, total_emissions_ordered.values, color="#e63946", width=0.6)

            ax.set_xticks(x_positions)
            ax.set_xticklabels(total_emissions_ordered.index, rotation=45, ha="right", fontsize=13, color="white")

            ax.set_title(f"Total CO₂e Emissions: {week_start.strftime('%d %B')} to {week_end.strftime('%d %B')}", fontsize=22, color='white', pad=20)
            ax.set_xlabel("Day of the Week", fontsize=16, color='white', labelpad=10)
            ax.set_ylabel("Total CO₂e Emissions (gCO₂e)", fontsize=16, color='white', labelpad=10)
            ax.tick_params(axis='y', labelsize=13, colors='white')

            for spine in ["bottom", "left"]:
             ax.spines[spine].set_color('white')
            ax.set_facecolor("none")
            fig.patch.set_alpha(0.0)

            st.pyplot(fig, use_container_width=True)







#####MONTHLY  

if page == "CO₂e Emissions" and view_button == "Monthly" and month is not None:
    month_number = month_names.index(month) + 1  

    if not (1 <= month_number <= 6 and year == 2025):
        st.warning("Please select a month between January 1st, 2025 and June 30th 2025.")
    
    else:
        month_start = date(year, month_number, 1)
        last_day = calendar.monthrange(year, month_number)[1] 
        month_end = date(year, month_number, last_day)

        mask = (df["Datetime"].dt.date >= month_start) & (df["Datetime"].dt.date <= month_end)
        monthly_data = df[mask]

        monthly_data = monthly_data[~(
            (monthly_data["Datetime"].dt.hour == 23) &
            (monthly_data["Datetime"].dt.minute == 30)
        )]

        monthly_data["date"] = monthly_data["Datetime"].dt.date
        total_energy_by_carbonmonth = monthly_data.groupby("date")["Emissions"].sum() #ADDING EMISSIONS BY DAY TO SHOW A MONTH

        #PLOT
        fig, ax = plt.subplots(figsize=(18, 6))
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")

        ax.bar(total_energy_by_carbonmonth.index, total_energy_by_carbonmonth.values, color="#e63946",width=0.6)
        ax.set_xticks(total_energy_by_carbonmonth.index)
        ax.set_xticklabels([date.strftime("%d %b") for date in total_energy_by_carbonmonth.index], rotation=45, ha="right", fontsize=13, color="white")

        ax.set_title(f"Total CO₂e Emissions: {month} {year}", fontsize=22, color='white', pad=20)
        ax.set_xlabel("Day of the Month", fontsize=16, color='white', labelpad=10)
        ax.set_ylabel("Total CO₂e Emissions (gCO₂e)", fontsize=16, color='white', labelpad=10)
        ax.tick_params(axis='y', labelsize=13, colors='white')

        for spine in ["bottom", "left"]:
         ax.spines[spine].set_color('white')
        ax.set_facecolor("none")
        fig.patch.set_alpha(0.0)

        st.pyplot(fig, use_container_width=True)







#####YEARLY 
if page == "CO₂e Emissions" and view_button == "Yearly" and year is not None:
    
    year = int(year)
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)

    if not (year == 2025):
        st.warning("Please select the year 2025.")

    else:
        mask = (df["Datetime"].dt.date >= year_start) & (df["Datetime"].dt.date <= year_end)
        yearly_data = df[mask]
        yearly_data = yearly_data[~(
            (yearly_data["Datetime"].dt.hour == 23) & 
            (yearly_data["Datetime"].dt.minute == 30)
        )]

        yearly_data["month"] = yearly_data["Datetime"].dt.month
        total_energy_by_carbonyear = yearly_data.groupby("month")["Emissions"].sum()

        total_energy_by_carbonyear = total_energy_by_carbonyear[total_energy_by_carbonyear.index <= 6]

        all_months = list(range(1, 13))  
        month_labels = [calendar.month_name[m] for m in all_months] 

        total_energy_by_carbonyear = total_energy_by_carbonyear.reindex(all_months, fill_value=0)

        #PLOT
        fig, ax = plt.subplots(figsize=(18, 6))
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle="--", alpha=0.3, color="white")

        ax.bar(all_months, total_energy_by_carbonyear.values, color="#e63946", width=0.6)
        ax.set_xticks(all_months)
        ax.set_xticklabels(month_labels, rotation=45, fontsize=13, color="white")

        ax.set_title(f"Total CO₂e Emissions: {year}", fontsize=22, color='white', pad=20)
        ax.set_xlabel("Month", fontsize=16, color="white", labelpad=10)
        ax.set_ylabel("Total CO₂e Emissions (gCO₂e)", fontsize=16, color="white", labelpad=10)
        ax.tick_params(axis='y', labelsize=13, colors='white')
       
        for spine in ["bottom", "left"]:
         ax.spines[spine].set_color('white')
        ax.set_facecolor("none")
        fig.patch.set_alpha(0.0)

        st.pyplot(fig, use_container_width=True)

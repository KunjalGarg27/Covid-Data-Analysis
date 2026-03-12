ṇṇimport pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyfiglet
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from colorama import Fore, Style, init
init(autoreset=True)

ascii_banner = pyfiglet.figlet_format("                       COVID DATA                            ANALYSIS                         ")
print(ascii_banner)

print("*"*75)
print("\n")
print("Welcome to the COVID-19 Data Analysis Project.")
print("This project explores real-world COVID-19 datasets to uncover insights on")
print("infection trends, vaccination rates, healthcare statistics, and more.")
print("Visualizations and data-driven analysis help us better understand the")
print("impact of the pandemic across different regions and time periods.\n")
print("*"*75)
print("\n")



def no_of_cases_india():
    xls = pd.ExcelFile(r"D:\kunjal garg\college\Python programming\Python Project\covid 190 data.xlsx")
    df = pd.read_excel(xls, sheet_name="StatewiseTestingDetails")
    df2=pd.read_csv("D:\kunjal garg\college\Python programming\Python Project\Latest Covid-19 India Status.csv")


    # Preprocessing
    df['Date'] = pd.to_datetime(df['Date'])
    df.dropna(subset=['Date', 'State'], inplace=True)
    df[['TotalSamples', 'Negative', 'Positive']] = df[['TotalSamples', 'Negative', 'Positive']].fillna(0)

    df['Month'] = df['Date'].dt.to_period('M')
    monthly = df.groupby(['State', 'Month'])[['TotalSamples', 'Positive']].sum().reset_index()


    while True:
        print("""
        ============================
            COVID CASE DATA VISUALIZER
        ============================
        1. State-wise Total Cases, Recoveries, and Deaths
        2. Line Chart - Monthly Trend of a State
        3. Fatality Rate vs Recovery Rate
        4. Show Raw Data
        5. Exit
        """)

        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print(" Invalid input.")
            continue

        match choice:
            case 1:
                x = np.arange(len(df2["State"]))
                width = 0.25

                plt.figure(figsize=(18, 8))
                plt.bar(x - width, df2["Total Cases"], width, label="Total Cases", color="orange")
                plt.bar(x, df2["Recovered"], width, label="Recovered", color="green")
                plt.bar(x + width, df2["Deaths"], width, label="Deaths", color="red")
                plt.xticks(x, df2["State"], rotation=90)
                plt.ylabel("Number of People")
                plt.title("COVID-19 Cases, Recoveries & Deaths by State")
                plt.legend()
                plt.tight_layout()
                plt.show()
            case 2:
                state = input("Enter the state name (e.g. Maharashtra): ").strip()
                state_data = monthly[monthly['State'].str.lower() == state.lower()]
                if state_data.empty:
                    print("Error: State not found. ")
                    continue
                plt.figure(figsize=(10, 6))
                plt.plot(state_data['Month'].astype(str), state_data['Positive'], marker='o', color='crimson')
                plt.title(f"Monthly COVID Positive Cases in {state}")
                plt.xlabel("Month")
                plt.ylabel("Positive Cases")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()
                plt.show()

            
            case 3:
                plt.figure(figsize=(8, 6))
                sns.scatterplot(x="Discharge Ratio", y="Death Ratio", data=df2, hue="State")
                plt.xlabel("Recovery Rate (%)")
                plt.ylabel("Case Fatality Rate (%)")
                plt.title("State-wise Recovery vs Fatality Rate")
                plt.legend(title="State", loc='lower center',bbox_to_anchor=(0.5, -0.3), ncol=4)                
                plt.grid(True)
                plt.tight_layout()
                plt.show()
                          

            case 4:
                print("Raw Data \n")
                print(df2)

            
            case 5:
                print("Exiting program. ")
                break

            case _:
                print(" Invalid choice. Try again.")


def vaccination():
    xls = pd.ExcelFile(r"D:\kunjal garg\college\Python programming\Python Project\vaccination data.xlsx")

  
    df1 = pd.read_excel(xls, sheet_name='vaccinationByAge')  # Age-wise vaccination
    df2 = pd.read_excel(xls, sheet_name='StateWiseVaccination')  # State-wise vaccination
    while True:
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + "     Vaccination Data  VISUALIZER   ")
        print(Fore.CYAN + "=" * 40)
        print("""
        Enter Your Choices:-
        1. Show Age-wise Vaccination Pie Chart
        2. Show Total Vaccines administered in all the Indian States
        3. Show the dose administered
        4. Show Raw Age-wise Data
        5. Show Raw State-wise Data
        6. Exit
        """)

        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                # Age-wise vaccination pie chart
                age_groups = df1.columns[0:] 
                vaccination_counts = df1.iloc[0, 0:]  

                plt.figure(figsize=(8, 6))
                plt.pie(vaccination_counts, labels=age_groups,autopct='%1.1f%%', startangle=140)
                plt.title("Vaccination Distribution by Age Group")
                plt.axis('equal')
                plt.tight_layout()
                plt.show()

            case 2:
                df2_sorted = df2.sort_values(by='total', ascending=False)  
                plt.figure(figsize=(16, 8))  
                plt.bar(df2_sorted['title'], df2_sorted['total'], color='skyblue')
                plt.xticks(rotation=90)
                plt.xlabel("State")
                plt.ylabel("Total Vaccinations")
                plt.title("Total Vaccinations by State")
                plt.tight_layout()
                plt.show()

            case 3:
                df2_sorted = df2.sort_values(by='total', ascending=False)

                # Plot
                plt.figure(figsize=(14, 8))

                # Stacked bar components
                plt.bar(df2_sorted['title'], df2_sorted['partial_vaccinated'], label='Partially Vaccinated')
                plt.bar(df2_sorted['title'], df2_sorted['totally_vaccinated'], bottom=df2_sorted['partial_vaccinated'], label='Totally Vaccinated')
                bottom_stack = df2_sorted['partial_vaccinated'] + df2_sorted['totally_vaccinated']
                plt.bar(df2_sorted['title'], df2_sorted['Precaution Dose'], bottom=bottom_stack, label='Precaution Dose')

                plt.xticks(rotation=90)
                plt.xlabel('States')
                plt.ylabel('Number of Vaccinations')
                plt.title('Vaccination Breakdown by State ')
                plt.legend()
                plt.tight_layout()
                plt.show()


            case 4:
                print("\nAge-wise Vaccination Data:\n")
                print(df1)

            case 5:
                print("\nState-wise Vaccination Data of India:\n")
                print(df2)

            case 6:
                print(" Exiting...")
                break
            
            case _:
                print("Invalid choice. Please try again.")

# Hospitals data 
def hospitals():
    df=pd.read_csv("D:\kunjal garg\college\Python programming\Python Project\hospital_beds.csv") # No. of beds
    xls = pd.ExcelFile(r"D:\kunjal garg\college\Python programming\Python Project\No. of hospitals.xlsx")  
    df2 = pd.read_excel(xls, sheet_name='Table 1') # No. of hospitals 
    xls=pd.ExcelFile(r"D:\kunjal garg\college\Python programming\Python Project\Complete hospital data.xlsx")
    df3 = pd.read_excel(xls, sheet_name='Sheet1') # ICU and Ventilators
    while True:
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + "     Hospital Data VISUALIZER    ")
        print(Fore.CYAN + "=" * 40)
        print("""
        Enter Your Choices:-
        1. Total hospitals in each state
        2. Total hospital beds available in each state
        3. Public sector vs Private Sector
        4. Total Number of ICU Beds in each state
        5. Total Number of Ventilators in each state
        6. Show Raw Data
        7. Exit""")

        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                x = np.arange(len(df2['State']))
                width = 0.25

                plt.figure(figsize=(18, 8))
                plt.bar(x - width, df2['Hospitals_Public'], width, label='Public', color='skyblue')
                plt.bar(x, df2['Hospitals_Private'], width, label='Private', color='salmon')
                plt.bar(x + width, df2['Hospitals_Total'], width, label='Total', color='seagreen')
                plt.xticks(x, df2['State'], rotation=90)
                plt.xlabel('States / UTs')
                plt.ylabel('Number of Hospitals')
                plt.title('Public, Private, and Total Hospitals by State / UT')
                plt.legend()
                plt.tight_layout()
                plt.show()

            case 2:
                df.columns = df.columns.str.strip()  
                plt.figure(figsize=(14, 8))
                sns.barplot(data=df, x='Total hospital beds', y='States', palette='coolwarm')
                plt.xticks(rotation=90)
                plt.title('Total Hospital Beds by Stateṣ')
                plt.xlabel('Number of Hospital Beds')
                plt.ylabel('States')
                plt.tight_layout()
                plt.show()
            
            case 3:
                x = np.arange(len(df['States']))
                width = 0.4

                plt.figure(figsize=(16, 8))

                plt.bar(x - width/2, df['Hospital beds in public sector'], width, label='Public', color='steelblue')
                plt.bar(x + width/2, df['Hospital beds in private sector'], width, label='Private', color='salmon')
                plt.xticks(x, df['States'], rotation=90)
                plt.xlabel('States')
                plt.ylabel('Number of Beds')
                plt.title('Public vs Private Hospital Beds by State')
                plt.legend()
                plt.tight_layout()
                plt.show()

            case 4:
                df_sorted = df3.sort_values(by='Total_ICU_Beds', ascending=False)

                plt.figure(figsize=(14, 8))
                sns.barplot(x='Total_ICU_Beds', y='States', data=df_sorted, palette='mako')
                plt.title('Total ICU Beds by State')
                plt.xlabel('Number of ICU Beds')
                plt.ylabel('State')
                plt.tight_layout()
                plt.show()

            case 5:
                plt.figure(figsize=(14, 8))
                sns.barplot(x='Total_ventilators', y='States', data=df3)
                plt.title('Total Ventilators by State')
                plt.xlabel('Number of Ventilators')
                plt.ylabel('State')
                plt.tight_layout()
                plt.show()

            case 6:
                print("Raw Data \n")
                print(df)
                print("\n")
                print(df2)
                print("\n")
                print(df3)

            case 7:
                print(" Exiting...")
                break
            
            case _:
                print("Invalid choice. Please try again.")


# Economic Impact              
def economy():
    df = pd.read_csv(r"D:\kunjal garg\college\Python programming\Python Project\unemployment_rate_rural.csv")
    df2=pd.read_csv("D:\kunjal garg\college\Python programming\Python Project\india_gdp_loss_covid_simulated.csv")   

    while True:
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + "     Economic Impact VISUALIZER    ")
        print(Fore.CYAN + "=" * 40)
        print("""
        Enter Your Choices:-
        1. Unemployment Rate Pre Covid and During Covid 
        2. Number of Employed People Pre Covid and During Covid from 2016-2021
        3. GDP Loss by Sector
        4. GDP Before vs During COVID
        5. Show Complete Raw Data
        6. Exit""")

        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                # Calculate average unemployment rates by state
                avg_data = df2.groupby('State')[['Unemployment_Rate_Before', 'Unemployment_Rate_During']].mean().reset_index()
                plt.figure(figsize=(12, 6))
                x = np.arange(len(avg_data['State']))
                width=0.35
                plt.bar(x - width/2, avg_data['Unemployment_Rate_Before'], width, label='Before')
                plt.bar(x + width/2, avg_data['Unemployment_Rate_During'], width, label='During')

                plt.xticks(x, avg_data['State'], rotation=45, ha='right')
                plt.ylabel('Average Unemployment Rate (%)')
                plt.title('Average Unemployment Rate Before and During COVID-19 by State')
                plt.legend()
                plt.tight_layout()
                plt.show()


            case 2:
                # Number of Employed People Pre Covid and During Covid from 2016-202
                plt.figure(figsize=(10, 5))
                plt.bar(df["Year"], df["Employed"], color='seagreen')
                plt.title("Number of Employed People in Rural Areas", fontsize=14)
                plt.xlabel("Year", fontsize=12)
                plt.ylabel("Employed (in Millions)", fontsize=12)
                plt.tight_layout()
                plt.show()

            case 3:
                sector_loss = df2.groupby("Sector")["GDP_Loss_Percent"].mean()

                plt.figure(figsize=(10,6))
                sns.barplot(x=sector_loss.values, y=sector_loss.index, palette="Reds_r")
                plt.xlabel("Average GDP Loss (in %)")
                plt.title("Average GDP Loss by Sector")
                plt.tight_layout()
                plt.show()

            case 4:
                sector_gdp = df2.groupby("Sector")[["GDP_Before_COVID", "GDP_During_COVID"]].mean()
                sector_gdp.plot(kind="bar", figsize=(12,6))
                plt.ylabel("GDP (in crores)")
                plt.title("GDP Before vs During COVID by Sector")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                
            
            case 5:
                print("Complete Raw Data: \n")
                print(df2)

            case 6:
                print("Exiting...")
                break
            case _ :
                print("Invalid Input . Try again")

def overall_analysis():
    df1=pd.read_csv("D:\kunjal garg\college\Python programming\Python Project\Latest Covid-19 India Status.csv")
    df2=pd.read_csv("D:\kunjal garg\college\Python programming\Python Project\india_gdp_loss_covid_simulated.csv")
    while True:
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + "     OVERALL ANALYSIS     ")
        print(Fore.CYAN + "=" * 40)
        print("""
        Enter Your Choices:-
        1. Population affected by Covid-19
        2. Relationship between GDP Loss and Health Index
        3. Overall Metric Data
        4. Policy Recommendations & Research Implications
        5. Linear Regression: Unemployment Before vs During COVID
        6. Linear Regression: % Population Affected vs Total Population
        7. Exit """)

        try:
            choice = int(input("Enter Your Choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case 1:
                print(""" 
Maharashtra reported the highest number of total cases and deaths, indicating both widespread infection and a significant fatality burden.
Kerala and Karnataka followed with substantial case counts but maintained relatively high recovery numbers, suggesting effective patient management. 
States like Uttar Pradesh and Tamil Nadu also recorded high infections with more balanced recovery-to-death ratios. 
In contrast, smaller states and union territories such as Sikkim, Mizoram, and Lakshadweep reported significantly lower cases and fatalities,
possibly due to geographic isolation and timely containment. 
High-density urban states like Maharashtra, Delhi, and Tamil Nadu contributed notably to the national death toll.
Meanwhile, states with high total cases but low death ratios (like Kerala and Telangana) reflected stronger clinical outcomes.
The consistently high recovery rates across many states—often exceeding 90%—point to efficient health responses, 
while discrepancies between total cases and discharges in some areas may hint at underreporting or delays in recovery updates.
Overall, the variation across regions reflects differences in healthcare access, reporting, and population dynamics during the pandemic.
                      """)
                # Calculate % of population affected
                df1['Population'] = df1['Population'].str.replace(',', '').astype(float)  # to convert string to numeric values 
                df1['% Population Affected'] = (df1['Total Cases'] / df1['Population']) * 100

                plt.figure(figsize=(12, 7))
                sns.regplot(data=df1, x='Population', y='% Population Affected', line_kws={'color': 'red'})
                for i in range(len(df1)):
                    plt.text(df1['Population'][i], df1['% Population Affected'][i], df1['State'][i], fontsize=6)
                plt.xlabel('Population')
                plt.ylabel("Percentage of Population Affected")
                plt.title('COVID-19 Impact: % Population Affected by State')
                plt.grid(True)
                plt.tight_layout()
                plt.show()


            case 3:
                covid_stats_df = pd.DataFrame({"Metric": ["Total COVID-19 Cases (Recorded)", 
                                                          "Total COVID-19 Deaths", "Case Fatality Rate (Approx.)", 
                                                          "Peak Daily Cases (April 2021)", "Peak Daily Deaths (Second Wave)", 
                                                          "Recovery Rate (2020)", "Recovery Rate (2021)", "Vaccination Start Date", 
                                                          "Highest Daily Cases Ever Recorded", "Most Affected Wave (by Cases)",
                                                            "Most Affected Wave (by Deaths)", 
                                                            "Lockdown Start Date", "India's Global Rank by Total Cases"], 

                                                            "Value": ["45,041,748", "533,623", "1.18%", "4,00,000+", "3,500+",
                                                                       "90%", "98%", "January 2021", "4,00,000+ (April 2021)", 
                                                                       "Second Wave (April–May 2021)", "Second Wave (April–May 2021)", 
                                                                        "25 March 2020", "3rd Highest "]})

                print(covid_stats_df)
                print("\n")
                print("""
India experienced one of the largest COVID-19 outbreaks globally, recording over 45 million confirmed cases and more than 533,000 deaths. 
The peak of the pandemic came during the second wave in April 2021, when daily cases crossed 4 lakh and deaths exceeded 3,500 per day.
 Despite these alarming numbers, India' s recovery rate improved significantly from 90 percent in 2020 to 98 percent in 2021, 
aided by a nationwide vaccination drive that began in January 2021. 
Covishield was the primary vaccine administered during the campaign.

To mitigate the crisis, the Government of India adopted a multi-pronged strategy. 
It ramped up healthcare infrastructure rapidly by setting up temporary hospitals and increasing ICU capacity. 
India became a key global player in vaccine manufacturing and distribution, supplying doses both domestically and internationally.
Aggressive testing and contact tracing efforts were implemented, while mass awareness campaigns were conducted through media channels to educate citizens on safety protocols. 
Financial relief was extended to vulnerable industries, and collaborative efforts with both ayurvedic and modern medical systems were promoted.
International cooperation and continuous monitoring enabled the country to respond dynamically to changing scenarios.
These combined efforts played a crucial role in controlling the spread and improving recovery outcomes across the nation.
                      """)

            case 2:
                print("""An analysis of the scatter plot depicting the relationship between the Health Index and GDP loss across Indian states reveals no strong linear correlation. 
The data points are widely dispersed, and the regression line remains relatively flat, indicating that states with better health infrastructure did not consistently 
experience less or more economic loss. 
This observation aligns with broader economic studies which suggest that while health infrastructure played a critical role in managing the pandemic, it was not the sole determinant of economic resilience.
Factors such as the structure of the state economy, the intensity and duration of lockdowns, digital adaptability, and interstate migration flows significantly influenced the economic impact. 
Consequently, some states with higher Health Index scores still faced substantial economic downturns, whereas others with lower scores did not experience proportionate GDP losses. 
This complex interplay highlights the need for multi-dimensional preparedness that extends beyond health metrics alone. \n""")
                plt.figure(figsize=(8,6))
                sns.regplot(data=df2, x="Health_Index", y="GDP_Loss_Percent")
                plt.xlabel("Health Index (Composite Score)")
                plt.ylabel("GDP Loss (%)")
                plt.title("GDP Loss vs Health Index with Regression Line")
                plt.grid(True)
                plt.tight_layout()
                plt.show()

            
            case 4:
                print("""
1. Strengthen Real-Time Health Surveillance
Governments should establish a nationwide integrated digital system for real-time monitoring of hospital admissions, ICU occupancy, and regional outbreaks to enable quicker and more localized responses.

2. Improve Health Infrastructure in Underserved Areas
Data showed significant disparities in healthcare access and hospital capacity across states. Investment should be prioritized in rural and northeastern regions with lower hospital bed and ICU availability.

3. Plan Targeted Vaccination Campaigns
While overall vaccination helped reduce cases, its impact varied across states. Researchers should study region-specific trends to design data-driven immunization campaigns in future outbreaks.

Develop Adaptive Economic Support Frameworks
State-level unemployment trends highlight the need for targeted economic relief mechanisms that can be activated rapidly during future waves or health crises.

6. Strengthen Collaboration Between Traditional & Modern Medicine
India's integrative approach (Ayurveda + modern medicine) opens opportunities for researchers to explore complementary treatment models and community trust-building strategies.

7. Formalize Post-Pandemic Review Mechanisms
Institutionalize review boards to evaluate pandemic responses state-wise to document lessons learned, prepare future playbooks, and support academic and policy research.
                      """)
            
            case 5:
                df = pd.read_csv("D:/kunjal garg/college/Python programming/Python Project/india_gdp_loss_covid_simulated.csv")
                df = df.dropna(subset=['Unemployment_Rate_Before', 'Unemployment_Rate_During'])
                X = df[['Unemployment_Rate_Before']]
                y = df['Unemployment_Rate_During']
                model = LinearRegression()
                model.fit(X, y)
                y_pred = model.predict(X)
                print("Slope:", model.coef_[0])
                print("Intercept:", model.intercept_)
                print("R² Score:", model.score(X, y))
                plt.figure(figsize=(8, 6))
                plt.scatter(X, y, color='blue', label='Actual')
                plt.plot(X, y_pred, color='red', linewidth=2, label='Regression Line')
                plt.xlabel("Unemployment Rate Before COVID")
                plt.ylabel("Unemployment Rate During COVID")
                plt.title("Linear Regression: Unemployment Before vs During COVID")
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()

            case 6:
                df = pd.read_csv("D:/kunjal garg/college/Python programming/Python Project/Latest Covid-19 India Status.csv")
                df['Population'] = df['Population'].str.replace(',', '').astype(float)
                df = df[df['Population'] > 0]
                df['% Affected'] = (df['Total Cases'] / df['Population']) * 100
                X = df[['Population']]
                y = df['% Affected']
                model = LinearRegression()
                model.fit(X, y)
                y_pred = model.predict(X)
                r2 = r2_score(y, y_pred)
                mse = mean_squared_error(y, y_pred)
                print("Slope:", model.coef_[0])
                print("Intercept:", model.intercept_)
                print("R² Score:", r2)
                print("Mean Squared Error:", mse)

                plt.figure(figsize=(10, 6))
                plt.scatter(df['Population'], df['% Affected'], color='blue', label='Actual')
                plt.plot(df['Population'], y_pred, color='red', label='Regression Line')
                plt.xlabel('Population')
                plt.ylabel('% of Population Affected')
                plt.title('% Population Affected vs Total Population (Linear Regression)')
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()
                print("""
The linear regression between total population and the percentage of population affected by COVID-19 reveals a weak positive correlation (R² ≈ 0.12). This indicates that more populous states did not consistently report a proportionally higher share of infections. Factors such as population density, public health measures, and testing rates likely played a larger role than absolute population in determining case spread.""")

            case 7:
                print("Exiting ....")
                break

            case _:
                print("Invalid Input . Try again")

# Asking for choices
while True:
    print("""
        What Analysis Do You Want To See?
        1. No. of Cases and Deaths
        2. Vaccination Data of India 
        3. Hospitals Data of India
        4. Impact On Economy
        5. Overall Analysis
        6. Exit Program""")

#Matching Choices
    try:
        choice = int(input("Enter your choice (1-5): "))
    except ValueError:
        print("Invalid input. ")
        
    match choice:
        case 1:
            no_of_cases_india()
        case 2:
            vaccination()
        case 3:
            hospitals()
        case 4:
            economy()
        case 5:
            overall_analysis()
        case 6:
            print("""Exiting...
Thank You
==================================================================================================================================================================================================== """)
            break
        case _:
            print("Invalid choice. Please try again.")
    




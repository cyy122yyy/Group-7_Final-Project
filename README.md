# Group-7_Final-Project
Our application consists of a dashboard for data visualization that tracks and analyzes crimes against women in India over a 21-year span (2001–2021). The dashboard's goal is to convert complicated crime statistics into clear, interactive visualizations that highlight geographic patterns, temporal trends, and comparative insights across various states and crime categories. This is driven by the need for data-driven policy creation in law enforcement. Law enforcement policymakers are the main target consumers since they need accurate, easily accessible data to guide resource allocation, decision-making, and evaluation of the efficacy of policies. Our program tackles the problems of detecting high-risk areas, comprehending the evolution of crime patterns over time, and assessing the effectiveness of prior actions by displaying crime data using interactive choropleth maps, trend line graphs, and comparative bar charts. This visualization solution enables policymakers to move beyond raw statistics to gain actionable insights that can help develop more effective strategies for preventing crimes against women and improving public safety across India.

**Project Team:** Shanaya Clysly D. Meimban and Cheska Ysabelle G. Young

**Setup Instructions:**
To run our Crimes Against Women in India visualization dashboard on your local machine, please follow these steps:

Download the required files:
1. CrimesOnWomenData.csv (crime statistics dataset)
2. IND_adm3.json (geographical boundary data for India)
3. mergedcrime_data.csv (pre-processed merged dataset)
4. crimes_on_women_in_india.py (main application file)

Create a new folder on your computer and place all downloaded files in this folder.

Install the required Python modules by opening your terminal/command prompt and running:
pip install pandas plotly dash numpy urllib3

Navigate to your project folder:
**For Windows:**
Press Win+R, type cmd, and press Enter
Type: cd "path\to\your\folder" (replace with your actual folder path)

**For Mac/Linux:**
Open Terminal
Type: cd "path/to/your/folder" (replace with your actual folder path)

Launch the application by running:
python crimes_on_women_in_india.py

Once the application starts, you'll see a message with a local URL (typically http://127.0.0.1:8050/). Click this link or copy it into your web browser to access the dashboard.
The visualization dashboard should now be running in your browser, allowing you to explore crime data through interactive maps and graphs.

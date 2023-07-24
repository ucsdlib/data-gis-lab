import requests
import pandas as pd
link = "https://opendata.sandag.org/api/views/inmb-xi9i/rows.csv?accessType=DOWNLOAD"
r = requests.get(link)
if r.status_code == 200:
    url_content = r.content
    with open("arjis_data.csv", "wb") as csv_file:
        csv_file.write(url_content)
crime = pd.read_csv("arjis_data.csv")
def process_df(input_df: pd.DataFrame) -> pd.DataFrame:
    cols_reordered = ['Crime Category','Agency','Charge Description','Date','Year','Month', 'State','Block Address','zipcode','Community', 'City']
    return(input_df
            .assign(
            State='CALIFORNIA',
            City=input_df["Community"],
            zipcode=input_df['ZIP Code'].astype("Int32"),
            Date=pd.to_datetime(input_df['Date']),
            Year=lambda df_: df_["Date"].dt.year,
            Month=lambda df_: df_['Date'].dt.month,
            )
            .drop(columns=["ZIP Code"])
            [cols_reordered]
    )
df2 = process_df(crime)
df2.to_csv("arjis_data.csv", index = False)

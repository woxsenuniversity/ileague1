import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import pytz
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import uuid
from datetime import datetime, time

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "14afCQaLe9KOHw5KPQupqWwCQJUmthuUPg_Tvs4jbhXY"
SHEET_NAME = "booked_slots"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

def header2(url): 
    st.markdown(f'<p style="color:#1261A0;font-size:40px;border-radius:2%;"><center><strong>{url}</strong></center></p>', unsafe_allow_html=True)

def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    values = (
        gsheet_connector.values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
            body=dict(values=row),
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )

@st.cache_resource()
def connect_to_gsheet():
    cred = {
  "type": "service_account",
  "project_id": "focus-sequencer-335515",
  "private_key_id": "4ad2d73126cd5338829bcb1650707c5ab5cb3051",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC05g6fDjKWRBCq\ndbnaUTYTpJu9uKq7b7ug9a+x84tDYHyfVo8+JEDz7EZd9gZGf+jx2QxQsJxqxp8e\ngO0fUZ6M9/1YdMICEqoHSUi/Em0d7bAGo8LSbCzn0TvK9zk2bhW4iKupWBJ0henB\nPbKLRVxUzmEcdhFqlziK1+z9YrmnKdBeXNTaMDJdYFjLskOhZ2Nos9h/WgEytlz/\n8tc9uxLrp6fkInK6g4eSm3OsI0w3YZfcN7/THrxRGLT9cpOUwPdIDGVFQJjJ1++k\nW2vWH4R67/YPEWoBMAuVTk4N7GSjSJvAS0P3J7q1u75S48npji/f3wGygr4xosHu\nlb4WnkjHAgMBAAECggEAL2wqBBdoOo1QYydml+13RDIAY/2PwIBbiygtLXTfmsOm\nF+1Msuk1H9zeW459+ahZjGEugc6yyqkUGJ6Kyw2OB32RbEl7fKig6zUSfYiak2B2\np17x2VDjesgWqTAjTvoP9qbZfZTpjaN3cqG2dx0xRcgunBP1n+BRwdA2P/zMF56E\nRWjnQk9EAzThfQ2v5p9I1WIaiwP06VRyEiUsI1+6S0qiPBhpA+GZY0yAQMO4wFg/\n8Q3k8rCcQivQIj0iaYnckEUsSNsa3QCjKlWa+1gHkqlfNEctWaqLVGpMdDHdz9cN\nVc+5DRIF6SPQvOufv5LrvVJyA4vIyxygiv+yptzDYQKBgQD1TzlLfgOrhv7OO6Xv\nDHA1VwVBhcTXuFgRupOLgf1Lturiq0OIDvRwxFvXHnXC2nr0U3raC2O1jS91WNhl\nnR0zmBd1EEv/8gzkP6em9F6xB7hSiNu+3HCorR0QarV+bg2CrHlszA54+Mfe4pvl\n7vL7zzyPfA2OOfqjkcvKf50r5wKBgQC8yD01Mr4OY4OG0thSC0+X6b/Q4meekBDV\nrIpcoUW6lbvn4KgvYUcV1rD7agseoPlwab1WTQm9XFQU2udPcko/WHbdB4KedXiv\nsgZhfPFlURiDbRTe0FKB8/oQ1N2wbbTJ5ciLaMVtHIHEBoDgG/lCQvshLQVvZp9t\n4pmp8VNgIQKBgQCCVl6l2sWObIKUByNKGPzBioPzZWTKDVtVyCE+3Yk8omq4lrCh\n6Pg9tkbpzHhbWIQ9ruE2WxjWTLarjdIkY08xq5zDCS6oRe5Nk/i6/1oUi3qG98px\n5WRCawBnSZs3Grg49vTpNp517hEcPqEAkW4vFtQhlJMLP4kJQZza8eULfwKBgQCZ\n8eRP9HAeBbKlCF1VElo2tGwyZ9495JeF120BOpZFIIOaBI7CDF7OhUPP0dr9gCHJ\nNMEsligCHj+Gvjfwhm/blkVf2xb+JydihxdC+oNTrr0Bt7tUM6eEx7M9dIjPrbbH\nCbXvUWHlp2B+vRrtJoKuMTbfB/qtrI8IKchLWDs4YQKBgQDJ5ySsyJewEXbefo/l\nGJBkV1RZSSA/qkmgQOgJWAjgteKxLqgahGfZFD+lD0c0Ot66oper1rOTU2Bgug+V\nl2jkowt1yNs4AVcbN8Q721kycWj7hiNpqrmWXw+MIfiAiL5qVHsbHnJfqxtnAyiu\n6ZfmW3PboX9B5usytdfzww4qBA==\n-----END PRIVATE KEY-----\n",
  "client_email": "access-drive@focus-sequencer-335515.iam.gserviceaccount.com",
  "client_id": "109156515093815992059",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/access-drive%40focus-sequencer-335515.iam.gserviceaccount.com"
}

    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(cred,
        scopes=[SCOPE],
    )

    service = build("sheets", "v4", credentials=credentials)
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


# def load_bookings_from_csv():
#     bookings = []
#     with open('bookings.csv', 'r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             bookings.append(row)
#     return bookings


# def process_email_response(response):
#     if "accept" in response.lower():
#         return "Accepted"
#     elif "decline" in response.lower():
#         return "Declined"
#     else:
#         return "Unknown"

# def update_csv_with_response(response, data):
#     with open('responses.csv', 'a', newline='') as csvfile:
#         fieldnames = ['Name', 'Sport', 'Slot', 'Response']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writerow({'Name': data['name'], 'Sport': data['sport'], 'Slot': data['slot'], 'Response': response})



#def send_email_notification(name, mail_id, sport_type, slot_time,sport_type1,slot_time1):
    # Email configuration
    
    
    # EMAIL_HOST = 'smtp.gmail.com'
    # EMAIL_PORT = 587
    # EMAIL_HOST_USER = 'woxsenlab@gmail.com'
    # EMAIL_HOST_PASSWORD = 'tyddzpgkjhsgpeid'
    # EMAIL_USE_TLS = True
    
     
    # smtp_server = "smtp.gmail.com"
    # smtp_port = 587
    # smtp_username = "woxsenlab@gmail.com"
    # smtp_password = "gdjxsjefnyxyvkcn"
    # recipient_email = "sports@woxsen.edu.in"

    # # Email content
    
    

    # subject = f"Slot Approval: {name} has booked a slot"
    # body = f"Dear Deepanshi Gaur,\n\n{name} has booked a slot for {sport_type} or {sport_type1} at {slot_time} or {slot_time1}. Please review and approve the slot.\n\nBest regards,\nSports"

    # # Create MIMEText and MIMEMultipart objects
    # msg = MIMEMultipart()
    # msg['From'] = smtp_username
    # msg['To'] = recipient_email
    # msg['Subject'] = subject
    # msg.attach(MIMEText(body, 'plain'))
        
    # # Connect to the SMTP server and send email
    # try:
    #     server = smtplib.SMTP(smtp_server, smtp_port)
    #     server.starttls()
    #     server.login(smtp_username, smtp_password)
    #     server.sendmail(smtp_username, recipient_email, msg.as_string())
    #     st.success("Email notification sent successfully.")
        
    # except Exception as e:
    #     st.error(f"Failed to send email notification: {e}")
    # finally:
    #     server.quit()


# @st.cache+
# def handle_approval_decline_action(action, booking_id):
#     bookings = load_bookings_from_csv()
#     for booking in bookings:
#         if booking['id'] == booking_id:
#             booking['status'] = action
#             save_bookings_to_csv(bookings)
#             return True
#     return False

# Endpoint for approving a booking
# if st.experimental_get_query_params().get('action', [None])[0] == 'approve':
#     booking_id = st.experimental_get_query_params().get('booking_id', [None])[0]
#     if booking_id:
#         if handle_approval_decline_action("approved", booking_id):
#             st.success("Booking approved!")
#         else:
#             st.error("Booking not found.")

# # Endpoint for declining a booking
# if st.experimental_get_query_params().get('action', [None])[0] == 'decline':
#     booking_id = st.experimental_get_query_params().get('booking_id', [None])[0]
#     if booking_id:
#         if handle_approval_decline_action("declined", booking_id):
#             st.error("Booking declined.")
#         else:
#             st.error("Booking not found.")simulate_email_responses() 
  
def indoor(gsheet_connector,name,mail_id,contact):
    sports = ["Select Your Ground","Table-Tennis 1", "Table-Tennis 2", "Table-Tennis 3","Badminton court-1","Badminton court-2","Badminton court-3","Badminton court-4","Badminton court-5","Badminton court-6","Badminton court-7","Badminton court-8","Squash-1","Squash-2"]
    
    sport_type1 = st.selectbox("Indoor",sports)
    if sport_type1 != "Select Your Ground":

                        df = get_data(gsheet_connector)
                        time_df = df[df["Venue"] == sport_type1]

                        booked = list(time_df["Slot Timing"])

                        all_slots = []

                        UTC = pytz.utc
                        IST = pytz.timezone('Asia/Kolkata')

                        hr = str(datetime.now(IST).time())

                        if int(hr[0:2]) == 23:
                            header2("Booking opens at 12AM")

                        else:
                            # Generate time slots from 5 AM to 11 AM
                            for i in range(5, 8):
                                x = "{:02d}:00 - {:02d}:00".format(i, i + 1)
                                all_slots.append(x)

                            new_slots = ["-"]

                            for s in all_slots:
                                if s not in booked:
                                    new_slots.append(s)

                            #del_slots = []
                            
                            # Generate time slots from 4 PM to 11 PM
                            for i in range(16, 23):
                                x = "{:02d}:00 - {:02d}:00".format(i, i + 1)
                                all_slots.append(x)

                            new_slots = ["-"]

                            for s in all_slots:
                                if s not in booked:
                                    new_slots.append(s)

                #if len(new_slots) == 1:
                # header2("No Slots Available")

                            # for i in range(16, 24):
                            #     x = "{:02d}:00 - {:02d}:00".format(i, i + 1)
                            #     del_slots.append(x)

                            # for i in del_slots:
                            #     if i in new_slots:
                            #         new_slots.remove(i)


                            if len(new_slots) == 1:
                                header2("No Slots Available")

                            else:
                                slot_time1 = st.selectbox("Choose your time slot", new_slots)

                                if slot_time1 != "-":
                                    if st.button("Submit"):
                                        add_row_to_gsheet(
                                            gsheet_connector, [[name, mail_id, contact, sport_type1, slot_time1]]
                                        )
                                        header2("Your slot has been booked!")
                                        st.success(" **Take a Screenshot of the slot details** ")
                                        st.write("**Name:**",name)
                                        st.write("**Venue:**", sport_type1)
                                        st.write("**Slot Time:**", slot_time1)
                                        
                                        
                                        send_email_notification(name, mail_id,"","", sport_type1, slot_time1)
                            st.button("refresh", key="refresh_button")
            
                



def outdoor(gsheet_connector, name,mail_id,contact):
    sports = ["Select Your Ground","Football pitch 1","Football pitch 2","Box Cricket","Basketball",
                          "Sand Volleyball","Volleyball Court 1","Volleyball Court 2",
                          "Lawn Tennis Court 1","Lawn Tennis Court 2","Kabaddi","Golf","Croquet"]
    sport_type = st.selectbox("Outdoor",sports)
    if sport_type != "Select Your Ground":

                    df = get_data(gsheet_connector)
                    time_df = df[df["Venue"] == sport_type]

                    booked = list(time_df["Slot Timing"])

                    all_slots = []

                    UTC = pytz.utc
                    IST = pytz.timezone('Asia/Kolkata')

                    hr = str(datetime.now(IST).time())

                    if int(hr[0:2]) == 23:
                        header2("Booking opens at 12AM")

                    else:
                        for i in range(int(hr[0:2]),22):
                           x = "{}:00 - {}:00".format(i+1,i+2)
                           all_slots.append(x)

                        new_slots = ["-"]

                        for s in all_slots:
                            if s not in booked:
                                new_slots.append(s)

                        del_slots = []

                        for i in range(0,6):
                            x = "{}:00 - {}:00".format(i,i+1)
                            del_slots.append(x)

                        for i in del_slots:
                            if i in new_slots:
                                new_slots.remove(i)

                        if len(new_slots) == 1:
                            header2("No Slots Available")

                        else:
                            slot_time = st.selectbox("Choose your time slot", new_slots)

                            if slot_time != "-":
                                if st.button("Submit"):
                                    add_row_to_gsheet(
                                        gsheet_connector, [[name, mail_id, contact, sport_type, slot_time]]
                                    )
                                    header2("Your slot has been booked!")
                                    st.success(" **Take a Screenshot of the slot details** ")
                                    st.write("**Name:**",name)
                                    st.write("**Venue:**", sport_type)
                                    st.write("**Slot Time:**", slot_time)
                                    
                                    send_email_notification(name, mail_id,sport_type, slot_time,"","")
                            st.button("refresh")





def slot_main():

    col1, col2, col3 = st.columns([0.4,1,0.2])
    with col2:
        st.image("league.jpeg",width = 300)

    col1, col2, col3 = st.columns([0.2,2,0.2])

    with col2:
        st.title("Slot Booking for The League")

    gsheet_connector = connect_to_gsheet()
    
    UTC = pytz.utc
    IST = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(IST).time()
    
           
    hr = str(datetime.now(IST).time())
    
    if int(hr[0:2]) == 22 or int(hr[0:2]) == 23:
        header2("Booking opens at 12AM")

    else:

        mail_id = st.text_input("Enter your woxsen Mail ID")

        if len(mail_id) == 0 or "woxsen.edu.in" in mail_id:

            name = st.text_input("Enter your Name")
            contact = st.text_input("Enter your contact")
            games = ["Select your Venue","Indoor", "Outdoor"]
            venue = st.selectbox("Venue",games)
            
            if len(name) != 0 and len(contact) != 0 and len(mail_id) != 0 and venue =="Indoor":
                indoor(gsheet_connector, name,mail_id,contact)
               
            elif len(name) != 0 and len(contact) != 0 and len(mail_id) != 0 and venue =="Outdoor":
                outdoor(gsheet_connector, name,mail_id,contact)
        else:
            st.error("You are not allowed to book a slot. Please enter woxsen mail ID")  





if __name__ == "__main__":
    st.set_page_config(page_title="The League: Slot Booking", layout="centered")
   
    slot_main()





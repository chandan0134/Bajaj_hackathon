import pandas as pd
import re
from datetime import datetime



data = pd.read_json('data.json')
# print(data["phoneNumber","appointmentId" ,"patientDetails"])


selected_columns = data['appointmentId', 'phoneNumber', 'patientDetails.firstName', 'patientDetails.lastName', 'patientDetails.gender', 'patientDetails.birthDate', 'consultationData.medicines']


selected_columns['patientDetails.gender'] = selected_columns['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')
#Q2
selected_columns['fullName'] = selected_columns['patientDetails.firstName'] + ' ' + selected_columns['patientDetails.lastName']

#Q1
selected_columns = selected_columns.rename(columns={'patientDetails.birthDate': 'DOB'})


#Q3
def is_valid_mobile(phone_number):
    pattern = r'^(\+|0)?91[6-9]\d{9}$'
    return bool(re.match(pattern, str(phone_number)))

selected_columns['isValidMobile'] = selected_columns['phoneNumber'].apply(is_valid_mobile)




#Q4
def generate_hash(phone_number):
    return str(abs(hash(phone_number)))[:10] if pd.notnull(phone_number) else None

selected_columns['phoneNumberHash'] = selected_columns['phoneNumber'].apply(generate_hash)

print(selected_columns)

#q5

def calculate_age(dob):
    if pd.isnull(dob):
        return None
    else:
        dob = pd.to_datetime(dob)
        now = datetime.now()
        age = now.year - dob.year
        if now.month < dob.month or (now.month == dob.month and now.day < dob.day):
            age -= 1
        return age

selected_columns['Age'] = selected_columns['DOB'].apply(calculate_age)




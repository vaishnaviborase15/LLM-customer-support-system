import re

def convert_to_hours(time_str):
    try:
        if 'hour' in str(time_str):
            return float(re.findall(r'\d+', str(time_str))[0])
        elif 'minute' in str(time_str):
            return float(re.findall(r'\d+', str(time_str))[0]) / 60
        else:
            return float(time_str)
    except:
        return 0

def preprocess(df):
    df['First_Response_Hours'] = df['First_Response_Time'].apply(convert_to_hours)
    df['Resolution_Hours'] = df['Time_to_Resolution'].apply(convert_to_hours)
    return df
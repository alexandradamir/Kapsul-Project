import pandas as pd

################################################ id_column ###########################################################
#check for _id column and add id column if doesn't exist
def id_column(data):
    for c in data.columns:
        if all(data[c]== list( range(1, 1 + len(data)))):
            if c!= '_id':
                data.rename(columns = {c:'_id'}, inplace = True)
        elif all(data[c]== list( range(0, len(data)))):
            data.drop(c, inplace=True, axis=1)
        elif '_id' not in data.columns:
            data.insert(0, '_id', range(1, 1 + len(data)))
        
############################################### columns_name #####################################################
def columns_name(data):
    #lowercase columns name
    if any(data.columns.str.find('İ')!= -1):
        data.columns=data.columns.str.replace('İ','I') #I added this because "İ" doesn't lowercase well
        data.columns=data.columns.str.lower()
    else: data.columns=data.columns.str.lower()

    #change turkish_letters
    t_letters=['ı', 'ğ', 'ü', 'ş', 'ö', 'ç']

    for x in t_letters:
        if any(data.columns.str.find(x)!= -1):
            if x=='ı':
                data.columns = data.columns.str.replace('ı','i')
            if x=="ğ":
                data.columns = data.columns.str.replace('ğ','g')
            if x=='ü':
                data.columns = data.columns.str.replace('ü','u')
            if x=='ş':
                data.columns = data.columns.str.replace('ş','s')
            if x=='ö':
                data.columns = data.columns.str.replace('ö','o')
            if x=='ç':
                data.columns = data.columns.str.replace('ç','c')
    # replace spaces with underscores 
    # and delete if spaces are at the beginning or end of the name or if there are several spaces next to each other            
    data.columns=data.columns.str.replace('\W',' ').str.replace(r'^\s+|\s+$','').str.replace(r'\s+','_', regex=True)

########################################## numeric_format #############################################################
def numeric_format(data):
    import re
    import numpy as np
    #list for the coord
    date_coord=[]
    for c in data:
        for i in data[c]:
            #check if the value contains at least 60% numbers
            if 100 * ( len(re.findall('\d', str(i))) / len(str(i))) > 60:
                #go through the non-number columns
                if np.issubdtype(data[c].dtype, np.number)==False:
                    #store the columns with geographic coordinates separately
                    if 100 * ( len([x for x in data[c] if re.match('\A3\d\\.{1}', str(x))]) / len(data[c]) ) > 50:
                        if c not in date_coord : date_coord.append(c)        
                    #check for the columns that could be a date
                    elif re.findall('\\.\d{2}\\.\d{2}', str(i)):
                        if c not in date_coord : date_coord.append(c)
                    #check if the values have both comma and point
                    elif all(x in str(i) for x in [',','.']):
                        #check the format of the number and make the necessary changes
                        if any(data[c].str.find(',') > data[c].str.find('.')):
                            data[c]=data[c].str.replace('.','').str.replace(',','.')
                            data[c]=pd.to_numeric(data[c], errors='coerce')
                        elif any(data[c].str.find(',') < data[c].str.find('.')):
                            data[c]=data[c].str.replace(',','')
                            data[c]=pd.to_numeric(data[c], errors='coerce')
                    #check if thousands separator is comma and make the necessary changes
                    elif re.search(',\d{3}', str(i)) and len(str(i))>=5:
                        data[c]=data[c].str.replace(',','')
                        data[c]=pd.to_numeric(data[c], errors='coerce')
                    #check if thousands separator is point and make the necessary changes
                    elif re.search('\\.\d{3}', str(i)) and len(str(i))>=5:
                        data[c]=data[c].str.replace('.','')
                        data[c]=pd.to_numeric(data[c], errors='coerce')
                    #check if thousands separator is space and make the necessary changes
                    elif re.search(' \d{3}', str(i)) and len(str(i))>=5:
                        data[c]=data[c].str.replace(' ','')
                        data[c]=pd.to_numeric(data[c], errors='coerce')
                    #check if decimal separator is comma and make the necessary changes
                    elif re.search(',\d', str(i)) and len(str(i))>=5:
                        data[c]=data[c].str.replace(',','.')
                        data[c]=pd.to_numeric(data[c], errors='coerce')
                    #check if decimal separator is point and convert column type to number
                    elif re.search('\\.\d', str(i)) and len(str(i))>=5:
                        data[c]=pd.to_numeric(data[c], errors='coerce')

############################################# date_format ###########################################################
def date_format(data):
    import re
    from datetime import datetime
    for c in data:
        #check if the column type is object, otherwise .str does not work
        if data[c].dtypes=='object':
            #check for a 4-digit (year) number starting with 20 or 19 at the beginning or end of the string
            if all(data[c].str.contains('(^19|20\d{2}|19|20\d{2}$)')):
                #replace any separator with "-"
                data[c]=data[c].str.replace('[^0-9a-zA-Z\s:]', '-', regex=True)
                #store the number next to the year to check if it is day or month
                if all(data[c].str.contains('(\d?\d-\d{4})')):
                    x=pd.to_numeric(pd.DataFrame(data[c].str.findall('\d?\d-\d{4}'))[c].str[0].str.replace('-\d{4}','').unique())
                elif all(data[c].str.contains('(\d{4}-\d?\d)')):
                    x=pd.to_numeric(pd.DataFrame(data[c].str.findall('\d{4}-\d?\d'))[c].str[0].str.replace('\d{4}-','').unique())
                #check if the number is greater than or equal to 12 (month)
                if len(x)!= 0 and all(y <= 12 for y in x):
                    #check if the year is at the end
                    if any(data[c].str.contains('(-\d{4})')):
                        #check if the column does not contain ":" (hour)
                        if not all(data[c].str.contains('(\d:\d?\d)')):
                            #check if the date also includes the day and chose de format accordingly
                            if not all(data[c].str.contains('(\d?\d-\d?\d-\d{4})')):
                                data[c] = pd.to_datetime(data[c],format="%m-%Y", errors='coerce')
                            else:
                                data[c] = pd.to_datetime(data[c],format="%d-%m-%Y", errors='coerce')
                        #check if the date includes the hour
                        elif any(data[c].str.contains('(\d:\d{2})')):
                            #store the hour to check the format
                            y=pd.to_numeric(pd.DataFrame(data[c].str.findall('\s\d?\d:'))[c].str[0].str.replace('[ :]','').unique())
                            if len(y)!= 0 and all(z <= 12 for z in y) and any(data[c].str.contains('([a-zA-Z]{2})')):
                                #check if the time also contains the seconds
                                if any(data[c].str.contains('(:\d{2}:)')):
                                    data[c] = pd.to_datetime(data[c],format="%d-%m-%Y %I:%M:%S %p", errors='coerce')
                                else:
                                    data[c] = pd.to_datetime(data[c],format="%d-%m-%Y %I:%M %p", errors='coerce')
                            elif len(y)!= 0 and all(z <= 24 for z in y):
                                #check if the time also contains the seconds
                                if any(data[c].str.contains('(:\d{2}:)')):
                                    data[c] = pd.to_datetime(data[c],format="%d-%m-%Y %H:%M:%S", errors='coerce')
                                else: 
                                    data[c] = pd.to_datetime(data[c],format="%d-%m-%Y %H:%M", errors='coerce')
                    #all the above variants can exist in this case as well
                    #check if the year is at the beginning
                    elif any(data[c].str.contains('(\d{4}-)')):
                        #check if the column does not contain ":" (hour)
                        if not all(data[c].str.contains('(\d:\d?\d)')):
                            #check if the date also includes the day and chose de format accordingly
                            if not all(data[c].str.contains('(\d{4}-\d?\d-\d?\d)')):
                                data[c] = pd.to_datetime(data[c],format="%Y-%m", errors='coerce')
                            else:
                                data[c] = pd.to_datetime(data[c], format="%Y-%m-%d", errors='coerce')
                #check if the number is greater than or equal to 31 (day)
                elif len(x)!= 0 and all(y <=31 for y in x):
                    #check if the year is at the end
                    if any(data[c].str.contains('(-\d{4})')):
                        #check if the column does not contain ":" (hour)
                        if not all(data[c].str.contains('(\d:\d?\d)')):
                            #check if the date also includes the month and chose de format accordingly
                            if not all(data[c].str.contains('(\d?\d-\d?\d-\d{4})')):
                                data[c] = pd.to_datetime(data[c],format="%d-%Y", errors='coerce')
                            else:
                                data[c] = pd.to_datetime(data[c],format="%m-%d-%Y", errors='coerce')
                        #check if the date includes the hour
                        elif any(data[c].str.contains('(\d:\d{2})')):
                            #store the hour to check the format
                            y=pd.to_numeric(pd.DataFrame(data[c].str.findall('\s\\d?\d:'))[c].str[0].str.replace('[ :]','').unique())
                            if len(y)!= 0 and all(z <= 12 for z in y) and any(data[c].str.contains('([a-zA-Z]{2})')):
                                #check if the time also contains the seconds
                                if any(data[c].str.contains('(:\d{2}:)')):
                                    data[c] = pd.to_datetime(data[c],format="%m-%d-%Y %I:%M:%S %p", errors='coerce')
                                else:
                                    data[c] = pd.to_datetime(data[c],format="%m-%d-%Y %I:%M %p", errors='coerce')
                            elif len(y)!= 0 and all(z <= 24 for z in y):
                                #check if the time also contains the seconds
                                if any(data[c].str.contains('(:\d{2}:)')):
                                    data[c] = pd.to_datetime(data[c],format="%m-%d-%Y %H:%M:%S", errors='coerce')
                                else: 
                                    data[c] = pd.to_datetime(data[c],format="%m-%d-%Y %H:%M", errors='coerce')
                    #all the above variants can exist in this case as well
                    #check if the year is at the beginning
                    elif any(data[c].str.contains('(\d{4}-)')):
                        #check if the column does not contain ":" (hour)
                        if not all(data[c].str.contains('(\d:\d?\d)')):
                            #check if the date also includes the day and chose de format accordingly
                            if not all(data[c].str.contains('(\d{4}-\d?\d-\d?\d)')):
                                data[c] = pd.to_datetime(data[c],format="%Y-%d", errors='coerce')
                            else:
                                data[c] = pd.to_datetime(data[c], format="%Y-%d-%m", errors='coerce')
                #the year version with 2 digits, month and day can also be added
                #the version with month in letters and year with 4 digits can also be added
            #check if there are dates with abbreviated month and 2-digit year
            elif all(data[c].str.contains('([a-zA-Z]{3}[^0-9a-zA-Z]\d{2})')):
                #replace any separator with "-"
                data[c]=data[c].str.replace('[^0-9a-zA-Z:]', '-', regex=True)
                #store the number to check if it is year or month
                z=pd.to_numeric(pd.DataFrame(data[c].str.findall('\d{2}'))[c].str[0].unique())
                if all(i + 2000 <= datetime.now().year for i in z):
                    data[c] = pd.to_datetime(data[c],format="%b-%y", errors='coerce')

def cleaning_data(data):
    id_column(data)
    columns_name(data)
    date_format(data)
    numeric_format(data)

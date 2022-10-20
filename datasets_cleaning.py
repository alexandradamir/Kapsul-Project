
import pandas as pd

bosna= pd.read_csv('/workspace/project/67_202107_havakalitesibosna.csv', sep=";", encoding= 'ISO8859-9', skiprows=1)
selcuklu=pd.read_csv('/workspace/project/77_202106_havakalitesiselcuklu.csv', sep=";", encoding= 'ISO8859-9', skiprows=1)

#store the datasets name
var={'bosna':bosna, 'selcuklu':selcuklu}

#rename the date column for all datasets
def clean_data(data):
    data.rename(columns={data.columns[0]: 'date'}, inplace=True)
    cleaning_data(data)

#apply the cleaning function I developed (see 'all_formating' file)
for c in var:
    if isinstance(var[c], pd.DataFrame):
        clean_data(var[c])

#check if the transformations were done correctly
[var[item].dtypes for item in var]

#save the datasets in csv format
for x in var:
    print(var[x])
    var[x].to_csv('/workspace/project/'+x+'.csv', index=False)

#import the stations location dataset
data= pd.read_csv('/workspace/project/23_202108_havaistasyonkonum.csv', sep=";", encoding= 'ISO8859-9', )

#convert the longitude and latitude to the correct format
data['ENLEM']=data['ENLEM'].str.rsplit(pat='.', n=1, expand=True).astype(str).agg(''.join, axis=1)
data['BOYLAM']=data['BOYLAM'].str.rsplit(pat='.', n=1, expand=True).astype(str).agg(''.join, axis=1)
#delete empty lines
data=data[:10]

data['ENLEM']=pd.to_numeric(data['ENLEM'])
data['BOYLAM']=pd.to_numeric(data['BOYLAM'])

#lowercase stations name
if any(data.ISTASYON_ADI.str.find('İ')!= -1):
    data.ISTASYON_ADI=data.ISTASYON_ADI.str.replace('İ','I') #I added this because "İ" doesn't lowercase well
    data.ISTASYON_ADI=data.ISTASYON_ADI.str.lower()
else: data.ISTASYON_ADI=data.ISTASYON_ADI.str.lower()

#change turkish_letters in stations name
t_letters=['ı', 'ğ', 'ü', 'ş', 'ö', 'ç']

for x in t_letters:
    if any(data.ISTASYON_ADI.str.find(x)!= -1):
        if x=='ı':
            data.ISTASYON_ADI = data.ISTASYON_ADI.str.replace('ı','i')
        if x=="ğ":
            data.ISTASYON_ADI = data.ISTASYON_ADI.str.replace('ğ','g')
        if x=='ü':
            data.ISTASYON_ADI = data.ISTASYON_ADI.str.replace('ü','u')
        if x=='ş':
            data.ISTASYON_ADI = data.ISTASYON_ADI.str.replace('ş','s')
        if x=='ö':
            data.ISTASYON_ADI = data.ISTASYON_ADI.str.replace('ö','o')
        if x=='ç':
            data.ISTASYON_ADI = data.ISTASYON_ADI.str.replace('ç','c')
# optional code
# replace spaces with underscores             
data.ISTASYON_ADI=data.ISTASYON_ADI.str.replace('\W',' ').str.replace(r'^\s+|\s+$','').str.replace(r'\s+','_', regex=True).str.replace('_istasyonu','', regex=True)

#save new dataset
data.to_csv('/workspace/project/23_202108_havaistasyonkonum.csv', index=False)

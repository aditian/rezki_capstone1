import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def load_telco():
    # Read data
    telco = pd.read_csv('data/telcochurn.csv')
    
    # Adjust dtypes
    catcol = telco.select_dtypes('object').columns
    telco[catcol] = telco[catcol].apply(lambda x: x.astype('category'))
    
    # Tenure Months to grouping categories
    def grouping_tenure(telco) :
        if telco["tenure_months"] <= 12 :
            return "< 1 Year"
        elif (telco["tenure_months"] > 12) & (telco["tenure_months"] <= 24 ):
            return "1-2 Year"
        elif (telco["tenure_months"] > 24) & (telco["tenure_months"] <= 48) :
            return "2-4 Year"
        elif (telco["tenure_months"] > 48) & (telco["tenure_months"] <= 60) :
            return "4-5 Year"
        else:
            return "> 5 Year"

    telco["tenure_group"] = telco.apply(lambda telco: grouping_tenure(telco), axis = 1) 

    # Adjust category order
    tenure_group = ["< 1 Year", "1-2 Year", "2-4 Year", "4-5 Year", "> 5 Year"]
    telco["tenure_group"] = pd.Categorical(telco["tenure_group"], categories = tenure_group, ordered=True)
    
    return(telco)

def table_churn(data):
    table = pd.crosstab(
        data['churn_label'],
        columns = 'percent',
        normalize = True
    )*100
    return(table)

def plot_phone(data):
    
    # ---- Phone Service Customer

    phone=pd.crosstab(
        data['phone_service'],
        columns =data['churn_label'],
        normalize=True
    )*100
    
    ax = phone.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Phone Service Customer')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_internet(data):

    # ---- Internet Service Customer

    internet=pd.crosstab(
        data['internet_service'],
        columns =data['churn_label'],
        normalize=True
    )*100
    
    ax = internet.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Internet Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_churn(data):
    
    # ---- Churn Rate by Tenure Group

    tenure=pd.crosstab(
        data['tenure_group'],
        columns =data['churn_label'],
        normalize=True
    ).round(4)*100
    
    ax = tenure.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_cltv(data):

    # ---- Average Lifetime Value by Tenure

    cltv=pd.crosstab(
        data['tenure_months'],
        columns = data['churn_label'],
        values = data['cltv'],
        aggfunc= 'mean'
    )
       
    ax = cltv.plot(color=['#333333','#b3b3b3'], figsize=(8, 6),style = '.--')

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.title('Average Lifetime Value by Tenure')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_demographic_churn(data):
    
    # ---- Churn Rate by Demographic
    demographic_churn=pd.crosstab(
        index=[data['gender'],data['senior_citizen'],data['dependents']],
        columns =data['churn_label'],
        normalize=True
    )*100

    ax = demographic_churn.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize=(10, 6),stacked=True)
    

    # Plot Configuration
    label=['Single Adult Woman', 'Adult Woman w/ Family', 'Single Senior Woman', 'Senior Woman w/ Family','Single Adult Man', 'Adult Man w/ Family', 'Single Senior Man', 'Senior Man w/ Family']
    
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.axes().get_yaxis().set_label_text('demographic')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Customer Demographic')
    ax.set_yticklabels(label)
    plt.grid()
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_demographic_cltv(data):
    
    # ---- Churn Rate by Demographic
    demographic_cltv=pd.crosstab(
        index=[data['gender'],data['senior_citizen'],data['dependents']],
        columns ='',
        values=data['cltv'],
        aggfunc='mean'
    )

    ax = demographic_cltv.plot(kind = 'barh', color=['#c34454'], figsize=(10, 6))
    
    # Plot Configuration
    label=['Single Adult Woman', 'Adult Woman w/ Family', 'Single Senior Woman', 'Senior Woman w/ Family','Single Adult Man', 'Adult Man w/ Family', 'Single Senior Man', 'Senior Man w/ Family']
    
    plt.axes().get_xaxis().set_label_text('')
    plt.legend('')
    plt.axes().get_yaxis().set_label_text('demographic')
    plt.xticks(rotation = 360)
    plt.title('CLTV by Customer Demographic')
    plt.grid()
    ax.set_yticklabels(label)
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

    


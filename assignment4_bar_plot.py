import pandas as pd
import numpy as np

def getReligionchange():
    url = 'http://www.thearda.com/rcms2010/rcms2010a.asp?U=26161&T=county&S=Name&Y=1990&CH=ON'
    df = pd.read_html(url,attrs={"class":"data"},flavor='lxml')
    df = df[0]
    df.dropna(inplace=True)
    return df

def getPopdata():
    url = 'https://en.wikipedia.org/wiki/Ann_Arbor,_Michigan#Demographics'
    df = pd.read_html(url,header=1,skiprows=(18,19),attrs={"class":"toccolours"},flavor='lxml')
    df =df[0]
    return df

def getReligiondata():
    url = 'http://www.thearda.com/rcms2010/rcms2010a.asp?U=26161&T=county&S=Name&Y=2010'
    df = pd.read_html(url,attrs={"class":"data"},flavor='lxml')
    df = df[0]
    df
    df.dropna(inplace=True)
    df['year'] = 2010
    url = 'http://www.thearda.com/rcms2010/rcms2010a.asp?U=26161&T=county&S=Name&Y=2000'
    df1 = pd.read_html(url,attrs={"class":"data"},flavor='lxml')
    df1 = df1[0]
    df1.dropna(inplace=True)
    df1['year'] = 2000
    url = 'http://www.thearda.com/rcms2010/rcms2010a.asp?U=26161&T=county&S=Name&Y=1990'
    df2 = pd.read_html(url,attrs={"class":"data"},flavor='lxml')
    df2 = df2[0]
    df2.dropna(inplace=True)
    df2['year'] = 1990
    frames = [df,df1,df2]
    final = pd.concat(frames,ignore_index=True)
    final['group'] = final[['Tradition','Family']].apply(lambda x: x['Tradition'] if x['Tradition'] != 'Other' else x['Family'], axis=1)
    final = final[['group','year','Congregations','Adherents']]
    return final

def data():
    pop = getPopdata()
    religion = getReligiondata()
    df = pd.merge(religion,pop, how='left', left_on=['year'], right_on=['Census'])
    df = df[['group','year','Congregations','Adherents','Pop.']]
    df.columns = ['group','year','cong','members','population']
    df['members'] = df['members'].str.replace('---','0').astype(int)
    df['cong'] = df['cong'].dropna()
    df['year'] = df['year'].astype(str)
    df['group'] = df['group'].apply(lambda x: 'Protestant' if 'Protestant' in x else x )
    return df

def image():
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcol
    import matplotlib.cm as cm
    fig, ax = plt.subplots(figsize=(7,7))
    colors = ['#3498DB','#28B463','#F1C40F','#D6EAF8','#8E44AD','#F39C12','#D35400']

    df = data()
    
    ax = plt.gca()
    years = ['1980','1990','2000','2010','2020']
    pop = df.groupby('year')['population'].max()
    mem = df.groupby('year')['members'].sum()
    group = df.groupby(['year', 'group'])['members'].sum().unstack('group').fillna(0)
    group = group.T
    group = group[((group['1990'] + group['2000'] + group['2010'])!=0)]
    group = group.T
    group = group[['Protestant','Catholic','Judaism','Latter-day Saints','Liberal','Orthodox','Other Groups']]
    bm=0
    bm1=0
    bm2=0
    i=0
    height = 0
    for column in group:
        so = group[column]
        change = (so.values[2] - so.values[0]) / so.values[2]
        label = column + ' (change: ' + "{:.0%}".format(change) + ')'
        plt.bar(years[1],so.values[0],bottom=bm,color = colors[i],edgecolor='darkslategray')
        plt.bar(years[2],so.values[1],bottom=bm1,color = colors[i],edgecolor='darkslategray')
        plt.bar(years[3],so.values[2],bottom=bm2,color = colors[i],edgecolor='darkslategray',label=label)
        bm+=so.values[0]
        bm1+=so.values[1]
        bm2+=so.values[2]
        i+=1
    pop.plot(kind='line',x='year',y='population',ax=ax,color='#7D3C98',alpha=1,marker='o')
    ax.set_xlim((-.6,2.6))
    ax.set_ylim((0,150000))
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.tick_params(which='none',top='off', bottom='off', left='off', right='off')
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
    ax.legend(loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1,fancybox=True)
    plt.xlabel('Year',color="darkslategray",alpha=.8)
    plt.ylabel('Population',color="darkslategray",alpha=.8)
    plt.title('Ann Arbor, MI, United States \n Religious Demographics 1990 - 2010',color="darkslategray",alpha=.8)
    plt.xticks(color="darkslategray",alpha=.8)
    plt.yticks(color="darkslategray",alpha=.8)
    plt.savefig('AnnArborReligiousPractitionerChange1990-2010.png')
    return plt.show()

    
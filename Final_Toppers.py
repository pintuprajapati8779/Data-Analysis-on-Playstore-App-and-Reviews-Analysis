from tkinter import messagebox,Scrollbar,Listbox,Label,Frame,Entry,Button,Canvas
import tkinter as tk
from tkinter import Tk,ttk
from PIL import ImageTk, Image
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
import datetime
from textblob import TextBlob
import re,pymysql


data = pd.read_csv("googleplaystore-App-data.csv")
data1=pd.read_csv("googleplaystore_user_reviews.csv")
cat_array=data.Category.unique()
cat_list=list(data.Category)
data['Is']=list(data.Installs)
data["Installs"] = [ float(i.replace('+','').replace(',', '')) if '+' in i or ',' in i else float(0) for i in data["Installs"] ]

def adjustWindow(window):
    w=900
    h=600
    ws=window.winfo_screenwidth()
    hs=window.winfo_screenheight()
    x=(ws/2)-(w/2)
    y=(hs/2)-(h/2)
    window.geometry('%dx%d+%d+%d' %(w,h,x,y))
    window.resizable(False,False)
    window.config(bg='white')
    
def feature1():
    total_installs=0.0
    for i in data.Installs:
        total_installs=total_installs+i
    cat_installs={}
    for i in cat_array:
        sum=0.0
        for j in range(len(cat_list)):
            if i==cat_list[j]:
                sum=sum+data.Installs[j]
        percentage=(sum/total_installs)*100        
        cat_installs.update({i:float("{:.2f}".format(percentage))})
    plt.figure(figsize=(14,8))
    percent_installs = plt.bar(range(len(cat_installs)), list(cat_installs.values()))
    plt.xticks(range(len(cat_installs)), list(cat_installs.keys()),rotation='vertical')
    plt.xlabel('Category',fontsize=15)
    plt.ylabel('%age of Downloads',fontsize=15)
    plt.tight_layout()
    for bar in percent_installs:
        yval = bar.get_height()
        plt.text(bar.get_x() - .2, yval + .1, str(yval)+"%",fontsize=8)
    
    canvas = FigureCanvasTkAgg(percent_installs,master=mainscreen)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def feature2():
    plt.figure(figsize=(14,8))
    a=0
    b=0
    c=0
    d=0
    e=0
    for i in data['Installs']:
        if 10000<=i<50000 :
            a=a+1
        elif 50000<=i<150000 :
            b=b+1
        elif 150000<= i <500000:
            c=c+1
        elif 500000<=i<5000000 :
            d=d+1
        else:
            e=e+1
    dic_data={"10000-50000":a,"50000-150000":b,"150000-500000":c,"500000-5000000":d,"5000000+":e}
    ran_downs = plt.bar(dic_data.keys(),dic_data.values(),color=['pink','green','brown','orange','grey'])
    plt.xlabel("Range",fontsize=15)
    plt.ylabel("No of Apps",fontsize=15)
    plt.tight_layout()
    for bar in ran_downs:
        yval = bar.get_height()
        plt.text(bar.get_x() + .3, yval + .3, str(yval),fontsize=12)
    
def feature3():
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 3")
    category_installs={}
    category_install_avg={}
    for i in cat_array:
        sum=0.0
        count=0
        for j in range(len(cat_list)):
            if i==cat_list[j]:
                sum=sum+data.Installs[j]
                count=count+1
        category_installs.update({i:sum})
        category_install_avg.update({i:sum/count})
    fig=Figure(figsize=(10,6))
    a=fig.add_subplot(211)
    #a.set_xlabel("Category")
    a.set_ylabel("No.of Installs")
    for tick in a.get_xticklabels():
        tick.set_rotation(90)
    a.bar(category_installs.keys(),category_installs.values(),color='yellow')
    canvas = FigureCanvasTkAgg(fig, master=sc)
    canvas.get_tk_widget().pack()
    canvas.draw()
    Label(sc,text="All Category",font=("Open Sans", 20, 'bold'),bg="white").place(x=50,y=360)
    lb=Listbox(sc,width=50)
    lb.place(x=50,y=400)
    for item in category_installs:
        lb.insert(tk.END,'{}   :  {}'.format(item,category_installs[item]))
    df = pd.DataFrame(data=category_installs, index=[0])
    df = pd.DataFrame(data=category_installs, index=[0])
    df = (df.T)
    data1=pd.read_excel("dict1.xlsx", sep='\t')
    data1.columns = ["Category","Installs"]
    
    for j in range(len(data1.Category)):
        if data1.Installs[j]==max(data1.Installs):
            txt=str("MOST DOWNLOAD :"+data1.Category[j])
            Label(sc,text=txt,font=("Open Sans", 15, 'bold'),bg="white").place(x=550,y=350)
    for j in range(len(data1.Category)):
        if (data1.Installs[j]==min(data1.Installs)):
            txt=str("LEAST DOWNLOAD :"+data1.Category[j])
            Label(sc,text=txt,font=("Open Sans", 15, 'bold'),bg="white").place(x=550,y=380)
            
    lb_avg=Listbox(sc,width=50)
    lb_avg.place(x=550,y=420)        
    for item in category_install_avg:
        if category_install_avg[item]>=250000:
           lb_avg.insert(tk.END,'{}      :  {}'.format(item,category_install_avg[item]))

def feature4():
   
    avg_rats={}
    for i in cat_array:
        sum=0.0
        count=0.0
        for j in range(len(cat_list)):
            if i==cat_list[j] and data.Rating[j]==data.Rating[j]:
                sum=sum+data.Rating[j]
                count+=1.0
        avg=sum/count        
        avg_rats.update({i:float("{:.2f}".format(avg))})
    fig=plt.figure(figsize=(14,8))
    a=fig.add_subplot(211)
    a.stem(range(len(avg_rats)), list(avg_rats.values()),basefmt=' ')
    plt.xticks(range(len(avg_rats)), list(avg_rats.keys()),rotation='vertical')
    plt.ylabel('Average Ratings',fontsize=15)
    m1=max(avg_rats.values())
    m2=min(avg_rats.values())
    for i in avg_rats.items():
        if i[1]==m1:
            ma=i[0]
    for i in avg_rats.items():
        if i[1]==m2:
            mi=i[0]
    ans = "Category with max avg ratings = "+ str(ma) +" ("+str(m1)+")\nCategory with min avg ratings = "+str(mi)+" ("+str(m2)+")"
    plt.xlabel('Category\n\n\n'+ans,fontsize=15)


def feature6():
    screen_6=Tk()
    adjustWindow(screen_6)
    screen_6.title("Feature 6")
    screen_6.config(bg="#91F661")
    
    
    category_installs1={}
    category_installs2={}
    category_installs3={}
    
    sum6=0.0
    sum7=0.0
    sum8=0.0
    sumo=0.0
    Categorys=data.Category.unique()
    for category in Categorys:
        
        cat=data.loc[data['Category']==category]#loc function is used for returning rows
        cat=cat.sort_values('Last Updated')
        ins = [ float(i.replace('+','').replace(',', '')) if '+' in i or ',' in i else float(0) for i in cat["Is"] ]
        dates=list(cat['Last Updated'])
        dates=[i.replace(',', '') if ',' in i else float(0) for i in cat["Last Updated"] ]
    
        list_sum=[]
        
    
        for year in ['2016','2017','2018']:
                sum=0.0
                for i in range(len(dates)):
                    j=dates[i].split()
                    if(j[2]==year):
                        sum=sum+ins[i]
                
                    
                list_sum.append(sum)
        category_installs1.update({category:list_sum[0]})
        category_installs2.update({category:list_sum[1]})
        category_installs3.update({category:list_sum[2]})
        sum6=sum6+list_sum[0]
        sum7=sum7+list_sum[1]
        sum8=sum8+list_sum[2]
        sumo=sumo+list_sum[0]+list_sum[1]+list_sum[2]
    def year_2016():
        fig=plt.figure(figsize=(10,8))
        #print("Year 2016") 
        plt.bar(category_installs1.keys(),category_installs1.values(),color='yellow')
        plt.xlabel("Category")
        plt.ylabel("No.of Installs in 2016")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    inverse=[(value,key) for key, value in category_installs1.items()]
    print("Highest no.of Installs in year 2016 is ",max(inverse)[1])
    print("Lowest no.of installs in year 2016 is ",min(inverse)[1])
    print("Year 2017")
    def year_2017():
        fig1=plt.figure(figsize=(10,8))
        plt.bar(category_installs2.keys(),category_installs2.values(),color='Red')
        plt.xlabel("Category")
        plt.ylabel("No.of Installs in 2017")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    invers=[(value,key) for key, value in category_installs2.items()]
    print("Highest no.of Installs in year 2017 is ",max(invers)[1])
    print("Lowest no.of installs in year 2017 is ",min(invers)[1])
    print("Year 2018")
    def year_2018():
        fig2=plt.figure(figsize=(10,8))
        plt.bar(category_installs3.keys(),category_installs3.values(),color='Green')
        plt.xlabel("Category")
        plt.ylabel("No.of Installs in 2018")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
        
    
    
    inver=[(value,key) for key, value in category_installs3.items()]
    print("Highest no.of Installs in year 2018 is ",max(inver)[1])
    print("Lowest no.of installs in year 2018 is ",min(inver)[1])
    
    inverse=[(value,key) for key, value in category_installs1.items()]
    txt=str("Highest no.of Installs in year 2016 is    :"+max(inverse)[1])
    Label(screen_6,text="\n",bg="#91F661").pack()
    Label(screen_6,text=txt,font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    txt=("Lowest no.of installs in year 2016 is   :"+min(inverse)[1]) 
    Label(screen_6,text=txt,font=("Open Sans", 20, 'bold'),bg="#91F661").pack()    
    Button(screen_6,text="Click Here",command=year_2016,width="20").pack()
    
    invers=[(value,key) for key, value in category_installs2.items()]
    Label(screen_6,text="\n",bg="#91F661").pack()
    txt1=str("Highest no.of Installs in year 2017 is    :"+max(invers)[1])
    Label(screen_6,text=txt1,font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    txt1=str("Lowest no.of installs in year 2017 is   :"+min(invers)[1]) 
    Label(screen_6,text=txt1,font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen_6,text="Click Here",command=year_2017,width="20").pack()
    
    Label(screen_6,text="\n",bg="#91F661").pack()
    txt2=str("Highest no.of Installs in year 2018 is    :"+max(inver)[1])
    Label(screen_6,text=txt2,font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    txt2=str("Lowest no.of installs in year 2018 is   :"+min(inver)[1]) 
    Label(screen_6,text=txt2,font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen_6,text="Click Here",command=year_2018,width="20").pack() 
    
    diff67=sum7-sum6
    per67=float((diff67/sumo)*100)
    diff78=sum8-sum7
    per78=float((diff78/sumo)*100)
    if per67>0:
        txt=str("Increase by percent of Installs of apps from year 2016 to 2017 is "+str(per67)+"%")
        Label(screen_6,text=txt,font=("Open Sans", 15, 'bold'),bg="#91F661").pack()
    else:
        print("Decrease by percent",per67)
    if per78>0:
        txt=str("Increase by percent of Installs of apps from year 2017 to 2018 is "+ str(per78)+"%")
        Label(screen_6,text=txt,font=("Open Sans", 15, 'bold'),bg="#91F661").pack()
    else:
        print("Decrease by percent",per78) 
        
def feature7():
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 7")
    
    Label(sc,text="Percentage Increases",width=30,height=3,bg="white",font=("Open Sans", 12, 'bold')).place(x=20,y=50)
        
    Andriod_version=data.loc[data['Android Ver']=='Varies with device']#loc function is used for returning rows
    last_Updated=[i.replace(',', '') if ',' in i else float(0) for i in Andriod_version["Last Updated"]] 
    last_updated=list(last_Updated)
    installs =list( Andriod_version["Installs"]) 
    last_updated1=[]
    for i in last_updated:
        j=i.split()
        last_updated1.append(j[2])
    total_install=0.0
    for i in installs:
        total_install=total_install+i
        
    dic_trend={}
    years=['2011','2012','2013','2014','2015','2016','2017','2018']
    for year in years:
        sum=0.0
        for i in range(len(last_updated1)):
            if last_updated1[i]==year:
                sum=sum+installs[i]
        dic_trend.update({year:sum})
    
           
    def graph():
        fig=plt.Figure(figsize=(6,6),dpi=80)
        a=fig.add_subplot(111)
        x=dic_trend.keys()
        y=dic_trend.values()
        a.bar(x,y)
        a.set_xlabel("years")
        a.set_ylabel("Downloads")
        canvas = FigureCanvasTkAgg(fig, master=sc)
        canvas.get_tk_widget().place(x=400,y=100)
        
    
    def percentage(x1,x2):
        return((x2-x1)/total_install *100)
        
    y=100
    for year in dic_trend:
        if year=='2018':
            break
        else:
            percent=percentage(dic_trend[year],dic_trend[str(int(year)+1)])
            txt=str(year+" to "+str(int(year)+1)+ "  :  "+"{:.2f}".format(percent)+"%")
            Label(sc,text=txt,bg="white",width=30,height=2).place(x=50,y=y)
            y=y+40
    Button(sc,text="Graph",width=20,height=2,bg="#80ff00",command=graph).place(x=400,y=30)
    
def feature9a():
    data["Lesmor"]=list(data.Installs)
    data.loc[data['Lesmor'] < 100000 , 'Lesmor'] = 0
    data.loc[data['Lesmor'] >= 100000 , 'Lesmor'] = 1
    data["Morles"]=list(data.Rating)
    data.loc[data['Rating'] < 4.1 , 'Morles'] = 0
    data.loc[data['Rating'] >= 4.1 , 'Morles'] = 1
    fig, ax = plt.subplots(figsize=(10,8))
    sns.countplot(x="Lesmor",hue='Morles',data=data,ax=ax,color='pink')
    ax.set_xlabel('Ratings with respect to Downloads',fontsize=15)
    plt.legend(title='Rating', loc='upper left', labels=['Less than 4.1', '4.1 and Above'],fontsize=15)
    
def feature9b():
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 9")
    fig=Figure(figsize=(8,8))
    dt=data[["Rating","Installs"]]
    a=fig.add_subplot(111)
    a.scatter(dt['Rating'],dt["Installs"],c='green')
    a.set_xlabel("Ratings",fontsize=12)
    a.set_ylabel("Downloads",fontsize=12)
    dt = dt[np.isfinite(dt['Rating'])]
    X = dt['Rating'].values.reshape(-1,1)
    Y = dt['Installs'].values.reshape(-1,1)
    reg = LinearRegression()
    reg.fit(X, Y)
    predictions =reg.predict(X)
    a.plot(dt['Rating'],predictions,c='red',linewidth=2)
    canvas = FigureCanvasTkAgg(fig,master=sc)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def feature11():
    #Installs= [ float(i.replace('+','').replace(',', '')) if '+' in i or ',' in i else float(0) for i in data["Installs"] ]
    Dates=[i.replace(',', '') if ',' in i else float(0) for i in data["Last Updated"] ]
    screen_11=Tk()
    adjustWindow(screen_11)
    screen_11.config(bg="#f6d9d5")
    screen_11.title("Feature 11")
    Label(screen_11,text="YEARS",font=("Courier New",18,"bold"),bg="#f6d9d5").place(x=30,y=20)
    Label(screen_11,text="QUARTER NUMBER",font=("Courier New",18,"bold"),bg="#f6d9d5").place(x=200,y=20)
    Label(screen_11,text="No of install",font=("Courier New",18,"bold"),bg="#f6d9d5").place(x=450,y=20)
    quarter1=['January','February','March']
    quarter2=['April','May','June']
    quarter3=['July','August','September']
    quarter4=['October','November','December']
    y1=60
    quat_max={}
    for year in ['2010','2011','2012','2013','2014','2015','2016','2017','2018']:
        sum1=0.0
        sum2=0.0
        sum3=0.0
        sum4=0.0
        Quarter_install={}
        
        for m in quarter1:
            for j in range(len(Dates)):
                l=Dates[j].split()
                if l[0]==m and l[2]==year:
                    sum1=sum1+data['Installs'][j]
        Quarter_install.update({"Quarter 1" : sum1})
        Quarter_install.update({"Quarter 1":sum1})            
        for m in quarter2:
            for j in range(len(Dates)):
                l=Dates[j].split()
                if l[0]==m and l[2]==year:
                    sum2=sum2+data['Installs'][j] 
        Quarter_install.update({"Quarter 2" : sum2})             
        for m in quarter3:
            for j in range(len(Dates)):
                l=Dates[j].split()
                if l[0]==m and l[2]==year:
                    sum3=sum3+data['Installs'][j]
        Quarter_install.update({"Quarter 3": sum3})             
        for m in quarter4:
            for j in range(len(Dates)):
                l=Dates[j].split()
                if l[0]==m and l[2]==year:
                    sum4=sum4+data['Installs'][j]        
        Quarter_install.update({"Quarter 4": sum4})
        mx=max(Quarter_install.values())
        for item in Quarter_install:
            if Quarter_install[item]==mx:
                Label(screen_11,text=year,font=("Courier New",12),bg="#f6d9d5").place(x=40,y=y1)
                Label(screen_11,text=item,font=("Courier New",12),bg="#f6d9d5").place(x=250,y=y1)
                Label(screen_11,text=int(Quarter_install[item]),font=("Courier New",12),bg="#f6d9d5").place(x=450,y=y1)
                quat_max.update({item+" of "+year:Quarter_install[item]})
                y1=y1+30
    mx=max(quat_max.values())
    for item in quat_max:
        if quat_max[item]==mx:
            txt=str(item + " has highest number of install("+str(int(quat_max[item]))+")")
            Label(screen_11,text=txt,font=("Courier New",15),fg="red",bg="#f6d9d5").place(x=30,y=400)
#     print(quat_max)      
    screen_11.mainloop()    
    
def feature12():
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 12")
    sc.config(bg="#CAD3C8")
    apps=list(data1.App.unique())
    data2=data1.dropna()
    app_column=list(data2.App)
    Sentiment_column=list(data2.Sentiment)
    Sentiment_pos={}
    Sentiment_neg={}
    for app in apps:
        pos,neg=0,0
        for i in range(len(app_column)):
            if app==app_column[i]:
                if Sentiment_column[i]=='Positive':
                    pos=pos+1
                elif Sentiment_column[i]=='Negative':
                    neg=neg+1
            Sentiment_pos.update({app:pos}) 
            Sentiment_neg.update({app:neg})
    list_pos=list(Sentiment_pos.values())  
    for item in Sentiment_pos.items():
        if item[1]==max(list_pos):
            ans1=item[0]      
    list_neg=list(Sentiment_neg.values())
    for item in Sentiment_neg.items():
        if item[1]==max(list_neg):
            ans2=item[0]
        
    Label(sc,text="\n",font=("",4),bg="#CAD3C8").pack()
    Label(sc,text="Review Analysis -",font=("Magneto",22),bg="#CAD3C8").pack()
    tk.Label(sc,text="App with most positive reviews:         "+str(ans1)+" ("+str(max(list_pos))+")",font=("Open Sans", 18, 'bold'),bg="#CAD3C8").place(x=10,y=80)
    tk.Label(sc,text="App with most negative reviews:       "+str(ans2)+" ("+str(max(list_neg))+")",font=("Open Sans", 18, 'bold'),bg="#CAD3C8").place(x=10,y=140)
    dic={}
    for i in range(len(apps)):
        if list_pos[i]!=0 :
            dic.update({apps[i]:list_pos[i]-list_neg[i]})  
    name_list,no_emoji=[],[] 
    for item in dic.items():
        if item[1]==0:
            name_list.append(item[0])
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF""]+", flags=re.UNICODE)
    for i in name_list:
        no_emoji.append(emoji_pattern.sub(r'',i))
        
    tk.Label(sc,text="Apps with same ratio of +ve and -ve reviews: ",font=("Open Sans", 18, 'bold'),bg="#CAD3C8").place(x=10,y=200)
    frame = tk.Frame(sc, highlightbackground="green", highlightthickness=1)
    frame.place(x=150,y=270)
    lt=tk.Listbox(frame,height=8,width=80)
    lt.insert(tk.END,*no_emoji)
    scroll = tk.Scrollbar(frame, orient="vertical")
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    lt.pack()
    scroll.config(command=lt.yview)
    lt.config(yscrollcommand=scroll.set)
    
def feature13():
    global data1
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 13")
    fig=Figure(figsize=(8,8))
    a=fig.add_subplot(111)
    a.scatter(data1['Sentiment_Polarity'],data1['Sentiment_Subjectivity'],c='pink')
    a.set_xlabel("Sentiment Polarity",fontsize=12)
    a.set_ylabel("Sentiment Subjectivity",fontsize=12)
    data1 = data1[np.isfinite(data1['Sentiment_Polarity'])]
    data1 = data1[np.isfinite(data1['Sentiment_Subjectivity'])]
    X = data1['Sentiment_Polarity'].values.reshape(-1,1)
    Y = data1['Sentiment_Subjectivity'].values.reshape(-1,1)
    reg = LinearRegression()
    reg.fit(X, Y)
    trend = "The linear model is: Sentiment Polarity = "+str(reg.intercept_[0])+" + "+str(reg.coef_[0][0])+" x Sentiment Subjectivity"
    Label(sc,text=trend,font=("Open Sans", 12),bg='white').pack()
    predictions =reg.predict(X)
    a.plot(data1['Sentiment_Polarity'],predictions,c='blue',linewidth=2)
    canvas = FigureCanvasTkAgg(fig,master=sc)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
def feature14():
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 14")
    sc.config(bg="#CAD3C8")
    
    def CurSelet(event):
        global select_app
        select_app=str((lt.get(lt.curselection())))
        app=data1.loc[data1['App']==select_app]
        trans=list(app.Translated_Review)
        sent=list(app.Sentiment)
        positive_rev,negative_rev,neutral_rev=[],[],[]
        for i in range(len(sent)):
            if sent[i]=='Positive':
                positive_rev.append(trans[i])
            elif sent[i]=='Negative':
                negative_rev.append(trans[i])
            elif sent[i]=='Neutral':
                neutral_rev.append(trans[i])
        pos_list=Listbox(frame2, height=6, width=60)
        pos_list.insert(tk.END,*positive_rev)
        pos_list.place(x=95,y=60)
        neg_list=Listbox(frame2, height=6, width=60)
        neg_list.insert(tk.END,*negative_rev)
        neg_list.place(x=95,y=190)
        neu_list=Listbox(frame2, height=6, width=60)
        neu_list.insert(tk.END,*neutral_rev)
        neu_list.place(x=95,y=320)
        ans = "Positive = "+str(len(positive_rev))+"\nNegative = "+str(len(negative_rev))+"\nNeutral = "+str(len(neutral_rev))
        Label(frame2,text=ans,font=("",10),fg="red",bg="#d2dae2").place(x=20,y=490)
                    
    name_list = list(data1.App.unique())
    no_emoji=[]
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF""]+", flags=re.UNICODE)
    for i in name_list:
        emoji_pattern.sub(r'',i)
        no_emoji.append(emoji_pattern.sub(r'',i))
    frame1 = Frame(sc, highlightbackground="green", highlightthickness=1)
    frame1.place(x=10,y=5,fill=None)
    frame1.config(bg="#d2dae2")
    frame2 = Frame(sc, highlightbackground="green", highlightthickness=1,width=550)
    frame2.pack(side="right",fill=tk.Y,padx=10,pady=10)
    frame2.config(bg="#d2dae2")
    Label(frame1,text="Seclect an App to view\n Reviews",font=("Magneto",15),bg="#d2dae2").pack()
    Label(frame1,text="\n",font=("",5),bg="#d2dae2").pack()
    lt=Listbox(frame1,height=31,width=50)
    lt.insert(tk.END,*no_emoji)
    scroll = Scrollbar(frame1, orient="vertical")
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    lt.pack()
    scroll.config(command=lt.yview)
    lt.config(yscrollcommand=scroll.set)
    lt.bind('<<ListboxSelect>>',CurSelet)
    Label(frame2,text="Categorised Reviews -",font=("Magneto",20,"bold"),bg="#d2dae2").place(x=10,y=15)
    Label(frame2,text="Positive : ",font=("",12),bg="#d2dae2").place(x=10,y=60)
    Label(frame2,text="Negative : ",font=("",12),bg="#d2dae2").place(x=10,y=190)
    Label(frame2,text="Neutral : ",font=("",12),bg="#d2dae2").place(x=10,y=320)
    Label(frame2,text="Count -",font=("",16),bg="#d2dae2").place(x=10,y=450)
    
def feature16():
    sc=Tk()
    adjustWindow(sc)
    dates=[i.replace(',', '') if ',' in i else float(0) for i in data["Last Updated"] ]
    months=['January','February','March','April','May','June','July','August','September','October','November','December']
    mon=[]
    for date in dates:
        j=date.split()
        mon.append(j[0])
    dic={}    
    for month in months:
        sum=0.0
        for i in range(len(mon)):
            if(month==mon[i]):
                sum=sum+data["Installs"][i]
        dic.update({month:sum})  
    fig=Figure(figsize=(12,8)) 
    a=fig.add_subplot(211)
    x=months
    y=dic.values()
    a.bar(x,y)
    a.set_ylabel("Sum of Downloads",fontsize=15)
    a.set_xlabel("Months",fontsize=15)
    for tick in a.get_xticklabels():
        tick.set_rotation(90)
    canvas = FigureCanvasTkAgg(fig,master=sc)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    mx=max(dic.values())
    for item in dic:
        if dic[item]==mx:
            txt=str(item+" has maximum download")
            Label(sc,text=txt,font=("Courier New",20,"bold"),bg="white",fg="red").place(x=300,y=400)
  
def feature17():
    sc=Tk()
    adjustWindow(sc)
    sc.title("Feature 11")
    size=[]
    for i in data["Size"]:
        if "M" in i:
            size.append(i.replace('M'," "))
        elif "k" in i:
            size.append(float(i.replace("k"," "))/1024)
        else:
            size.append(i)
    install,Size=[],[]        
    for i in range(len(data.Installs)):
        if size[i]=="Varies with device":
            pass
        else:
            Size.append(float(size[i]))
            install.append(float(data.Installs[i]))
    
    df = pd.DataFrame(list(zip(Size, install)), columns =['Size', 'Installs'])  
         
    fig=Figure(figsize=(14,8))        
    a=fig.add_subplot(111)
    a.scatter(df['Size'],df["Installs"],c='green')
    a.set_xlabel("Ratings",fontsize=12)
    a.set_ylabel("Downloads",fontsize=12)
    X = df['Size'].values.reshape(-1,1)
    Y = df['Installs'].values.reshape(-1,1)
    reg = LinearRegression()
    reg.fit(X, Y)
    predictions =reg.predict(X)
    a.plot(df['Size'],predictions,c='red',linewidth=2)
    canvas = FigureCanvasTkAgg(fig,master=sc)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    sc.mainloop()
      

def feature18():
    root.destroy()    
    def submit():
        global app_name,rating,reviews,size,installs,date,version
        print(app_name.get(),rating.get(),reviews.get(),size.get(),installs.get(),date.get(),version.get())
        if app_name.get() and rating.get() and reviews.get() and size.get() and installs.get() and date.get() and version.get() and combo.get():
            try:
                if float(rating.get()) >5.0:
                   Label(lf,text="                                               ",font=("Courier New",12),fg="red").place(x=100,y=50)
                   Label(lf,text="Invalid rating",font=("Courier New",12),fg="red").place(x=100,y=50)
                   return
            except:
                   Label(lf,text="                                               ",font=("Courier New",12),fg="red").place(x=100,y=50)
                   Label(lf,text="Rating should be float or int",font=("Courier New",12),fg="red").place(x=100,y=50)
                   return
            try:
               if float(size.get()):
                  pass
            except:    
               Label(lf,text="                                                     ",font=("Courier New",12),fg="red").place(x=100,y=50)
               Label(lf,text="Invalid size",font=("Courier New",12),fg="red").place(x=100,y=50)
               return
    #################            ######################################
            try:
               if float(reviews.get()):
                  pass
            except:
                  Label(lf,text="                                                                ",font=("Courier New",12),fg="red").place(x=100,y=50)
                  Label(lf,text="No. of review should be an integer value only",font=("Courier New",12),fg="red").place(x=100,y=50)
                  return
    #################################                
            I=list(installs.get())  
            for i in I:
                if I.count('+')>=2 or i.isalpha() or I.count('-')>=1 or I.count('/')>=1 or I.count('*')>=1 :
                      Label(lf,text="                                                               ",font=("Courier New",12),fg="red").place(x=100,y=50)
                      Label(lf,text="No. of installs should be an integer value only",font=("Courier New",12),fg="red").place(x=100,y=50)
                      return
                
            try:
                datetime.datetime.strptime(date.get(), '%d/%m/%Y')
            except ValueError:
                Label(lf,text="                                                       ",font=("Courier New",12),fg="red").place(x=100,y=50)
                Label(lf,text="Incorrect data format ,should be DD/MM/YYYY",font=("Courier New",12),fg="red").place(x=100,y=50)
                return
                     
    #######################  
                
            connection = pymysql.connect(host="localhost", user="root", passwd="", database="appdata") # database connection
            cursor = connection.cursor() 
            select_query = "INSERT INTO app_details(name,rating, reviews,version,date,size,install) VALUES('"+ app_name.get() + "', '"+rating.get() + "', '"+reviews.get()+ "', '"+ version.get() + "', '"+ date.get() + "','"+size.get()+combo.get()+"','"+installs.get()+"' );" # queries for inserting values 
            cursor.execute(select_query) # executing the queries
            connection.commit() # commiting the connection then closing it.
            connection.close() 
            
    ################
            Label(lf,text="                                                     ",font=("Courier New",12),fg="red").place(x=100,y=50)
            Label(lf,text="DATA ADDED SUCCESSFULLY",font=("Courier New",12),fg="red").place(x=100,y=50)            
        else:
            Label(lf,text="Please fill all the details",font=("Courier New",12),fg="red").place(x=100,y=50)
        
    
    def submit2():
        Label(lf,text="                                                     ",font=("Courier New",12),fg="red").place(x=100,y=50)
        global input_val,tex,subj,polar,sen
        subj=tk.StringVar()
        polar=tk.StringVar()
        sen=tk.StringVar()
        input_val=rev.get("1.0","end-1c")
        if app_name2.get() and input_val:
            tex=TextBlob(str(input_val))
            polar=tex.sentiment.polarity
            if polar<0:
                sen="Negative"
            elif polar>0:
                sen="Positive"
            elif polar==0:
                sen="Neutral"
            subj=tex.sentiment.subjectivity
            Label(tab2,text=sen,font=("Courier New",12)).place(x=200,y=180)
            Label(tab2,text=str(polar),font=("Courier New",12)).place(x=300,y=230)
            Label(tab2,text=str(subj),font=("Courier New",12)).place(x=300,y=280)
            
            connection = pymysql.connect(host="localhost", user="root", passwd="", database="appdata") # database connection
            cursor = connection.cursor() 
            select_query = "INSERT INTO app_reviews(app_name2,Review,Sentiment,Sentiment_polarity,Sentiment_subjective) VALUES('"+ app_name2.get() + "', '"+ input_val + "', '"+ sen + "', '"+ str(polar) + "', '"+ str(subj) +"');" # queries for inserting values 
            cursor.execute(select_query) # executing the queries
            connection.commit() # commiting the connection then closing it.
            connection.close()
            messagebox.showinfo("Result", "Added Successfully", parent=tab2)
            app_name2.initialize(" ")
            
        else:
            Label(lf,text="Please fill all the details            ",font=("Courier New",12),fg="red").place(x=80,y=50)    
   

    win=Tk()
    adjustWindow(win)
    tabControl = ttk.Notebook(win, height=370)  
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)    
    tabControl.add(tab1, text='App Data')
    tabControl.add(tab2, text='App Review')
    tabControl.pack(expand=0, fill=tk.X, side=tk.TOP, padx=5, pady=5) 
    lf = ttk.Labelframe(win, text='Error', height=200)
    lf.pack(expand=0, fill=tk.X, padx=5, pady=5)
        
        
    global app_name,rating,reviews,size,installs,date,version,app_name2
    app_name=tk.StringVar()
    app_name2=tk.StringVar()  
    rating=tk.StringVar()
    reviews=tk.StringVar()
    size=tk.StringVar()
    installs=tk.StringVar()
    date=tk.StringVar()
    version=tk.StringVar()
      
    Label(tab1,text="App Name *: ",font=("Courier New",12)).place(x=10,y=10)
    Entry(tab1,textvar=app_name).place(x=200,y=10)
    Label(tab1,text="Rating *: ",font=("Courier New",12)).place(x=10,y=50)
    Entry(tab1,textvar=rating).place(x=200,y=50)
    Label(tab1,text="(out of 5)",font=("Courier New",12),fg="red").place(x=350,y=50)
    Label(tab1,text="No of Reviews *: ",font=("Courier New",12)).place(x=10,y=90)
    Entry(tab1,textvar=reviews).place(x=200,y=90)
    Label(tab1,text="Size *: ",font=("Courier New",12)).place(x=10,y=130)
    Entry(tab1,textvar=size).place(x=200,y=130)
    combo=ttk.Combobox(tab1,values=['MB','KB','GB'],width=5)
    combo.place(x=270,y=130)
    Label(tab1,text="(MB/KB/GB)",font=("Courier New",12),fg="red").place(x=350,y=130)
    Label(tab1,text="Installs *: ",font=("Courier New",12)).place(x=10,y=170)
    Entry(tab1,textvar=installs).place(x=200,y=170)
    Label(tab1,text="Last Updated *: ",font=("Courier New",12)).place(x=10,y=210)
    e=Entry(tab1,textvar=date)
      
    e.place(x=200,y=210)
    Label(tab1,text="eg:16/02/2011",font=("Courier New",12),fg="red").place(x=350,y=210)
    Label(tab1,text="Version: ",font=("Courier New",12)).place(x=10,y=250)
    Entry(tab1,textvar=version).place(x=200,y=250)
    Button(tab1,text="SUBMIT",width=20,command=submit).place(x=130,y=300)
      
       ###########################################################################################################
    Label(tab2,text="App Name *: ",font=("Courier New",12)).place(x=20,y=20)
    Label(tab2,text="Written Review *: ",font=("Courier New",12)).place(x=20,y=70)
    Label(tab2,text="(Auto Generated based on Review) ",font=("Courier New",8),fg="red").place(x=20,y=155)
    Label(tab2,text="Sentiment : ",font=("Courier New",12)).place(x=20,y=180)
    Label(tab2,text="Sentiment Polarity : ",font=("Courier New",12)).place(x=20,y=230)
    Label(tab2,text="Sentiment Subjectivity : ",font=("Courier New",12)).place(x=20,y=280)
    Entry(tab2,textvar=app_name2).place(x=200,y=20)
    frame1 = tk.Frame(tab2)
    frame1.place(x=200,y=70,fill=None)
    rev = tk.Text(frame1, height=4, width=50)
    scroll = tk.Scrollbar(frame1, orient="vertical")
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    rev.pack(fill=tk.BOTH)
    scroll.config(command=rev.yview)
    rev.config(yscrollcommand=scroll.set)
    Button(tab2,text="SUBMIT",width=20,command=submit2).place(x=240,y=320)
    win.mainloop()
 
def splashscreen():
    splash_screen = Tk()
    splash_screen.overrideredirect(True)
    width = splash_screen.winfo_screenwidth()
    height = splash_screen.winfo_screenheight()
    splash_screen.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))
    image_file = "google-play-store.gif"
    image = ImageTk.PhotoImage(file=image_file)
    canvas = Canvas(splash_screen, height=height*0.8, width=width*0.8, bg="brown")
    canvas.create_image(width*0.8/2, height*0.8/2, image=image)
    canvas.pack()
    splash_screen.after(5000, splash_screen.destroy)
    splash_screen.mainloop()
    mainscreen()

def mainscreen():
    global root
    root= Tk()
    adjustWindow(root)
    back= Image.open("google-play-store-ratings.png")
    back= back.resize((900,600), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(back) # opening right side image - Note: If image is in same folder then no need to mention the full path 
    label1 = Label(root, image=photo) # attaching image to the label 
    label1.pack()
    label1.image = photo
    
    but1= Image.open("Download.png")
    p1 = ImageTk.PhotoImage(but1)
    but2= Image.open("bar.png")
    p2 = ImageTk.PhotoImage(but2)
    but3= Image.open("AppsReview.png")
    p3 = ImageTk.PhotoImage(but3)
    but4= Image.open("core.png")
    p4 = ImageTk.PhotoImage(but4)
    but5= Image.open("data_add.png")
    p5 = ImageTk.PhotoImage(but5)
    
    Button(root, image = p1, command=but1screen).place(x=50,y=38)
    Button(root, image = p2, command=but2screen).place(x=540,y=40)
    Button(root, image = p3, command=but3screen).place(x=50,y=380)
    Button(root, image = p4, command=but4screen).place(x=540,y=380)
    Button(root, image = p5, command=feature18).place(x=315,y=230)
    root.mainloop()

def but1screen():
    global screen1
    screen1 = Tk()
    adjustWindow(screen1)
    screen1.config(bg="#5DADE2")
    Label(screen1,text="Percentage download in each category on the playstore",font=("Open Sans", 17, 'bold'),bg="#5DADE2").pack()
    Button(screen1,text="Click Here",width='20',command=feature1).pack()
    Label(screen1,text="How many apps have managed to get the following number of \ndownloads\na) Between 10,000 and 50,000\tb) Between 50,000 and 150000\nc) Between 150000 and 500000\td) Between 500000 and 5000000\ne) More than 5000000",font=("Open Sans", 17, 'bold'),bg="#5DADE2").pack()
    Button(screen1,text="Click Here",width='20',command=feature2).pack()
    Label(screen1,text="Which category of apps have managed to get the most,least and\n an average of 2,50,000 downloads atleast?",font=("Open Sans", 17, 'bold'),bg="#5DADE2").pack()
    Button(screen1,text="Click Here",width='20',command=feature3).pack()
    Label(screen1,text="All those apps who have managed to get over 1,00,000 downloads,\n have they managed to get an average rating of 4.1 and above?",font=("Open Sans", 17, 'bold'),bg="#5DADE2").pack()
    Button(screen1,text="Click Here",width='20',command=feature9a).pack()
    Label(screen1,text="All those apps , whose android version is not an issue and can \nwork with varying devices ,what is the percentage increase\n or decrease in the downloads.",font=("Open Sans",17, 'bold'),bg="#5DADE2").pack()
    Button(screen1,text="Click Here",width='20',command=feature7).pack()
    Label(screen1,text="Which quarter of which year has generated the highest number of\n install for each app used in the study",font=("Open Sans", 17, 'bold'),bg="#5DADE2").pack()
    Button(screen1,text="Click Here",width='20',command=feature11).pack()      
    screen1.mainloop()

def but2screen():
    global screen2
    screen2 = Tk()
    adjustWindow(screen2)
    screen2.config(bg="#91F661")
    Label(screen2,text="\n\n\n",bg="#91F661").pack()
    Label(screen2,text="For the years 2016,2017,2018 what are the category of apps\n that have got the most and the least downloads.\n What is the percentage increase or decrease that the apps have\n got over the period of three years.",font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen2,text="Click Here",width='20',command=feature6).pack()
    Label(screen2,text="\n\n",bg="#91F661").pack()
    Label(screen2,text="Which month(s) of the year , is the best indicator to the avarage\n downloads that an app will generate over the entire year?",font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen2,text="Click Here",width='20',command=feature16).pack()
    screen2.mainloop()

def but3screen():
    global screen3
    screen3 = Tk()
    adjustWindow(screen3)
    screen3.config(bg="#91F661")
    Label(screen3,text="\n",bg="#91F661").pack()
    Label(screen3,text="Which category of apps have managed to get the highest maximum\n average ratingsfrom the users.",font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen3,text="Click Here",width='20',command=feature4).pack()
    Label(screen3,text="\n",bg="#91F661").pack()
    Label(screen3,text="Which of all the apps given have managed to generate the most\n positive and negative sentiments.Also figure out the app which has\n generated approximately the same ratio for positive and negative\n sentiments.",font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen3,text="Click Here",width='20',command=feature12).pack()
    Label(screen3,text="\n",bg="#91F661").pack()
    Label(screen3,text="Generate an interface where the client can see the reviews\n categorized as positive,negative and neutral once they have \nselected the app from a list of apps available for the study.",font=("Open Sans", 20, 'bold'),bg="#91F661").pack()
    Button(screen3,text="Click Here",width='20',command=feature14).pack()
    screen3.mainloop()
    
def but4screen():
    global screen4
    screen4 = Tk()
    adjustWindow(screen4)
    screen4.config(bg="#F7DC6F")
    Label(screen4,text="\n\n",bg="#F7DC6F").pack()
    Label(screen4,text="Can we conclude something in co-relation to the number of \ndownloads and the ratings received?",font=("Open Sans", 20, 'bold'),bg="#F7DC6F").pack()
    Button(screen4,text="Click Here",width='20',command=feature9b).pack()
    Label(screen4,text="\n\n",bg="#F7DC6F").pack()
    Label(screen4,text="Study and find out the relation between the Sentiment-polarity and \nSentiment-subjectivity of all the apps",font=("Open Sans", 20, 'bold'),bg="#F7DC6F").pack()
    Button(screen4,text="Click Here",width='20',command=feature13).pack()
    Label(screen4,text="Does the size of the App influence the number\n of installs that it gets ? if,yes the trend is positive or negative \nwith the increase in the app size.",font=("Open Sans", 20, 'bold'),bg="#F7DC6F").pack()
    Button(screen4,text="Click Here",width='20',command=feature17).pack()
    screen4.mainloop()
    
splashscreen()
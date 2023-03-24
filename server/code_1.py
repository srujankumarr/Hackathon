import pandas as pd
from sklearn.cluster import KMeans
import sys
import matplotlib.pyplot as plt
from connection import create_connection

n=int(sys.argv[1])

db = create_connection()
df=pd.read_sql('SELECT Rollno,TotalGpa,Nocert,Extra from Studentdetails',con=db)

#mycursor = db_connect.cursor()
#mycursor.execute("INSERT ")
df['Nocert']=df['Nocert'].apply(lambda x:min(10,x*2))
df['Extra']=df['Extra'].apply(lambda x:min(10,x*3))
df['Total']=df['TotalGpa']+df['Nocert']+df['Extra']


df2=df['Rollno']
del df['Rollno']

size = n
selected_cols=["Total","TotalGpa","Nocert","Extra"]
cluster_data=df.loc[:,selected_cols]

kmeans_sel=KMeans(init='k-means++',n_clusters=n,n_init=100,random_state=1).fit(df,sample_weight=None)
labels=pd.DataFrame(kmeans_sel.labels_)

clustered_data=cluster_data.assign(Cluster=labels)

# Calculate the size of each cluster
cluster_sizes = clustered_data.groupby(["Cluster"]).size()

# Group the data by cluster and calculate the mean
grouped_km = clustered_data.groupby(["Cluster"]).mean().round(2)

# Add the cluster sizes to the grouped_km DataFrame
grouped_km["Cluster Size"] = cluster_sizes

grouped_km=grouped_km.sort_values(by=['Total'],ascending=False)
grouped_km['Type']=[chr(ord('A')+i) for i in range(n)]

clustered_data['Rollno']=df2

print(clustered_data)
print(grouped_km)

legend_labels = []
explode = [0.1]

for i in range(25):
    explode.append(0)

for i in range(26):
    legend_labels.append(chr(65+i))
# print(legend_labels)

wedges, texts, autotexts = plt.pie(grouped_km['Cluster Size'], autopct='%1.1f%%', shadow=True, radius=0.8, explode=explode[:size])

plt.legend(wedges, legend_labels[:size], loc='lower right', bbox_to_anchor=(1, 0, 0.25, 1), fontsize=10)
plt.title('Clustered Performance', fontsize=20)

# plt.show()

plt.savefig('./assets/img/Charts/Cluster.png')
db.close()
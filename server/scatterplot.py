import pandas as pd
import matplotlib.pyplot as plt
from connection import create_connection

db = create_connection()
colors = ['red', 'green', 'blue', 'orange', 'yellow', 'violet']
# barWidth = 0.5
df = pd.read_sql('select * from studentperformance', con=db)

# fig, ax = plt.subplots()
# bars = ax.bar(df['name'], df['gpa'], color=colors, width=barWidth)

# plt.show()

plt.scatter(df['cocurricular'], df['gpa'], alpha=0.75, c=df['extracurricular'],
            marker='o', cmap='viridis', s=25*df['extracurricular'] + 150, edgecolors='gray')
plt.title('Student Overall performance', fontsize=20)
plt.xlabel('Student cocurricular activities ---->', fontsize=12)
plt.ylabel('Student Grades ---->', fontsize=12)

cbar = plt.colorbar()
cbar.set_label('Student Extracurricular Activities ---->', fontsize=12)

# plt.show()

plt.savefig('Charts/scatter_plot.png')
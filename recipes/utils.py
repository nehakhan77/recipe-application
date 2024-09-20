from recipes.models import Recipe
from io import BytesIO 
import base64
import matplotlib.pyplot as plt

def get_recipename_from_id(val):
   #this ID is used to retrieve the name from the record
   recipename=Recipe.objects.get(id=val)
   #and the name is returned back
   return recipename

def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close()

   #return the image/graph
   return graph


#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')

   #specify figure size
   fig=plt.figure(figsize=(6,3))

   print(data.columns)
    
    # Check if 'date_created' is in the columns
   if 'date_created' not in data.columns:
        raise KeyError("The column 'date_created' is not present in the DataFrame.")

   #select chart_type based on user input from the form
   if chart_type == 'bar_chart':
       #Bar chart for cooking time
       plt.bar(data['name'], data['cooking_time'])
       plt.xlabel('Recipe Name')
       plt.ylabel('Cooking Time in min')
       plt.xticks(rotation=35, ha='right') #set angle of recipe names
       plt.title('Recipes by Cooking Time')

   elif chart_type == 'pie_chart':
       #generate pie chart based on difficulty levels
        difficulty_counts = data['difficulty'].value_counts()
        labels = difficulty_counts.index
        values = difficulty_counts.values
        plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#135E46', '#478966', '#73A788', '#53BD99'])
        plt.title('Recipes by Difficulty')      

   elif chart_type == 'line_chart':
        plt.rcParams.update({'axes.facecolor': 'none'})
        data['formatted_date'] = data['date_created'].apply(lambda x: x.strftime('%Y-%m-%d')) #format date_created
        recipes_per_day = data.groupby(data['formatted_date']).size()
        plt.plot(recipes_per_day.index, recipes_per_day, color='#ef9b00')
        plt.xlabel('Date Created')
        plt.ylabel('Number of Recipes')
        plt.title('Number of Recipes Created per Day')
        plt.xticks(rotation=35, ha='right') #set angle of recipe names
        plt.gca().spines['right'].set_visible(False) #make right side of frame invisible
        plt.gca().spines['top'].set_visible(False) #make top side of frame invisible

   else:
       print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart =get_graph() 
   return chart    
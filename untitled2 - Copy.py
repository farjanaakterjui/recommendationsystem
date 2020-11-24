from flask import Flask, render_template, request
import pandas as pd
import csv
from scipy import sparse

ratings = pd.read_csv("F:/Introduction-to-Machine-Learning-master/Collaborative Filtering/dataset/ratings.csv")
movies = pd.read_csv("F:/Introduction-to-Machine-Learning-master/movies.csv")
ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)
#print(ratings.shape)
#ratings.head()
userRatings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
#userRatings.head()
userRatings = userRatings.fillna(0,axis=1)
#userRatings.fillna(0, inplace=True)
#print("After: ",userRatings.shape)
corrMatrix = userRatings.corr(method='pearson')
#corrMatrix.head(100)
#f= open("prac.txt","w+")

def get_similar(movie_name,rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings     
    #f.write(str(similar_ratings))


#action_lover = [("Amazing Spider-Man, The (2012)",5),("Mission: Impossible III (2006)",4),("Toy Story 3 (2010)",2),("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)",4)]

app = Flask(__name__)

@app.route('/')
def entry():
   return render_template('entry.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
        
    p = request.form['Name']    
    q = float(request.form['rating'])
    x=0
    with open("F:/Introduction-to-Machine-Learning-master/movies.csv", "r",encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if (row[1].lower()==p.lower()):
                x=1 
                p=row[1]
                break
                #print("not found")
    print(p) 
    print(x)         
    if(x==1):
        action_lover = [(p,q)]
        similar_movies = pd.DataFrame()
        for movie,rating in action_lover:
            similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)
        similar_movies.head(10)
        return render_template('result.html',result=similar_movies.sum().sort_values(ascending=False).head(20)) 
    else:
        return render_template('sorry.html')
     
if __name__ == '__main__':
    app.run()
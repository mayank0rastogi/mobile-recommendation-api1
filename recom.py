import math
import numpy as np
import operator

mobiles_titles_map = {}
mobiles_user_map={}
user_mobiles_map={}
user_avg_rating = {}
db = {}

def read_mobiles_title(fname): 
    with open(fname) as f:
      for line in f.readlines():
        parts = [x.strip() for x in line.split(',')]
        mobiles_id = int(parts[0])
        mobiles_titles_map[mobiles_id] = str(parts[1]) #+ "("+ parts[1]+")"    
            

def get_ratings_map(fname):
    with open(fname) as f:
        for line in f.readlines():
            parts = [x.strip() for x in line.split(',')]
            mobiles_title_id = int(parts[0])
            user_id = int(parts[1])
            rating = int(parts[2])
            if user_id not in user_mobiles_map:
                user_mobiles_map[user_id]={}
            user_mobiles_map[user_id][mobiles_title_id] = rating
            
            if mobiles_title_id not in mobiles_user_map:
                mobiles_user_map[mobiles_title_id] = []
            mobiles_user_map[mobiles_title_id].append(user_id)

def get_user_avg_rating():
    for user in user_mobiles_map:
        sum = 0
        i=0
        for mobiles in user_mobiles_map[user]:
            sum = sum + float(user_mobiles_map[user][mobiles])
            i = i + 1 
        avg = sum/i
        user_avg_rating[user]=avg


mobiles_titles_filename="Mobiles_list_csv.txt"
ratings_filename="ratings_without_reviews_csv.txt"
read_mobiles_title(mobiles_titles_filename)
get_ratings_map(ratings_filename)
get_user_avg_rating()


def get_user_corr(active_user):
    user_correlation = {}
    for user in user_mobiles_map:
        if user!=active_user:
            nominator = 0
            sum_vaj_diff = 0
            sum_vij_diff = 0
            for mobiles in user_mobiles_map[active_user]:
                if mobiles in user_mobiles_map[user]:                
                    nominator +=  (user_mobiles_map[active_user][mobiles] - user_avg_rating[active_user]) * (user_mobiles_map[user][mobiles] - user_avg_rating[user])
                    sum_vaj_diff +=  np.power(user_mobiles_map[active_user][mobiles] - user_avg_rating[active_user], 2)
                    sum_vij_diff +=  np.power(user_mobiles_map[user][mobiles] - user_avg_rating[user], 2)
            denominator= np.sqrt(sum_vaj_diff * sum_vij_diff)  
            if denominator!=0:
                user_correlation[user] = nominator/denominator
    return user_correlation





#app=Flask(__name__)
#@app.route('/recommendation')
def recommendation(active_user, K):
    if active_user not in db:
        user_correlation = get_user_corr(active_user)
        predicted_rating ={}
        for mobiles in mobiles_titles_map:
            temp_rating = 0
            if mobiles in mobiles_user_map:
                for user in mobiles_user_map[mobiles]:
                    if user in user_correlation:
                        temp_rating +=user_correlation[user]*(user_mobiles_map[user][mobiles]- user_avg_rating[user])
            predicted_rating[mobiles] = temp_rating

        predicted_rating = sorted(predicted_rating.items(), key=lambda kv: kv[1], reverse=True)
        db[active_user] = predicted_rating
    else:
        predicted_rating= db[active_user]
        
    recommended_mobiles = predicted_rating[:K]
    result=list()
    for mobiles in recommended_mobiles:
       result.append(mobiles_titles_map[mobiles[0]])
    return result
'''
receive=[]
receive=recommendation(723873,15)

print(receive)
'''
#app.run(host='127.0.0.1')ss
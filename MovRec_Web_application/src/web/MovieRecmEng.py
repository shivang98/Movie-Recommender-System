from collections import defaultdict
import csv
import random
from .models import Myrating
def Myrecommend(userid):
    transactions=defaultdict(lambda:'')
    data=iter(Myrating.objects.all().values())
    for row in data:
        transactions[(row['movie_id'],row['rating'])]=transactions[(row['movie_id'],row['rating'])]+str(row['user_id'])+','

    with open('./data','w') as file:
        for key,value in transactions.items():
            file.write(value[:-1]+'\n')

    del transactions

    similarity_dict=defaultdict(lambda:{})
    count_uid={}

    with open('./data','r') as file:
        freader=csv.reader(file)
        for row in freader:
            for pos,x in enumerate(row):
                for y in row[pos:]:
                    if x!=y:
                        similarity_dict[x][y]=similarity_dict[x].get(y,0)+1
                        similarity_dict[y][x]=similarity_dict[y].get(x,0)+1
                    else:
                        count_uid[x]=count_uid.get(x,0)+1
    if count_uid[str(userid)]<=1:
        return random.choice(count_uid.keys()) 
    print(similarity_dict[str(userid)])
    return max(similarity_dict[str(userid)].keys(),key=lambda x:similarity_dict[str(userid)][x])
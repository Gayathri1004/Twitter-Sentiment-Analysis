from textblob import TextBlob
import matplotlib.pyplot as plt

movie=input("Enter a movie name:")
print("Enter the list of viewer reviews:")
reviews=[]
for i in range(10):
    print("enter review:",i+1)
    reviews.append(input())

polarity=[]
for i in range(10):
    senti = TextBlob(reviews[i])
    p = senti.sentiment.polarity
    polarity.append(p)
    

positive = 0
negative = 0
neutral = 0

for i in range(10):
    if (polarity[i] == 0):
        neutral +=1
    elif (polarity[i] < 0.00):
        negative +=1
    elif (polarity[i]> 0.00):
        positive +=1

labels = ['Positive ['+str(positive)+'%]'], ['negative ['+str(negative)+'%]'],['neutral ['+str(neutral)+'%]']
sizes=[positive , negative, neutral]
colors=['blue','red','gold']
patches,texts=plt.pie(sizes,colors=colors,startangle=90)
plt.legend(patches,labels,loc="best")
plt.title("overall movie review")
plt.axis('equal')
plt.tight_layout()
plt.show()

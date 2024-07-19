# Importing necessary libraries
import psycopg2
import matplotlib.pyplot as plt
import datetime

# Establishing connection to the PostgreSQL database
conn = psycopg2.connect(
dbname= "Viral Cascade",
user="postgres",
password="wapuh717",
host="localhost",
port="5432"
)

# Creating a cursor object
cursor = conn.cursor()

forum_ids = [1,2,3,4,5,6,7,8,9,10]
#1,2,3,4,5,6,7,8,9,10
#2, 4, 8, 9
unique_user_requirement = 10
alpha = 10
beta = 2
# SQL query to retrieve data
for forum_id in forum_ids:
    
    """
    query = f"select p.topic_id, count(distinct p.user_id) " \
            f"from posts p inner join topics t on t.topic_id = p.topic_id " \
            f"where t.forum_id = {forum_id} and length(content_post) > 10 group by p.topic_id"
    #and length(content_post) > 10 and classification_topic >= 0.5 
    # Executing the query
    """
    query = f"SELECT DISTINCT posts.topic_id, posts.user_id, posts.dateadded_post, LENGTH(posts.content_post) AS content_length " \
            f"FROM posts INNER JOIN topics ON posts.topic_id = topics.topic_id " \
            f"WHERE topics.forum_id = {forum_id} AND length(content_post) > 10"
    cursor.execute(query)

    # Fetching all the rows
    rows = cursor.fetchall()
    betaID = []
    alphaID = []
    for x in rows:
        count = x[0]
        if count >= alpha*beta:
            betaID.append(x[0])
        if count >= alpha:
            alphaID.append(x[0])
    
    print(f"Forum ID: {forum_id}, Number of Topics: {len(betaID)}")

cursor.close()
conn.close()


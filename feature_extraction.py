# Importing necessary libraries
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine
import networkx as nx

# Establishing connection to the PostgreSQL database
conn = psycopg2.connect(
#change these:
dbname= "Viral Cascade",
user="postgres",
password="wapuh717",
host="localhost",
port="5432"
)

# Creating a cursor object
cursor = conn.cursor()

forum_ids = [4]
#All Forums: 1,2,3,4,5,6,7,8,9,10,11
#Has Results: 2,5,8,9,11
#No Results: 1,3,4,6,7,10

unique_user_requirement = 10
alphas = [30]
betas = [2]
# SQL query to retrieve data
def get_db_connection():
    engine = create_engine('postgresql://postgres:wapuh717@localhost:5432/Viral Cascade')
    return engine.connect()

def get_db(forum_id, alpha, beta):
    conn = get_db_connection()
    query = """select p.topic_id, p.user_id, p.dateadded_post 
            from posts p inner join topics t on t.topic_id = p.topic_id 
            where forum_id = %s and length(content_post) > 10 and t.classification2_topic >= 0.5 group by p.post_id, t.topic_id"""
    #classification_topic
    # Executing the query
    df = pd.read_sql(query, conn, params=(forum_id,))
    conn.close()

    df['dateadded_post'] = pd.to_datetime(df['dateadded_post'], utc=True)
    df = df.drop_duplicates(subset=['topic_id', 'user_id'])
    return df

for forum in forum_ids:
    # Fetching all the rows
    for alpha in alphas:
        for beta in betas:
            
            db = get_db(forum, alpha, beta)

            alphaUsers = {}
            betaUsers = {}
            alphaUsersDate = {}
            betaUsersDate = {}
            rootUsers = {}
            
            for topic_id, group in db.groupby('topic_id'):
                sorted_group = group.sort_values(by='dateadded_post')
                alphaUsers[topic_id] = sorted_group['user_id'].tolist()[:alpha]
                betaUsers[topic_id] = sorted_group['user_id'].tolist()[:beta]
                alphaUsersDate[topic_id] = sorted_group['dateadded_post'].tolist()[:alpha]
                betaUsersDate[topic_id] = sorted_group['dateadded_post'].tolist()[:beta]
                rootUsers[topic_id] = sorted_group['user_id'].tolist()[:1]

                centrality = 

            
            #Root User Features
            #Degree centrality
            centrality = {}
            for user, group in rootUsers.groupby('user_id'):
                centrality[user] = so


                

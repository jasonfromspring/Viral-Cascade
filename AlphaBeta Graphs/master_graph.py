# Importing necessary libraries
import psycopg2
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates


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

forum_ids = [2,4,8,9]
#All Forums: 1,2,3,4,5,6,7,8,9,10,11
#Has Results: 2,5,8,9,11
#No Results: 1,3,4,6,7,10

unique_user_requirement = 10
alphas = [10]
betas = [5]
start_date_text = '2020-01-01 00:00:00'
start_date = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
# SQL query to retrieve data
for forum_id in forum_ids:
    query = f"select p.topic_id, count(distinct p.user_id) " \
            f"from posts p inner join topics t on t.topic_id = p.topic_id " \
            f"where forum_id = {forum_id} and classification2_topic >= 0.5 and p.dateadded_post > '{start_date_text}' and length(content_post) > 10 group by p.topic_id"
    #classification_topic
    # and length(content_post) > 10
    # Executing the query
    cursor.execute(query)
    # Fetching all the rows
    threads = cursor.fetchall()
    print(len(threads))
    for alpha in alphas:
        for beta in betas:
            betaID = []
            alphaID = []
            for x in threads:
                count = x[1]
                if count >= alpha*beta:
                    betaID.append(x[0])
                elif count >= alpha:
                    alphaID.append(x[0])
            print(f"Forum {forum_id} has {len(betaID)} for alpha {alpha} and beta {beta}")
            startDates = []
            endOfAlphas = []
            endOfBetas = []
            endOfLatests = []
            for x in betaID[:]:
                id = x
                #Find the first post = start
                query = f"SELECT min(dateadded_post) FROM posts WHERE topic_id = {id}"

                cursor.execute(query)
                rows = cursor.fetchall()
                start = rows[0]
                start = start[0]

                if(start >= start_date):
                    startDates.append(start)

                    #print(f"For thread number {id}")
                    query = f"SELECT user_id, min(dateadded_post) date " \
                            f"FROM (SELECT * FROM posts WHERE topic_id = {id} ORDER BY dateadded_post) " \
                            f"GROUP BY user_id"
                    # and length(content_post) > 10 
                    # Executing the query
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    y = []
                    for z in rows:
                        y.append(z[1])
                    ends = sorted(y)
                    tdBeta = ends[beta*alpha-1] - start
                    tdAlpha = ends[alpha] - start
                    tdLatest = ends[-1] - start
                    endOfBetas.append(tdBeta)
                    endOfAlphas.append(tdAlpha)
                    endOfLatests.append(tdLatest)

                    #time delta values:
                    tdSoloBeta = tdBeta - tdAlpha
                    #print(f"Thread {id} has beta {tdBeta}")
                    #print(tdAlpha)
                    #print(tdSoloBeta)
                else:
                    betaID.remove(x)
                    print(x)
                    print(start)

            #find delta t
            print(startDates)
            print(len(startDates))
            print(betaID)
            print(len(betaID))
            fig, ax = plt.subplots(figsize=(14, 8))
            # Add bars for the start time, time to reach alpha, and time to reach beta
            ax.barh(range(len(startDates)), endOfLatests, left=startDates, align='center', color='red', label='Time to Most Recent Post')
            ax.barh(range(len(startDates)), endOfBetas, left=startDates, align='center', color='blue', label='Time to Reach Beta After Alpha')
            ax.barh(range(len(startDates)), endOfAlphas, left=startDates, align='center', color='grey', label='Time to Reach Alpha')
            ax.set_yticks(range(len(startDates)))
            ax.set_yticklabels(betaID)

            #xfmt = mdates.DateFormatter('%b')
            months = mdates.MonthLocator()
            ax.xaxis.set_major_locator(months)
            #ax.xaxis.set_major_formatter(xfmt)
            ax.tick_params(axis='x', labelrotation=90, labelsize=9)


            ax.set_xlabel('Days Passed since first post by root user')
            ax.set_title(f'Forum {forum_id} with alpha {alpha} and multiplier {beta}X')
            ax.legend()
            #plt.show()
            #plt.savefig(f'NoLengthFilter_Forum{forum_id}_Alpha{alpha}Beta{beta}X.png')
            #plt.savefig(f'Forum{forum_id}_Alpha{alpha}Beta{beta}X.png')
            plt.savefig(f'2020Start_Forum{forum_id}_Alpha{alpha}Beta{beta}X.png')


cursor.close()
conn.close()


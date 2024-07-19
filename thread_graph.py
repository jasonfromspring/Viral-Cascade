# Importing necessary libraries
import psycopg2
import matplotlib.pyplot as plt

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

forum_ids = [6]
#2, 4, 8, 9
unique_user_requirement = 10

# SQL query to retrieve data
for forum_id in forum_ids:
    query = f"select p.topic_id, count(distinct p.user_id) " \
            f"from posts p inner join topics t on t.topic_id = p.topic_id " \
            f"where forum_id = {forum_id} and length(content_post) > 10 and classification_topic >= 0.5 group by p.topic_id"
    # Executing the query
    cursor.execute(query)

    # Fetching all the rows
    rows = cursor.fetchall()
    print(rows)
    thread_count_dict = {5: 0, 10: 0, 20: 0, 30: 0, 50: 0, 100: 0, 200: 0, 300: 0}
    for x in rows:
        count = x[1]
        if count >= 300:
            thread_count_dict[300] += 1
        elif count >= 200:
            thread_count_dict[200] += 1
        elif count >= 100:
            thread_count_dict[100] += 1
        elif count >= 50:
            thread_count_dict[50] += 1
        elif count >= 30:
            thread_count_dict[30] += 1
        elif count >= 20:
            thread_count_dict[20] += 1
        elif count >= 10:
            thread_count_dict[10] += 1
        elif count >= 5:
            thread_count_dict[5] += 1


    key_strings = []
    values = []
    for key in sorted(thread_count_dict.keys()):
        if key >= 5:
            key_strings.append(str(key) + "+")
        else:
            key_strings.append(str(key))
        values.append(thread_count_dict[key])

    color = "navy"
    if forum_id == '77':
        color = "navy"
    elif forum_id == '84':
        color = "#a17f1a"  # dark gold
    else:
        color = "maroon"

    plt.bar(key_strings, values, color=color,
            width=0.4)

    plt.xlabel("Amount of distinct users")
    plt.ylabel("Amount of threads")
    plt.title("Unique thread meaningful participation by user for forum " + str(forum_id))
    plt.show()

cursor.close()
conn.close()
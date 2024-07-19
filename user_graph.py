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

forum_ids = [1,2,3,4,5,6,7,8,9,10]
unique_user_requirement = 10

# SQL query to retrieve data
for forum_id in forum_ids:
    query = f"select p.user_id, count(p.post_id), count(distinct p.topic_id) from posts p inner join topics t on t.topic_id = p.topic_id " \
            f"where t.forum_id = {forum_id} and length(content_post) > 10 and t.classification_topic < 0.5 " \
            f"group by p.user_id"
    # Executing the query
    cursor.execute(query)

    # Fetching all the rows
    rows = cursor.fetchall()
    print(rows)
    """
    count_dict = {20:0}
    for x in rows:
        count = x[1]
        if count >= 3:
            if count >= 20:
                count_dict[20] += 1
            elif count not in count_dict:
                count_dict[count] = 1
            else:
                count_dict[count] += 1
    """
    count_dict = {5: 0, 10: 0, 20: 0, 30: 0, 50: 0, 100: 0, 200: 0, 300: 0}
    for x in rows:
        count = x[2]
        if count >= 300:
            count_dict[300] += 1
        elif count >= 200:
            count_dict[200] += 1
        elif count >= 100:
            count_dict[100] += 1
        elif count >= 50:
            count_dict[50] += 1
        elif count >= 30:
            count_dict[30] += 1
        elif count >= 20:
            count_dict[20] += 1
        elif count >= 10:
            count_dict[10] += 1
        elif count >= 5:
            count_dict[5] += 1


    key_strings = []
    values = []
    for key in sorted(count_dict.keys()):
        if key >= 20:
            key_strings.append(str(key) + "+")
        else:
            key_strings.append(str(key))
        values.append(count_dict[key])

    color = "navy"
    if forum_id == '77':
        color = "navy"
    elif forum_id == '84':
        color = "#a17f1a"  # dark gold
    else:
        color = "maroon"

    plt.bar(key_strings, values, color=color,
            width=0.4)

    plt.xlabel("Amount of posts")
    plt.ylabel("Amount of users")
    plt.title("Total posts per user for forum " + str(forum_id))
    plt.show()

cursor.close()
conn.close()
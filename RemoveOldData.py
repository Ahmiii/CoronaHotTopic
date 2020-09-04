from mysql import connector
import time
mydb=connector.connect(
    host="localhost",
    user="root",
    password="",
    database="CoronaTweets",
    charset='utf8'
)

def Update(rows,mycursor):
    print(rows)
    if (rows>0):
        time.sleep(3)
        mycursor.execute("DELETE FROM CoronaTweetData ORDER BY created_at LIMIT ")
        rows=mycursor.rowcount
        mydb.commit()
        return Update(rows,mycursor)
    else:
        mydb.close()
        return False

if __name__ == "__main__":
    mycursor=mydb.cursor()
    mycursor.execute("DELETE FROM CoronaTweetData ORDER BY created_at LIMIT 1")
    rows=mycursor.rowcount
    Update(rows,mycursor)

import MySQLdb

db = MySQLdb.connect(host="den1.mysql2.gear.host",    # your host, usually localhost
                     user="iatestsb4",         # your username
                     passwd="At05Ays2~WE-",  # your password
                     db="iatestsb4")        # name of the data base
print "Connected"
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Create Questions table query
questions = "CREATE TABLE Questions (" \
            + "Id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
            + "Field INT(6) UNSIGNED NOT NULL," \
            + "DifficultyLevel INT(6) UNSIGNED NOT NULL," \
            + "Statememnt VARCHAR(500)," \
            + "Type VARCHAR(50)" \
            + ")"

#Create Answers table query
answers = "CREATE TABLE Answers (" \
        + "Id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
        + "QuestionId INT(6) UNSIGNED NOT NULL," \
        + "Statememnt VARCHAR(50)," \
        + "IsValid TINYINT(1)" \
        + ") "
#Create Fields table query
fields = "CREATE TABLE Fields (" \
        + "Id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
        + "Name VARCHAR(50)" \
        + ")"


cur.execute(questions)
print "Questions created"

cur.execute(answers)
print "Answers created"

cur.execute(fields)
print "Fields created"

# print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

db.close()
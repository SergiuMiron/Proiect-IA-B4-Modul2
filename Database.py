import MySQLdb

db = MySQLdb.connect(host="den1.mysql2.gear.host",    # your host, usually localhost
                     user="iatestsb4",         # your username
                     passwd="At05Ays2~WE-",  # your password
                     db="iatestsb4")        # name of the data base
print "Connected"
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# delete all tables
cur.execute("DROP TABLE Questions")
print "Questions dropped"

cur.execute("DROP TABLE Answers")
print "Answers dropped"

cur.execute("DROP TABLE Domains")
print "Domains dropped"

cur.execute("DROP TABLE DomainsHierarchy")
print "DomainsHierarchy dropped"


# Create Questions table query
questions = "CREATE TABLE Questions (" \
            + "id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
            + "domain_id BIGINT(20) UNSIGNED," \
            + "difficulty INT(11) UNSIGNED NOT NULL," \
            + "body VARCHAR(500) NOT NULL," \
            + "question_type INT(11)," \
            + "expected_secs_to_answer INT(11) NOT NULL" \
            + ")"

#Create Answers table query
answers = "CREATE TABLE Answers (" \
        + "id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
        + "question_id INT(6) UNSIGNED NOT NULL," \
        + "body VARCHAR(500)," \
        + "is_correct TINYINT(1)" \
        + ")"
#Create Fields table query
domains = "CREATE TABLE Domains (" \
        + "id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
        + "name VARCHAR(50) NOT NULL" \
        + ")"

domainsHierarchy = "CREATE TABLE DomainsHierarchy (" \
        + "id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
        + "current BIGINT(20) UNSIGNED NOT NULL," \
        + "subdomain BIGINT(20) UNSIGNED NOT NULL" \
        + ")"

cur.execute(questions)
print "Questions created"

cur.execute(answers)
print "Answers created"

cur.execute(domains)
print "Domains created"

cur.execute(domainsHierarchy)
print "Domains Hierarchy created"
# print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

db.close()
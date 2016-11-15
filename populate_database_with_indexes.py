import mysql.connector
from CapstoneProject.settings import DATABASES


def populate_databae_with_indexes(index_name, index_file):
    conn = mysql.connector.connect(user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'], database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
    cursor = conn.cursor()
    cursor.execute("SELECT id from indexes where index_name='"+index_name+"'")
    q = cursor.fetchall()
    if len(q)==0:
        cursor.execute("INSERT INTO indexes (`index_name`) VALUES ('"+index_name+"')")
        conn.commit()
    f = open(index_file, 'r')
    for line in f:
        ticker = line.split("\t")[0]
        company_name = line.split("\t")[1].replace("'","''")
        cursor.execute("select * from security where yahoo_ticker='"+ticker+"' and sec_name='"+company_name+"'")
        q = cursor.fetchall()
        if len(q)==0:
            q1 = "insert into security (`yahoo_ticker`,`sec_name`) VALUES ('"+ticker+"','"+company_name+"')"
            cursor.execute(q1)
            conn.commit()
            q2 = "insert into constituents (`index_id`,`sec_id`) VALUES ((select id from indexes where index_name='"+index_name+"'),(select id from security where yahoo_ticker='"+ticker+"' and sec_name='"+company_name+"'))"
            cursor.execute(q2)
    conn.commit()
    conn.close()


populate_databae_with_indexes("FTSE100", "Indexes/FTSE100.tsv")
populate_databae_with_indexes("S&P500", "Indexes/SNP500.tsv")
populate_databae_with_indexes("NIFTY50", "Indexes/NIFTY50.tsv")



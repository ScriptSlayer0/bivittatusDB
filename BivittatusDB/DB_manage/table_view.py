import BivittatusDB as bdb

def use_table():
    #load existing database
    db=bdb.database("test").use()

    #pull table from database to use
    tb1=db.load_table("table1")

    print(tb1)
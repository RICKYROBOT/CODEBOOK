import sqlite3

def connect():
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    conn.commit()
    conn.close()

def addCategory(name):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("create table if not exists " + name + "(id int primary key, ""name text, code text)")
    conn.commit()
    conn.close()

def getCategories():
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    return(cur.fetchall())

def getSnipets(category):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("SELECT name FROM " + category)
    return(cur.fetchall())

def addSnipet(category, codeName):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO " + category + " VALUES (NULL, ?, ?)", (codeName, ""))
    conn.commit()
    conn.close()

def updateCode(category, codeName, code):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("UPDATE " + category + " SET code=? WHERE name=?", (code, codeName))
    conn.commit()
    conn.close()

def renamecategory(currentName, newName):
    conn = sqlite3.connect("codes.db")
    cur = conn.cursor()
    cur.execute("ALTER TABLE " + currentName + " RENAME TO " + newName)
    conn.commit()
    conn.close()

def renamesnip(category, currentName, newName):
    conn = sqlite3.connect("codes.db")
    cur = conn.cursor()
    cur.execute("UPDATE " + category + " SET name=? WHERE name=?", (newName, currentName))
    conn.commit()
    conn.close()

def removeCat(category):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("DROP TABLE IF EXISTS " + category)
    conn.commit()
    conn.close()

def removeSnip(category, Snip):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM " + category + " WHERE name='" + Snip +"'")
    conn.commit()
    conn.close()

def getCode(category, name):
    conn=sqlite3.connect("codes.db")
    cur=conn.cursor()
    cur.execute("SELECT * from " + category)
    List = cur.fetchall()
    for entries in List:
        if (entries[1] == name):
            return(entries[2])
# move hongbao amount from allowance to user's online pay 
#  fetch all the hongbao
#    update bill: add hongbao to onlinepay and deduct hongbao from allowance
#

import MySQLdb as mdb
import sys


try:
    dbhost = "172.16.10.24"
    dbuser = "eleme"
    dbpass = "eleMe"
    dbname = "hydros"

    con = mdb.connect(dbhost, dbuser,dbpass,dbname)
    
    cur = con.cursor()
    cur.execute("SELECT id, bill_id, amount FROM `tbl_bill_promotion` where promotion_type_id = '0hongbao' and amount > 0;")
    
    print "get all hongbao"
    #print 'there has %s rows record' % count

    rows = cur.fetchall()

    conupdate = mdb.connect(dbhost, dbuser,dbpass,dbname)
    curupdate = conupdate.cursor()

    for row in rows:
        try:
            allownanceId, billid, hongbaoamount  = row


            print "hongbao amount %d" % hongbaoamount

            curupdate.execute("update tbl_bill set online_pay_amount = online_pay_amount+%d, eleme_allowance_amount = eleme_allowance_amount - %d where id = %d" % (hongbaoamount,hongbaoamount,billid))
            curupdate.execute("update tbl_bill_promotion set amount = 0 where id = %d" % (allownanceId))

            conupdate.commit()

        except mdb.Error, e:
            if conupdate:
                conupdate.rollback();
            raise mdb.Error
    
    if conupdate:
        conupdate.close()
    

    if con:
        con.close()

except mdb.Error, e:
  
    try:
        if con:
            con.rollback()
    except Exception, ex:
        pass
        
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    

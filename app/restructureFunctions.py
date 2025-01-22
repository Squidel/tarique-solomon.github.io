from app_config import db
import uuid 

def updateExistingTables_withGUID(table1, table2):
    print("Entered updateExistingTables_withGUID function")

    cursor = None
    
    try:
        db.autocommit(False)

        cursor = db.cursor()
        query = f"SELECT COUNT(*) AS row_count FROM {table1}"
        cursor.execute(query)
        row_count = cursor.fetchone()[0]

        for i in range(row_count+1):
            guid_string = str(uuid.uuid4())
            query1 = f"UPDATE `{table1}` SET guid = %s WHERE id = %s"
            query2 = f"UPDATE `{table2}` SET guid = %s WHERE id = %s"
            cursor.execute(query1, (guid_string, i + 1))
            cursor.execute(query2, (guid_string, i + 1))
        
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"ERROR: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        print("Exiting updateExistingTables_withGUID function")

#updateExistingTables_withGUID('PureMoneyChristmas_Forms', 'PureMoneyChristmas_Submissions')

def addGUIDto_ExistingTable(table):
    print("Entered addGUIDto_ExistingTable function")

    cursor = None
    
    try:
        db.autocommit(False)

        cursor = db.cursor()

        query = f"SELECT form_submission_id FROM {table}"
        cursor.execute(query)
        form_submission_ids = cursor.fetchall()

        for form_submission_id in form_submission_ids:
            guid_string = str(uuid.uuid4())
            query = f"UPDATE `{table}` SET id = %s WHERE form_submission_id = %s"
            cursor.execute(query, (guid_string, form_submission_id))
        
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"ERROR: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        print("Exiting addGUIDto_ExistingTable function")

#addGUIDto_ExistingTable('Promotions_Submission_References')
import random, sys, logging, uuid
from app_config import db

logging.basicConfig(filename='logs/winners.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

class Participant:
    def __init__(self, full_name, phone_num, email_addr, reference_number):
        self.full_name = full_name
        self.phone_num = phone_num
        self.email_addr = email_addr
        self.reference_number = reference_number

    def __str__(self):
        return f"Participant: {self.full_name}, Phone: {self.phone_num}, Email: {self.email_addr}, Ref #: {self.reference_number}"

def selectWinnerPool_usingPromotionID(id):
    cursor = None
    try:
        cursor = db.cursor()
        query = "SELECT promotion_name FROM Promotion_Names WHERE id = %s;"
        cursor.execute(query, id)
        promotion_name = cursor.fetchone()
        if promotion_name:
            promotion_name = promotion_name[0]
            logging.info(f"Promotion name obtained: {promotion_name}")
            
            try:
                num_winners = int(sys.argv[2])
                logging.info("Obtaining names of participants")
                query = """
                    SELECT CONCAT(pfs.first_name, ' '  , pfs.last_name) AS full_name, pfs.phone_num, pfs.email_addr, psr.reference_number
                    FROM Promotions_Form_Submissions as pfs
                    INNER JOIN Promotions_Submission_References as psr 
                    ON pfs.id = psr.form_submission_id
                    WHERE pfs.promotion_id = %s; 
                """   
                logging.info("About to execute query")
                cursor.execute(query, id)
                logging.info("Query executed")
                participants = cursor.fetchall()
                logging.info(f"Participant Data: {participants}")
                if participants:
                    participants_objects = [Participant(*participant_data) for participant_data in participants]
                    winners = select_winners(participants_objects, num_winners)
                    for winner in winners:
                        logging.info(winner)
                        save_winner(db, winner, id)
                
                else:
                    logging.error("No participant data obtained")


            except ValueError:
                logging.critical("Invalid type for number of winners. Please provide a valid integer.")
                raise

            except Exception as e:
                logging.error(f"Some other error occured when getting names of participants: {str(e)}")
                raise

    except Exception as e:
        logging.error(f"Error within selectWinnerPool_usingPromotionID: {str(e)}")

    finally:
        if cursor:
            cursor.close()


def select_winners(participants, num_winners):
    participants_copy = participants.copy()
    random.shuffle(participants_copy)
    winners = participants_copy[:num_winners]
    return winners

def save_winner(db, winner, id):
    cursor = None
    db.autocommit(False)
    try:
        cursor = db.cursor()
        query = """
            INSERT INTO Promotion_Winners (promotion_winner_id, promotion_id, reference_number)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (str(uuid.uuid4()), id, winner.reference_number))
        db.commit()
    
    except Exception as e:
        db.rollback()
        logging.error(f"An error occured when saving the winner: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
            db.autocommit(True)



def main():
    if len(sys.argv) != 3:
        print("USAGE: python generateWinners.py <promotion_id> <number_of_winners>")
        sys.exit(1)

    try:
        promotion_id = int(sys.argv[1])
        print(promotion_id)
        selectWinnerPool_usingPromotionID(promotion_id)

    except ValueError:
        logging.critical("Invalid promotion ID. Please provide a valid integer.")
        sys.exit(1)


if __name__ == "__main__":
    main()

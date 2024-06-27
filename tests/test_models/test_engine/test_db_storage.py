import unittest
import MySQLdb
from console import HBNBCommand
from models import storage

class TestDBStorage(unittest.TestCase):
    
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_create_state(self):
        """Test create state command adds a new state to the database"""
        # Connect to the database
        db = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = db.cursor()
        
        # Get initial number of states
        cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = cursor.fetchone()[0]
        
        # Execute console command to create new state
        console = HBNBCommand()
        console.onecmd('create State name="California"')
        
        # Get updated number of states
        cursor.execute("SELECT COUNT(*) FROM states")
        updated_count = cursor.fetchone()[0]
        
        # Close database connection
        cursor.close()
        db.close()
        
        # Assert that the number of states has increased by 1
        self.assertEqual(updated_count, initial_count + 1)

if __name__ == "__main__":
    unittest.main()


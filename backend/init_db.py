from database.database import engine, Base 
from models.user import User 
from models.movie import Movie 
from models.booking import Booking 
import logging 
 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
 
def init_database(): 
    logger.info("Creating database tables...") 
    Base.metadata.create_all(bind=engine) 
    logger.info("Database tables created successfully!") 
 
if __name__ == "__main__": 
    init_database() 

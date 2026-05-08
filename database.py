# database.py
import csv
import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Uses ENV variable if available, otherwise defaults to local Windows port
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@127.0.0.1:5433/shoestore")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Shoe(Base):
    __tablename__ = "shoes"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    size = Column(Float)
    price = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    shoe_id = Column(Integer)
    quantity = Column(Integer, default=1)
    status = Column(String, default="Confirmed")

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if database is empty to inject test data from CSV
    if db.query(Shoe).count() == 0:
        csv_file_path = "shoes_inventory.csv"
        
        if os.path.exists(csv_file_path):
            print(f"Populating database from {csv_file_path}...")
            shoes_to_insert = []
            
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    shoes_to_insert.append(
                        Shoe(
                            brand=row['brand'],
                            model=row['model'],
                            size=float(row['size']),
                            price=float(row['price']),
                            stock=int(row['stock'])
                        )
                    )
            
            # Bulk insert all shoes at once for better performance
            db.add_all(shoes_to_insert)
            db.commit()
            print(f"Successfully inserted {len(shoes_to_insert)} shoes into the database!")
        else:
            print(f"Warning: {csv_file_path} not found. Could not seed the database.")
            
    else:
        print("Database already contains data. Skipping initialization.")
        
    db.close()

if __name__ == "__main__":
    init_db()


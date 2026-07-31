from app import create_app
from scripts.seed import seed_users,seed_ports,seed_vessels,seed_shipments,seed_containers,seed_tasks

app = create_app()

with app.app_context():

    seed_users()

    seed_ports()
    
    seed_vessels()
    seed_shipments()
    seed_containers()
    seed_tasks()

    print("Database Seed Completed")
# from app import app
from models import db, Node, NodeProperty
from datetime import datetime

def seed_data():
    # with app.app_context(): 
    # Create nodes
    nodes = [
        Node(id=1, name="Intrepid", parent_id=None, created_at=datetime.now()),
        Node(id=2, name="Bus", parent_id=1, created_at=datetime.now()),
        Node(id=3, name="Thruster1", parent_id=2, created_at=datetime.now()),
        Node(id=4, name="Thruster2", parent_id=2, created_at=datetime.now()),
        Node(id=5, name="Thruster3", parent_id=2, created_at=datetime.now()),
        Node(id=6, name="Payload", parent_id=1, created_at=datetime.now()),
        Node(id=7, name="DarkmatterCamera", parent_id=6, created_at=datetime.now())
    ]

    # Create node properties
    properties = [
        NodeProperty(id=1, key="Mass", value=124.00, node_id=1, created_at=datetime.now()),
        NodeProperty(id=2, key="Thrust", value=9.493, node_id=3, created_at=datetime.now()),
        NodeProperty(id=3, key="ISP", value=12.156, node_id=3, created_at=datetime.now()),
        NodeProperty(id=4, key="Thrust", value=9.413, node_id=4, created_at=datetime.now()),
        NodeProperty(id=5, key="ISP", value=11.632, node_id=4, created_at=datetime.now()),
        NodeProperty(id=6, key="Thrust", value=9.899, node_id=5, created_at=datetime.now()),
        NodeProperty(id=7, key="ISP", value=12.551, node_id=5, created_at=datetime.now()),
        NodeProperty(id=8, key="Exposure", value=1.622, node_id=7, created_at=datetime.now()),
        NodeProperty(id=9, key="Sensitivity", value=15.11, node_id=7, created_at=datetime.now())
    ]

    # Add to database
    print("********Start Seeding************")
    db.session.bulk_save_objects(nodes)
    db.session.bulk_save_objects(properties)
    db.session.commit()
    print("********End Seeding************")
if __name__ == '__main__':
    seed_data()




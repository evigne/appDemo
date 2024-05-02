from flask import Flask, jsonify, request
from models import db, Node
from config import create_app
from utils import add_node, insert_property, build_subtree
from seed_database import seed_data
from werkzeug.serving import is_running_from_reloader

app = create_app()
# app = Flask(__name__)
# CORS(app)
# app.config.from_object(Config)
# db.init_app(app)

@app.route('/create_node', methods=['POST'])
def create_node():
    data = request.get_json(force=True)
    name = data.get('name')
    parent_id = data.get('parent_id')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    node = add_node(name, parent_id)
    if not node:
        return jsonify({'error': 'Unexpected Error'}), 500
    else:
        return jsonify({'message': 'Node created', 'id': node.id}), 201


@app.route('/add_property', methods=['POST'])
def add_property():
    data = request.get_json(force=True)
    node_id = data.get('node_id')
    key = data.get('key')
    value = data.get('value')

    if not all([node_id, key, value]):
        return jsonify({'error': 'Node ID, key, and value are required'}), 400

    node = Node.query.get(node_id)
    if not node:
        return jsonify({'error': 'Node not found'}), 404

    insert_property(key, value, node_id)

    return jsonify({'message': 'Property added'}), 201


@app.route('/get_subtree/<path:node_path>', methods=['GET'])
def get_subtree(node_path):
    nodes = [node.capitalize() for node in node_path.split('/')]
    root_nodes = Node.query.filter(Node.name.startswith(nodes[0])).all()

    if not root_nodes:
        return jsonify({'error': 'Root node not found'}), 404
    subtrees = [build_subtree(root_node, nodes[1:]) for root_node in root_nodes]
    return jsonify(subtrees)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not is_running_from_reloader():
            seed_data()
    app.run(host="0.0.0.0",debug=True)

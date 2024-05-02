from models import db, Node, NodeProperty


def add_node(name, parent_id):
    node = Node(name=name, parent_id=parent_id)
    db.session.add(node)
    db.session.commit()
    return node


def insert_property(key, value, node_id):
    node_property = NodeProperty(key=key, value=value, node_id=node_id)
    db.session.add(node_property)
    db.session.commit()
    return node_property


def get_children(node):
    children = []
    for child in node.children:
        children.append({
            'name': child.name,
            'created_at': child.created_at,
            'properties': [{'key': prop.key, 'value': str(prop.value),'created_at': prop.created_at} for prop in child.properties],
            'children': get_children(child),

        })
    return children


def build_subtree(node, remaining_path):
    subtree = {
        'name': node.name,
        'created_at': node.created_at,
        'properties': [{'key': prop.key, 'value': str(prop.value),  'created_at': prop.created_at} for prop in node.properties],
        'children': []
    }

    if remaining_path:
        for child in node.children:
            if child.name.startswith(remaining_path[0]):
                subtree['children'].append(build_subtree(child, remaining_path[1:]))
    else:
        subtree['children'] = get_children(node)

    return subtree

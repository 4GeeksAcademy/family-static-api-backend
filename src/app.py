"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson") # es una clase

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# endpoints siiiii
@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()

        if members == []:
            return jsonify({"Error": "Members not found"}), 404
        return jsonify(members), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# obtener la info de un solo member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        a_member = jackson_family.get_member(member_id)
        if a_member == 'Member not found':
            return jsonify({'error':'Member not found'}), 404
        return jsonify(a_member), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message':str(e)}), 500
@app.route('/member', methods=['POST'])
def add_new_member():
    try:
        member = request.get_json()
        if not member:
            return jsonify({'error':'Invalid information'}), 400
        update_members = jackson_family.add_member(member)
        return jsonify(update_members), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message':str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        delete_member = jackson_family.delete_member(member_id)
        if not delete_member:
            return jsonify({'error':'Member not found'}), 404
        return jsonify({'done': True}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message':str(e)}), 500
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

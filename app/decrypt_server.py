from flask import Blueprint, request, jsonify
import gnupg
import json
from os import path

# Create a blueprint
decrypt_bp = Blueprint('decrypt_bp', __name__)

# Initialize GPG
gpg_home = path.abspath('./encryption')
gpg = gnupg.GPG(gnupghome=gpg_home)

@decrypt_bp.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        encrypted_data = request.json['data']
        passphrase = "1password"  # Avoid hardcoding in production
        decrypted_data = gpg.decrypt(encrypted_data, passphrase=passphrase)

        if not decrypted_data.ok:
            return jsonify({'error': 'Decryption failed', 'status': decrypted_data.status}), 400

        # Assuming decrypted data is a JSON string, parse it before sending
        decrypted_json = json.loads(str(decrypted_data))
        return jsonify(decrypted_json), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Decryption successful but JSON parsing failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

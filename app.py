from flask import Flask, request, jsonify, render_template
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.types import InputPhoneContact

app = Flask(__name__)

# তোমার API ডিটেইলস
api_id = 29431487
api_hash = 'e0f02d4f0ae012ec495adcd1789936d3'
session_name = 'heycheck_session'

client = TelegramClient(session_name, api_id, api_hash)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_telegram():
    phone_numbers = request.form['numbers'].splitlines()
    phone_contacts = [InputPhoneContact(client_id=i, phone=phone.strip(), first_name="User", last_name="Check")
                      for i, phone in enumerate(phone_numbers)]

    with client:
        result = client(ImportContactsRequest(phone_contacts))
        users = result.users

        found_numbers = [user.phone for user in users]
        results = []
        for num in phone_numbers:
            clean_num = num.strip().replace('+', '').replace(' ', '')
            if clean_num in found_numbers:
                results.append({'number': num, 'telegram': True})
            else:
                results.append({'number': num, 'telegram': False})

        client(DeleteContactsRequest(id=users))

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

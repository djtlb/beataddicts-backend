import os, uuid, stripe, soundfile as sf
from flask import Flask, request, jsonify, send_file, abort
from generate_song import generate_song
from generate_dj_drop import generate_dj_drop
from split_stems import split_stems
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

stripe.api_key = os.getenv('STRIPE_SECRET')
PLATINUM_PRICE_ID = os.getenv('PLATINUM_PRICE_ID')

@app.route('/generate_song', methods=['POST'])
def handle_generate_song():
    prompt = request.json.get('prompt', 'Chill trap beat')
    audio = generate_song(prompt)
    filename = f'static/outputs/{uuid.uuid4().hex}.wav'
    sf.write(filename, audio.T, 32000)
    return send_file(filename, as_attachment=True)

@app.route('/generate_dj_drop', methods=['POST'])
def handle_dj_drop():
    text = request.json.get('text', 'You are locked in with Beat Addicts')
    path = generate_dj_drop(text)
    return send_file(path, as_attachment=True)

@app.route('/split_stems', methods=['POST'])
def handle_split_stems():
    if 'file' not in request.files:
        return jsonify({'error': 'Missing file'}), 400
    f = request.files['file']
    filepath = f'static/uploads/{uuid.uuid4().hex}.wav'
    f.save(filepath)
    output = split_stems(filepath)
    return jsonify({'stems': output})

@app.route('/export_daw', methods=['POST'])
def export_daw():
    customer_id = request.json.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Missing Stripe customer_id'}), 400
    try:
        subs = stripe.Subscription.list(customer=customer_id, status='active')
        for sub in subs.auto_paging_iter():
            for item in sub['items']['data']:
                if item['price']['id'] == PLATINUM_PRICE_ID:
                    return send_file('daw_templates/musicgen_template.als', as_attachment=True)
        return abort(403)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

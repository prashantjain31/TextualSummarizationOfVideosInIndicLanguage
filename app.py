from flask import Flask, request, jsonify, make_response
import main
from flask_cors import CORS
import base64
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process_youtube', methods=['POST'])
def process_youtube():
    data = request.json
    youtube_url = data.get('youtube_url')
    target_language = data.get('target_language')

    try:
        # Download audio from YouTube
        main.download_youtube_audio(youtube_url)

        # Transcribe audio
        main.transcribe_audio()

        # Summarize text
        summary = main.summarize_txt()

        # Translate summary
        translated_summary = main.translate(target_language, summary)

        # Save translated summary as audio
        main.save_summary_as_audio(translated_summary, target_language)

        # Read audio file as bytes
        audio_file_path = "./summary.wav"
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        # Send the audio file and translated summary back to the frontend
        # response = make_response(jsonify({
        #     'message': 'Process completed successfully',
        #     'translated_summary': translated_summary
        # }), 200)
        
        # response.headers['Content-Disposition'] = f"attachment; filename=summary.wav"
        # response.headers['Content-Type'] = 'audio/wav'
        # response.set_data(audio_data)
        # return response
        return jsonify({
            'message': 'Process completed successfully',
            'translated_summary': translated_summary,
            'audio_file': audio_base64
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
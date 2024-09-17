# /backend/routes/main.py

from flask import Blueprint, request, jsonify
from services.youtube_service import get_video_id, get_video_metadata, check_captions_available, download_audio

main = Blueprint('main', __name__)

@main.route('/process_video', methods=['POST'])
def process_video():
    data = request.get_json()
    video_url = data.get('video_url')

    try:
        video_id = get_video_id(video_url)
        metadata = get_video_metadata(video_id)
        captions_available = check_captions_available(video_id)

        # For now, we'll just return the metadata and captions availability
        response = {
            'video_id': video_id,
            'metadata': metadata,
            'captions_available': captions_available
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

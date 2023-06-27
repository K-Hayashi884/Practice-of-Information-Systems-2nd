from youtube_transcript_api import YouTubeTranscriptApi


# video_idを渡すと、対応する動画の字幕をとってくる関数
# 返り値：以下の形のdictがたくさん入ったlist
# {'text': 字幕本体(str), 'start': 開始秒数(float), 'duration': 持続時間(float)}
def get_youtube_transcript(video_id: str):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id=video_id)
    transcript = transcript_list.find_transcript(['ja', 'en'])
    return transcript.fetch()





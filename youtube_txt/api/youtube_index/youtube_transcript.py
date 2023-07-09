from youtube_transcript_api import YouTubeTranscriptApi
from youtube_index import transcript_data_to_index


# video_idを渡すと、対応する動画の字幕をとってくる関数
# 返り値：以下の形のdictがたくさん入ったlist
# {'text': 字幕本体(str), 'start': 開始秒数(float), 'duration': 持続時間(float)}
def get_youtube_transcript(video_id: str):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id=video_id)
    transcript = transcript_list.find_transcript(['ja', 'en'])
    return transcript.fetch()


def extract_text(transcript_list):
    transcript = ""
    for t in transcript_list:
        transcript += t["text"] + " "
    return transcript


# 秒で返ってくる値を、HH:MM:SS形式に変換
def seconds_to_hh_mm_ss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours == 0:
        time_str = f"{minutes:01d}:{seconds:02d}"
    else:
        time_str = f"{hours:01d}:{minutes:02d}:{seconds:02d}"
    return time_str


# video_idを受け取り、目次を生成する
# flutter側に供給するためのもの
def videoid_to_index(video_id: str):
    transcript_list = get_youtube_transcript(video_id=video_id)

    indices = transcript_data_to_index(transcript_data=transcript_list)

    # { “video”: dict
    #     {“id”: 動画のid, (string)
    #     “url”: 動画のurl, (string)
    #     “title”: 動画のタイトル (string) },
    #     “indices”: list<dict>   # 目次のリスト
    #         [ { “timestamp”: 時刻（text   10:55  など）
    #         “headline”: GPTで生成した見出し   (string)
    #     } ]
    #             “comments”:  list<dict>  　　# オプション。時刻リンクを含んだコメント
    #         [ { “text”: 時刻リンクを含むコメント本文 (string) } ]
    # }

    return {
        "video": {
            "video_id": video_id,
            "url": "video_url(now inplementing ...)",
            "title": "video_title(now inplementing ...)",
            "indices": [
                {"timestamp": seconds_to_hh_mm_ss(i["timestamp"]),
                 "headline": i["headline"]}for i in indices],
            "comments": ["this is optional. (now implementing ...)"]
        },
    }


# video_idを受け取り、目次を生成する
# タイムスタンプをfloatで保存
def videoid_to_floated_index(video_id: str):
    transcript_list = get_youtube_transcript(video_id=video_id)

    indices = transcript_data_to_index(transcript_data=transcript_list)

    # { “video”: dict
    #     {“id”: 動画のid, (string)
    #     “url”: 動画のurl, (string)
    #     “title”: 動画のタイトル (string) },
    #     “indices”: list<dict>   # 目次のリスト
    #         [ { “timestamp”: 時刻（float 10.55 (sec)  など）
    #         “headline”: GPTで生成した見出し   (string)
    #     } ]
    #             “comments”:  list<dict>  　　# オプション。時刻リンクを含んだコメント
    #         [ { “text”: 時刻リンクを含むコメント本文 (string) } ]
    # }

    return {
        "video": {
            "video_id": video_id,
            "url": "video_url(now inplementing ...)",
            "title": "video_title(now inplementing ...)",
            "indices": indices,
            "comments": ["this is optional. (now implementing ...)"]
        },
    }

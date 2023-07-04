from youtube_transcript_api import YouTubeTranscriptApi
from youtube_index import split_paragraph
from youtube_index import identify_timestamp
from youtube_index import transcript_to_index


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


# video_idを受け取り、目次を生成する
def videoid_to_index(video_id: str):
    transcript_list = get_youtube_transcript(video_id=video_id)

    # プロンプト生成
    prompt_transcript = ""
    prompt_transcript2 = ""
    for i, t in enumerate(transcript_list):
        prompt_transcript += (
            "start: " + str(t["start"]) +
            " text: " + t["text"] + ", "
        )
        prompt_transcript2 += t["text"]

    splitted_transcript = split_paragraph(prompt_transcript2)

    time_and_script = identify_timestamp(transcript_list, splitted_transcript)

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

    indices = transcript_to_index(time_and_script)

    return {
        "video": {
            "video_id": video_id,
            "url": "video_url(now inplementing ...)",
            "title": "video_title(now inplementing ...)",
            "indices": [
                {"timestamp": i["start"], "headline": i["text"]}
                for i in indices
            ],
            "comments": ["this is optional. (now implementing ...)"]
        },
    }


# # 20分：8QJZSjAgEqs
# # １分: Osg_WYVV6bU
# # transcript_list = get_youtube_transcript("8QJZSjAgEqs")
# transcript_list = get_youtube_transcript("Osg_WYVV6bU")
# # print(extract_text(transcript_list))

# # プロンプト生成
# prompt_transcript = ""
# prompt_transcript2 = ""
# for i, t in enumerate(transcript_list):
    # prompt_transcript += (
    #     "start: " + str(t["start"]) +
    #     " text: " + t["text"] + ", "
    # )
#     prompt_transcript2 += t["text"]

# # print(prompt_transcript)
# # print(prompt_transcript2)

# splitted_transcript = split_paragraph(prompt_transcript2)
# print(splitted_transcript)

# time_and_script = identify_timestamp(transcript_list, splitted_transcript)

# print(transcript_to_index(time_and_script))

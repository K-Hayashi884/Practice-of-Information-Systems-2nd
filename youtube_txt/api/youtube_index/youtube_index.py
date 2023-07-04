import json
import openai


def split_paragraph(transcript: str):
    # 空白区切りなしで文章を連結したトランスクリプトを入力として受け取る
    # keys.jsonファイルのパスを指定
    json_file_path = "keys.json"

    # ファイルを開いて内容を読み込む
    with open(json_file_path, "r") as json_file:
        # JSONデータをデコードしてPythonオブジェクトに変換
        data = json.load(json_file)

    # 読み込んだデータを利用する（例：キーを指定して値を取得する）
    OPENAI_API_KEY = data["OPENAI_API_KEY"]

    openai.organization = "org-kaiK6XlzhOWBRvhZnZ40LYvq"
    openai.api_key = OPENAI_API_KEY

    prompt = (transcript + "　段落ごとに分割してlist[\"text1\", \"text2\", \"text3\"]形式で出力:")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": prompt}
            ]
    )
    print(response)
    # 文字列で返ってきたリストをlist型に変換
    eval_list = eval(
        response["choices"][0]["message"]["content"]
        .replace("。", ".").replace("、", ",")
    )
    return eval_list


def identify_timestamp(time_transcript, splitted_transcript):
    i = 0
    time_script_pairs = []
    for split in splitted_transcript[i:]:
        for j, time in enumerate(time_transcript):
            if split.startswith(time["text"]):
                time_script_pairs.append({"start": time["start"], "text": time["text"]})
                i = j
    return time_script_pairs


def transcript_to_index(timescripts):
    # timescript: identify_timestampの出力を

    # keys.jsonファイルのパスを指定
    json_file_path = "keys.json"

    # ファイルを開いて内容を読み込む
    with open(json_file_path, "r") as json_file:
        # JSONデータをデコードしてPythonオブジェクトに変換
        data = json.load(json_file)

    # 読み込んだデータを利用する（例：キーを指定して値を取得する）
    OPENAI_API_KEY = data["OPENAI_API_KEY"]

    openai.organization = "org-kaiK6XlzhOWBRvhZnZ40LYvq"
    openai.api_key = OPENAI_API_KEY

    responses = []

    for timescript in timescripts:

        prompt = (timescript["text"] + "#入力 ネタバレにならない見出しを一文で生成 #出力 ")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": prompt}
                ]
        )

        responses.append(
            {"start": timescript["start"], 
             "text": response["choices"][0]["message"]["content"]}
        )

    return responses

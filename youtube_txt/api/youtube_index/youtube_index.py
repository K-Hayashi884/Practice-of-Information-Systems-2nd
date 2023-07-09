import json
import openai
import pprint


# 長い文字列をchunk_size字ごとに区切る
def split_string(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


# transcriptの段落分けを行い、分割結果とタイトルを取得
# また
def transcript_data_to_index(transcript_data: list):
    print("## transcript_data:")
    pprint.pprint(transcript_data)
    # youtube-transcript-apiで取得したデータを入力
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
    eval_lists = []

    # 長すぎる入力をカット（1分ごとにカット）
    splitted_strings = []
    tmp_text = ""
    split_second_counter = 0
    for t in transcript_data:
        tmp_text += t["text"]
        if int(t["start"]) / 120 > split_second_counter and len(tmp_text) > 200:
            splitted_strings.append(tmp_text)
            tmp_text = ""
            split_second_counter += 1
    splitted_strings.append(tmp_text)
    pprint.pprint("splitted strings: " + str(splitted_strings))

    # GPTにプロンプトを投げる部分
    for transcript in splitted_strings:
        prompt = (
            transcript +
            " 段落ごとに分割してその最初の10文字と最後の10文字、ネタバレにならないタイトル10文字以内を" +
            "dictのlist[{\"start_text\": , \"end_text\": , \"headline\": }]" +
            "形式で出力:"
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": prompt}
                ]
        )

        # 文字列で返ってきたリストをlist型に変換
        print(response["choices"][0]["message"]["content"])
        try:
            eval_list = eval(
                response["choices"][0]["message"]["content"]
                .replace("。", ".").replace("、", ",")
            )
        except SyntaxError:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "user", "content": prompt}
                    ]
            )
            eval_list = eval(
                    response["choices"][0]["message"]["content"]
                    .replace("。", ".").replace("、", ",")
                )

        eval_lists += eval_list
    print("eval_lists: ", eval_lists)
    pprint.pprint(eval_lists)

    # # デバッグ用
    # # GPTに投げるリクエスト節約
    # eval_lists = [{'start_text': 'こんにちは皆さん演習ですこのチャ', 'end_text': 'お話しさせていただきます', 'headline': '岩手山噴火未遂事件'}, {'start_text': '西ノ島がすごい理由', 'end_text': '最新の大きさ', 'headline': '西ノ島の最新の大きさは国分の大きさ'}, {'start_text': '西ノ島がすごい理由', 'end_text': '最新の大きさ', 'headline': '西ノ島の最新の大きさは琵琶湖をまるまる国分'}, {'start_text': '西ノ島がすごい理由', 'end_text': '最新の大きさ', 'headline': '西ノ島の最新の大きさは国分です'}, {'start_text': '西ノ島がすごい理由', 'end_text': '最新の大きさ', 'headline': '西ノ島の最新の大きさは琵琶湖ぐらい'}, {'start_text': '西ノ島がすごい理由', 'end_text': '最新の大きさ', 'headline': '西ノ島の最新の大きさは琵琶湖くらい'}, {'start_text': '熱々の火山ガスが出ているためにこのように濁っているわけですねそしてこの1973年9月14日に濁っている場所から噴火が発生いたしましたそしてこの噴火によって西の島の次男が産声をあげたわけなんですねそして誕生しましたはいで1973年はねこんな形でしたが1974年には蛇のような形になっていたということですね大きさは0.07平方キロメートルから0.32m2に拡大いたしましたでちょっとですねこの1974年の姿をスケッチとってみますとまずはフライドチキンのところが長男ですねそしてエビのようなところがですね次男であるということになりますはいというわけでこのように長男と次男が合体していた状況だったんですねそしてその後西ノ島ですねしばらく噴火をお休みいたします噴火をお休みするんですけども島の形はですね行きまして蛇のような形から北海道のような形になっていたんですねはい', 'end_text': 'この2007年の西ノ島の形ですねスケッチしますとまずは長男と次男の部分がありますけども長男と次男の間に砂がたまっているような状況ですねそのために北海道のような形になっておりますさらに砂と次男の間のここなんですけども湖ができておりました興味深いですよねそしてその後2013年に三男が誕生いたしますこの2013年西ノ島さらににですね噴火を起こしました', 'headline': '西ノ島の形の変化と噴火の歴史'}, {'start_text': '拡大していったと', 'end_text': 'になってしまった', 'headline': '西ノ島の驚くべき変化'}, {'start_text': '小さくなっているということなんですね詳しくお話', 'end_text': '2023年6月はですね最新は', 'headline': '西ノ島の大きさの変化'}, {'start_text': '3.71m2だったということですね', 'end_text': 'と思いますね', 'headline': '西ノ島の大きさの変化の理由と潮の満ち引きの影響'}, {'start_text': 'もよかったらご感想ですねお待ちしておりますはい気になりますねまあ余談はですねこれぐらいにしておきまし', 'end_text': '山頂の2カ所から噴火まあこういった噴火もしかしたら将来見られるかもしれないということありましてねはいというわけでね今西島ですけど噴火止まっておりまして面積が4.1km2から3.71m2', 'headline': '西尾島の最新情報！活発な火山活動の様子を公開！'}, {'start_text': 'なっているということでねそろそろですね', 'end_text': '本格的な噴火をよろしくですねお願い申し上げ奉ってるということなんですね', 'headline': '本格的な噴火をお願いしたいな'}, {'start_text': '噴火が止まっているからです', 'end_text': '本格的な噴火よろしくお願い申し上げ縦も取ります', 'headline': '噴火状況と将来の可能性について'}]
    # pprint.pprint(eval_lists)

    print("len(eval_lists): ", len(eval_lists))

    # eval_listsからstart_textとend_textが全く同じになってしまっている冗長なdictを排除
    unique_data = []
    existing_pairs = set()
    for d in eval_lists:
        text_pair = (d["start_text"], d["end_text"])
        if text_pair not in existing_pairs:
            unique_data.append(d)
            existing_pairs.add(text_pair)
    eval_lists = unique_data
    print("unique len(eval_lists): ", len(eval_lists))
    
    # ここから時刻特定開始
    i = 0
    time_headline_pairs = []
    for split_info in eval_lists:
        # split_infoは{\"start_text\": , \"end_text\": , \"headline\": }形式
        split_start = split_info["start_text"]
        tmp = i
        added = False
        for td in transcript_data[i:]:
            if len(split_start) > len(td["text"]):
                if split_start.startswith(td["text"]) or split_start in (td["text"]):
                    time_headline_pairs.append(
                        {"timestamp": td["start"],
                         "headline": split_info["headline"]}
                    )
                    tmp += 1
                    added = True
                    break
            else:
                if td["text"].startswith(split_start) or td["text"] in (split_start):
                    time_headline_pairs.append(
                        {"timestamp": td["start"],
                         "headline": split_info["headline"]}
                    )
                    tmp += 1
                    added = True
                    break
            tmp += 1
        
        # もしここまでに対応する時刻が見つけられていなければ、
        # 共通部分文字列長が最も長いテキストを含む時刻を採用する
        if not added:
            print(split_info)
            print("i", i)
            max_id = i
            max_com_len = 0
            for j, td in enumerate(transcript_data[i:]):
                lcs = longest_common_substring(td["text"], split_start)
                if lcs > max_com_len:
                    max_com_len = lcs
                    max_id = i + j
            print("max_id: ", max_id)
            print("len(transcript_data): ", len(transcript_data))
            time_headline_pairs.append(
                {"timestamp": transcript_data[max_id]["start"],
                    "headline": split_info["headline"]}
            )
            i = max_id + 1
        else:
            i = tmp
    print("## time headline pairs")
    pprint.pprint(time_headline_pairs)
    print("len(time_headline_pairs): ", len(time_headline_pairs))
    return time_headline_pairs


# 2つの文字列 text1 と text2 の共通部分文字列の長さを求める
# 動的計画法を用いたアルゴリズム
def longest_common_substring(text1, text2):
    m = len(text1)
    n = len(text2)

    # 共通部分文字列の長さを保持するテーブル
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    max_length = 0  # 最長の共通部分文字列の長さ

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_length = max(max_length, dp[i][j])

    return max_length



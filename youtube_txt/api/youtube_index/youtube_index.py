import json
import openai
import pprint
import time


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

    # 長すぎる入力をカット（3分ごとにカット）
    splitted_strings = []
    full_string = ""
    tmp_text = ""
    split_second_counter = 0
    for t in transcript_data:
        tmp_text += t["text"].replace("[音楽]", "")
        full_string += t["text"].replace("[音楽]", "")
        if int(t["start"]) / 180 > split_second_counter and len(tmp_text) > 200:
            splitted_strings.append(tmp_text)
            tmp_text = ""
            split_second_counter += 1
    splitted_strings.append(tmp_text)
    pprint.pprint("splitted strings: " + str(splitted_strings))


    # GPTにプロンプトを投げる部分
    for transcript in splitted_strings:
        prompt = (
            transcript +
            " 段落ごとに分割して、その最初の10文字と最後の10文字と、ネタバレにならない短い(20文字以内）小見出しを" +
            "dictのlist[{\"start_text\": , \"end_text\": , \"headline\": }, {\"start_text\": , \"end_text\": , \"headline\": }, ...]" +
            "形式で出力:"
        )

        eval_flag = False
        while eval_flag is False:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "user", "content": prompt}
                        ]
                )

                # 文字列で返ってきたリストをlist型に変換
                returned_list = response["choices"][0]["message"]["content"]
                print(returned_list)

                eval_list = eval(
                    returned_list
                    .replace("。", ".").replace("、", ",")
                )
                eval_flag = True
            except SyntaxError:
                eval_flag = False

        if type(eval_list) == dict:
            eval_list = [eval_list]

        eval_lists += eval_list
        time.sleep(5)
    print("eval_lists: ", eval_lists)
    pprint.pprint(eval_lists)

    # # デバッグ用
    # # GPTに投げるリクエスト節約
    # eval_lists =  [{'start_text': 'こんにちははじめしゃちょーですは', 'end_text': '完成したということで', 'headline': '新しい乗り物の登場！'}, {'start_text': 'まだどこも情報が出て', 'end_text': 'ない', 'headline': '大注目の世界最速マシン！'}, {'start_text': '残念ながら詳細はまだ', 'end_text': '明かされていませんが', 'headline': '楽しみに待ちましょう！'}, {'start_text': 'らしくですねなんかガチの本当の最速らしくてメディアさんとかよりも先も誰よりも最速で乗ることができるみたいです', 'end_text': '見るとなんかどういう感じなのかちょっとわかるかいやでもすごいぞ', 'headline': '最速で乗ることができる新しい乗り物の開発途中'}, {'start_text': 'か結構長くないぐねぐねすごいねなんか高さというよりこう', 'end_text': '感じになってきたぞここで普段だったらスタッフの方が安全に説明し', 'headline': '最新の乗り物ついさっき45億円です俺の家15個買った俺の家が15個食べます'}, {'start_text': 'もよねでも俺絶対ダメなんですよこう見えて山場が', 'end_text': 'れてるところジャンプアクションとかあるのこれちょっと何にもまだ情報がないのでわかんないですけども早速ちょっと乗ってみたいと思いますなんか入っていきましょうすごいめっちゃ可愛い花あ', 'headline': '山場が何個あると思うんですよーんってなってるところもちょっと怖いしそこまでねそこもすごいなんか角度ついてそうレールの角度とかも一番困るのはこのレールが途中で途切れてるところ'}, {'start_text': 'な感じですねかっこいい最新だねさあつきましたエントランスですこれが最終なんか', 'end_text': 'ーヤーチーケットを受け取ってもらう必要がありますねいざ」と言われてちょっと緊張しましたまさかの最終チェック', 'headline': 'こんなこと言われたらすごい緊張しちゃうよねファイナルチェックとか入れたらやばいいよいよって感じになってきたぞここで普段だったらスタッフの方が安全に説'}, {'start_text': 'てくれる場所らしいです', 'end_text': '安全はありません', 'headline': '常に安全な姿勢を取って備えてください'}, {'start_text': '次に安全な姿勢についてのご案内です', 'end_text': 'ありがとうございます', 'headline': 'ポイントは2つ'}, {'start_text': '1つ目商品を置いたまま乗ること', 'end_text': 'ハンドルに手が届かない方は安全はありません', 'headline': 'ハンドルにつかまること'}, {'start_text': 'ありがとうございます', 'end_text': 'あるあるあるある', 'headline': '急加速系ね'}, {'start_text': 'あーやばいもうある', 'end_text': 'ないやなこれはじゃあ乗ります', 'headline': 'ピンクのネオンライトっぽい'}, {'start_text': '初だからねもう行く', 'end_text': 'しかないやなこれはじゃあ乗ります', 'headline': 'キャリア怪しいな'}, {'start_text': '初だからねもう行く', 'end_text': 'しかないやなこれはじゃあ乗ります', 'headline': 'ピンクのネオンライトっぽい'}, {'start_text': 'うち俺バイク乗ってたんで', 'end_text': 'それだけですね行ってきますね', 'headline': 'じゃあ乗ります'}, {'start_text': 'じゃあ乗ります', 'end_text': '行ってきます[拍手]', 'headline': '行ってきます'}, {'start_text': 'まずはこういう感じね', 'end_text': 'はいゆっくり入りますゆっくり入ります', 'headline': 'まずはこういう感じね'}, {'start_text': 'やばいやばいやばい', 'end_text': 'やばいやばいやばいやばいやばいやばいやばいやばい', 'headline': '段落ごとに分割して'}, {'start_text': 'やばいやばいやばい', 'end_text': 'やばいやばいやばいやばいやばいやばいやばいやばい', 'headline': 'その最初の10文字と最後の10文字と'}, {'start_text': 'やばいやばいやばい', 'end_text': 'やばいやばいやばいやばいやばいやばいやばいやばい', 'headline': 'ネタバレにならない短い(20文字以内）小見出しをdictのlist[{'}, {'start_text': 'はいはいはいゆっくり入りますゆっくり入ります', 'end_text': 'やばいやばいやばいやばいやばいやばいやばいやばい', 'headline': 'まずはこういう感じね'}, {'start_text': '段[拍手]まずはこういう感じねはいはいはいゆっくり入りますゆっくり', 'end_text': '入りますやばいやばいやばいやばい', 'headline': '入ります'}, {'start_text': '終わったかいや何が起きてたかあれで', 'end_text': 'じゃ大丈夫ですもう終わりもう終わりかなもう終わりかなこれ終わりかよかった', 'headline': '終わりかなもう終わりかなこれ終わりかよかったすごいな面白いですね'}, {'start_text': 'お疲れ様でした史', 'end_text': 'ます最初の感想楽しかったです楽しかったもちろん怖かったよ絶叫', 'headline': '史上初乗ってみました最初の感想楽しかったです楽しかったもちろん怖かったよ'}, {'start_text': '絶叫系苦手で怖かっ', 'end_text': 'いと線路ないとこで1回心臓止まりました見てた逆走した', 'headline': '絶叫系苦手で怖かったけどバイクの姿勢なのがすごい臨場感があってバイク乗りとしてはすごい楽しかったです'}, {'start_text': '本当にバイクでこの感', 'end_text': 'しくて楽しかったのと線路ないとこで1回心臓停', 'headline': '本当にバイクでこの感じなんか坂道走ってる感じこういうグニグニしてて楽しかったのと線路ないとこで1回心臓止まりました見てた逆走した'}, {'start_text': 'それがねすごい感覚だっ', 'end_text': 'ジェットコースターとかそんな俺に乗ったこ', 'headline': 'それがねすごい感覚だった後ろ向きで外れジェットコースターとかそんな俺に乗ったことなかったからそこもびっくりしました'}, {'start_text': '体感速度一応非公開とな', 'end_text': 'でした 段落ごとに分割して,その最初の10文字と最後の10文字と,ネタバレにならない短い', 'headline': '体感速度はどうだった体感速度一応非公開となったんですけども僕の乗ってみた体幹速度5200kmでした'}, {'start_text': 'こだまです正直藤山慣れしてるからかもしれないです', 'end_text': '俺は乗りたいって思っちゃう', 'headline': '藤山に慣れたけど,新しいジェットコースターも楽しめました'}, {'start_text': '次で富士急ハイランドさんで45億円で作られた新しい乗り物続墾', 'end_text': '乗れますので皆さんぜひ乗ってみてください', 'headline': '富士急ハイランドさんで新しい乗り物が登場！7月20日から乗れます'}, {'start_text': 'いや俺はめっちゃ好きだ藤山とこっちどっちに乗るって言われたら', 'end_text': 'こっちを選びます', 'headline': '俺は藤山よりもこっちを選ぶ'}, {'start_text': 'ぜひバイク好きな人とかバイク乗ってみたいなっていう人は', 'end_text': '乗ってみたらいいかなと思いますお願いします', 'headline': 'バイク好きな人におすすめ！新しい乗り物'}]
    # pprint.pprint(eval_lists)

    print("len(eval_lists): ", len(eval_lists))

    # eval_listsからstart_textとend_textが全く同じになってしまっている冗長なdictを排除
    # また、start_textがfull_stringに含まれていないものを削除
    unique_data = []
    existing_pairs = set()
    for d in eval_lists:
        print(d)
        if d['start_text'] in full_string:
            text_pair = (d["start_text"], d["end_text"])
            if text_pair not in existing_pairs:
                unique_data.append(d)
                existing_pairs.add(text_pair)
        eval_lists = unique_data
    print("unique len(eval_lists): ", len(eval_lists))
    
    # ここから時刻特定開始
    time_headline_pairs = []
    prev_max_id = 0
    for split_info in eval_lists:
        # split_infoは{\"start_text\": , \"end_text\": , \"headline\": }形式
        split_start = split_info["start_text"]
        
        # 共通部分文字列長が最も長いテキストを含む時刻を、対応する時刻とする
        max_id = 0
        max_com_len = 0
        max_id_diff = 0
        for j, td in enumerate(transcript_data):
            lcs = longest_common_substring(td["text"], split_start)
            if lcs > max_com_len:
                max_com_len = lcs
                max_id = j
                max_id_diff = abs(max_id - prev_max_id)
                # print("1", max_id, j, len(transcript_data), td["text"], split_start, max_id_diff)
            elif lcs == max_com_len and max_id_diff > abs(j - prev_max_id):
                max_com_len = lcs
                max_id = j
                max_id_diff = abs(max_id - prev_max_id)
                # print("2", max_id, j, len(transcript_data), td["text"], split_start, max_id_diff)
  
        # print(max_id, len(transcript_data))
        prev_max_id = max_id
        time_headline_pairs.append(
            {"timestamp": transcript_data[max_id]["start"],
                "headline": split_info["headline"]}
        )
        # i = max_id + 1

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



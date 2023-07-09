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
            " 段落ごとに分割して、その最初の10文字と最後の10文字と、ネタバレにならない短い(10文字以内）小見出しを" +
            "dictのlist[{\"start_text\": , \"end_text\": , \"headline\": }, {\"start_text\": , \"end_text\": , \"headline\": }, ...]" +
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
    # eval_lists = [{'start_text': 'ニュータイプの全てを見届けてきた男', 'end_text': 'の人生ブライトノアの人生', 'headline': 'ブライトノアの人生'}, {'start_text': 'ブライトノアはアニメ機動戦士ガンダムに初めて登場して以来', 'end_text': '登場する人物です', 'headline': 'ブライトノアの登場'}, {'start_text': '劇中では主に各シリーズの主人公が登場する母艦のキャプテンを務めることが多く', 'end_text': '猛者です', 'headline': 'ブライトノアの役割'}, {'start_text': 'また反骨的な精神を持つガンダムパイロットたちを制する立ち位置にいることから', 'end_text': 'の苦労人としても', 'headline': 'ブライトノアの人格'}, {'start_text': '知られています', 'end_text': '大人へと成長していきました', 'headline': 'ブライトノアの成長'}, {'start_text': 'ドライトを務めているブライトノアは', 'end_text': 'なっています', 'headline': 'ブライトノアの背景設定'}, {'start_text': '宇宙世紀0079に主観学校を卒業し', 'end_text': '板挟み', 'headline': 'ホワイトベースの新艇長'}, {'start_text': 'の立場として戦場へ繰り出すこととなります', 'end_text': '進化していきました', 'headline': '戦場への繰り出しと成長'}, {'start_text': 'しかし新兵ながら卓越した指揮能力を見せ', 'end_text': 'を上げました', 'headline': '卓越した指揮能力の発揮'}, {'start_text': 'しかし式以外の面では精神的な余裕のなさから', 'end_text': 'を取っていました', 'headline': '精神的な余裕の欠如'}, {'start_text': 'そのためこのアムロに対する対応について', 'end_text': 'を求められます', 'headline': 'アムロへの対応の変化'}, {'start_text': 'そしてジャブローにて今までの戦果を認められ', 'end_text': 'を戦い抜きました', 'headline': 'ジャブローでの戦闘勲章'}, {'start_text': '昇進ホワイトベースのディアンヌ艦隊へと配属されたことで再び宇宙へと上がります', 'end_text': '未来を見守り続けます', 'headline': '再び宇宙へ'}, {'start_text': '未来には許嫁のカムランブルームやジャブローから補充要員として登場したスレッカーローなどいくつもの障壁がありました', 'end_text': '一歩引いた場所から不器用ながらも未来を見守り続けます', 'headline': 'いくつもの障壁'}, {'start_text': 'ソロモン攻略戦の際には未来がスレッダーと再出撃するまでのわずかな時間を過ごせるようサブブリッジから人員を派遣するなど気遣いを見せ自分の気持ちを未来に告げています', 'end_text': '乗組員と無事に生還を果たしました', 'headline': 'ソロモン攻略戦'}, {'start_text': '最終的にはホワイトベースが高校不能となったため要塞に着底させて白兵戦に持ち込みその後アムロからの呼びかけに応えて大韓命令を出したことで乗組員と無事に生還を果たしました', 'end_text': '終結します', 'headline': '終戦と生還'}, {'start_text': '1年戦争後は実直に思い続けたことが実りブライトは未来と結婚しましたさらにハサウェイとチェーミンという2人の子供に恵まれるなど私生活は充実していました', 'end_text': '散々な目にあっていました', 'headline': '私生活の充実と苦境'}, {'start_text': '機動戦士データガンダムの作中では宇宙世紀0087グリーンノアで起きたエウーゴによりガンダムMk2の強奪の際', 'end_text': 'ならない短い(10文字以内）小見出しを', 'headline': 'グリーンノアでの事件'}, {'start_text': '避難民をテンプテーションで保護しグリーンノアから脱出したことでブライトの運命は大きく変わります', 'end_text': 'ウーゴン正式に参加しアーガマの指揮を偏見劣化ナーから引き継ぐことになります', 'headline': 'ブライトの新たな役割'}, {'start_text': '指揮官として戦場に戻るのは7年ぶりでしたが全くブランクを感じさせない手腕を発揮し就任直後にジャブロー効果作戦の指揮を担当します', 'end_text': 'クワトロバジーナコトシャアーズナブルたちと共に戦うことになりました', 'headline': '復帰したブライトの指揮能力'}, {'start_text': 'カミーユはニュータイプ能力やパイロットとしても技量は高いもののアムロ以上の反骨精神に加え精神的に不安定な部分も多く手を焼いていました', 'end_text': '父親となった一面も垣間見えます', 'headline': 'ブライトとカミーユの関係'}, {'start_text': 'ブライト主導のもとメールストローム作戦を実行に移しました', 'end_text': 'コロニーレーザーによってターンズを壊滅させることに成功しました', 'headline': 'グリプス戦役の最終作戦'}, {'start_text': '精神崩壊を起こしまともな戦力はファーユイリーただ1人となってしまいますこうして疲弊しきったアーガマは修復を兼ねてサイドバンのシャングリラコロニーに立ち寄りましたここからが機動戦士ガンダムダブルゼータの物語となりますこの船の手伝いをしてもらえないか何だったらここでずっと働いてくれてもいいんだ', 'end_text': '寄稿したシャングリラではジャンク屋の少年である受動は明日に出会います', 'headline': 'アーガマ修復とシャングリラでの出会い'}, {'start_text': '当初児童は元ティターンズのヤザンテーブルと手を組んでゼータガンダムを奪取しにアーナを吸収しブライトもそれに応戦していましたしかしジュドーが初めてモビルスーツに乗ったにもかかわらずzガンダムを見事に動かしたことからブライトはジュドーにアムロやカミーユといった歴代のニュータイプの姿を重ねます', 'end_text': 'ジュドーの活躍を見たブライトは深刻な戦力不足を解消するため児童たちジャンク屋の少年少女アーガマのクルーにスカウト', 'headline': 'ブライトの戦力不足と児童たちのスカウト'}, {'start_text': 'さらに補給で立ち寄ったラビアンローズにて艦長代理のエマリー4隻異性として興味を持たれもうアプローチを受けます本人もまんざらではない姿は見られたものの真面目で家族思いな性格から何とか踏みとどまっていましたその後ネオジオンの地球侵略を阻止するためアーガまで地球へ降下しさらにネオジオンによるコロニー落としを阻止するべくダブリンに', 'end_text': '段落ごとに分割してその最初の10文字と最後の10文字,ネタバレにならない短い(10文字以内）小見出しをdictのlist[{"start_text": , "end_text": , "headline": }, {"start_text": , "end_text": , "headline": }, ...]形式で出力:', 'headline': 'エマリーのアプローチとネオジオンの阻止'}, {'start_text': '向かいますが結局コロニー落としの阻止はできませんでした', 'end_text': 'したことから...', 'headline': 'コロニー落としの阻止失敗'}, {'start_text': 'そしてダブリンの避難民を救助した後にアーガマを置いて再び宇宙へと戻ります', 'end_text': 'に託しました', 'headline': 'ダブリンの避難民救助とアーガマの送還'}, {'start_text': 'そしてラビアンローズにてメールアーガマを受領しますが月への移動が決定したので艦長の席をビーチャオーレムに託しました', 'end_text': 'ジュドーたちに補給物資を送るため奔走していました', 'headline': 'メールアーガマの受領とジュドーへの支援物資'}, {'start_text': '児童たちはネオジオンとの抗争に勝利します', 'end_text': 'の行き場のない拳を受け止めました', 'headline': '児童たちの抗争勝利とジュドーの怒り'}, {'start_text': '宇宙世紀009連邦軍が治安維持を行うべく外郭部隊ロンドベルを編成しブライトはその司令官を務めることになります', 'end_text': '長として登場しました', 'headline': 'ブライトのロンドベル司令官就任'}, {'start_text': 'ガンダムダブルゼータで見せたような柔和な様子は消え再び指揮官として厳しい態度を貫いていました', 'end_text': '阻止するため行動していきます', 'headline': 'ブライトの厳しい指揮官姿勢'}, {'start_text': 'また一年戦争時の潜入であるアムロと再び菅をにしており同志として心を許した間柄として', 'end_text': 'に挑みます', 'headline': 'アムロとの再会とシャアへの対抗'}, {'start_text': 'その後シャアのアクシズ落としを阻止するため三段構えの作戦をとりネオジオンとの決戦に挑みます', 'end_text': '決戦に挑みます', 'headline': 'アクシズ落としの作戦とネオジオンとの決戦'}, {'start_text': '島がみんなの命をくれというセリフは', 'end_text': '総選挙でベスト5に入っています', 'headline': 'ブライトの調子像を表す屈指の名台詞として語り継がれ三強が行った逆襲のシャア明言総選挙でベスト5に入っています'}, {'start_text': 'またブリッジに残ることを選んだハサウェイに', 'end_text': 'の生き様が多く描かれています', 'headline': 'ブリッジに残ることを選んだハサウェイに遺書を書かせるなどブライトの軍人としての生き様が多く描かれています'}, {'start_text': 'こうして決死の覚悟でアクシズの', 'end_text': 'の落下コースに入ってしまいました', 'headline': 'こうして決死の覚悟でアクシズの分断作戦を敢行しますが核ミサイルを使った攻撃では完全な破壊には至らず自らアクシズに乗り込み内部からの爆破を試みますこの工作の結果アクシズの分断に成功しますが爆破の威力が強すぎたことで分断したアクシズの半分が地球への落下コースに入ってしまいました'}, {'start_text': 'ブライトは結果的にシャアの手助けをすることになった', 'end_text': 'アクシズを押すよう無茶な指示を出していました', 'headline': 'ブライトは結果的にシャアの手助けをすることになった状況を黙って見ていることができずダーカイラムでアクシズを押すよう無茶な指示を出していました'}, {'start_text': 'そんな地球圏から離れていくアクシズと', 'end_text': '逆襲のシャアの物語は幕を閉じました', 'headline': 'そんな地球圏から離れていくアクシズと戦友を尻目にブライトは再び激戦を生き残り逆襲のシャアの物語は幕を閉じました'}, {'start_text': 'ジュドーのイメージが目', 'end_text': 'をして欲しいというメッセージを受けた', 'headline': 'ブライトの新たな使命'}, {'start_text': 'そして3年後宇宙世紀0096部隊は', 'end_text': 'ガンダムユニコーンへと移ります', 'headline': 'ブライトと宇宙世紀0096部隊'}, {'start_text': 'ラプラス事変と呼ばれる騒動の', 'end_text': 'ブライトは参謀本部の目論見により', 'headline': 'ブライトとラプラス事変'}, {'start_text': '事件に関わらないよう遠ざけられて', 'end_text': '我されました', 'headline': 'ブライトの立場の変化'}, {'start_text': 'バナージにかつてのニュータイプたちの', 'end_text': 'に送り出しました', 'headline': 'ブライトとバナージの協力'}, {'start_text': 'その後は地球連邦軍参謀本部を', 'end_text': '活躍の裏で事態の収集に動いていき', 'headline': 'ブライトと事態の収集'}, {'start_text': 'その後さらに時は流れ再び', 'end_text': '9年後宇宙世紀を暗号5のマフティ動乱', 'headline': 'ブライトとマフティ動乱'}, {'start_text': 'かつてのニュータイプたちの思いを', 'end_text': '政治の世界へ進出することを考えていました', 'headline': 'ブライトの進路の選択'}, {'start_text': 'ブライトの連邦軍退役という辞職願', 'end_text': 'ままとなっています', 'headline': 'ブライトの辞職願'}, {'start_text': '休憩部隊の指令に着任し地球に', 'end_text': '捕らえられた後であり', 'headline': 'ブライトとマフティーの対面'}, {'start_text': 'マフティー処刑とも別室に待機させられてい', 'end_text': '発表されることになってしまいました', 'headline': 'ブライトの心境は明かされていません'}, {'start_text': 'ブライトはこの報道でマフティーの正体が息子のハ', 'end_text': 'の動向に関しても不明でケネスの推測では3カ月後そのまま退役するだろうとだけ語られています', 'headline': 'ブライトの心境は明かされていません'}, {'start_text': 'ブライトはガンダムシリーズ屈指のクロー人であり地', 'end_text': 'したという汚名を着せられることになりました', 'headline': 'ブライトの心境は明かされていません'}, {'start_text': '過去に直接クエスを殺してしまった', 'end_text': '原作とは違った活躍が見られるかもしれません', 'headline': 'クエスの運命が異なる展開かも'}, {'start_text': 'ブライトに関しても原作とは違った', 'end_text': '活躍が見られるかもしれません', 'headline': 'ブライトの活躍に注目'}, {'start_text': 'サンオブブライトの制作スケジュールが', 'end_text': 'サンゴブライトは2025年公開なのではないか', 'headline': 'サンゴブライトの公開予定は2025年？'}]
    # pprint.pprint(eval_lists)

    print("len(eval_lists): ", len(eval_lists))

    # eval_listsからstart_textとend_textが全く同じになってしまっている冗長なdictを排除
    unique_data = []
    existing_pairs = set()
    for d in eval_lists:
        print(d)
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
        
        # 共通部分文字列長が最も長いテキストを含む時刻を、対応する時刻とする
        max_id = i
        max_com_len = 0
        for j, td in enumerate(transcript_data[i:]):
            lcs = longest_common_substring(td["text"], split_start)
            if lcs > max_com_len:
                max_com_len = lcs
                max_id = i + j
        
        time_headline_pairs.append(
            {"timestamp": transcript_data[max_id]["start"],
                "headline": split_info["headline"]}
        )
        i = max_id + 1

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



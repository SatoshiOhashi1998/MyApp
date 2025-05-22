import pandas as pd

def save_to_excel(input_string, output_file):
    # 文字列を " OR " で分割
    keywords = input_string.split(" OR ")

    # データフレームに変換
    df = pd.DataFrame(keywords, columns=["Keywords"])

    # Excelファイルに保存
    df.to_excel(output_file, index=False)

# 使用例
input_string = (
    "#soraArt OR #ロボ子Art OR #miko_Art OR #ほしまちぎゃらりー OR #AZKiART OR "
    "#メルArt OR #アロ絵 OR #はあとart OR #絵フブキ OR #祭絵 OR #あくあーと OR "
    "#シオンの書物 OR #しょこらーと OR #プロテインザスバル OR #百鬼絵巻 OR "
    "#みおーん絵 OR #絵かゆ OR #できたてころね OR #ぺこらーと OR #絵クロマンサー OR "
    "#しらぬえ OR #ノエラート OR #マリンのお宝 OR #かなたーと OR #つのまきあーと OR "
    "#TOWART OR #ルーナート OR #みかじ絵 OR #LamyArt OR #ねねアルバム OR "
    "#ししらーと OR #絵まる OR #まのあろ絵 OR #Laplus_Artdesu OR #Luillust OR "
    "#こよりすけっち OR #さかまた飼育日記 OR #いろはにも絵を OR #絵ーちゃん OR "
    "#のどかあーと OR #ioarts OR #HoshinovArt OR #GambaRisu OR #graveyART OR "
    "#anyatelier OR #Reinessance OR #Zetacrylic OR #inKaela OR #AeruSeni OR "
    "#callillust OR #artsofashes OR #inART OR #gawrt OR #ameliaRT OR #IRySart OR "
    "#galaxillust OR #FineFaunart OR #kronillust OR #drawMEI OR #illustrayBAE OR "
    "#BaelzBrush OR #絵リーラ OR #pendorART OR #PomuPaint OR #Finanart OR #Artsuki OR "
    "#GalleryOfRoses OR #PetraArt OR #エナーアート OR #Palouette OR #DrawKosaka OR "
    "#Reimural OR #Endoujin OR #DrawMillie OR #Ikenography OR #MystArt OR #Akurylic OR "
    "#drawluca OR #YaminoArt OR #AlbanKnoxArt OR #AsumArt OR #Artchivist OR #Briskart OR "
    "#VioletAtelier OR #drawkyo OR #MariArt OR #Arcadiart OR #AiaAmARTe OR #RenZottoArt OR "
    "#ScarleArt OR #WiffyArt OR #ruri_Art OR #yuyamuyart OR #suha_art OR #GaonArt OR "
    "#kingkaenfanart OR #LOROUART OR #ChihoArt OR #HakurenArt OR #nagiart OR #Ara_Art OR "
    "#Siu_Art OR #Bora_art OR #Ray_art OR #Roha_Art OR #Nari_art OR #hari_art OR #kiru_art OR "
    "#PREEART OR #Seffynart OR #mi_art OR #hada_art OR #Yamiart OR #HayunArt OR #Sera_art OR "
    "#Leeonart OR #Taka_Radjimart OR #hanamaki_art OR #ZEA_art OR #Derem_Art OR #Rai_Art OR "
    "#Amicia_MichellArt OR #miyu_ottaviart OR #riks_art OR #Azura_Art OR #Maunggambart OR "
    "#Nagisa_Arciart OR #Siska_art OR #bonnivierart OR #Etna_Art OR #Layl_art OR #ARTVANLUNA OR "
    "#Elatiorart OR #Xiart_Wangy OR #Melatikaart OR #フレン見て OR #絵リッサ OR #絵ブラヒム OR "
    "#長尾百景 OR #上弦画 OR #描いた晴 OR #きら名画 OR #アカネ色の世界 OR #描くンゴ OR "
    "#画ハク OR #ヒスイワークス OR #ニシゾノート OR #AXIART OR #イロ絵す OR "
    "#まめねことレオス OR #絵バンス OR #レインの依頼書 OR #むにゃーと OR #ぽんとれーと OR "
    "#Yotsuh_Art OR #サロメ百万展 OR #ふうらーと OR #わたらいらすと OR #四季彩画 OR #SeraPic OR "
    "#ドーラの宝物庫 OR #絵馬絵 OR #あずま絵 OR #出雲墨絵 OR #クリエイツ轟京子 OR #描いたよクレアさん OR "
    "#お花畑青空大写生大会 OR #社築納品物 OR #もっとももちゃんあーと OR #漆黒の水鏡 OR #緑仙はやく見ろ OR "
    "#絵画コウ OR #ゆずの朔品 OR #クリ笑イト OR #こがね絵 OR #ぴよあーと OR #絵アル OR #雨森と美術 OR "
    "#リオンあーと OR #しら画 OR #尊絵巻 OR #でびるさまにささげるえ OR #リツキあーと OR #描いてみまちた OR "
    "#おつきみあーと OR #ジョー設展 OR #遠い北からの絵手紙 OR #なるアート OR #デラスのお品書き OR "
    "#りねの自由帳 OR #絵かける OR #しばのドッグタグ OR #みとあーと OR #ちーあーと OR #えるの絵だよ OR "
    "#でろあーと OR #凛Art OR #ピク渋 OR #アキくんちゃんアート OR #もいもいらすと OR #詩子あーと OR "
    "#いちごのあとりえ OR #むぎあーと OR #りりあーと OR #有栖の絵本 OR #のらねっこあら OR #絵ガク OR "
    "#ギルザレン画廊 OR #金剛力也像 OR #森中びじゅつかん OR #かな絵 OR #赤羽絵葉書 OR #笹の絵 OR "
    "#モルルアート OR #ひまあーと OR #りりむとおえかき OR #KuzuArt OR #氷画 OR #しいなーと"
)

def main():
    output_file = "keywords.xlsx"

    save_to_excel(input_string, output_file)
    print(f"Keywords have been saved to {output_file}.")

if __name__ == '__main__':
    main()

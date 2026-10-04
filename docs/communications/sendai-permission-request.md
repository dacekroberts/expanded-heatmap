# Sendai: permission request — DRAFTED 2026-09-24, NOT SENT

**Status: drafted 2026-09-24 for the owner to send**, from the owner's own
address. Nothing sent yet. Tracked as item 21 in `docs/gated_access.md`.

**To**: `fuk005530@city.sendai.jp`, 健康福祉局生活衛生課. The address is listed on
the city's organisation page (`/soshikikanri/shise/gaiyo/soshiki/052/074.html`)
under 食品衛生係. The two lists' own pages name the division, with 食品衛生係 on
022-214-8205 and 生活衛生係 on 022-214-8206. **Untested**: whether the address
delivers.

## Why this exists

Sendai has not adopted CC BY 4.0 or 政府標準利用規約 site-wide, which is where it
differs from Osaka, Kobe and Sapporo. Its copyright page
(`https://www.city.sendai.jp/sesakukoho/chosakuken/index.html`) is the default:

> 「「私的使用のための複製」や「引用」など著作権法上認められた場合を除き、無断で複製・転用することはできません。」

It gives way only where a page says otherwise
(「ただし、仙台市ホームページ内の各ページに特段の定めがある場合には、その取り扱いが優先されます。」),
and **neither list page does**. The city marks each open-data file with a CC BY
4.0 badge (`class="openDataFile"`). These links carry none, neither list is
in the city's 5,907-row catalogue, and the files carry no notice of their own.
The "facts are not 著作物" reading was recorded and **not relied on**
(`read-licence` step 8). Deep links to the list pages are also gated:
「その他のページへリンクを希望される場合は、それぞれの担当課へお問い合わせください。」

The owner's rule (2026-09-24) was: if the terms are clear, draft a short
request in proper formal Japanese; if not, probe further. They were judged
clear. **Sendai waits in the access-blocked band until the city answers.** The
data is measured and joined (95.1% block) in `docs/build_briefs/sendai.md`.

## The request (formal Japanese; fill in the three placeholders)

It describes the project as a **non-profit personal portfolio map**; correct
that if it is not accurate.

```text
宛先：fuk005530@city.sendai.jp
件名：「食品衛生関係の営業許可事業者の一覧」等の二次利用に関するお伺い

仙台市 健康福祉局 生活衛生課
食品衛生係・生活衛生係 ご担当者様

突然のご連絡失礼いたします。
[氏名]と申します。

現在、個人のポートフォリオとして、鉄道駅周辺における飲食店や理容・美容店などの集積度を可視化する、非営利のウェブ地図を制作しております。
つきましては、貴課が仙台市ホームページで公開されている下記の一覧をこの地図に利用させていただけないかと考え、ご連絡を差し上げました。

■ 対象
1. 食品衛生関係の営業許可事業者の一覧
   https://www.city.sendai.jp/sekatsuese-shokuhin/kyokalist/joho.html
2. 仙台市生活衛生関係施設一覧（理容所・美容所・クリーニング所）
   https://www.city.sendai.jp/sekatsuese/facilitylist/list.html

■ 利用方法
・使用する項目は、屋号（施設名称）、営業種類、営業所所在地のみです。営業者氏名、代表者名、電話番号など個人に関する情報は、一切使用・掲載いたしません。
・所在地を国土交通省の位置参照情報と照合して地図上の位置に変換し、駅周辺の施設数として集計・表示いたします。
・元のファイルを再配布することはございません。
・「仙台市『食品衛生関係の営業許可事業者の一覧』等を加工して作成」のように出典を明記し、仙台市が作成したものと誤解されない表示といたします。
・掲載内容についてご指摘をいただいた場合は、速やかに削除いたします。

■ お伺いしたい事項
1. 上記の方法による利用をお認めいただけますでしょうか。
2. 出典の表示方法について、ご指定がございましたらご教示ください。
3. 出典表示の際、上記一覧のページへリンクを設定してもよろしいでしょうか。

ご多忙のところ誠に恐れ入りますが、ご検討いただけますと幸いです。
何卒よろしくお願い申し上げます。

――――――――――――
[氏名]
メール：[メールアドレス]
ウェブサイト：[URL]
――――――――――――
```

**In English**, it introduces the owner and the map, and names the two lists.
It says only the trade name, business type and premises address are used,
never operator names or phones, and that the files are not redistributed. It
credits the city as "processed from" its lists, does not imply the city made
the map, and removes anything on request. It asks three things: may we use it,
is there required credit wording, and may we link the list pages.

## When a reply comes

- **Yes**: record the reply's wording and date here and in `DECISIONS.md`, apply
  any credit it specifies, and move Sendai from the access-blocked band to A.
- **No**: Sendai goes to the discards, kind `terms` (Tel Aviv's shape).
- **Conditions**: bring them to the owner.
- **Silence is not consent.** Nothing is built on silence.

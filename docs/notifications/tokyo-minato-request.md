# Tokyo — Minato: request to publish the complete food-permit list — DRAFTED 2026-09-24, PARKED (last resort)

⏸ **PARKED 2026-09-24 as the LAST RESORT (owner).** Contacting an agency comes only after the probe methods we control have failed, because the answer is out of our hands. Do not send, or present as the next step, until then.

**Status**: drafted 2026-09-24 for the owner to send, from the owner's own
address. Nothing sent yet. Tracked as item 31 in `docs/gated_access.md`.

**To**: みなと保健所 生活衛生課 (food hygiene). ⚠️ **The address is not
verified.** Take the e-mail address or inquiry form from the ward's
food-permit page (`https://www.city.minato.tokyo.jp/shokuhinkouiki/kuse/egyokyoka/tetsuzuki/shokuhin.html`)
before sending.

## Why this exists

- **What the ward publishes**: `food_business_all` on the ward's CKAN
  (`opendata.city.minato.tokyo.jp`) and the Tokyo catalogue, CC BY 4.0. Its
  own description says 「オープンデータへの公開に同意が得られた施設のみです」: consenting
  facilities only.
  - It holds **4,781 restaurants against 16,073 in force** (the ward's own
    monitoring report, 2026-03-31: 11,631 new-law and 4,442 old-law), about
    30%.
  - It has **no old-law permits** at all, and no old-law list exists anywhere.
- **The ward's own form points the other way.** The new-law application form
  says details are, in principle, published as open data (「原則オープンデータとして公開」),
  with an opt-out for names only. That mismatch is the fair question to ask,
  and publication would come with CC BY.
- **The fallback** is a 情報公開請求. It is routine at Minato (64 requests in
  FY2025) and returns PDF on CD-R for ¥100, with no open licence.
- **What happens meanwhile**: Tokyo builds last, and Minato's food layer is an
  undercount the page must disclose. Minato stays valid as the join control.

## The request (formal Japanese; fill in the placeholders)

```text
件名：食品衛生法に基づく営業許可施設一覧（オープンデータ）の公開範囲に関するお伺い

みなと保健所 生活衛生課
食品衛生ご担当者様

突然のご連絡失礼いたします。
[氏名]と申します。

現在、個人のポートフォリオとして、鉄道駅周辺における飲食店や理容・美容店などの集積度を可視化する、非営利のウェブ地図を制作しております。東京都内については、各区がオープンデータとして公開されている営業許可施設の一覧を利用させていただいております。

貴区がオープンデータとして公開されている「食品等営業許可・届出一覧」（food_business_all）を利用させていただいておりますが、説明欄に「オープンデータへの公開に同意が得られた施設のみ」とあり、改正前の食品衛生法による許可施設も含まれていないようでございました。貴区のモニタリング結果の資料では、令和8年3月末時点の飲食店営業の許可施設数は16,073件とされており、公開データはその一部であるものと理解しております。

一方で、営業許可申請の様式には、記載事項を原則としてオープンデータとして公開する旨の記載がございましたので、以下の点についてお伺いできれば幸いです。

■ お伺いしたい事項
1. 現在営業許可を受けている施設（改正前の食品衛生法による許可を含む）について、屋号（施設名称）、営業の種類、営業所所在地の項目に限り、オープンデータとして公開していただくことは可能でしょうか。
2. 上記が難しい場合、同じ項目に限った一覧をご提供いただき、下記の方法で地図に利用させていただくことは可能でしょうか。
3. いずれも難しい場合、情報公開制度による手続きが適切でしたら、その旨ご教示いただけますと幸いです。

■ 利用方法
・使用する項目は、屋号（施設名称）、営業の種類、営業所所在地のみです。営業者氏名、電話番号など個人に関する情報は、一切使用・掲載いたしません。
・所在地を国土交通省の位置参照情報と照合して地図上の位置に変換し、駅周辺の施設数として集計・表示いたします。
・元のデータを再配布することはございません。
・「港区『食品等営業許可・届出一覧』を加工して作成」のように出典を明記し、港区が作成したものと誤解されない表示といたします。
・掲載内容についてご指摘をいただいた場合は、速やかに削除いたします。

ご多忙のところ誠に恐れ入りますが、ご検討いただけますと幸いです。
何卒よろしくお願い申し上げます。

――――――――――――
[氏名]
メール：[メールアドレス]
ウェブサイト：[URL]
――――――――――――
```

**In English**: the letter notes that the open data covers only consenting
facilities and no old-law permits, against 16,073 restaurants in the ward's
own report. It points out that the application form says details are
published as open data "in principle". Then it asks three things:
1. Could every permit in force be published, limited to trade name, business
   type and address?
2. If not, could such a list be provided for this use?
3. If not, is a disclosure request the right route?

It promises the same use terms as the other letters.

## When a reply comes

- **Published**: download it, re-run `screen_japan_join.py minato` (Minato is
  the join control, so check that it still reads 99.8%), then
  `python scripts/japan_ward_table.py --write`. Record it in `DECISIONS.md`.
- **Provided under conditions**: bring the conditions to the owner.
- **No**: Minato stays an undercount, disclosed on the Tokyo page.
- **Silence is not consent.**

# Tokyo — Chūō: request for the complete food-permit list — DRAFTED 2026-09-24, NOT SENT

**Status**: drafted 2026-09-24 for the owner to send, from the owner's own
address. Nothing sent yet. Tracked as item 29 in `docs/gated_access.md`.

**To**: Chūō ward's public health centre, 中央区保健所 生活衛生課 (food hygiene).
⚠️ **The address is not verified.** Take the e-mail address or inquiry form
from the ward's food-hygiene page on `www.city.chuo.lg.jp` before sending.

## Why this exists

- **What the ward publishes**: `https://www.city.chuo.lg.jp/documents/984/syokuhineigyoukyoka.csv`,
  CC BY 4.0, published 2024-03 and never updated. It holds only permits
  granted **2021-06 to 2022-12**: 1,319 restaurants against **11,056**
  飲食店営業 in Tokyo's statistical yearbook (FY2024), about 12%.
- **Nothing fills the gap.** A probe on 2026-09-24 found no other list in any
  format: not on the ward's site, not in the Tokyo catalogue, not in the web
  archive.
- **The fallback** is a disclosure request under 中央区情報公開条例 (¥300 per
  item, ¥80 per CD, a decision within 30 days). Its form text is at the end.
- **What happens meanwhile**: Tokyo builds last, and Chūō's food layer is an
  undercount the page must disclose until this is answered.

## The request (formal Japanese; fill in the placeholders)

It describes the project as a **non-profit personal portfolio map**; correct
that if it is not accurate.

```text
件名：食品衛生法に基づく営業許可施設一覧の公開（更新）に関するお願い

中央区保健所 生活衛生課
食品衛生ご担当者様

突然のご連絡失礼いたします。
[氏名]と申します。

現在、個人のポートフォリオとして、鉄道駅周辺における飲食店や理容・美容店などの集積度を可視化する、非営利のウェブ地図を制作しております。東京都内については、各区がオープンデータとして公開されている営業許可施設の一覧を利用させていただいております。

貴区がオープンデータとして公開されている「食品衛生営業許可施設一覧」（https://www.city.chuo.lg.jp/documents/984/syokuhineigyoukyoka.csv）を拝見いたしましたところ、令和3年6月から令和4年12月までに許可された施設のみが掲載されているようでございました。東京都統計年鑑では、令和6年度末の貴区の飲食店営業施設数は11,056件とされており、現在の許可施設の全体をお示しするものではないものと理解しております。

つきましては、以下の点についてご検討いただけますと幸いです。

■ お伺いしたい事項
1. 現在営業許可を受けている施設の一覧（改正前の食品衛生法による許可を含む）を、オープンデータとして更新・公開していただくご予定はございますでしょうか。
2. 公開が難しい場合、屋号（施設名称）、営業の種類、営業所所在地の項目に限った一覧をご提供いただくことは可能でしょうか。
3. いずれも難しい場合、情報公開制度による手続きが適切でしたら、その旨ご教示いただけますと幸いです。

■ 利用方法
・使用する項目は、屋号（施設名称）、営業の種類、営業所所在地のみです。営業者氏名、電話番号など個人に関する情報は、一切使用・掲載いたしません。
・所在地を国土交通省の位置参照情報と照合して地図上の位置に変換し、駅周辺の施設数として集計・表示いたします。
・元のデータを再配布することはございません。
・「中央区『食品衛生営業許可施設一覧』を加工して作成」のように出典を明記し、中央区が作成したものと誤解されない表示といたします。
・掲載内容についてご指摘をいただいた場合は、速やかに削除いたします。

ご多忙のところ誠に恐れ入りますが、ご検討いただけますと幸いです。
何卒よろしくお願い申し上げます。

――――――――――――
[氏名]
メール：[メールアドレス]
ウェブサイト：[URL]
――――――――――――
```

**In English**: the letter introduces the owner and the map. It notes that the
ward's open-data list covers only permits of June 2021 to December 2022,
against 11,056 restaurants in Tokyo's yearbook. Then it asks three things:
1. Will the ward update the open data to every permit in force, old-law
   permits included?
2. If not, could it provide a list of trade name, business type and address
   only?
3. If not, is a disclosure request the right route?

It promises the same use terms as the Sendai letter: premises columns only,
no redistribution, a "processed from" credit, removal on request.

## The fallback: text for the disclosure request form (公文書開示請求書)

Used only if the ward points to 情報公開制度. It is filed through the ward's
own form, which carries the owner's name, so it is the owner's act.

```text
請求する公文書の件名又は内容：
食品衛生法に基づく営業許可に係る台帳（又はそれに相当する電磁的記録）のうち、請求日時点で有効な営業許可（改正前の食品衛生法による許可を含む。）について、施設の名称（屋号）、営業の種類及び営業所の所在地が分かる部分

開示の方法：電磁的記録の写しの交付（CD-R、CSV又はExcel形式を希望）
```

Material released this way carries **no open licence**. Publishing from it is
a separate decision for the owner, and the credit and removal commitments
still apply.

## When a reply comes

- **The open data is updated**: download it from the ward's site, run
  `screen_japan_join.py chuo`, then
  `python scripts/japan_ward_table.py --write`. Record it in `DECISIONS.md`.
- **A list is provided under conditions**: bring the conditions to the owner.
- **No**: Chūō stays an undercount, disclosed on the Tokyo page.
- **Silence is not consent.**

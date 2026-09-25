# Tokyo — Shinjuku: request to reuse or publish the FY2025-end food-permit list — DRAFTED 2026-09-24, PARKED (last resort)

⏸ **PARKED 2026-09-24 as the LAST RESORT (owner).** Contacting an agency comes only after the probe methods we control have failed, because the answer is out of our hands. Do not send, or present as the next step, until then.

**Status**: drafted 2026-09-24 for the owner to send, from the owner's own
address. Nothing sent yet. Tracked as item 32 in `docs/gated_access.md`.

**To**: 新宿区 健康部 衛生課 食品保健係. ⚠️ **The page gives only a phone number**
(03-5273-3827), with no e-mail address and no form (the licence read of
2026-09-24). The section's inquiry page is `/soshiki/340500eisei_00001.html`
(not opened). The site terms route reuse questions to that section or to
区政情報課 (03-5273-4064).

## Why this exists

- **What we use today**: Shinjuku's open-data file, `000399975.csv` (CC BY 2.1
  JP on the ward's portal, CC BY 4.0 on the Tokyo catalogue). It is complete
  but **dated 2023-01-01**, and reads 84% of the yearbook's 15,356
  restaurants.
- **A current list exists, but not as open data.** The ward publishes a full
  list of every permit at the end of FY2025, 「令和7年度末全食品衛生許可施設一覧」
  (`https://www.city.shinjuku.lg.jp/content/000452833.pdf`, 1,023 pages,
  15,333 permits). It also publishes monthly new-permit PDFs.
- **Those PDFs are not on the open-data portal**, so the site's general
  terms apply (`/kusei/about.html`), and they forbid secondary use without
  permission.
- **The PDFs also carry operator columns.** Any use reads only the trade-name
  and premises lines.
- **The best outcome** is the FY2025-end list added to the portal as CSV,
  as the 2023 list was.

## The request (formal Japanese; fill in the placeholders)

```text
件名：「令和7年度末全食品衛生許可施設一覧」の二次利用又はオープンデータ化に関するお伺い

新宿区 健康部 衛生課
食品保健係 ご担当者様

突然のご連絡失礼いたします。
[氏名]と申します。

現在、個人のポートフォリオとして、鉄道駅周辺における飲食店や理容・美容店などの集積度を可視化する、非営利のウェブ地図を制作しております。貴区につきましては、オープンデータとして公開されている食品営業許可施設の一覧（令和5年1月1日時点）を利用させていただいております。

このたび、貴区ホームページにて「令和7年度末全食品衛生許可施設一覧」（PDF）を拝見いたしました。より新しい情報を地図に反映させたいと考えておりますが、同資料はオープンデータのページには掲載されていないため、ご連絡を差し上げました。

■ お伺いしたい事項
1. 上記一覧（令和7年度末時点）を、令和5年1月1日時点の一覧と同様に、オープンデータ（CSV形式）として公開していただくご予定はございますでしょうか。
2. 公開のご予定がない場合、上記一覧および毎月の新規許可施設一覧のうち、屋号（施設名称）、営業の種類、営業所所在地の項目に限り、下記の方法で地図に利用させていただくことは可能でしょうか。
3. 出典の表示方法について、ご指定がございましたらご教示ください。

■ 利用方法
・使用する項目は、屋号（施設名称）、営業の種類、営業所所在地のみです。営業者氏名、代表者氏名、住所、電話番号など個人に関する情報は、一切使用・掲載いたしません。
・所在地を国土交通省の位置参照情報と照合して地図上の位置に変換し、駅周辺の施設数として集計・表示いたします。
・元の資料を再配布することはございません。
・「新宿区『令和7年度末全食品衛生許可施設一覧』を加工して作成」のように出典を明記し、新宿区が作成したものと誤解されない表示といたします。
・掲載内容についてご指摘をいただいた場合は、速やかに削除いたします。

ご多忙のところ誠に恐れ入りますが、ご検討いただけますと幸いです。
何卒よろしくお願い申し上げます。

――――――――――――
[氏名]
メール：[メールアドレス]
ウェブサイト：[URL]
――――――――――――
```

**In English**: the letter says the map already uses Shinjuku's 2023 open
data, and that a newer FY2025-end list exists on the ward's site but not on
its open-data page. Then it asks three things:
1. Will the FY2025-end list be published as open-data CSV, like the 2023 one?
2. If not, may the map use that list and the monthly lists, limited to trade
   name, business type and address?
3. What credit wording is required?

It promises the same use terms as the other letters.

## When a reply comes

- **CSV published**: download it into `data/tokyo/raw/13104/`, re-run
  `screen_japan_join.py shinjuku` and the Japan list, and record it in
  `DECISIONS.md`.
- **Permission to use the PDF**: record its wording and date here and in
  `DECISIONS.md`, then parse the premises lines only (the probe's parser is in
  `scratchpad/tokyo_fix/sj_*.py`, and it must drop the operator line).
- **No**: Shinjuku stays on its 2023 list, with the vintage disclosed.
- **Silence is not consent.**

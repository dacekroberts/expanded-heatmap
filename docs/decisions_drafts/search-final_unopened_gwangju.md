# Gwangju: stations the index step skipped as not yet open

For `docs/place_search_unopened_stations.json`, to be added by Cleanup when
the branches come together (Cleanup, 2026-10-13). Read 2026-10-13 from
`data/gwangju/raw/osm_places_2026-10-13.json` (south-korea-261012). All 35 are
`station=light_rail`; none carries a line or network tag. "Line by id" is what
a relation says of this node: relations 8032733 (2호선 내선순환) and 9283743
(2호선 외선순환), both `state=in_progress`, are in
`data/gwangju/raw/osm_rail_routes.json` and list other stop nodes, so one node
is a member by id. "Name in relation" is whether a stop of that name is a
member, which is evidence of a name and not of the node. 유덕 is two nodes
about 10 m apart, so 35 rows are 34 stations. The unopened 광주 node carries
the open Korail station's wikidata (Q489731).

| OSM id | Name | Tag that skipped it | ref | Line by id | Name in the Line 2 relations |
|---|---|---|---|---|---|
| node/10678377270 | 시청 | railway=construction | 201 | null | yes |
| node/10678377271 | 치평 | railway=construction | 202 | null | yes |
| node/8201420445 | 상무 | railway=construction | 203 | null | yes |
| node/10678377272 | 금호 | railway=construction | 204 | null | yes |
| node/6356359134 | 금부 | railway=construction | 205 | null | yes |
| node/6356359135 | 마재 | railway=construction | 206 | null | yes |
| node/6356359136 | 월드컵경기장 | railway=construction | 207 | null | yes |
| node/6356359137 | 풍암 | railway=construction | 208 | null | yes |
| node/6356359138 | 원광대병원 | railway=construction | 209 | null | yes |
| node/6356359139 | 주월 | railway=construction | 210 | null | yes |
| node/6356359140 | 백운(남구청) | railway=construction | none | null | yes |
| node/10678377251 | 양림 | railway=construction | 212 | null | yes |
| node/6356362774 | 조선대 | railway=construction | 215 | null | yes |
| node/6390594777 | 지산(법원·검찰청) | railway=construction | 216 | null | yes |
| node/6390594778 | 두암 | railway=construction | 217 | null | yes |
| node/6390594779 | 서방사거리(교대) | railway=construction | 218 | null | yes |
| node/8201420439 | 광주 | railway=construction | none | null | yes |
| node/8201420440 | 전남대(북구청) | railway=construction | none | null | yes |
| node/10678377253 | 용봉 | railway=construction | 221 | null | yes |
| node/10678377254 | 오치 | railway=construction | 222 | null | yes |
| node/10678377255 | 매곡 | railway=construction | 223 | null | yes |
| node/10678377256 | 삼각 | railway=construction | none | null | yes |
| node/10678377257 | 일곡 | railway=construction | 225 | null | yes |
| node/10678377258 | 본촌산단 | railway=construction | none | null | yes |
| node/10678377260 | 양산 | railway=construction | 228 | null | yes |
| node/10678377261 | 용두 | railway=construction | none | null | yes |
| node/10678377262 | 신용 | railway=construction | 230 | null | no |
| node/10678377263 | 지스트 | railway=construction | 231 | null | yes |
| node/10678377264 | 첨단사거리 | railway=construction | 232 | null | yes |
| node/10678377265 | 응암공원 | railway=construction | 233 | null | yes |
| node/10678377266 | 하남산단 | railway=construction | 234 | null | yes |
| node/10678377267 | 수완 | railway=construction | 235 | null | yes |
| node/10678377268 | 운남 | railway=construction | 236 | null | yes |
| node/6253309709 | 유덕 | construction:railway=station | 238 | Line 2, relations 8032733 and 9283743 | yes |
| node/13509361841 | 유덕 | construction:railway=station | 238 | null | yes |

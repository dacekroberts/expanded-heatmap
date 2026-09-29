# DGAE (Portugal): data request for Lisbon and Porto — DRAFTED 2026-09-28, NOT SENT

**Status: drafted 2026-09-28 for the owner to review and, if they choose,
send** from their own address. Nothing sent. Kept to revisit; Lisbon waits in
Band R (restricted or request only). Tracked as item 28 in
`docs/gated_access.md`.

**To**: `mapadocomercio@dgae.gov.pt`, the contact named on the site's privacy
page, together with Av. Visconde de Valmor, 72, 1069-041 Lisboa and
+351 217 919 100. The site's credits page names the Secretaria-Geral da
Economia e Mar for technical maintenance (the export and accounts). **Untested**:
whether the address delivers.

## Why this exists

DGAE's **Mapa do Comércio, Serviços e Restauração** (`mapadocomercio.dgae.gov.pt`)
is the public face of the RJACSR national register of retail, services and
restaurant establishments. The owner checked it on 2026-09-28:

- **The public map works without login**, nationwide, with Lisbon-area clusters
  of about 6,700 to 11,000 points. A point shows **exploration type**
  (Comércio / Serviços / Restauração: the project's three buckets), the **CAE**
  activity, a **full street address**, **coordinates** and a registration code.
  There is no status or closing date.
- **Bulk access is not open to individuals.** The data interface's export
  (`/estabelecimentos/exportar`) answers 401 anonymously (probe of 2026-09-24),
  and the registration form's *entity type* offers only Administração Pública
  Central, Município and Estrutura Associativa. An account is therefore not
  something the owner can honestly hold, which makes this route a request.
- **Reuse terms are silent.** The site's legal page is a visitor privacy
  policy only (Law 67/98). `dados.gov.pt` carries no copy of the register,
  only aggregate statistics.
- **Two traps the request addresses up front:** sole traders appear under
  their own names, often at home addresses (never published, by the owner's
  rule); and market and mobile traders are registered at the trader's home
  (excluded as non-storefront).

The owner's rule (2026-09-28): request-only cities sit in Band R. A yes with
an export and permissive terms would move **Lisbon and Porto** together.

## The request (European Portuguese; fill in the placeholders)

It describes the project as a **personal, non-profit portfolio map**; correct
that if it is not accurate.

```text
Para: mapadocomercio@dgae.gov.pt
Assunto: Pedido de dados do Mapa do Comércio, Serviços e Restauração (municípios de Lisboa e do Porto)

Exmos. Senhores,
Direção-Geral das Atividades Económicas
Equipa do Mapa do Comércio, Serviços e Restauração

O meu nome é [Nome]. Estou a desenvolver, a título pessoal e sem fins lucrativos, um mapa web que representa a densidade de estabelecimentos de comércio, serviços e restauração em torno das estações de metropolitano e de comboio urbano de várias cidades do mundo.

Consultei o Mapa do Comércio, Serviços e Restauração e verifiquei que o registo previsto no RJACSR contém precisamente a informação de que necessito. Uma vez que o registo na plataforma se destina a entidades da Administração Pública, municípios e estruturas associativas, venho por este meio solicitar:

1. Uma exportação dos estabelecimentos registados nos municípios de Lisboa e do Porto, com os seguintes campos: tipo de exploração (comércio, serviços, restauração), CAE, morada, coordenadas e, se disponível, a data de registo ou a situação do estabelecimento (em atividade / encerrado);
2. Informação sobre as condições de reutilização destes dados, nomeadamente a licença aplicável e a forma de citação da fonte.

Quanto à utilização prevista:
- Os dados seriam apresentados num mapa de densidade, por categoria de atividade;
- Não publicaria nomes de pessoas singulares (empresários em nome individual); esses estabelecimentos surgiriam apenas pela respetiva categoria;
- Excluiria o comércio não sedentário (feiras, bancas e unidades móveis), cujo registo corresponde frequentemente à residência do titular;
- A DGAE seria identificada como fonte, nos termos que indicarem, e os dados seriam retirados a qualquer pedido vosso.

Fico ao dispor para qualquer esclarecimento adicional e agradeço desde já a atenção dispensada.

Com os melhores cumprimentos,
[Nome]
[Email]
[Endereço do projeto]
```

## English copy (for the owner; not to send)

```text
To: mapadocomercio@dgae.gov.pt
Subject: Request for data from the Retail, Services and Restaurants Map (municipalities of Lisbon and Porto)

Dear Sirs,
Directorate-General for Economic Activities (DGAE)
Retail, Services and Restaurants Map team

My name is [Name]. I am building, personally and on a non-profit basis, a web map showing the density of retail, service and restaurant establishments around metro and urban rail stations in several cities around the world.

I have consulted the Retail, Services and Restaurants Map and found that the RJACSR register holds exactly the information I need. As registration on the platform is intended for public administration bodies, municipalities and associations, I am writing to request:

1. An export of the establishments registered in the municipalities of Lisbon and Porto, with these fields: exploration type (retail, services, restaurants), CAE, address, coordinates and, if available, the registration date or the establishment's status (active / closed);
2. Information on the conditions for reusing this data, in particular the applicable licence and how the source should be credited.

On the intended use:
- The data would be shown on a density map, by activity category;
- I would not publish the names of natural persons (sole traders); their establishments would appear by category only;
- I would exclude non-sedentary trade (markets, stalls and mobile units), whose registration often corresponds to the holder's home;
- DGAE would be credited as the source, as you indicate, and the data would be withdrawn at any request from you.

I remain available for any further clarification and thank you in advance for your attention.

Kind regards,
[Name]
[Email]
[Project address]
```

## If DGAE replies

- **With an export and terms**: run `read-licence` on the terms, add a
  `docs/data_sources/portugal.md` row, and move Lisbon (and Porto) toward
  Band A with a brief. Record the date and the reply in item 28.
- **With terms but no export**: record the terms; the public map is not a bulk
  route (no scraping of its interface).
- **With a refusal**: honour it, record it, and move Lisbon and Porto to the
  discards on terms.

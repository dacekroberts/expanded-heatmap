"""Seattle (Regional)-specific settings, scoped to one city per this project's
per-city folder architecture (see docs/project_context.md, "Architecture").

Scaffolded by scripts/scaffold_city.py. The brief is
docs/build_briefs/seattle.md; every call below is the owner's, settled
2026-10-01 and 2026-10-02 (the brief's "Open for the owner").

ONE PAGE, ELEVEN CITIES, FIVE PUBLISHERS. Link's 1 and 2 Lines serve 39
stations in 11 cities across King and Snohomish Counties. No register covers
them all, so each bucket in each place comes from whoever publishes it (the
brief's "What each jurisdiction publishes"):

  source       publisher                                  where                  buckets
  -----------  -----------------------------------------  ---------------------  -------------------
  seattle      City of Seattle, Business Locations        Seattle                all three
  bellevue     City of Bellevue, Business Licenses (All)  Bellevue               Retail, Personal
  kc_food      Public Health - Seattle & King County      King County (in        Food (and food
                                                          Seattle, what the      shops, as Retail)
                                                          register lacks)
  sno_food     Snohomish County, Food Service             Lynnwood, Mountlake    Food (and grocers,
               Establishments (2025)                      Terrace                as Retail)
  lcb_retail   WA Liquor and Cannabis Board, off-premise  outside Seattle and    Retail (alcohol
                                                          Bellevue               licensees only)

`pipeline/taxonomies/seattle.py` dispatches on `source`.
"""

from pathlib import Path

SLUG = "seattle"

# --- Paths ---------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
DATA_RAW = ROOT / "data" / "seattle" / "raw"
DATA_PROCESSED = ROOT / "data" / "seattle" / "processed"
OUTPUTS = ROOT / "outputs" / "seattle"

HEATMAP_HTML = OUTPUTS / "heatmap.html"
# Stations left out, with the reason and the city each lies in.
EXCLUDED_STATIONS_CSV = OUTPUTS / "excluded_stations.csv"
# Every station's city (Miami's precedent: the boundary names, never filters).
STATION_CITIES_CSV = OUTPUTS / "station_municipalities.csv"
PROVENANCE_JSON = OUTPUTS / "provenance.json"

STATIONS_CSV = DATA_PROCESSED / "stations.csv"
BUSINESSES_CLEAN_CSV = DATA_PROCESSED / "businesses_clean.csv"
# Step 1 writes the two lines (track ways only) for load_geojson_line_shapes.
LINES_GEOJSON = DATA_PROCESSED / "lines.geojson"
# Step 1 writes the area businesses are drawn from: the station cities plus
# every station's 0.6 mi ring, wherever it falls (the brief, item 7).
SCOPE_GEOJSON = DATA_PROCESSED / "business_scope.geojson"

# --- Raw inputs (fetch_sources.py downloads; no step fetches) --------------

# RAIL FROM OPENSTREETMAP, NOT SOUND TRANSIT'S GTFS (owner, 2026-10-02: "we
# can use openstreetmap here"). The feed is current (SC-Fall-2026.3, feed_info
# 2026-09-01 to 2027-03-26), so the ground is its terms, not staleness: the
# Transit Data Terms add a "No Changes" clause, a duty to pass the terms on,
# an open indemnity, registration by email and usage metrics on request.
# data/seattle/raw/st_gtfs_40.zip measured the 39 stations for the brief and
# is NOT a source. Gate 3's count is Sound Transit's own station pages.
OSM_ROUTES_JSON = DATA_RAW / "osm_rail.json"
# One Overpass query for the corridor box, Lynnwood to Federal Way and
# Seattle to Redmond: every light-rail, subway and tram relation in it, so
# step 1 must name anything it does not draw.
RAIL_BBOX = (47.28, -122.42, 47.84, -122.08)          # south, west, north, east

# King County's city polygons (CITY_KC_AREA_446): every King County station
# city, Des Moines, Beaux Arts and the unincorporated areas the rings reach.
KC_CITIES_URL = ("https://services.arcgis.com/Ej0PsM5Aw677QF1W/arcgis/rest/services/"
                 "CITY_KC_AREA_446/FeatureServer/0/query")
KC_CITIES_QUERY = {"where": "1=1", "outFields": "JURIS,CITYNAME", "outSR": "4326",
                   "f": "geojson"}
KC_CITIES_GEOJSON = DATA_RAW / "kc_city_polygons.geojson"

# Lynnwood and Mountlake Terrace are in Snohomish County, outside King
# County's layer: the Census Bureau's place polygons (TIGERweb, current
# Incorporated Places), a federal work in the public domain, the family
# Buffalo and Washington D.C. already read.
SNO_CITIES_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
                  "Places_CouSub_ConCity_SubMCD/MapServer/4/query")
# NAME reads "Lynnwood city"; BASENAME is the bare name.
SNO_CITIES_QUERY = {"where": "STATE='53' AND BASENAME IN ('Lynnwood','Mountlake Terrace')",
                    "outFields": "GEOID,NAME,BASENAME,AREALAND,AREAWATER", "outSR": "4326",
                    "f": "geojson"}
SNO_CITIES_GEOJSON = DATA_RAW / "sno_city_polygons_tiger.geojson"

# The eleven station cities, as King County's layer and TIGER name them.
STATION_CITIES = ("Seattle", "Bellevue", "Redmond", "Shoreline", "SeaTac", "Kent",
                  "Tukwila", "Federal Way", "Mercer Island", "Lynnwood",
                  "Mountlake Terrace")
# Unincorporated King County's polygons carry CITYNAME "King County" (JURIS
# KC); this label names them in every count.
KC_UNINCORPORATED_CITYNAME = "King County"
UNINCORPORATED = "Unincorporated King County"
# The part of a ring in no loaded polygon. Only Lynnwood City Center's ring
# has one (11.7% of it, measured 2026-10-02): unincorporated Snohomish
# County, north of the King County line. Step 1 refuses a gap further south.
SNO_UNINCORPORATED = "Unincorporated Snohomish County"
SNO_GAP_MIN_LAT = 47.775    # the King-Snohomish line runs at about 47.777
# Step 1 writes every place a business can be in (the station cities, the
# places the rings reach, and the Snohomish gap), for step 2's labels.
PLACES_GEOJSON = DATA_PROCESSED / "places.geojson"

# ArcGIS layers are paged (maxRecordCount 1000-2000) by objectid.
ARCGIS_PAGE = 1000

# King County's address points (ADDRESS_POINT_642, 674,254 points), the join
# target for King County food (by parcel PIN) and the Liquor Board's premises
# (by address). ONLY the geometry and the County's own fields: CTYNAME,
# POSTALCTYNAME and the ZIP fields come from the USPS ZIP+4 product and are
# never requested (owner, 2026-10-01).
KC_ADDRESS_URL = ("https://services.arcgis.com/Ej0PsM5Aw677QF1W/arcgis/rest/services/"
                  "ADDRESS_POINT_642/FeatureServer/0")
KC_ADDRESS_FIELDS = ("OBJECTID,PIN,MAJOR,MINOR,ADDR_FULL,ADDR_HN,ADDR_PD,ADDR_PT,"
                     "ADDR_SN,ADDR_ST,ADDR_SD,PRIM_ADDR,SITETYPE,LAT,LON")
KC_ADDRESS_CSV = DATA_RAW / "kc_address_points.csv"

# Snohomish County's building address points (SnocoGIS, E911 addressing),
# the Liquor Board join target in Lynnwood and Mountlake Terrace, bounded to
# the two cities' box at download. Geometry and the address fields only.
SNO_ADDRESS_URL = ("https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/"
                   "Building_Address_Points/FeatureServer/0")
SNO_ADDRESS_FIELDS = ("OBJECTID,Add_Number,AddNum_Suf,St_PreDir,St_PreTyp,St_Name,"
                      "St_PosTyp,St_PosDir,Unit,FULL_ADDR,Inc_Muni,Lat,Long")
SNO_ADDRESS_BBOX = (47.76, -122.36, 47.87, -122.24)   # south, west, north, east
SNO_ADDRESS_CSV = DATA_RAW / "sno_address_points.csv"

# Each business source: the raw file, the endpoint, the fields requested
# (never a contact, mailing or person column), and the columns step 2 reads.
SOURCES = {
    "seattle": {
        "file": DATA_RAW / "seattle_licences.csv",
        "endpoint": ("https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/"
                     "Seattle_Business_License/FeatureServer/0"),
        # BUSLIC_CONTACT_NAME, BUSLIC_PHONE_NUM, BUSLIC_MAIL_ADRS_TEXT and
        # the legal name are never requested; step 2 asserts it.
        "fields": ("objectid,BUSLIC_ID,BUSLIC_LOCATION_ID,BUSLIC_BUSINESS_ID,"
                   "BUSLIC_YEAR_NUM,BUSLIC_EXPIRATION_DATE,BUSLIC_TRADE_NAME,"
                   "BUSLIC_LOCATION_TYPE,BUSLIC_STATUS_TYPE,BUSLIC_NAICS_CODE,"
                   "BUSLIC_NAICS_DESC,BUSLIC_LOCATION_ADRS_TEXT,BUSLIC_OPENDATE"),
        "key_column": "BUSLIC_LOCATION_ID",
        "name_column": "BUSLIC_TRADE_NAME",
        "category_column": "BUSLIC_NAICS_CODE",
    },
    # Seattle's locations whose trade name IS the legal name, asked of the
    # server as a column comparison so the legal names never download: only
    # the location ids come back (20,519 of 54,689 on 2026-10-02). Step 2's
    # name rule reads it.
    "seattle_same_name": {
        "file": DATA_RAW / "seattle_trade_is_legal.csv",
        "endpoint": ("https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/"
                     "Seattle_Business_License/FeatureServer/0"),
        "where": "BUSLIC_TRADE_NAME = BUSLIC_LEGAL_NAME",
        "fields": "objectid,BUSLIC_LOCATION_ID",
        "key_column": "BUSLIC_LOCATION_ID",
        "aux": True,
    },
    "bellevue": {
        "file": DATA_RAW / "bellevue_licences.csv",
        "endpoint": ("https://services1.arcgis.com/EYzEZbDhXZjURPbP/arcgis/rest/services/"
                     "Business_Licenses_(All)/FeatureServer/3"),
        # LegalEntityName, Ubi and every Mailing* field are never requested:
        # a row with no trade name shows its category (owner, 2026-10-02).
        "fields": ("OBJECTID,BusinessId,Dba,Naic,LegalEntityType,FirstActivityDate,"
                   "CancelDate,IssueDate,PhysicalAddressLine1,PhysicalAddressLine2,"
                   "PhysicalCity,NeighborhoodArea,PlanningZone,Latitude,Longitude"),
        "key_column": "BusinessId",
        "name_column": "Dba",
        "category_column": "Naic",
    },
    "kc_food": {
        "file": DATA_RAW / "kc_food_inspections.csv",
        "endpoint": "https://data.kingcounty.gov/resource/r878-4sxa.csv",
        # One row per inspection and violation; the violation text is not
        # requested. Step 2 keeps a business by its latest inspection.
        "query": {
            "$select": "business_id,name,program_identifier,classification,"
                       "seating_range,risk_category,address,city,zip_code,"
                       "parcel_number,inspection_date,inspection_type,"
                       "inspection_closed_business,inspection_serial_num",
            "$order": "business_id,inspection_date,inspection_serial_num",
            "$limit": "500000",
        },
        "key_column": "business_id",
        "name_column": "name",
        "category_column": "classification",
    },
    "sno_food": {
        "file": DATA_RAW / "sno_food_establishments.csv",
        "endpoint": ("https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/"
                     "Food_Service_Establishments/FeatureServer/0"),
        # The layer's waste-hauler and yard-waste fields are not requested.
        "fields": ("OBJECTID,User_Fld,USER_Name,USER_Full_Site_Address,USER_City,"
                   "USER_Program_Element,USER_Program_Identifier,USER_Facility_ID,"
                   "USER_Record_ID,Icon"),
        "key_column": "USER_Facility_ID",
        "name_column": "USER_Name",
        "category_column": "Icon",
    },
}

# --- Coordinate reference systems -----------------------------------------

CRS_GEOGRAPHIC = "EPSG:4326"

# UTM zone 10N: the corridor (~-122.33 to -122.13) falls in the -126 to -120
# band. Derived per city, not copied - see docs/project_context.md's CRS
# lesson. The sources' own CRSs (Washington North feet, EPSG:2926; Web
# Mercator) are only ever read back to WGS84 by the server (outSR 4326).
CRS_PROJECTED = "EPSG:32610"

# --- Ring geometry ---------------------------------------------------------
# THE SHARED EDGES: the 39 stations' median nearest neighbour is 1,346 m (the
# brief's read of the GTFS), far above the 0.6 mi outer ring. Step 1 prints
# OSM's own figure.
METERS_PER_MILE = 1609.344
RING_EDGES_MILES = [0.0, 0.1, 0.2, 0.3, 0.6]
RING_EDGES_METERS = [m * METERS_PER_MILE for m in RING_EDGES_MILES]
RING_LABELS = ["0-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi", "0.3-0.6 mi"]

# --- Station scope ----------------------------------------------------------
#
# Link's 1 Line (Lynnwood City Center - Federal Way Downtown) and 2 Line
# (Lynnwood City Center - Downtown Redmond), every station: a grade-separated
# light-rail system with stations a median 1.3 km apart, so nothing is
# thinned. Matched on network + ref + route, a whitelist; every other
# relation in the box is named in NOT_DRAWN or step 1 exits.
ROUTE_TYPES = ("light_rail", "subway", "tram")    # what the query fetches
# OSM's four Link relations (1 Line 3494092 and 5517060; 2 Line 17499739 and
# 17499740) carry network "Link" and ref "1 Line" / "2 Line" (read
# 2026-10-02, overpass.kumi.systems).
NETWORK = "Link"
LINE_REFS = {"1": "1 Line", "2": "2 Line"}
# The relations in the box that are not drawn, each with its reason. The
# owner's scope is Link's 1 and 2 Lines (PLAN.md's Seattle item, 2026-09-20).
NOT_DRAWN = {
    4748655: "Seattle Streetcar, South Lake Union line: a streetcar, outside the "
             "owner's Link scope",
    4748656: "Seattle Streetcar, South Lake Union line (other direction)",
    4755830: "Seattle Streetcar, First Hill line: a streetcar, outside the owner's "
             "Link scope",
    4755831: "Seattle Streetcar, First Hill line (other direction)",
    6495673: "SEA Underground: the airport's terminal people mover, not public transit",
    6495674: "SEA Underground (Blue)",
    6495675: "SEA Underground (Green)",
    10077846: "SEA Underground (Yellow, southbound)",
}

# Line colours: Sound Transit's own (the relations' colour tags) moved just
# far enough to clear the project's CIE76 Delta-E of 45 against the pins
# (add-city Step 6; Edmonton's and Pittsburgh's way). The 1 Line's #3DAE2B
# scored 37.8 against Personal services; lightened x1.15 at the same hue it
# is #46C831, 46.2. The 2 Line's #00A0DF scored 28.6 against Retail; six
# degrees of hue toward cyan make #00B6DF, 45.3. Darkening alone needed
# x0.38 and x0.42 lightness (#174210, #00435E), too dark to tell apart.
LINE_COLOURS = {"1": "#46C831", "2": "#00B6DF"}

# One stop under two names (the two directions' stop nodes): none. OSM's 38
# names collapse cleanly (read 2026-10-02).
STATION_NAME_ALIASES = {}

SPACING_MIN_M = 400.0

# GATE 3: Sound Transit's own line pages (soundtransit.org/ride-with-us/
# routes-schedules/1-line and 2-line, read 2026-10-02): the 1 Line serves 27
# stations and the 2 Line 26, 39 distinct, 14 on both, Pinehurst included.
OPERATOR_STATION_COUNTS = {"1 Line": 27, "2 Line": 26}
OPERATOR_STATION_TOTAL = 39
OPERATOR_COUNTS_SOURCE = ("Sound Transit's 1 Line and 2 Line pages, read 2026-10-02: "
                          "27 and 26 stations, 39 distinct, Pinehurst included")
# Stations Sound Transit serves that OSM's relations did not yet carry
# (2026-10-02): placed from the operator's own station page, and refused once
# the relations carry them (Taoyuan's rule, osm-rail "Three more"). Pinehurst
# opened 2026-09-30; its page gives "13110 5th Ave NE, Seattle, WA 98125",
# placed at King County's address point for that address.
STATIONS_ADDED = {
    "Pinehurst": {"address": "13110 5TH AVE NE", "lines": ("1", "2"),
                  "opened": "2026-09-30",
                  "source": "Sound Transit's Pinehurst Station page (13110 5th Ave NE), "
                            "at King County's address point"},
}

# --- Business filtering ------------------------------------------------

# The fetch date, against which licence years and inspection dates are read.
# Set by fetch_sources.py's run; step 2 re-applies it, so a re-run and a drift
# check stay deterministic.
AS_OF_DATE = "2026-10-02"

# In-city rows are identified by point-in-boundary, never by a city-name
# field: Seattle's addresses all read "SEATTLE" although 1,012 rows lie in
# other places, and King County food's `city` is the postal city.
CITY_KEEP = None

TAXONOMY_SYSTEM = "seattle"
# Already the taxonomy's VALUE_COLUMN, so step 2's rename is a no-op.
RAW_CLASSIFICATION_COLUMN = "business_category"

# Sanity bounds: the business scope's extent (Lynnwood to Federal Way,
# Seattle to Redmond) plus ~0.02 deg.
SEATTLE_BBOX = {
    "lat_min": 47.27,
    "lat_max": 47.85,
    "lon_min": -122.45,
    "lon_max": -122.06,
}

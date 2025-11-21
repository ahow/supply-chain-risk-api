"""
OECD ICIO Extended Country and Sector Data

Data source: OECD ICIO Extended Edition (2020)
85 countries/regions (including firm heterogeneity splits)
56 sectors (ISIC Rev. 4 classification)
"""

OECD_ICIO_COUNTRIES = [
  {
    "code": "AGO",
    "name": "Angola",
    "is_extended": False
  },
  {
    "code": "ARE",
    "name": "ARE",
    "is_extended": False
  },
  {
    "code": "ARG",
    "name": "Argentina",
    "is_extended": False
  },
  {
    "code": "AUS",
    "name": "Australia",
    "is_extended": False
  },
  {
    "code": "AUT",
    "name": "Austria",
    "is_extended": False
  },
  {
    "code": "BEL",
    "name": "Belgium",
    "is_extended": False
  },
  {
    "code": "BGD",
    "name": "BGD",
    "is_extended": False
  },
  {
    "code": "BGR",
    "name": "Bulgaria",
    "is_extended": False
  },
  {
    "code": "BLR",
    "name": "BLR",
    "is_extended": False
  },
  {
    "code": "BRA",
    "name": "Brazil",
    "is_extended": False
  },
  {
    "code": "BRN",
    "name": "Brunei",
    "is_extended": False
  },
  {
    "code": "CAN",
    "name": "Canada",
    "is_extended": False
  },
  {
    "code": "CHE",
    "name": "Switzerland",
    "is_extended": False
  },
  {
    "code": "CHL",
    "name": "Chile",
    "is_extended": False
  },
  {
    "code": "CHN",
    "name": "China",
    "is_extended": False
  },
  {
    "code": "CIV",
    "name": "C\u00f4te d'Ivoire",
    "is_extended": False
  },
  {
    "code": "CMR",
    "name": "Cameroon",
    "is_extended": False
  },
  {
    "code": "CN1",
    "name": "CN1",
    "is_extended": False
  },
  {
    "code": "CN2",
    "name": "CN2",
    "is_extended": False
  },
  {
    "code": "COD",
    "name": "COD",
    "is_extended": False
  },
  {
    "code": "COL",
    "name": "Colombia",
    "is_extended": False
  },
  {
    "code": "CRI",
    "name": "Costa Rica",
    "is_extended": False
  },
  {
    "code": "CYP",
    "name": "Cyprus",
    "is_extended": False
  },
  {
    "code": "CZE",
    "name": "Czech Republic",
    "is_extended": False
  },
  {
    "code": "DEU",
    "name": "Germany",
    "is_extended": False
  },
  {
    "code": "DNK",
    "name": "Denmark",
    "is_extended": False
  },
  {
    "code": "EGY",
    "name": "Egypt",
    "is_extended": False
  },
  {
    "code": "ESP",
    "name": "Spain",
    "is_extended": False
  },
  {
    "code": "EST",
    "name": "Estonia",
    "is_extended": False
  },
  {
    "code": "FIN",
    "name": "Finland",
    "is_extended": False
  },
  {
    "code": "FRA",
    "name": "France",
    "is_extended": False
  },
  {
    "code": "GBR",
    "name": "United Kingdom",
    "is_extended": False
  },
  {
    "code": "GRC",
    "name": "Greece",
    "is_extended": False
  },
  {
    "code": "HKG",
    "name": "Hong Kong",
    "is_extended": False
  },
  {
    "code": "HRV",
    "name": "Croatia",
    "is_extended": False
  },
  {
    "code": "HUN",
    "name": "Hungary",
    "is_extended": False
  },
  {
    "code": "IDN",
    "name": "Indonesia",
    "is_extended": False
  },
  {
    "code": "IND",
    "name": "India",
    "is_extended": False
  },
  {
    "code": "IRL",
    "name": "Ireland",
    "is_extended": False
  },
  {
    "code": "ISL",
    "name": "Iceland",
    "is_extended": False
  },
  {
    "code": "ISR",
    "name": "Israel",
    "is_extended": False
  },
  {
    "code": "ITA",
    "name": "Italy",
    "is_extended": False
  },
  {
    "code": "JOR",
    "name": "JOR",
    "is_extended": False
  },
  {
    "code": "JPN",
    "name": "Japan",
    "is_extended": False
  },
  {
    "code": "KAZ",
    "name": "Kazakhstan",
    "is_extended": False
  },
  {
    "code": "KHM",
    "name": "Cambodia",
    "is_extended": False
  },
  {
    "code": "KOR",
    "name": "South Korea",
    "is_extended": False
  },
  {
    "code": "LAO",
    "name": "Laos",
    "is_extended": False
  },
  {
    "code": "LTU",
    "name": "Lithuania",
    "is_extended": False
  },
  {
    "code": "LUX",
    "name": "Luxembourg",
    "is_extended": False
  },
  {
    "code": "LVA",
    "name": "Latvia",
    "is_extended": False
  },
  {
    "code": "MAR",
    "name": "Morocco",
    "is_extended": False
  },
  {
    "code": "MEX",
    "name": "Mexico",
    "is_extended": False
  },
  {
    "code": "MLT",
    "name": "Malta",
    "is_extended": False
  },
  {
    "code": "MMR",
    "name": "Myanmar",
    "is_extended": False
  },
  {
    "code": "MX1",
    "name": "MX1",
    "is_extended": False
  },
  {
    "code": "MX2",
    "name": "MX2",
    "is_extended": False
  },
  {
    "code": "MYS",
    "name": "Malaysia",
    "is_extended": False
  },
  {
    "code": "NGA",
    "name": "Nigeria",
    "is_extended": False
  },
  {
    "code": "NLD",
    "name": "Netherlands",
    "is_extended": False
  },
  {
    "code": "NOR",
    "name": "Norway",
    "is_extended": False
  },
  {
    "code": "NZL",
    "name": "New Zealand",
    "is_extended": False
  },
  {
    "code": "PAK",
    "name": "PAK",
    "is_extended": False
  },
  {
    "code": "PER",
    "name": "Peru",
    "is_extended": False
  },
  {
    "code": "PHL",
    "name": "Philippines",
    "is_extended": False
  },
  {
    "code": "POL",
    "name": "Poland",
    "is_extended": False
  },
  {
    "code": "PRT",
    "name": "Portugal",
    "is_extended": False
  },
  {
    "code": "ROU",
    "name": "Romania",
    "is_extended": False
  },
  {
    "code": "ROW",
    "name": "Rest of World",
    "is_extended": False
  },
  {
    "code": "RUS",
    "name": "Russia",
    "is_extended": False
  },
  {
    "code": "SAU",
    "name": "Saudi Arabia",
    "is_extended": False
  },
  {
    "code": "SEN",
    "name": "Senegal",
    "is_extended": False
  },
  {
    "code": "SGP",
    "name": "Singapore",
    "is_extended": False
  },
  {
    "code": "STP",
    "name": "STP",
    "is_extended": False
  },
  {
    "code": "SVK",
    "name": "Slovakia",
    "is_extended": False
  },
  {
    "code": "SVN",
    "name": "Slovenia",
    "is_extended": False
  },
  {
    "code": "SWE",
    "name": "Sweden",
    "is_extended": False
  },
  {
    "code": "THA",
    "name": "Thailand",
    "is_extended": False
  },
  {
    "code": "TUN",
    "name": "Tunisia",
    "is_extended": False
  },
  {
    "code": "TUR",
    "name": "Turkey",
    "is_extended": False
  },
  {
    "code": "TWN",
    "name": "Taiwan",
    "is_extended": False
  },
  {
    "code": "UKR",
    "name": "UKR",
    "is_extended": False
  },
  {
    "code": "USA",
    "name": "United States",
    "is_extended": False
  },
  {
    "code": "VNM",
    "name": "Vietnam",
    "is_extended": False
  },
  {
    "code": "ZAF",
    "name": "South Africa",
    "is_extended": False
  }
]

OECD_ICIO_SECTORS = [
  {
    "code": "A01",
    "name": "Crop and animal production, hunting"
  },
  {
    "code": "A02",
    "name": "Forestry and logging"
  },
  {
    "code": "A03",
    "name": "Fishing and aquaculture"
  },
  {
    "code": "B05",
    "name": "Mining of coal and lignite"
  },
  {
    "code": "B06",
    "name": "Extraction of crude petroleum and natural gas"
  },
  {
    "code": "B07",
    "name": "Mining of metal ores"
  },
  {
    "code": "B08",
    "name": "Other mining and quarrying"
  },
  {
    "code": "B09",
    "name": "Mining support service activities"
  },
  {
    "code": "C10T12",
    "name": "Food products, beverages and tobacco"
  },
  {
    "code": "C13T15",
    "name": "Textiles, wearing apparel, leather"
  },
  {
    "code": "C16",
    "name": "Wood and products of wood"
  },
  {
    "code": "C17_18",
    "name": "Paper and printing"
  },
  {
    "code": "C19",
    "name": "Coke and refined petroleum products"
  },
  {
    "code": "C20",
    "name": "Chemicals and chemical products"
  },
  {
    "code": "C21",
    "name": "Pharmaceuticals"
  },
  {
    "code": "C22",
    "name": "Rubber and plastics products"
  },
  {
    "code": "C23",
    "name": "Other non-metallic mineral products"
  },
  {
    "code": "C24A",
    "name": "Basic metals (iron and steel)"
  },
  {
    "code": "C24B",
    "name": "Basic metals (non-ferrous)"
  },
  {
    "code": "C25",
    "name": "Fabricated metal products"
  },
  {
    "code": "C26",
    "name": "Computer, electronic and optical products"
  },
  {
    "code": "C27",
    "name": "Electrical equipment"
  },
  {
    "code": "C28",
    "name": "Machinery and equipment n.e.c."
  },
  {
    "code": "C29",
    "name": "Motor vehicles"
  },
  {
    "code": "C301",
    "name": "Ships and boats"
  },
  {
    "code": "C302T309",
    "name": "Other transport equipment"
  },
  {
    "code": "C31T33",
    "name": "Furniture; other manufacturing"
  },
  {
    "code": "D",
    "name": "Electricity, gas, steam and air conditioning"
  },
  {
    "code": "DPABR",
    "name": "DPABR"
  },
  {
    "code": "E",
    "name": "Water supply; sewerage, waste management"
  },
  {
    "code": "F",
    "name": "Construction"
  },
  {
    "code": "G",
    "name": "Wholesale and retail trade"
  },
  {
    "code": "GFCF",
    "name": "GFCF"
  },
  {
    "code": "GGFC",
    "name": "GGFC"
  },
  {
    "code": "H49",
    "name": "Land transport"
  },
  {
    "code": "H50",
    "name": "Water transport"
  },
  {
    "code": "H51",
    "name": "Air transport"
  },
  {
    "code": "H52",
    "name": "Warehousing and support activities"
  },
  {
    "code": "H53",
    "name": "Postal and courier activities"
  },
  {
    "code": "HFCE",
    "name": "HFCE"
  },
  {
    "code": "I",
    "name": "Accommodation and food services"
  },
  {
    "code": "INVNT",
    "name": "INVNT"
  },
  {
    "code": "J58T60",
    "name": "J58T60"
  },
  {
    "code": "J61",
    "name": "Telecommunications"
  },
  {
    "code": "J62_63",
    "name": "J62_63"
  },
  {
    "code": "K",
    "name": "K"
  },
  {
    "code": "L",
    "name": "Real estate activities"
  },
  {
    "code": "M",
    "name": "M"
  },
  {
    "code": "N",
    "name": "N"
  },
  {
    "code": "NPISH",
    "name": "NPISH"
  },
  {
    "code": "O",
    "name": "Public administration and defence"
  },
  {
    "code": "P",
    "name": "Education"
  },
  {
    "code": "Q",
    "name": "Q"
  },
  {
    "code": "R",
    "name": "R"
  },
  {
    "code": "S",
    "name": "S"
  },
  {
    "code": "T",
    "name": "Household activities"
  }
]

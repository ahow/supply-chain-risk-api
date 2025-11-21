"""
EXIOBASE 3 Country and Sector Data

Data source: EXIOBASE 3 (2022)
163 EXIOBASE industries mapped to 34 OECD sectors
49 regions (44 countries + 5 Rest of World)
"""

EXIOBASE_COUNTRIES = [
  {
    "code": "AT",
    "name": "Austria",
    "is_rest_of_world": False
  },
  {
    "code": "BE",
    "name": "Belgium",
    "is_rest_of_world": False
  },
  {
    "code": "BG",
    "name": "Bulgaria",
    "is_rest_of_world": False
  },
  {
    "code": "CY",
    "name": "Cyprus",
    "is_rest_of_world": False
  },
  {
    "code": "CZ",
    "name": "Czech Republic",
    "is_rest_of_world": False
  },
  {
    "code": "DE",
    "name": "Germany",
    "is_rest_of_world": False
  },
  {
    "code": "DK",
    "name": "Denmark",
    "is_rest_of_world": False
  },
  {
    "code": "EE",
    "name": "Estonia",
    "is_rest_of_world": False
  },
  {
    "code": "ES",
    "name": "Spain",
    "is_rest_of_world": False
  },
  {
    "code": "FI",
    "name": "Finland",
    "is_rest_of_world": False
  },
  {
    "code": "FR",
    "name": "France",
    "is_rest_of_world": False
  },
  {
    "code": "GR",
    "name": "Greece",
    "is_rest_of_world": False
  },
  {
    "code": "HR",
    "name": "Croatia",
    "is_rest_of_world": False
  },
  {
    "code": "HU",
    "name": "Hungary",
    "is_rest_of_world": False
  },
  {
    "code": "IE",
    "name": "Ireland",
    "is_rest_of_world": False
  },
  {
    "code": "IT",
    "name": "Italy",
    "is_rest_of_world": False
  },
  {
    "code": "LT",
    "name": "Lithuania",
    "is_rest_of_world": False
  },
  {
    "code": "LU",
    "name": "Luxembourg",
    "is_rest_of_world": False
  },
  {
    "code": "LV",
    "name": "Latvia",
    "is_rest_of_world": False
  },
  {
    "code": "MT",
    "name": "Malta",
    "is_rest_of_world": False
  },
  {
    "code": "NL",
    "name": "Netherlands",
    "is_rest_of_world": False
  },
  {
    "code": "PL",
    "name": "Poland",
    "is_rest_of_world": False
  },
  {
    "code": "PT",
    "name": "Portugal",
    "is_rest_of_world": False
  },
  {
    "code": "RO",
    "name": "Romania",
    "is_rest_of_world": False
  },
  {
    "code": "SE",
    "name": "Sweden",
    "is_rest_of_world": False
  },
  {
    "code": "SI",
    "name": "Slovenia",
    "is_rest_of_world": False
  },
  {
    "code": "SK",
    "name": "Slovakia",
    "is_rest_of_world": False
  },
  {
    "code": "GB",
    "name": "United Kingdom",
    "is_rest_of_world": False
  },
  {
    "code": "US",
    "name": "United States",
    "is_rest_of_world": False
  },
  {
    "code": "JP",
    "name": "Japan",
    "is_rest_of_world": False
  },
  {
    "code": "CN",
    "name": "China",
    "is_rest_of_world": False
  },
  {
    "code": "CA",
    "name": "Canada",
    "is_rest_of_world": False
  },
  {
    "code": "KR",
    "name": "South Korea",
    "is_rest_of_world": False
  },
  {
    "code": "BR",
    "name": "Brazil",
    "is_rest_of_world": False
  },
  {
    "code": "IN",
    "name": "India",
    "is_rest_of_world": False
  },
  {
    "code": "MX",
    "name": "Mexico",
    "is_rest_of_world": False
  },
  {
    "code": "RU",
    "name": "Russia",
    "is_rest_of_world": False
  },
  {
    "code": "AU",
    "name": "Australia",
    "is_rest_of_world": False
  },
  {
    "code": "CH",
    "name": "Switzerland",
    "is_rest_of_world": False
  },
  {
    "code": "TR",
    "name": "Turkey",
    "is_rest_of_world": False
  },
  {
    "code": "TW",
    "name": "Taiwan",
    "is_rest_of_world": False
  },
  {
    "code": "NO",
    "name": "Norway",
    "is_rest_of_world": False
  },
  {
    "code": "ID",
    "name": "Indonesia",
    "is_rest_of_world": False
  },
  {
    "code": "ZA",
    "name": "South Africa",
    "is_rest_of_world": False
  },
  {
    "code": "WA",
    "name": "RoW Asia and Pacific",
    "is_rest_of_world": True
  },
  {
    "code": "WL",
    "name": "RoW America",
    "is_rest_of_world": True
  },
  {
    "code": "WE",
    "name": "RoW Europe",
    "is_rest_of_world": True
  },
  {
    "code": "WF",
    "name": "RoW Africa",
    "is_rest_of_world": True
  },
  {
    "code": "WM",
    "name": "RoW Middle East",
    "is_rest_of_world": True
  }
]

EXIOBASE_SECTORS = [
  {
    "code": "D01T03",
    "name": "Agriculture, forestry and fishing"
  },
  {
    "code": "D05T09",
    "name": "Mining and quarrying"
  },
  {
    "code": "D10T12",
    "name": "Food products, beverages and tobacco"
  },
  {
    "code": "D13T15",
    "name": "Textiles, wearing apparel, leather and related products"
  },
  {
    "code": "D16",
    "name": "Wood and products of wood and cork"
  },
  {
    "code": "D17T18",
    "name": "Paper and printing"
  },
  {
    "code": "D19",
    "name": "Coke and refined petroleum products"
  },
  {
    "code": "D20T21",
    "name": "Chemicals and pharmaceutical products"
  },
  {
    "code": "D23",
    "name": "Other non-metallic mineral products"
  },
  {
    "code": "D24",
    "name": "Basic metals"
  },
  {
    "code": "D25",
    "name": "Fabricated metal products"
  },
  {
    "code": "D26T27",
    "name": "Computer, electronic and optical products; Electrical equipment"
  },
  {
    "code": "D29T30",
    "name": "Transport equipment"
  },
  {
    "code": "D31T33",
    "name": "Furniture; other manufacturing"
  },
  {
    "code": "D35T39",
    "name": "Electricity, gas, water supply, sewerage, waste and remediation services"
  },
  {
    "code": "D41T43",
    "name": "Construction"
  },
  {
    "code": "D49T53",
    "name": "Transportation and storage"
  },
  {
    "code": "D61",
    "name": "Telecommunications"
  },
  {
    "code": "D64T66",
    "name": "Financial and insurance activities"
  },
  {
    "code": "D68",
    "name": "Real estate activities"
  },
  {
    "code": "D77T82",
    "name": "Administrative and support services"
  },
  {
    "code": "D85",
    "name": "Education"
  },
  {
    "code": "D86T88",
    "name": "Human health and social work"
  },
  {
    "code": "D90T96",
    "name": "Arts, entertainment, recreation and other service activities"
  },
  {
    "code": "D97T98",
    "name": "Activities of households as employers"
  }
]

# Mapping from EXIOBASE 163 sectors to OECD 34 sectors
EXIOBASE_TO_OECD_MAPPING = {
  "Cultivation of paddy rice": "D01T03",
  "Cultivation of wheat": "D01T03",
  "Cultivation of cereal grains nec": "D01T03",
  "Cultivation of vegetables, fruit, nuts": "D01T03",
  "Cultivation of oil seeds": "D01T03",
  "Cultivation of sugar cane, sugar beet": "D01T03",
  "Cultivation of plant-based fibers": "D01T03",
  "Cultivation of crops nec": "D01T03",
  "Cattle farming": "D01T03",
  "Pigs farming": "D01T03",
  "Poultry farming": "D01T03",
  "Meat animals nec": "D01T03",
  "Animal products nec": "D90T96",
  "Raw milk": "D01T03",
  "Wool, silk-worm cocoons": "D01T03",
  "Manure treatment (conventional), storage and land application": "D90T96",
  "Manure treatment (biogas), storage and land application": "D90T96",
  "Forestry, logging and related service activities (02)": "D01T03",
  "Fishing, operating of fish hatcheries and fish farms; service activities incidental to fishing (05)": "D01T03",
  "Mining of coal and lignite; extraction of peat (10)": "D05T09",
  "Extraction of crude petroleum and services related to crude oil extraction, excluding surveying": "D05T09",
  "Extraction of natural gas and services related to natural gas extraction, excluding surveying": "D05T09",
  "Extraction, liquefaction, and regasification of other petroleum and gaseous materials": "D05T09",
  "Mining of uranium and thorium ores (12)": "D05T09",
  "Mining of iron ores": "D05T09",
  "Mining of copper ores and concentrates": "D05T09",
  "Mining of nickel ores and concentrates": "D05T09",
  "Mining of aluminium ores and concentrates": "D05T09",
  "Mining of precious metal ores and concentrates": "D05T09",
  "Mining of lead, zinc and tin ores and concentrates": "D05T09",
  "Mining of other non-ferrous metal ores and concentrates": "D05T09",
  "Quarrying of stone": "D05T09",
  "Quarrying of sand and clay": "D05T09",
  "Mining of chemical and fertilizer minerals, production of salt, other mining and quarrying n.e.c.": "D05T09",
  "Processing of meat cattle": "D01T03",
  "Processing of meat pigs": "D01T03",
  "Processing of meat poultry": "D01T03",
  "Production of meat products nec": "D01T03",
  "Processing vegetable oils and fats": "D10T12",
  "Processing of dairy products": "D10T12",
  "Processed rice": "D10T12",
  "Sugar refining": "D10T12",
  "Processing of Food products nec": "D10T12",
  "Manufacture of beverages": "D10T12",
  "Manufacture of fish products": "D90T96",
  "Manufacture of tobacco products (16)": "D10T12",
  "Manufacture of textiles (17)": "D13T15",
  "Manufacture of wearing apparel; dressing and dyeing of fur (18)": "D13T15",
  "Tanning and dressing of leather; manufacture of luggage, handbags, saddlery, harness and footwear (19)": "D13T15",
  "Manufacture of wood and of products of wood and cork, except furniture; manufacture of articles of straw and plaiting materials (20)": "D16",
  "Re-processing of secondary wood material into new wood material": "D16",
  "Pulp": "D17T18",
  "Re-processing of secondary paper into new pulp": "D17T18",
  "Paper": "D17T18",
  "Publishing, printing and reproduction of recorded media (22)": "D17T18",
  "Manufacture of coke oven products": "D19",
  "Petroleum Refinery": "D19",
  "Processing of nuclear fuel": "D90T96",
  "Plastics, basic": "D20T21",
  "Re-processing of secondary plastic into new plastic": "D90T96",
  "N-fertiliser": "D90T96",
  "P- and other fertiliser": "D90T96",
  "Chemicals nec": "D20T21",
  "Manufacture of rubber and plastic products (25)": "D20T21",
  "Manufacture of glass and glass products": "D23",
  "Re-processing of secondary glass into new glass": "D23",
  "Manufacture of ceramic goods": "D23",
  "Manufacture of bricks, tiles and construction products, in baked clay": "D23",
  "Manufacture of cement, lime and plaster": "D23",
  "Re-processing of ash into clinker": "D90T96",
  "Manufacture of other non-metallic mineral products n.e.c.": "D90T96",
  "Manufacture of basic iron and steel and of ferro-alloys and first products thereof": "D24",
  "Re-processing of secondary steel into new steel": "D24",
  "Precious metals production": "D24",
  "Re-processing of secondary preciuos metals into new preciuos metals": "D90T96",
  "Aluminium production": "D24",
  "Re-processing of secondary aluminium into new aluminium": "D24",
  "Lead, zinc and tin production": "D90T96",
  "Re-processing of secondary lead into new lead, zinc and tin": "D90T96",
  "Copper production": "D24",
  "Re-processing of secondary copper into new copper": "D24",
  "Other non-ferrous metal production": "D90T96",
  "Re-processing of secondary other non-ferrous metals into new other non-ferrous metals": "D90T96",
  "Casting of metals": "D24",
  "Manufacture of fabricated metal products, except machinery and equipment (28)": "D25",
  "Manufacture of machinery and equipment n.e.c. (29)": "D90T96",
  "Manufacture of office machinery and computers (30)": "D26T27",
  "Manufacture of electrical machinery and apparatus n.e.c. (31)": "D90T96",
  "Manufacture of radio, television and communication equipment and apparatus (32)": "D26T27",
  "Manufacture of medical, precision and optical instruments, watches and clocks (33)": "D26T27",
  "Manufacture of motor vehicles, trailers and semi-trailers (34)": "D29T30",
  "Manufacture of other transport equipment (35)": "D90T96",
  "Manufacture of furniture; manufacturing n.e.c. (36)": "D31T33",
  "Recycling of waste and scrap": "D35T39",
  "Recycling of bottles by direct reuse": "D90T96",
  "Production of electricity by coal": "D05T09",
  "Production of electricity by gas": "D35T39",
  "Production of electricity by nuclear": "D35T39",
  "Production of electricity by hydro": "D35T39",
  "Production of electricity by wind": "D35T39",
  "Production of electricity by petroleum and other oil derivatives": "D19",
  "Production of electricity by biomass and waste": "D35T39",
  "Production of electricity by solar photovoltaic": "D35T39",
  "Production of electricity by solar thermal": "D35T39",
  "Production of electricity by tide, wave, ocean": "D35T39",
  "Production of electricity by Geothermal": "D35T39",
  "Production of electricity nec": "D35T39",
  "Transmission of electricity": "D35T39",
  "Distribution and trade of electricity": "D90T96",
  "Manufacture of gas; distribution of gaseous fuels through mains": "D90T96",
  "Steam and hot water supply": "D35T39",
  "Collection, purification and distribution of water (41)": "D90T96",
  "Construction (45)": "D41T43",
  "Re-processing of secondary construction material into aggregates": "D41T43",
  "Sale, maintenance, repair of motor vehicles, motor vehicles parts, motorcycles, motor cycles parts and accessoiries": "D29T30",
  "Retail sale of automotive fuel": "D90T96",
  "Wholesale trade and commission trade, except of motor vehicles and motorcycles (51)": "D29T30",
  "Retail trade, except of motor vehicles and motorcycles; repair of personal and household goods (52)": "D29T30",
  "Hotels and restaurants (55)": "D90T96",
  "Transport via railways": "D29T30",
  "Other land transport": "D49T53",
  "Transport via pipelines": "D90T96",
  "Sea and coastal water transport": "D49T53",
  "Inland water transport": "D49T53",
  "Air transport (62)": "D49T53",
  "Supporting and auxiliary transport activities; activities of travel agencies (63)": "D90T96",
  "Post and telecommunications (64)": "D61",
  "Financial intermediation, except insurance and pension funding (65)": "D64T66",
  "Insurance and pension funding, except compulsory social security (66)": "D64T66",
  "Activities auxiliary to financial intermediation (67)": "D90T96",
  "Real estate activities (70)": "D68",
  "Renting of machinery and equipment without operator and of personal and household goods (71)": "D90T96",
  "Computer and related activities (72)": "D26T27",
  "Research and development (73)": "D90T96",
  "Other business activities (74)": "D90T96",
  "Public administration and defence; compulsory social security (75)": "D77T82",
  "Education (80)": "D85",
  "Health and social work (85)": "D86T88",
  "Incineration of waste: Food": "D35T39",
  "Incineration of waste: Paper": "D17T18",
  "Incineration of waste: Plastic": "D35T39",
  "Incineration of waste: Metals and Inert materials": "D35T39",
  "Incineration of waste: Textiles": "D13T15",
  "Incineration of waste: Wood": "D16",
  "Incineration of waste: Oil/Hazardous waste": "D35T39",
  "Biogasification of food waste, incl. land application": "D35T39",
  "Biogasification of paper, incl. land application": "D17T18",
  "Biogasification of sewage slugde, incl. land application": "D90T96",
  "Composting of food waste, incl. land application": "D35T39",
  "Composting of paper and wood, incl. land application": "D16",
  "Waste water treatment, food": "D35T39",
  "Waste water treatment, other": "D35T39",
  "Landfill of waste: Food": "D35T39",
  "Landfill of waste: Paper": "D17T18",
  "Landfill of waste: Plastic": "D35T39",
  "Landfill of waste: Inert/metal/hazardous": "D35T39",
  "Landfill of waste: Textiles": "D13T15",
  "Landfill of waste: Wood": "D16",
  "Activities of membership organisation n.e.c. (91)": "D90T96",
  "Recreational, cultural and sporting activities (92)": "D90T96",
  "Other service activities (93)": "D90T96",
  "Private households with employed persons (95)": "D97T98",
  "Extra-territorial organizations and bodies": "D90T96"
}

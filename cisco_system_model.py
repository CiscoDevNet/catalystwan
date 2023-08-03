
from enum import Enum
from pathlib import Path
from typing import ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class Timezone(str, Enum):
    EUROPE_ANDORRA = "Europe/Andorra"
    ASIA_DUBAI = "Asia/Dubai"
    ASIA_KABUL_= "Asia/Kabul"
    AMERICA_ANTIGUA_= "America/Antigua"
    AMERICA_ANGUILLA_= "America/Anguilla"
    EUROPE_TIRANE_= "Europe/Tirane"
    ASIA_YEREVAN_= "Asia/Yerevan"
    AFRICA_LUANDA_= "Africa/Luanda"
    ANTARCTICA_MCMURDO = "Antarctica/McMurdo"
    ANTARCTICA_ROTHERA = "Antarctica/Rothera"
    ANTARCTICA_PALMER = "Antarctica/Palmer"
    ANTARCTICA_MAWSON = "Antarctica/Mawson"
    ANTARCTICA_DAVIS = "Antarctica/Davis"
    ANTARCTICA_CASEY = "Antarctica/Casey"
    ANTARCTICA_VOSTOK = "Antarctica/Vostok"
    ANTARCTICA_DUMONTDURVILLE = "Antarctica/DumontDUrville"
    ANTARCTICA_SYOWA = "Antarctica/Syowa"
    AMERICA_ARGENTINA/BUENOS_AIRES = "America/Argentina/Buenos_Aires"
    AMERICA_ARGENTINA/CORDOBA = "America/Argentina/Cordoba"
    AMERICA_ARGENTINA/SALTA = "America/Argentina/Salta"
    AMERICA_ARGENTINA/JUJUY = "America/Argentina/Jujuy"
    AMERICA_ARGENTINA/TUCUMAN = "America/Argentina/Tucuman"
    AMERICA_ARGENTINA/CATAMARCA = "America/Argentina/Catamarca"
    AMERICA_ARGENTINA/LA_RIOJA = "America/Argentina/La_Rioja"
    AMERICA_ARGENTINA/SAN_JUAN = "America/Argentina/San_Juan"
    AMERICA_ARGENTINA/MENDOZA = "America/Argentina/Mendoza"
    AMERICA_ARGENTINA/SAN_LUIS = "America/Argentina/San_Luis"
    AMERICA_ARGENTINA/RIO_GALLEGOS = "America/Argentina/Rio_Gallegos"
    AMERICA_ARGENTINA/USHUAIA = "America/Argentina/Ushuaia"
    PACIFIC_PAGO_PAGO = "Pacific/Pago_Pago"
    EUROPE_VIENNA = "Europe/Vienna"
    AUSTRALIA_LORD_HOWE = "Australia/Lord_Howe"
    ANTARCTICA_MACQUARIE = "Antarctica/Macquarie"
    AUSTRALIA_HOBART = "Australia/Hobart"
    AUSTRALIA_CURRIE = "Australia/Currie"
    AUSTRALIA_MELBOURNE = "Australia/Melbourne"
    AUSTRALIA_SYDNEY = "Australia/Sydney"
    AUSTRALIA_BROKEN_HILL = "Australia/Broken_Hill"
    AUSTRALIA_BRISBANE = "Australia/Brisbane"
    AUSTRALIA_LINDEMAN = "Australia/Lindeman"
    AUSTRALIA_ADELAIDE = "Australia/Adelaide"
    AUSTRALIA_DARWIN = "Australia/Darwin"
    AUSTRALIA_PERTH = "Australia/Perth"
    AUSTRALIA_EUCLA = "Australia/Eucla"
    AMERICA_ARUBA = "America/Aruba"
    EUROPE_MARIEHAMN = "Europe/Mariehamn"
    ASIA_BAKU = "Asia/Baku"
    EUROPE_SARAJEVO = "Europe/Sarajevo"
    AMERICA_BARBADOS = "America/Barbados"
    ASIA_DHAKA = "Asia/Dhaka"
    EUROPE_BRUSSELS = "Europe/Brussels"
    AFRICA_OUAGADOUGOU = "Africa/Ouagadougou"
    EUROPE_SOFIA = "Europe/Sofia"
    ASIA_BAHRAIN = "Asia/Bahrain"
    AFRICA_BUJUMBURA = "Africa/Bujumbura"
    AFRICA_PORTO_NOVO = "Africa/Porto-Novo"
    AMERICA_ST_BARTHELEMY = "America/St_Barthelemy"
    ATLANTIC_BERMUDA = "Atlantic/Bermuda"
    ASIA_BRUNEI = "Asia/Brunei"
    AMERICA_LA_PAZ = "America/La_Paz"
    AMERICA_KRALENDIJK = "America/Kralendijk"
    AMERICA_NORONHA = "America/Noronha"
    AMERICA_BELEM = "America/Belem"
    AMERICA_FORTALEZA = "America/Fortaleza"
    AMERICA_RECIFE = "America/Recife"
    AMERICA_ARAGUAINA = "America/Araguaina"
    AMERICA_MACEIO = "America/Maceio"
    AMERICA_BAHIA = "America/Bahia"
    AMERICA_SAO_PAULO = "America/Sao_Paulo"
    AMERICA_CAMPO_GRANDE = "America/Campo_Grande"
    AMERICA_CUIABA = "America/Cuiaba"
    AMERICA_SANTAREM = "America/Santarem"
    AMERICA_PORTO_VELHO = "America/Porto_Velho"
    AMERICA_BOA_VISTA = "America/Boa_Vista"
    AMERICA_MANAUS = "America/Manaus"
    AMERICA_EIRUNEPE = "America/Eirunepe"
    AMERICA_RIO_BRANCO = "America/Rio_Branco"
    AMERICA_NASSAU = "America/Nassau"
    ASIA_THIMPHU = "Asia/Thimphu"
    AFRICA_GABORONE = "Africa/Gaborone"
    EUROPE_MINSK = "Europe/Minsk"
    AMERICA_BELIZE = "America/Belize"
    AMERICA_ST_JOHNS = "America/St_Johns"
    AMERICA_HALIFAX = "America/Halifax"
    AMERICA_GLACE_BAY = "America/Glace_Bay"
    AMERICA_MONCTON = "America/Moncton"
    AMERICA_GOOSE_BAY = "America/Goose_Bay"
    AMERICA_BLANC_SABLON = "America/Blanc-Sablon"
    AMERICA_TORONTO = "America/Toronto"
    AMERICA_NIPIGON = "America/Nipigon"
    AMERICA_THUNDER_BAY = "America/Thunder_Bay"
    AMERICA_IQALUIT = "America/Iqaluit"
    AMERICA_PANGNIRTUNG = "America/Pangnirtung"
    AMERICA_RESOLUTE = "America/Resolute"
    AMERICA_ATIKOKAN = "America/Atikokan"
    AMERICA_RANKIN_INLET = "America/Rankin_Inlet"
    AMERICA_WINNIPEG = "America/Winnipeg"
    AMERICA_RAINY_RIVER = "America/Rainy_River"
    AMERICA_REGINA = "America/Regina"
    AMERICA_SWIFT_CURRENT = "America/Swift_Current"
    AMERICA_EDMONTON = "America/Edmonton"
    AMERICA_CAMBRIDGE_BAY = "America/Cambridge_Bay"
    AMERICA_YELLOWKNIFE = "America/Yellowknife"
    AMERICA_INUVIK = "America/Inuvik"
    AMERICA_CRESTON = "America/Creston"
    AMERICA_DAWSON_CREEK = "America/Dawson_Creek"
    AMERICA_VANCOUVER = "America/Vancouver"
    AMERICA_WHITEHORSE = "America/Whitehorse"
    AMERICA_DAWSON = "America/Dawson"
    INDIAN_COCOS = "Indian/Cocos"
    AFRICA_KINSHASA = "Africa/Kinshasa"
    AFRICA_LUBUMBASHI = "Africa/Lubumbashi"
    AFRICA_BANGUI = "Africa/Bangui"
    AFRICA_BRAZZAVILLE = "Africa/Brazzaville"
    EUROPE_ZURICH = "Europe/Zurich"
    AFRICA_ABIDJAN = "Africa/Abidjan"
    PACIFIC_RAROTONGA = "Pacific/Rarotonga"
    AMERICA_SANTIAGO = "America/Santiago"
    PACIFIC_EASTER = "Pacific/Easter"
    AFRICA_DOUALA = "Africa/Douala"
    ASIA_SHANGHAI = "Asia/Shanghai"
    ASIA_HARBIN = "Asia/Harbin"
    ASIA_CHONGQING = "Asia/Chongqing"
    ASIA_URUMQI = "Asia/Urumqi"
    ASIA_KASHGAR = "Asia/Kashgar"
    AMERICA_BOGOTA = "America/Bogota"
    AMERICA_COSTA_RICA = "America/Costa_Rica"
    AMERICA_HAVANA = "America/Havana"
    ATLANTIC_CAPE_VERDE = "Atlantic/Cape_Verde"
    AMERICA_CURACAO = "America/Curacao"
    INDIAN_CHRISTMAS = "Indian/Christmas"
    ASIA_NICOSIA = "Asia/Nicosia"
    EUROPE_PRAGUE = "Europe/Prague"
    EUROPE_BERLIN = "Europe/Berlin"
    EUROPE_BUSINGEN = "Europe/Busingen"
    AFRICA_DJIBOUTI = "Africa/Djibouti"
    EUROPE_COPENHAGEN = "Europe/Copenhagen"
    AMERICA_DOMINICA = "America/Dominica"
    AMERICA_SANTO_DOMINGO = "America/Santo_Domingo"
    AFRICA_ALGIERS = "Africa/Algiers"
    AMERICA_GUAYAQUIL = "America/Guayaquil"
    PACIFIC_GALAPAGOS = "Pacific/Galapagos"
    EUROPE_TALLINN = "Europe/Tallinn"
    AFRICA_CAIRO = "Africa/Cairo"
    AFRICA_EL_AAIUN = "Africa/El_Aaiun"
    AFRICA_ASMARA = "Africa/Asmara"
    EUROPE_MADRID = "Europe/Madrid"
    AFRICA_CEUTA = "Africa/Ceuta"
    ATLANTIC_CANARY = "Atlantic/Canary"
    AFRICA_ADDIS_ABABA = "Africa/Addis_Ababa"
    EUROPE_HELSINKI = "Europe/Helsinki"
    PACIFIC_FIJI = "Pacific/Fiji"
    ATLANTIC_STANLEY = "Atlantic/Stanley"
    PACIFIC_CHUUK = "Pacific/Chuuk"
    PACIFIC_POHNPEI = "Pacific/Pohnpei"
    PACIFIC_KOSRAE = "Pacific/Kosrae"
    ATLANTIC_FAROE = "Atlantic/Faroe"
    EUROPE_PARIS = "Europe/Paris"
    AFRICA_LIBREVILLE = "Africa/Libreville"
    EUROPE_LONDON = "Europe/London"
    AMERICA_GRENADA = "America/Grenada"
    ASIA_TBILISI = "Asia/Tbilisi"
    AMERICA_CAYENNE = "America/Cayenne"
    EUROPE_GUERNSEY = "Europe/Guernsey"
    AFRICA_ACCRA = "Africa/Accra"
    EUROPE_GIBRALTAR = "Europe/Gibraltar"
    AMERICA_GODTHAB = "America/Godthab"
    AMERICA_DANMARKSHAVN = "America/Danmarkshavn"
    AMERICA_SCORESBYSUND = "America/Scoresbysund"
    AMERICA_THULE = "America/Thule"
    AFRICA_BANJUL = "Africa/Banjul"
    AFRICA_CONAKRY = "Africa/Conakry"
    AMERICA_GUADELOUPE = "America/Guadeloupe"
    AFRICA_MALABO = "Africa/Malabo"
    EUROPE_ATHENS = "Europe/Athens"
    ATLANTIC_SOUTH_GEORGIA = "Atlantic/South_Georgia"
    AMERICA_GUATEMALA = "America/Guatemala"
    PACIFIC_GUAM = "Pacific/Guam"
    AFRICA_BISSAU = "Africa/Bissau"
    AMERICA_GUYANA = "America/Guyana"
    ASIA_HONG_KONG = "Asia/Hong_Kong"
    AMERICA_TEGUCIGALPA = "America/Tegucigalpa"
    EUROPE_ZAGREB = "Europe/Zagreb"
    AMERICA_PORT_AU_PRINCE = "America/Port-au-Prince"
    EUROPE_BUDAPEST = "Europe/Budapest"
    ASIA_JAKARTA = "Asia/Jakarta"
    ASIA_PONTIANAK = "Asia/Pontianak"
    ASIA_MAKASSAR = "Asia/Makassar"
    ASIA_JAYAPURA = "Asia/Jayapura"
    EUROPE_DUBLIN = "Europe/Dublin"
    ASIA_JERUSALEM = "Asia/Jerusalem"
    EUROPE_ISLE_OF_MAN = "Europe/Isle_of_Man"
    ASIA_KOLKATA = "Asia/Kolkata"
    INDIAN_CHAGOS = "Indian/Chagos"
    ASIA_BAGHDAD = "Asia/Baghdad"
    ASIA_TEHRAN = "Asia/Tehran"
    ATLANTIC_REYKJAVIK = "Atlantic/Reykjavik"
    EUROPE_ROME = "Europe/Rome"
    EUROPE_JERSEY = "Europe/Jersey"
    AMERICA_JAMAICA = "America/Jamaica"
    ASIA_AMMAN = "Asia/Amman"
    ASIA_TOKYO = "Asia/Tokyo"
    AFRICA_NAIROBI = "Africa/Nairobi"
    ASIA_BISHKEK = "Asia/Bishkek"
    ASIA_PHNOM_PENH = "Asia/Phnom_Penh"
    PACIFIC_TARAWA = "Pacific/Tarawa"
    PACIFIC_ENDERBURY = "Pacific/Enderbury"
    PACIFIC_KIRITIMATI = "Pacific/Kiritimati"
    INDIAN_COMORO = "Indian/Comoro"
    AMERICA_ST_KITTS = "America/St_Kitts"
    ASIA_PYONGYANG = "Asia/Pyongyang"
    ASIA_SEOUL = "Asia/Seoul"
    ASIA_KUWAIT = "Asia/Kuwait"
    AMERICA_CAYMAN = "America/Cayman"
    ASIA_ALMATY = "Asia/Almaty"
    ASIA_QYZYLORDA = "Asia/Qyzylorda"
    ASIA_AQTOBE = "Asia/Aqtobe"
    ASIA_AQTAU = "Asia/Aqtau"
    ASIA_ORAL = "Asia/Oral"
    ASIA_VIENTIANE = "Asia/Vientiane"
    ASIA_BEIRUT = "Asia/Beirut"
    AMERICA_ST_LUCIA = "America/St_Lucia"
    EUROPE_VADUZ = "Europe/Vaduz"
    ASIA_COLOMBO = "Asia/Colombo"
    AFRICA_MONROVIA = "Africa/Monrovia"
    AFRICA_MASERU = "Africa/Maseru"
    EUROPE_VILNIUS = "Europe/Vilnius"
    EUROPE_LUXEMBOURG = "Europe/Luxembourg"
    EUROPE_RIGA = "Europe/Riga"
    AFRICA_TRIPOLI = "Africa/Tripoli"
    AFRICA_CASABLANCA = "Africa/Casablanca"
    EUROPE_MONACO = "Europe/Monaco"
    EUROPE_CHISINAU = "Europe/Chisinau"
    EUROPE_PODGORICA = "Europe/Podgorica"
    AMERICA_MARIGOT = "America/Marigot"
    INDIAN_ANTANANARIVO = "Indian/Antananarivo"
    PACIFIC_MAJURO = "Pacific/Majuro"
    PACIFIC_KWAJALEIN = "Pacific/Kwajalein"
    EUROPE_SKOPJE = "Europe/Skopje"
    AFRICA_BAMAKO = "Africa/Bamako"
    ASIA_RANGOON = "Asia/Rangoon"
    ASIA_ULAANBAATAR = "Asia/Ulaanbaatar"
    ASIA_HOVD = "Asia/Hovd"
    ASIA_CHOIBALSAN = "Asia/Choibalsan"
    ASIA_MACAU = "Asia/Macau"
    PACIFIC_SAIPAN = "Pacific/Saipan"
    AMERICA_MARTINIQUE = "America/Martinique"
    AFRICA_NOUAKCHOTT = "Africa/Nouakchott"
    AMERICA_MONTSERRAT = "America/Montserrat"
    EUROPE_MALTA = "Europe/Malta"
    INDIAN_MAURITIUS = "Indian/Mauritius"
    INDIAN_MALDIVES = "Indian/Maldives"
    AFRICA_BLANTYRE = "Africa/Blantyre"
    AMERICA_MEXICO_CITY = "America/Mexico_City"
    AMERICA_CANCUN = "America/Cancun"
    AMERICA_MERIDA = "America/Merida"
    AMERICA_MONTERREY = "America/Monterrey"
    AMERICA_MATAMOROS = "America/Matamoros"
    AMERICA_MAZATLAN = "America/Mazatlan"
    AMERICA_CHIHUAHUA = "America/Chihuahua"
    AMERICA_OJINAGA = "America/Ojinaga"
    AMERICA_HERMOSILLO = "America/Hermosillo"
    AMERICA_TIJUANA = "America/Tijuana"
    AMERICA_SANTA_ISABEL = "America/Santa_Isabel"
    AMERICA_BAHIA_BANDERAS = "America/Bahia_Banderas"
    ASIA_KUALA_LUMPUR = "Asia/Kuala_Lumpur"
    ASIA_KUCHING = "Asia/Kuching"
    AFRICA_MAPUTO = "Africa/Maputo"
    AFRICA_WINDHOEK = "Africa/Windhoek"
    PACIFIC_NOUMEA = "Pacific/Noumea"
    AFRICA_NIAMEY = "Africa/Niamey"
    PACIFIC_NORFOLK = "Pacific/Norfolk"
    AFRICA_LAGOS = "Africa/Lagos"
    AMERICA_MANAGUA = "America/Managua"
    EUROPE_AMSTERDAM = "Europe/Amsterdam"
    EUROPE_OSLO = "Europe/Oslo"
    ASIA_KATHMANDU = "Asia/Kathmandu"
    PACIFIC_NAURU = "Pacific/Nauru"
    PACIFIC_NIUE = "Pacific/Niue"
    PACIFIC_AUCKLAND = "Pacific/Auckland"
    PACIFIC_CHATHAM = "Pacific/Chatham"
    ASIA_MUSCAT = "Asia/Muscat"
    AMERICA_PANAMA = "America/Panama"
    AMERICA_LIMA = "America/Lima"
    PACIFIC_TAHITI = "Pacific/Tahiti"
    PACIFIC_MARQUESAS = "Pacific/Marquesas"
    PACIFIC_GAMBIER = "Pacific/Gambier"
    PACIFIC_PORT_MORESBY = "Pacific/Port_Moresby"
    ASIA_MANILA = "Asia/Manila"
    ASIA_KARACHI = "Asia/Karachi"
    EUROPE_WARSAW = "Europe/Warsaw"
    AMERICA_MIQUELON = "America/Miquelon"
    PACIFIC_PITCAIRN = "Pacific/Pitcairn"
    AMERICA_PUERTO_RICO = "America/Puerto_Rico"
    ASIA_GAZA = "Asia/Gaza"
    ASIA_HEBRON = "Asia/Hebron"
    EUROPE_LISBON = "Europe/Lisbon"
    ATLANTIC_MADEIRA = "Atlantic/Madeira"
    ATLANTIC_AZORES = "Atlantic/Azores"
    PACIFIC_PALAU = "Pacific/Palau"
    AMERICA_ASUNCION = "America/Asuncion"
    ASIA_QATAR = "Asia/Qatar"
    INDIAN_REUNION = "Indian/Reunion"
    EUROPE_BUCHAREST = "Europe/Bucharest"
    EUROPE_BELGRADE = "Europe/Belgrade"
    EUROPE_KALININGRAD = "Europe/Kaliningrad"
    EUROPE_MOSCOW = "Europe/Moscow"
    EUROPE_VOLGOGRAD = "Europe/Volgograd"
    EUROPE_SAMARA = "Europe/Samara"
    ASIA_YEKATERINBURG = "Asia/Yekaterinburg"
    ASIA_OMSK = "Asia/Omsk"
    ASIA_NOVOSIBIRSK = "Asia/Novosibirsk"
    ASIA_NOVOKUZNETSK = "Asia/Novokuznetsk"
    ASIA_KRASNOYARSK = "Asia/Krasnoyarsk"
    ASIA_IRKUTSK = "Asia/Irkutsk"
    ASIA_YAKUTSK = "Asia/Yakutsk"
    ASIA_KHANDYGA = "Asia/Khandyga"
    ASIA_VLADIVOSTOK = "Asia/Vladivostok"
    ASIA_SAKHALIN = "Asia/Sakhalin"
    ASIA_UST_NERA = "Asia/Ust-Nera"
    ASIA_MAGADAN = "Asia/Magadan"
    ASIA_KAMCHATKA = "Asia/Kamchatka"
    ASIA_ANADYR = "Asia/Anadyr"
    AFRICA_KIGALI = "Africa/Kigali"
    ASIA_RIYADH = "Asia/Riyadh"
    PACIFIC_GUADALCANAL = "Pacific/Guadalcanal"
    INDIAN_MAHE = "Indian/Mahe"
    AFRICA_KHARTOUM = "Africa/Khartoum"
    EUROPE_STOCKHOLM = "Europe/Stockholm"
    ASIA_SINGAPORE = "Asia/Singapore"
    ATLANTIC_ST_HELENA = "Atlantic/St_Helena"
    EUROPE_LJUBLJANA = "Europe/Ljubljana"
    ARCTIC_LONGYEARBYEN = "Arctic/Longyearbyen"
    EUROPE_BRATISLAVA = "Europe/Bratislava"
    AFRICA_FREETOWN = "Africa/Freetown"
    EUROPE_SAN_MARINO = "Europe/San_Marino"
    AFRICA_DAKAR = "Africa/Dakar"
    AFRICA_MOGADISHU = "Africa/Mogadishu"
    AMERICA_PARAMARIBO = "America/Paramaribo"
    AFRICA_JUBA = "Africa/Juba"
    AFRICA_SAO_TOME = "Africa/Sao_Tome"
    AMERICA_EL_SALVADOR = "America/El_Salvador"
    AMERICA_LOWER_PRINCES = "America/Lower_Princes"
    ASIA_DAMASCUS = "Asia/Damascus"
    AFRICA_MBABANE = "Africa/Mbabane"
    AMERICA_GRAND_TURK = "America/Grand_Turk"
    AFRICA_NDJAMENA = "Africa/Ndjamena"
    INDIAN_KERGUELEN = "Indian/Kerguelen"
    AFRICA_LOME = "Africa/Lome"
    ASIA_BANGKOK = "Asia/Bangkok"
    ASIA_DUSHANBE = "Asia/Dushanbe"
    PACIFIC_FAKAOFO = "Pacific/Fakaofo"
    ASIA_DILI = "Asia/Dili"
    ASIA_ASHGABAT = "Asia/Ashgabat"
    AFRICA_TUNIS = "Africa/Tunis"
    PACIFIC_TONGATAPU = "Pacific/Tongatapu"
    EUROPE_ISTANBUL = "Europe/Istanbul"
    AMERICA_PORT_OF_SPAIN = "America/Port_of_Spain"
    PACIFIC_FUNAFUTI = "Pacific/Funafuti"
    ASIA_TAIPEI = "Asia/Taipei"
    AFRICA_DAR_ES_SALAAM = "Africa/Dar_es_Salaam"
    EUROPE_KIEV = "Europe/Kiev"
    EUROPE_UZHGOROD = "Europe/Uzhgorod"
    EUROPE_ZAPOROZHYE = "Europe/Zaporozhye"
    EUROPE_SIMFEROPOL = "Europe/Simferopol"
    AFRICA_KAMPALA = "Africa/Kampala"
    PACIFIC_JOHNSTON = "Pacific/Johnston"
    PACIFIC_MIDWAY = "Pacific/Midway"
    PACIFIC_WAKE = "Pacific/Wake"
    AMERICA_NEW_YORK = "America/New_York"
    AMERICA_DETROIT = "America/Detroit"
    AMERICA_KENTUCKY/LOUISVILLE = "America/Kentucky/Louisville"
    AMERICA_KENTUCKY/MONTICELLO = "America/Kentucky/Monticello"
    AMERICA_INDIANA/INDIANAPOLIS = "America/Indiana/Indianapolis"
    AMERICA_INDIANA/VINCENNES = "America/Indiana/Vincennes"
    AMERICA_INDIANA/WINAMAC = "America/Indiana/Winamac"
    AMERICA_INDIANA/MARENGO = "America/Indiana/Marengo"
    AMERICA_INDIANA/PETERSBURG = "America/Indiana/Petersburg"
    AMERICA_INDIANA/VEVAY = "America/Indiana/Vevay"
    AMERICA_CHICAGO = "America/Chicago"
    AMERICA_INDIANA/TELL_CITY = "America/Indiana/Tell_City"
    AMERICA_INDIANA/KNOX = "America/Indiana/Knox"
    AMERICA_MENOMINEE = "America/Menominee"
    AMERICA_NORTH_DAKOTA/CENTER = "America/North_Dakota/Center"
    AMERICA_NORTH_DAKOTA/NEW_SALEM = "America/North_Dakota/New_Salem"
    AMERICA_NORTH_DAKOTA/BEULAH = "America/North_Dakota/Beulah"
    AMERICA_DENVER = "America/Denver"
    AMERICA_BOISE = "America/Boise"
    AMERICA_PHOENIX = "America/Phoenix"
    AMERICA_LOS_ANGELES = "America/Los_Angeles"
    AMERICA_ANCHORAGE = "America/Anchorage"
    AMERICA_JUNEAU = "America/Juneau"
    AMERICA_SITKA = "America/Sitka"
    AMERICA_YAKUTAT = "America/Yakutat"
    AMERICA_NOME = "America/Nome"
    AMERICA_ADAK = "America/Adak"
    AMERICA_METLAKATLA = "America/Metlakatla"
    PACIFIC_HONOLULU = "Pacific/Honolulu"
    AMERICA_MONTEVIDEO = "America/Montevideo"
    ASIA_SAMARKAND = "Asia/Samarkand"
    ASIA_TASHKENT = "Asia/Tashkent"
    EUROPE_VATICAN = "Europe/Vatican"
    AMERICA_ST_VINCENT = "America/St_Vincent"
    AMERICA_CARACAS = "America/Caracas"
    AMERICA_TORTOLA = "America/Tortola"
    AMERICA_ST_THOMAS = "America/St_Thomas"
    ASIA_HO_CHI_MINH = "Asia/Ho_Chi_Minh"
    PACIFIC_EFATE = "Pacific/Efate"
    PACIFIC_WALLIS = "Pacific/Wallis"
    PACIFIC_APIA = "Pacific/Apia"
    ASIA_ADEN = "Asia/Aden"
    INDIAN_MAYOTTE = "Indian/Mayotte"
    AFRICA_JOHANNESBURG = "Africa/Johannesburg"
    AFRICA_LUSAKA = "Africa/Lusaka"
    AFRICA_HARARE = "Africa/Harare"
    UTC_= "UTC"

class MobileNumber(BaseModel):
    number: str
class SiteType(str, Enum):
    TYPE_1 = "type-1"
    TYPE_2 = "type-2"
    TYPE_3 = "type-3"
    CLOUD = "cloud"
    BRANCH = "branch"
    BR = "br"
    SPOKE = "spoke"
class ConsoleBaudRate(str, Enum):
    ONE_THOUSAND_TWO_HUNDRED = "1200"
    TWO_THOUSAND_FOUR_HUNDRED = "2400"
    FOUR_THOUSAND_EIGHT_HUNDRED = "4800"
    9600 = "9600"
    19200 = "19200"
    38400 = "38400"
    57600 = "57600"
    115200 = "115200"
class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"
class Boolean(str, Enum):
    OR = "or"
    AND = "and"
class Type(str, Enum):
    INTERFACE = "interface"
    STATIC_ROUTE = "static-route"
class Tracker(BaseModel):
    name: str
    endpoint_ip: str = Field(alias="endpoint-ip")
    endpoint_ip: str = Field(alias="endpoint-ip")
    protocol: Protocol
    port: int
    endpoint_dns_name: str = Field(alias="endpoint-dns-name")
    endpoint_api_url: str = Field(alias="endpoint-api-url")
    elements: List[str]
    boolean: Optional[Boolean] = Boolean.OR
    threshold: Optional[int] = 300
    interval: Optional[int] = 60
    multiplier: Optional[int] = 3
    type: Optional[Type] = Type.INTERFACE
    class Config:
	    allow_population_by_field_name = True
class Object(BaseModel):
    number: int
class Boolean(str, Enum):
    AND = "and"
    OR = "or"
class ObjectTrack(BaseModel):
    object_number: int = Field(alias="object-number")
    interface: str
    sig: str
    ip: str
    mask: Optional[str] = "0.0.0.0"
    vpn: int
    object: List[Object]
    boolean: Boolean
    class Config:
	    allow_population_by_field_name = True
class Role(str, Enum):
    EDGE_ROUTER = "edge-router"
    BORDER_ROUTER = "border-router"
class AffinityPerVrf(BaseModel):
    affinity_group_number: Optional[int]  = Field(alias='affinity-group-number')
    vrf_range: Optional[str]  = Field(alias='vrf-range')
    class Config:
	    allow_population_by_field_name = True
class EnableMrfMigration(str, Enum):
    ENABLE = "enabled"
    ENABLE_FROM_BGP_CORE = "enabled-from-bgp-core"
class Vrf(BaseModel):
    vrf_id: int = Field(alias="vrf-id")
    gateway_preference: Optional[List[int]]  = Field(alias='gateway-preference')
    class Config:
	    allow_population_by_field_name = True
class Epfr(str, Enum):
    DISABLED = "disabled"
    AGGRESSIVE = "aggressive"
    MODERATE = "moderate"
    CONSERVATIVE = "conservative"


class CiscoSystemModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
    timezone: Optional[Timezone] = Timezone.UTC
    host_name: str = Field(alias="host-name")
    description: Optional[str] 
    location: Optional[str] 
    latitude: Optional[float] 
    longitude: Optional[float] 
    enable: Optional[bool] 
    range: Optional[int] = 100
    enable: Optional[bool] 
    mobile_number: Optional[List[MobileNumber]] = Field(alias='mobile-number')
    device_groups: Optional[List[str]]  = Field(alias='device-groups')
    controller_group_list: Optional[List[int]]  = Field(alias='controller-group-list')
    system_ip: str = Field(alias="system-ip")
    overlay_id: Optional[int]  = Field(1, alias='overlay-id')
    site_id: int = Field(alias="site-id")
    site_type: Optional[List[SiteType]]  = Field(alias='site-type')
    port_offset: Optional[int]  = Field(alias='port-offset')
    port_hop: Optional[bool]  = Field(True, alias='port-hop')
    control_session_pps: Optional[int]  = Field(300, alias='control-session-pps')
    track_transport: Optional[bool]  = Field(True, alias='track-transport')
    track_interface_tag: Optional[int]  = Field(alias='track-interface-tag')
    console_baud_rate: ConsoleBaudRate = Field(alias="console-baud-rate")
    max_omp_sessions: Optional[int]  = Field(alias='max-omp-sessions')
    multi_tenant: bool = Field(alias="multi-tenant")
    track_default_gateway: Optional[bool]  = Field(True, alias='track-default-gateway')
    admin_tech_on_failure: Optional[bool]  = Field(True, alias='admin-tech-on-failure')
    idle_timeout: Optional[int]  = Field(alias='idle-timeout')
    tracker: Optional[List[Tracker]]
    object_track: Optional[List[ObjectTrack]] = Field(alias='object-track')
    enable: Optional[bool] 
    idle_timeout: Optional[int]  = Field(10, alias='idle-timeout')
    region_id: Optional[int]  = Field(alias='region-id')
    secondary_region: Optional[int]  = Field(alias='secondary-region')
    role: Optional[Role] 
    affinity_group_number: Optional[int]  = Field(alias='affinity-group-number')
    preference: Optional[List[int]] 
    preference_auto: Optional[bool]  = Field(alias='preference-auto')
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = Field(alias='affinity-per-vrf')
    transport_gateway: Optional[bool]  = Field(alias='transport-gateway')
    enable_mrf_migration: Optional[EnableMrfMigration]  = Field(alias='enable-mrf-migration')
    migration_bgp_community: Optional[int]  = Field(alias='migration-bgp-community')
    enable_management_region: Optional[bool]  = Field(alias='enable-management-region')
    vrf: Optional[List[Vrf]]
    management_gateway: Optional[bool]  = Field(alias='management-gateway')
    epfr: Optional[Epfr] = Epfr.DISABLED

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_system"

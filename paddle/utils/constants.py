from typing import Literal

TAX_CATEGORY = Literal[
    "digital-goods",
    "ebooks",
    "implementation-services",
    "professional-services",
    "saas",
    "software-programming-services",
    "standard",
    "training-services",
    "website-hosting",
]

# Supported three-letter ISO 4217 currency code.
CURRENCY_CODE = Literal[
    "USD",  # United States Dollar
    "EUR",  # Euro
    "GBP",  # Pound Sterling
    "JPY",  # Japanese Yen
    "AUD",  # Australian Dollar
    "CAD",  # Canadian Dollar
    "CHF",  # Swiss Franc
    "HKD",  # Hong Kong Dollar
    "SGD",  # Singapore Dollar
    "SEK",  # Swedish Krona
    "ARS",  # Argentine Peso
    "BRL",  # Brazilian Real
    "CNY",  # Chinese Yuan
    "COP",  # Colombian Peso
    "CZK",  # Czech Koruna
    "DKK",  # Danish Krone
    "HUF",  # Hungarian Forint
    "ILS",  # Israeli Shekel
    "INR",  # Indian Rupee
    "KRW",  # South Korean Won
    "MXN",  # Mexican Peso
    "NOK",  # Norwegian Krone
    "NZD",  # New Zealand Dollar
    "PLN",  # Polish Zloty
    "RUB",  # Russian Ruble
    "THB",  # Thai Baht
    "TRY",  # Turkish Lira
    "TWD",  # New Taiwan Dollar
    "UAH",  # Ukrainian Hryvnia
    "VND",  # Vietnamese Dong
    "ZAR",  # South African Rand
]

# Supported two-letter ISO 3166-1 alpha-2 country codes
COUNTRY_CODE = Literal[
    "AD",  # Andorra
    "AE",  # United Arab Emirates
    "AG",  # Antigua and Barbuda
    "AI",  # Anguilla
    "AL",  # Albania
    "AM",  # Armenia
    "AO",  # Angola
    "AR",  # Argentina
    "AS",  # American Samoa
    "AT",  # Austria
    "AU",  # Australia
    "AW",  # Aruba
    "AX",  # Åland Islands
    "AZ",  # Azerbaijan
    "BA",  # Bosnia and Herzegovina
    "BB",  # Barbados
    "BD",  # Bangladesh
    "BE",  # Belgium
    "BF",  # Burkina Faso
    "BG",  # Bulgaria
    "BH",  # Bahrain
    "BI",  # Burundi
    "BJ",  # Benin
    "BL",  # Saint Barthélemy
    "BM",  # Bermuda
    "BN",  # Brunei
    "BO",  # Bolivia
    "BQ",  # Caribbean Netherlands
    "BR",  # Brazil
    "BS",  # Bahamas
    "BT",  # Bhutan
    "BV",  # Bouvet Island
    "BW",  # Botswana
    "BZ",  # Belize
    "CA",  # Canada
    "CC",  # Cocos Islands
    "CG",  # Republic of Congo
    "CH",  # Switzerland
    "CI",  # Côte d'Ivoire
    "CK",  # Cook Islands
    "CL",  # Chile
    "CM",  # Cameroon
    "CN",  # China
    "CO",  # Colombia
    "CR",  # Costa Rica
    "CV",  # Cape Verde
    "CW",  # Curaçao
    "CX",  # Christmas Island
    "CY",  # Cyprus
    "CZ",  # Czechia
    "DE",  # Germany
    "DJ",  # Djibouti
    "DK",  # Denmark
    "DM",  # Dominica
    "DO",  # Dominican Republic
    "DZ",  # Algeria
    "EC",  # Ecuador
    "EE",  # Estonia
    "EG",  # Egypt
    "EH",  # Western Sahara
    "ER",  # Eritrea
    "ES",  # Spain
    "ET",  # Ethiopia
    "FI",  # Finland
    "FJ",  # Fiji
    "FK",  # Falkland Islands
    "FM",  # Micronesia
    "FO",  # Faroe Islands
    "FR",  # France
    "GA",  # Gabon
    "GB",  # United Kingdom
    "GD",  # Grenada
    "GE",  # Georgia
    "GF",  # French Guiana
    "GG",  # Guernsey
    "GH",  # Ghana
    "GI",  # Gibraltar
    "GL",  # Greenland
    "GM",  # Gambia
    "GN",  # Guinea
    "GP",  # Guadeloupe
    "GQ",  # Equatorial Guinea
    "GR",  # Greece
    "GS",  # South Georgia
    "GT",  # Guatemala
    "GU",  # Guam
    "GW",  # Guinea-Bissau
    "GY",  # Guyana
    "HK",  # Hong Kong
    "HM",  # Heard Island
    "HN",  # Honduras
    "HR",  # Croatia
    "HU",  # Hungary
    "ID",  # Indonesia
    "IE",  # Ireland
    "IL",  # Israel
    "IM",  # Isle of Man
    "IN",  # India
    "IO",  # British Indian Ocean Territory
    "IQ",  # Iraq
    "IS",  # Iceland
    "IT",  # Italy
    "JE",  # Jersey
    "JM",  # Jamaica
    "JO",  # Jordan
    "JP",  # Japan
    "KE",  # Kenya
    "KG",  # Kyrgyzstan
    "KH",  # Cambodia
    "KI",  # Kiribati
    "KM",  # Comoros
    "KN",  # Saint Kitts and Nevis
    "KR",  # South Korea
    "KW",  # Kuwait
    "KY",  # Cayman Islands
    "KZ",  # Kazakhstan
    "LA",  # Laos
    "LB",  # Lebanon
    "LC",  # Saint Lucia
    "LI",  # Liechtenstein
    "LK",  # Sri Lanka
    "LR",  # Liberia
    "LS",  # Lesotho
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "LV",  # Latvia
    "MA",  # Morocco
    "MC",  # Monaco
    "MD",  # Moldova
    "ME",  # Montenegro
    "MF",  # Saint Martin
    "MG",  # Madagascar
    "MH",  # Marshall Islands
    "MK",  # Macedonia
    "ML",  # Mali
    "MM",  # Myanmar
    "MN",  # Mongolia
    "MO",  # Macao
    "MP",  # Northern Mariana Islands
    "MQ",  # Martinique
    "MR",  # Mauritania
    "MS",  # Montserrat
    "MT",  # Malta
    "MU",  # Mauritius
    "MV",  # Maldives
    "MW",  # Malawi
    "MX",  # Mexico
    "MY",  # Malaysia
    "MZ",  # Mozambique
    "NA",  # Namibia
    "NC",  # New Caledonia
    "NE",  # Niger
    "NF",  # Norfolk Island
    "NG",  # Nigeria
    "NI",  # Nicaragua
    "NL",  # Netherlands
    "NO",  # Norway
    "NP",  # Nepal
    "NR",  # Nauru
    "NU",  # Niue
    "NZ",  # New Zealand
    "OM",  # Oman
    "PA",  # Panama
    "PE",  # Peru
    "PF",  # French Polynesia
    "PG",  # Papua New Guinea
    "PH",  # Philippines
    "PK",  # Pakistan
    "PL",  # Poland
    "PM",  # Saint Pierre and Miquelon
    "PN",  # Pitcairn
    "PR",  # Puerto Rico
    "PS",  # Palestinian territories
    "PT",  # Portugal
    "PW",  # Palau
    "PY",  # Paraguay
    "QA",  # Qatar
    "RE",  # Reunion
    "RO",  # Romania
    "RS",  # Serbia
    "RU",  # Russia
    "RW",  # Rwanda
    "SA",  # Saudi Arabia
    "SB",  # Solomon Islands
    "SC",  # Seychelles
    "SD",  # Sudan
    "SE",  # Sweden
    "SG",  # Singapore
    "SH",  # Saint Helena
    "SI",  # Slovenia
    "SJ",  # Svalbard and Jan Mayen
    "SK",  # Slovakia
    "SL",  # Sierra Leone
    "SM",  # San Marino
    "SN",  # Senegal
    "SO",  # Somalia
    "SR",  # Suriname
    "SS",  # South Sudan
    "ST",  # São Tomé and Príncipe
    "SV",  # El Salvador
    "SX",  # Sint Maarten
    "SY",  # Syria
    "SZ",  # Eswatini
    "TC",  # Turks and Caicos Islands
    "TD",  # Chad
    "TF",  # French Southern Territories
    "TG",  # Togo
    "TH",  # Thailand
    "TJ",  # Tajikistan
    "TK",  # Tokelau
    "TL",  # Timor-Leste
    "TM",  # Turkmenistan
    "TN",  # Tunisia
    "TO",  # Tonga
    "TR",  # Turkey
    "TT",  # Trinidad and Tobago
    "TV",  # Tuvalu
    "TW",  # Taiwan
    "TZ",  # Tanzania
    "UA",  # Ukraine
    "UG",  # Uganda
    "UM",  # United States Minor Outlying Islands
    "US",  # United States
    "UY",  # Uruguay
    "UZ",  # Uzbekistan
    "VA",  # Vatican City
    "VC",  # Saint Vincent and the Grenadines
    "VE",  # Venezuela
    "VG",  # British Virgin Islands
    "VI",  # U.S. Virgin Islands
    "VN",  # Vietnam
    "VU",  # Vanuatu
    "WF",  # Wallis and Futuna
    "WS",  # Samoa
    "XK",  # Kosovo
    "YE",  # Yemen
    "YT",  # Mayotte
    "ZA",  # South Africa
    "ZM",  # Zambia
    "ZW",  # Zimbabwe
]

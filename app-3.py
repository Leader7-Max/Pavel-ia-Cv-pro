"""
PAVEL TV — application Streamlit de télévision en direct.

Fonctionnalités :
- Interface mobile/desktop moderne
- Recherche
- Catégories
- Pays
- Favoris
- Playlists M3U publiques
- Lecteur HLS (.m3u8)
- Chaînes camerounaises
- Liens officiels lorsque le flux direct n'est pas directement intégrable

Important :
Les URL de flux doivent être publiques et/ou utilisées avec l'autorisation
du détenteur des droits. L'application ne contourne aucun accès payant,
géoblocage ou protection technique.
"""

import html
import json
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Pavel TV",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_NAME = "PAVEL TV"
BASE = "https://iptv-org.github.io/iptv"
PAGE_SIZE = 48
HOME_PER_BLOCK = 8
REQUEST_TIMEOUT = 30

# Playlists M3U que TU possèdes ou que TU es autorisé à utiliser.
# Exemple :
# EXTRA_M3U = ["https://example.com/ma-playlist.m3u"]
EXTRA_M3U = []


# ============================================================
# CHAÎNES / LIENS OFFICIELS
# ============================================================

OFFICIAL_CAMEROON = [
    {
        "name": "CRTV",
        "country": "cm",
        "logo": "",
        "url": "",
        "official": "https://crtv.cm/live/crtv",
        "group": "Cameroun",
        "description": "Direct officiel CRTV",
    },
    {
        "name": "CRTV NEWS",
        "country": "cm",
        "logo": "",
        "url": "",
        "official": "https://crtv.cm/live/crtv-news",
        "group": "Cameroun",
        "description": "Direct officiel CRTV News",
    },
    {
        "name": "CRTV SPORT",
        "country": "cm",
        "logo": "",
        "url": "",
        "official": "https://sports.crtv.cm/live/",
        "group": "Cameroun",
        "description": "Direct officiel CRTV Sport",
    },
    {
        "name": "Canal 2 International",
        "country": "cm",
        "logo": "",
        "url": "",
        "official": "https://www.canal2international.net/",
        "group": "Cameroun",
        "description": "Site officiel / Canal 2 Play",
    },
]


POPULAR = [
    "CRTV",
    "CRTV NEWS",
    "CRTV SPORT",
    "Canal 2 International",
    "France 2",
    "France 3",
    "TF1",
    "M6",
    "Arte",
    "France 24",
    "Euronews",
    "TV5Monde",
    "BBC News",
    "DW",
    "Al Jazeera",
    "Africa 24",
]


LANGS = {
    "Français": "fra",
    "English": "eng",
    "Español": "spa",
    "العربية": "ara",
    "Português": "por",
    "Deutsch": "deu",
    "Italiano": "ita",
    "Türkçe": "tur",
}


COUNTRIES = {
    "fr": "France",
    "cm": "Cameroun",
    "ci": "Côte d'Ivoire",
    "sn": "Sénégal",
    "ma": "Maroc",
    "dz": "Algérie",
    "tn": "Tunisie",
    "be": "Belgique",
    "ch": "Suisse",
    "ca": "Canada",
    "gb": "Royaume-Uni",
    "us": "États-Unis",
    "es": "Espagne",
    "de": "Allemagne",
    "it": "Italie",
    "pt": "Portugal",
    "tr": "Turquie",
    "br": "Brésil",
    "mx": "Mexique",
    "ar": "Argentine",
    "ru": "Russie",
    "in": "Inde",
    "ae": "Émirats arabes unis",
    "qa": "Qatar",
    "eg": "Égypte",
    "nl": "Pays-Bas",
    "pl": "Pologne",
}


COUNTRY_PRIORITY = {
    code: i
    for i, code in enumerate(
        ["fr", "cm", "ci", "sn", "ma", "be", "ch", "ca"]
    )
}


BLOCKS = [
    ("pop", "🔥", "À la une", "Accueil"),
    ("cm", "🇨🇲", "Chaînes camerounaises", "Afrique"),
    ("fr", "🇫🇷", "Chaînes françaises", "Francophone"),
    ("frall", "🌍", "Toutes les chaînes francophones", "Francophone"),
    ("sport", "⚽", "Sports", "Sports"),
    ("news", "📰", "Actualités", "Thématiques"),
    ("ent", "🎭", "Divertissement", "Thématiques"),
    ("doc", "📚", "Documentaires", "Thématiques"),
    ("film", "🎬", "Films et séries", "Thématiques"),
]


LABEL = {b[0]: f"{b[1]} {b[2]}" for b in BLOCKS}
BLOCK_BY_LABEL = {LABEL[b[0]]: b[0] for b in BLOCKS}

HOME_BLOCKS = [
    "pop",
    "cm",
    "fr",
    "sport",
    "news",
    "frall",
]

COUNTRY_BLOCKS = [
    "fr",
    "cm",
    "ci",
    "sn",
    "ma",
]

CATEGORY_FILES = {
    "sport": "categories/sports.m3u",
    "news": "categories/news.m3u",
    "ent": "categories/entertainment.m3u",
    "doc": "categories/documentary.m3u",
    "movies": "categories/movies.m3u",
    "series": "categories/series.m3u",
}


# ============================================================
# REGEX / OUTILS
# ============================================================

ATTR = re.compile(r'([\w-]+)="([^"]*)"')
COUNTRY_IN_ID = re.compile(r"\.([a-z]{2})(?:@|$)", re.I)
CANAL = re.compile(
    r"canal\s*(\+|plus)|\b(cstar|c8|cnews)\b|"
    r"(cin[eé]ma|plan[eè]te)\s*\+",
    re.I,
)
BEIN = re.compile(r"bein\s*sport", re.I)
CM = re.compile(
    r"crtv|canal\s*2|equinoxe|vision\s*4|cameroun|cameroon|"
    r"mboa|afrique\s*media",
    re.I,
)
FILMS = re.compile(
    r"cin[eé]ma|cin[eé]\s*\+|\baction\b|ocs|paramount|"
    r"\btcm\b|polar|film|s[eé]rie",
    re.I,
)


def norm(value):
    value = value or ""
    value = re.sub(r"[\(\[].*?[\)\]]", "", value)
    value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode()
        .lower()
    )
    value = re.sub(r"[^a-z0-9]", "", value)
    return re.sub(r"(fhd|uhd|hd)$", "", value)


RANK = {norm(name): i for i, name in enumerate(POPULAR)}


def flag(code):
    code = {"uk": "gb"}.get(code or "", code or "")
    if len(code) == 2 and code.isalpha():
        return "".join(
            chr(0x1F1E6 + ord(char) - 97)
            for char in code.lower()
        )
    return "🌐"


# ============================================================
# M3U
# ============================================================

def parse_m3u(text, default_country=""):
    channels = []
    seen = set()
    attrs = None
    name = None

    for raw in (text or "").splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith("#EXTINF"):
            attrs = {
                key.lower(): value
                for key, value in ATTR.findall(line)
            }

            comma = line.rfind(",")
            name = (
                line[comma + 1:].strip()
                if comma >= 0
                else ""
            )

            name = (
                name
                or attrs.get("tvg-name")
                or "Chaîne"
            )

        elif line.startswith("#"):
            continue

        elif attrs is not None and line.startswith("http"):
            if line not in seen:
                seen.add(line)

                match = COUNTRY_IN_ID.search(
                    attrs.get("tvg-id", "").lower()
                )

                channels.append(
                    {
                        "name": name,
                        "url": line,
                        "logo": attrs.get("tvg-logo", ""),
                        "country": (
                            match.group(1)
                            if match
                            else default_country
                        ),
                        "group": attrs.get("group-title", ""),
                        "key": norm(name),
                        "official": "",
                        "description": "",
                    }
                )

            attrs = None
            name = None

    return channels


# ============================================================
# RÉSEAU / CACHE
# ============================================================

@st.cache_resource
def raw_cache():
    return {}


RAW = raw_cache()


def fetch(url, default_country=""):
    cached = RAW.get(url)

    if cached and time.time() - cached[0] < 3600:
        return cached[1]

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT,
        headers={
            "User-Agent": "PavelTV/3.0",
            "Accept": "*/*",
        },
    )
    response.raise_for_status()

    data = parse_m3u(
        response.text,
        default_country,
    )

    RAW[url] = (time.time(), data)

    return data


def fetch_all(sources):
    def one(source):
        url, country = source

        try:
            return url, fetch(url, country)
        except Exception:
            return url, None

    with ThreadPoolExecutor(max_workers=8) as executor:
        return dict(executor.map(one, sources))


def dedupe(lists):
    seen = set()
    output = []

    for channel_list in lists:
        if not channel_list:
            continue

        for channel in channel_list:
            url = channel.get("url", "")

            if url and url not in seen:
                seen.add(url)
                output.append(channel)

    return output


def sort_channels(channels):
    return sorted(
        channels,
        key=lambda channel: (
            RANK.get(channel.get("key", ""), 999),
            COUNTRY_PRIORITY.get(
                channel.get("country", ""),
                99,
            ),
            0 if channel.get("logo") else 1,
            channel.get("name", "").lower(),
        ),
    )


# ============================================================
# TEST DES FLUX
# ============================================================

@st.cache_resource
def probe_cache():
    return {}


PROBES = probe_cache()


def probe(url):
    if url in PROBES:
        return PROBES[url]

    try:
        response = requests.get(
            url,
            timeout=(4, 6),
            stream=True,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
        )

        status = response.status_code
        content_type = response.headers.get(
            "content-type",
            "",
        ).lower()

        response.close()

        if status != 200:
            result = (
                False,
                f"HTTP {status}",
            )
        elif "text/html" in content_type:
            result = (
                False,
                "Le lien renvoie une page web.",
            )
        else:
            result = (True, "OK")

    except Exception:
        result = (
            False,
            "Serveur injoignable ou trop lent.",
        )

    PROBES[url] = result
    return result


def probe_many(urls):
    todo = [
        url
        for url in dict.fromkeys(urls)
        if url and url not in PROBES
    ]

    if todo:
        with ThreadPoolExecutor(max_workers=24) as executor:
            list(executor.map(probe, todo))

    return {
        url: PROBES[url][0]
        for url in urls
        if url in PROBES
    }


def playable_channels(channels, needed):
    output = []
    index = 0

    while len(output) < needed and index < len(channels):
        batch = channels[index:index + PAGE_SIZE]
        index += PAGE_SIZE

        good = probe_many(
            [channel["url"] for channel in batch]
        )

        output.extend(
            channel
            for channel in batch
            if good.get(channel["url"])
        )

    return output[:needed], (
        len(output) > needed
        or index < len(channels)
    )


# ============================================================
# CSS
# ============================================================

LOGO_SVG = """
<svg width="56" height="56" viewBox="0 0 64 64"
xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="pg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#7C3AED"/>
<stop offset=".55" stop-color="#EC4899"/>
<stop offset="1" stop-color="#F59E0B"/>
</linearGradient>
</defs>
<rect x="2" y="2" width="60" height="60" rx="17"
fill="url(#pg)"/>
<path d="M25 17 L25 47 L48 32 Z" fill="#fff"/>
</svg>
"""


CSS = """
<style>
.stApp {
    background:
        radial-gradient(
            1100px 520px at 8% -8%,
            rgba(124,58,237,.38),
            transparent 60%
        ),
        radial-gradient(
            900px 480px at 100% 0%,
            rgba(236,72,153,.28),
            transparent 55%
        ),
        #080812;
}

#MainMenu,
footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1350px;
}

.hero {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 18px 22px;
    border-radius: 24px;
    margin-bottom: 14px;
    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,.40),
            rgba(236,72,153,.24),
            rgba(245,158,11,.18)
        );
    border: 1px solid rgba(255,255,255,.13);
    box-shadow: 0 12px 45px rgba(124,58,237,.20);
}

.brand-name {
    font-size: 34px;
    font-weight: 900;
    letter-spacing: 1px;
    line-height: 1;
    color: #fff;
}

.brand-name span {
    background:
        linear-gradient(
            135deg,
            #EC4899,
            #F59E0B
        );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-left: 6px;
}

.tagline {
    color: rgba(255,255,255,.72);
    font-size: 14px;
    margin-top: 7px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 26px 0 12px;
    font-size: 22px;
    font-weight: 900;
    color: #fff;
}

.section-title:before {
    content: "";
    width: 6px;
    height: 27px;
    border-radius: 8px;
    background:
        linear-gradient(
            180deg,
            #8B5CF6,
            #EC4899,
            #F59E0B
        );
}

.section-title small {
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 999px;
    background: rgba(255,255,255,.10);
    color: rgba(255,255,255,.75);
}

.group-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .5px;
    color: #EC4899;
    margin: 12px 0 3px;
}

.channel-card {
    background:
        linear-gradient(
            160deg,
            rgba(255,255,255,.085),
            rgba(255,255,255,.025)
        );
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 20px;
    padding: 12px;
    min-height: 180px;
    transition: all .18s ease;
}

.channel-card:hover {
    transform: translateY(-3px);
    border-color: rgba(236,72,153,.65);
    box-shadow: 0 12px 30px rgba(236,72,153,.18);
}

.channel-logo {
    height: 86px;
    border-radius: 14px;
    background: rgba(255,255,255,.96);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
    overflow: hidden;
}

.channel-logo img {
    max-height: 64px;
    max-width: 86%;
    object-fit: contain;
}

.placeholder {
    font-size: 38px;
}

.channel-name {
    font-size: 13px;
    font-weight: 800;
    color: #fff;
    text-align: center;
    min-height: 38px;
    line-height: 1.3;
    overflow: hidden;
}

.country {
    font-size: 12px;
    color: rgba(255,255,255,.65);
    text-align: center;
    margin-top: 3px;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: 750;
    border: 1px solid rgba(255,255,255,.13);
}

button[data-testid="stBaseButton-primary"],
button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #7C3AED,
            #EC4899
        );
    border: 0;
    color: #fff;
}

.stTextInput input {
    border-radius: 999px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.14);
    padding: 12px 18px;
}

[data-testid="stSidebar"] {
    background: #0D0D1E;
    border-right: 1px solid rgba(255,255,255,.07);
}

[data-testid="stPopover"] button,
[data-testid="stPopoverButton"] {
    border-radius: 999px !important;
    padding: .65rem 1.4rem !important;
    font-weight: 800 !important;
    background:
        linear-gradient(
            135deg,
            #7C3AED,
            #EC4899
        ) !important;
    color: #fff !important;
    border: 0 !important;
}

@media (max-width: 900px) {
    .brand-name {
        font-size: 28px;
    }

    .hero {
        padding: 14px 16px;
    }
}

@media (max-width: 640px) {
    .brand-name {
        font-size: 24px;
    }

    .channel-card {
        min-height: 165px;
        padding: 9px;
    }
}
</style>
"""


HERO = f"""
<div class="hero">
    {LOGO_SVG}
    <div>
        <div class="brand-name">
            PAVEL<span>TV</span>
        </div>
        <div class="tagline">
            La télévision du monde, partout avec vous
        </div>
    </div>
</div>
"""


# ============================================================
# LECTEUR HLS
# ============================================================

PLAYER_HTML = """
<video id="v" controls autoplay playsinline
style="width:100%;height:auto;max-height:65vh;
background:#000;border-radius:16px"></video>

<div id="err"
style="color:#ff9a9a;font-family:sans-serif;
font-size:14px;margin-top:8px"></div>

<script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.15"></script>

<script>
const url = __URL__;
const raw = __RAW__;

const video = document.getElementById("v");
const errorBox = document.getElementById("err");

function fail(message) {
    errorBox.innerHTML =
        "⚠️ " + message +
        "<br><a style='color:#8ab4ff'
        target='_blank'
        href='" + raw + "'>
        Ouvrir le flux</a>";
}

if (location.protocol === "https:" &&
    raw.startsWith("http:")) {

    fail("Flux HTTP bloqué sur une page HTTPS.");

} else if (window.Hls && Hls.isSupported()) {

    const hls = new Hls({
        manifestLoadingMaxRetry: 2,
        levelLoadingMaxRetry: 2,
        fragLoadingMaxRetry: 3
    });

    hls.loadSource(url);
    hls.attachMedia(video);

    let recovered = false;
    let retried = false;

    hls.on(Hls.Events.ERROR, function(event, data) {

        if (!data.fatal) {
            return;
        }

        if (
            data.type === Hls.ErrorTypes.MEDIA_ERROR
            && !recovered
        ) {
            recovered = true;
            hls.recoverMediaError();
            return;
        }

        if (
            data.type === Hls.ErrorTypes.NETWORK_ERROR
            && !retried
        ) {
            retried = true;
            hls.startLoad();
            return;
        }

        const code = data.response
            ? data.response.code
            : 0;

        if (code === 403 || code === 451) {
            fail("Accès refusé ou géoblocage.");
        } else if (code === 0) {
            fail("Serveur indisponible ou CORS.");
        } else {
            fail("Flux indisponible (HTTP " + code + ").");
        }
    });

} else if (
    video.canPlayType(
        "application/vnd.apple.mpegurl"
    )
) {

    video.src = url;

    video.onerror = function() {
        fail("Lecture impossible.");
    };

} else {

    video.src = url;

    video.onerror = function() {
        fail("Format vidéo non pris en charge.");
    };
}
</script>
"""


# ============================================================
# ÉTAT
# ============================================================

st.session_state.setdefault("favs", {})
st.session_state.setdefault("custom", [])
st.session_state.setdefault("nav", "🏠 Accueil")
st.session_state.setdefault("shown", PAGE_SIZE)
st.session_state.setdefault("search", "")


def go(label):
    st.session_state.nav = label
    st.session_state.shown = PAGE_SIZE


def toggle_fav(channel):
    url = channel.get("url", "")

    if not url:
        return

    if url in st.session_state.favs:
        del st.session_state.favs[url]
    else:
        st.session_state.favs[url] = channel


def more_channels():
    st.session_state.shown += PAGE_SIZE


def add_custom(channels):
    st.session_state.custom = dedupe(
        [
            st.session_state.custom,
            channels,
        ]
    )


@st.dialog("📺 Pavel TV", width="large")
def watch(channel):
    name = channel.get("name", "Chaîne")
    url = channel.get("url", "")
    official = channel.get("official", "")

    st.markdown(f"### 🔴 {html.escape(name)}")

    if url:
        player(url)

        is_fav = url in st.session_state.favs

        st.button(
            "💔 Retirer des favoris"
            if is_fav
            else "❤️ Ajouter aux favoris",
            key="dialog_fav",
            on_click=toggle_fav,
            args=(channel,),
        )

        st.caption(
            "La lecture dépend du serveur de la chaîne "
            "et de la compatibilité du flux avec le navigateur."
        )

        with st.expander("🔗 Afficher le lien du flux"):
            st.code(url, language=None)

    elif official:
        st.info(
            "Cette chaîne ne fournit pas ici un flux "
            "M3U/HLS public à intégrer directement."
        )

        st.link_button(
            "▶ Ouvrir le direct officiel",
            official,
            use_container_width=True,
        )

        st.caption(
            channel.get(
                "description",
                "Page officielle de la chaîne.",
            )
        )

    else:
        st.warning("Aucun flux disponible pour cette chaîne.")


def player(url):
    components.html(
        PLAYER_HTML
        .replace("__URL__", json.dumps(url))
        .replace("__RAW__", json.dumps(url)),
        height=520,
    )


# ============================================================
# CARTES
# ============================================================

def card(channel, prefix, index):
    name = html.escape(
        channel.get("name", "Chaîne")
    )

    logo = channel.get("logo", "")
    country = channel.get("country", "")

    if logo:
        visual = (
            '<img src="'
            + html.escape(logo, quote=True)
            + '" alt="" loading="lazy" '
              'referrerpolicy="no-referrer">'
        )
    else:
        visual = '<span class="placeholder">📺</span>'

    country_text = (
        f"{flag(country)} "
        if country
        else ""
    )

    st.markdown(
        f"""
        <div class="channel-card">
            <div class="channel-logo">
                {visual}
            </div>
            <div class="channel-name">
                {name}
            </div>
            <div class="country">
                {country_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    url = channel.get("url", "")
    official = channel.get("official", "")

    if url:
        button_text = "▶ Regarder"
    elif official:
        button_text = "▶ Direct officiel"
    else:
        button_text = "Indisponible"

    if st.button(
        button_text,
        key=f"play_{prefix}_{index}",
        type="primary",
        disabled=not (url or official),
    ):
        watch(channel)


def grid(channels, prefix, per_row=4):
    for start in range(0, len(channels), per_row):
        cols = st.columns(per_row)

        for offset, col in enumerate(cols):
            index = start + offset

            if index >= len(channels):
                continue

            with col:
                card(
                    channels[index],
                    prefix,
                    index,
                )


def section_title(title, count=None):
    badge = (
        f"<small>{count}</small>"
        if count is not None
        else ""
    )

    st.markdown(
        f"""
        <div class="section-title">
            {html.escape(title)}
            {badge}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FILTRES / PAGINATION
# ============================================================

def apply_filters(channels, https_only=True, logo_only=False):
    output = list(channels)

    if https_only:
        output = [
            channel
            for channel in output
            if channel.get("url", "").startswith("https://")
            or not channel.get("url")
        ]

    if logo_only:
        output = [
            channel
            for channel in output
            if channel.get("logo")
        ]

    return output


def paged_grid(
    channels,
    signature,
    only_playable=True,
    https_only=True,
    logo_only=False,
):
    if st.session_state.get("sig") != signature:
        st.session_state.sig = signature
        st.session_state.shown = PAGE_SIZE

    filtered = apply_filters(
        channels,
        https_only=https_only,
        logo_only=logo_only,
    )

    shown = st.session_state.shown

    if only_playable:
        playable, more = playable_channels(
            [
                c for c in filtered
                if c.get("url")
            ],
            shown,
        )

        # Les chaînes officielles sans flux direct restent visibles.
        official_only = [
            c for c in filtered
            if not c.get("url")
            and c.get("official")
        ]

        view = playable + official_only[:max(
            0,
            shown - len(playable),
        )]

        st.caption(
            f"{len(view)} chaîne(s) affichée(s)"
        )
    else:
        view = filtered[:shown]
        more = len(filtered) > shown

        st.caption(
            f"{len(filtered)} chaîne(s)"
        )

    if not view:
        st.info(
            "Aucune chaîne disponible. "
            "Désactive le filtre HTTPS ou "
            "choisis une autre catégorie."
        )
        return

    grid(view, "paged")

    if more:
        st.button(
            "Afficher plus ⬇",
            key="more_channels",
            on_click=more_channels,
        )


# ============================================================
# CHARGEMENT DES PLAYLISTS
# ============================================================

sources = (
    [
        (f"{BASE}/countries/{country}.m3u", country)
        for country in COUNTRY_BLOCKS
    ]
    + [
        (f"{BASE}/{path}", "")
        for path in CATEGORY_FILES.values()
    ]
    + [
        (f"{BASE}/languages/fra.m3u", ""),
        (f"{BASE}/index.m3u", ""),
    ]
    + [
        (url, "")
        for url in EXTRA_M3U
    ]
)


with st.spinner("📡 Chargement des chaînes..."):
    pools = fetch_all(sources)


def P(path):
    return pools.get(
        f"{BASE}/{path}"
    ) or []


fra = P("languages/fra.m3u")
fra_urls = {
    channel["url"]
    for channel in fra
}


extra = dedupe(
    [
        pools.get(url)
        for url in EXTRA_M3U
    ]
)


ALL = dedupe(
    [
        *[
            P(f"countries/{country}.m3u")
            for country in COUNTRY_BLOCKS
        ],
        *[
            P(path)
            for path in CATEGORY_FILES.values()
        ],
        fra,
        P("index.m3u"),
        extra,
        st.session_state.custom,
    ]
)


# Ajouter les chaînes officielles camerounaises.
ALL = dedupe(
    [
        ALL,
        OFFICIAL_CAMEROON,
    ]
)


RAW_BLOCKS = {
    country: sort_channels(
        P(f"countries/{country}.m3u")
    )
    for country in COUNTRY_BLOCKS
}


for key in ("sport", "news", "ent", "doc"):
    RAW_BLOCKS[key] = sort_channels(
        P(CATEGORY_FILES[key])
    )


# Cameroun = playlist publique + chaînes officielles.
RAW_BLOCKS["cm"] = sort_channels(
    dedupe(
        [
            RAW_BLOCKS.get("cm", []),
            [
                channel
                for channel in ALL
                if channel.get("country") == "cm"
                or CM.search(channel.get("name", ""))
            ],
            OFFICIAL_CAMEROON,
        ]
    )
)


RAW_BLOCKS["frall"] = sort_channels(
    dedupe(
        [
            fra,
            RAW_BLOCKS.get("fr", []),
        ]
    )
)


RAW_BLOCKS["film"] = sort_channels(
    dedupe(
        [
            [
                channel
                for channel in dedupe(
                    [
                        P("categories/movies.m3u"),
                        P("categories/series.m3u"),
                    ]
                )
                if channel["url"] in fra_urls
            ],
            [
                channel
                for channel in ALL
                if FILMS.search(
                    channel.get("name", "")
                )
                and (
                    channel.get("url", "") in fra_urls
                    or channel.get("country", "")
                    in {"fr", "cm", "ci", "sn", "ma"}
                )
            ],
        ]
    )
)


best = {}

for channel in sort_channels(
    [
        channel
        for channel in ALL
        if channel.get("key", "") in RANK
    ]
):
    best.setdefault(
        channel["key"],
        channel,
    )


# Forcer les chaînes camerounaises officielles
# dans "À la une".
for channel in OFFICIAL_CAMEROON:
    best[channel["key"]] = channel


RAW_BLOCKS["pop"] = sorted(
    best.values(),
    key=lambda channel: RANK.get(
        channel.get("key", ""),
        999,
    ),
)


# ============================================================
# SIDEBAR
# ============================================================

st.markdown(CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            margin-bottom:15px;
        ">
            {LOGO_SVG}
            <div class="brand-name"
                 style="font-size:26px">
                PAVEL<span>TV</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Réglages")

    only_playable = st.checkbox(
        "Masquer les flux indisponibles",
        value=True,
        help=(
            "Teste les flux M3U avant de les afficher. "
            "Les liens officiels restent disponibles."
        ),
    )

    https_only = st.checkbox(
        "HTTPS uniquement",
        value=True,
    )

    logo_only = st.checkbox(
        "Seulement les chaînes avec logo",
        value=False,
    )

    st.markdown("---")
    st.markdown("### 🇨🇲 Cameroun")

    st.caption(
        "Les chaînes camerounaises sont regroupées "
        "dans une rubrique dédiée."
    )

    if st.button(
        "🇨🇲 Ouvrir les chaînes camerounaises",
        use_container_width=True,
    ):
        go(LABEL["cm"])

    st.markdown("---")
    st.markdown("### ⭐ Favoris")

    st.caption(
        f"{len(st.session_state.favs)} "
        "chaîne(s) enregistrée(s)"
    )

    if st.button(
        "⭐ Mes favoris",
        use_container_width=True,
    ):
        go("⭐ Favoris")

    st.markdown("---")
    st.markdown("### 💾 Sauvegarde")

    export_data = json.dumps(
        {
            "favs": list(
                st.session_state.favs.values()
            ),
            "custom": st.session_state.custom,
        },
        ensure_ascii=False,
        indent=2,
    )

    st.download_button(
        "Télécharger mes favoris",
        export_data,
        file_name="pavel_tv.json",
        mime="application/json",
        use_container_width=True,
    )

    upload = st.file_uploader(
        "Restaurer une sauvegarde",
        type=["json"],
    )

    if upload is not None:
        try:
            data = json.load(upload)

            favs = data.get("favs", [])
            custom = data.get("custom", [])

            for channel in favs:
                if channel.get("url"):
                    st.session_state.favs[
                        channel["url"]
                    ] = channel

            add_custom(custom)

            st.success("Sauvegarde restaurée.")
        except Exception:
            st.error("Fichier de sauvegarde invalide.")


# ============================================================
# INTERFACE PRINCIPALE
# ============================================================

st.markdown(
    HERO,
    unsafe_allow_html=True,
)

top_left, top_right = st.columns([1, 3])

with top_left:
    with st.popover("☰  Catégories"):
        st.button(
            "🏠 Accueil",
            key="menu_home",
            on_click=go,
            args=("🏠 Accueil",),
        )

        st.button(
            f"⭐ Favoris ({len(st.session_state.favs)})",
            key="menu_favs",
            on_click=go,
            args=("⭐ Favoris",),
        )

        st.markdown(
            '<div class="group-title">Afrique</div>',
            unsafe_allow_html=True,
        )

        st.button(
            LABEL["cm"],
            key="menu_cm",
            on_click=go,
            args=(LABEL["cm"],),
        )

        st.markdown(
            '<div class="group-title">Francophone</div>',
            unsafe_allow_html=True,
        )

        for bid in ("fr", "frall"):
            st.button(
                LABEL[bid],
                key=f"menu_{bid}",
                on_click=go,
                args=(LABEL[bid],),
            )

        st.markdown(
            '<div class="group-title">Thématiques</div>',
            unsafe_allow_html=True,
        )

        for bid in ("sport", "news", "ent", "doc", "film"):
            st.button(
                LABEL[bid],
                key=f"menu_{bid}",
                on_click=go,
                args=(LABEL[bid],),
            )

        st.markdown(
            '<div class="group-title">Autres</div>',
            unsafe_allow_html=True,
        )

        st.button(
            "🌍 Par pays",
            key="menu_country",
            on_click=go,
            args=("🌍 Par pays",),
        )

        st.button(
            "🔗 Ma liste M3U",
            key="menu_custom",
            on_click=go,
            args=("🔗 Ma liste M3U",),
        )


with top_right:
    query = st.text_input(
        "Recherche",
        placeholder=(
            "🔍 Rechercher une chaîne "
            "(CRTV, Canal 2, France 2...)"
        ),
        label_visibility="collapsed",
        key="search_box",
    )


if any(value is None for value in pools.values()):
    st.caption(
        "⚠️ Certaines listes publiques n'ont pas pu "
        "être chargées. Recharge la page."
    )


nav = st.session_state.nav


# ============================================================
# RECHERCHE
# ============================================================

if query.strip():
    search = query.strip().lower()

    section_title(
        f"Résultats pour « {query.strip()} »"
    )

    hits = [
        channel
        for channel in ALL
        if search in channel.get(
            "name",
            "",
        ).lower()
    ]

    paged_grid(
        hits,
        ("search", search),
        only_playable=only_playable,
        https_only=https_only,
        logo_only=logo_only,
    )


# ============================================================
# ACCUEIL
# ============================================================

elif nav == "🏠 Accueil":

    if st.session_state.favs:
        section_title(
            "⭐ Mes favoris",
            len(st.session_state.favs),
        )

        grid(
            list(
                st.session_state.favs.values()
            )[:HOME_PER_BLOCK],
            "home_favs",
        )

    for block_id in HOME_BLOCKS:
        channels = apply_filters(
            RAW_BLOCKS.get(block_id, []),
            https_only=https_only,
            logo_only=logo_only,
        )

        if not channels:
            continue

        section_title(
            LABEL[block_id],
            len(channels),
        )

        if only_playable:
            playable, _ = playable_channels(
                [
                    c for c in channels
                    if c.get("url")
                ],
                HOME_PER_BLOCK,
            )

            official = [
                c for c in channels
                if not c.get("url")
                and c.get("official")
            ]

            view = (
                playable
                + official[:max(
                    0,
                    HOME_PER_BLOCK - len(playable),
                )]
            )
        else:
            view = channels[:HOME_PER_BLOCK]

        grid(
            view,
            f"home_{block_id}",
        )

        if len(channels) > HOME_PER_BLOCK:
            st.button(
                f"Voir toutes les chaînes · {LABEL[block_id]}",
                key=f"all_{block_id}",
                on_click=go,
                args=(LABEL[block_id],),
            )


# ============================================================
# FAVORIS
# ============================================================

elif nav == "⭐ Favoris":

    section_title(
        "⭐ Mes favoris",
        len(st.session_state.favs),
    )

    st.button(
        "← Accueil",
        key="back_favs",
        on_click=go,
        args=("🏠 Accueil",),
    )

    if st.session_state.favs:
        grid(
            list(
                st.session_state.favs.values()
            ),
            "favorites",
        )
    else:
        st.info(
            "Tu n'as pas encore ajouté de chaîne "
            "aux favoris."
        )


# ============================================================
# CATÉGORIE
# ============================================================

elif nav in BLOCK_BY_LABEL:

    block_id = BLOCK_BY_LABEL[nav]

    section_title(
        nav,
        len(RAW_BLOCKS.get(block_id, [])),
    )

    st.button(
        "← Accueil",
        key=f"back_{block_id}",
        on_click=go,
        args=("🏠 Accueil",),
    )

    paged_grid(
        RAW_BLOCKS.get(block_id, []),
        (
            nav,
            https_only,
            logo_only,
            only_playable,
        ),
        only_playable=only_playable,
        https_only=https_only,
        logo_only=logo_only,
    )


# ============================================================
# PAR PAYS
# ============================================================

elif nav == "🌍 Par pays":

    section_title("🌍 Par pays")

    st.button(
        "← Accueil",
        key="back_country",
        on_click=go,
        args=("🏠 Accueil",),
    )

    selected_country = st.selectbox(
        "Pays",
        list(COUNTRIES),
        format_func=lambda code: (
            f"{flag(code)} {COUNTRIES[code]}"
        ),
    )

    try:
        country_channels = sort_channels(
            fetch(
                f"{BASE}/countries/"
                f"{selected_country}.m3u",
                selected_country,
            )
        )
    except Exception:
        country_channels = []
        st.error(
            "La liste de ce pays est momentanément "
            "indisponible."
        )

    paged_grid(
        country_channels,
        (
            "country",
            selected_country,
            https_only,
            logo_only,
            only_playable,
        ),
        only_playable=only_playable,
        https_only=https_only,
        logo_only=logo_only,
    )


# ============================================================
# MA LISTE M3U
# ============================================================

elif nav == "🔗 Ma liste M3U":

    section_title("🔗 Ma liste M3U")

    st.button(
        "← Accueil",
        key="back_custom",
        on_click=go,
        args=("🏠 Accueil",),
    )

    tab_link, tab_text, tab_file, tab_one = st.tabs(
        [
            "🔗 URL M3U",
            "📋 Coller",
            "📁 Fichier",
            "➕ Une chaîne",
        ]
    )

    with tab_link:
        link = st.text_input(
            "URL de la playlist",
            placeholder="https://exemple.com/playlist.m3u",
            key="custom_m3u_url",
        )

        if st.button(
            "Charger la playlist",
            key="load_custom_url",
        ):
            if not link.strip():
                st.warning(
                    "Indique une URL M3U."
                )
            else:
                try:
                    channels = fetch(
                        link.strip()
                    )
                    add_custom(channels)

                    st.success(
                        f"{len(channels)} chaîne(s) ajoutée(s)."
                    )
                except Exception as exc:
                    st.error(
                        "Impossible de charger la playlist."
                    )
                    st.caption(str(exc))

    with tab_text:
        text = st.text_area(
            "Contenu M3U",
            height=180,
            placeholder=(
                "#EXTM3U\n"
                "#EXTINF:-1,Ma chaîne\n"
                "https://exemple.com/live.m3u8"
            ),
            key="custom_m3u_text",
        )

        if st.button(
            "Importer le texte",
            key="load_custom_text",
        ):
            if text.strip():
                channels = parse_m3u(text)
                add_custom(channels)

                st.success(
                    f"{len(channels)} chaîne(s) ajoutée(s)."
                )
            else:
                st.warning(
                    "Colle d'abord le contenu M3U."
                )

    with tab_file:
        uploaded = st.file_uploader(
            "Fichier .m3u / .m3u8 / .txt",
            type=["m3u", "m3u8", "txt"],
            key="custom_file",
        )

        if uploaded is not None:
            if st.button(
                "Importer le fichier",
                key="load_custom_file",
            ):
                content = uploaded.getvalue().decode(
                    "utf-8",
                    "ignore",
                )

                channels = parse_m3u(content)
                add_custom(channels)

                st.success(
                    f"{len(channels)} chaîne(s) ajoutée(s)."
                )

    with tab_one:
        name = st.text_input(
            "Nom de la chaîne",
            key="custom_name",
        )

        url = st.text_input(
            "Lien du flux (.m3u8)",
            key="custom_url",
        )

        group = st.text_input(
            "Catégorie",
            key="custom_group",
        )

        logo = st.text_input(
            "Logo (URL facultative)",
            key="custom_logo",
        )

        if st.button(
            "Ajouter la chaîne",
            key="add_custom_one",
        ):
            if not name.strip():
                st.warning(
                    "Indique le nom de la chaîne."
                )
            elif not url.strip().startswith(
                "http"
            ):
                st.warning(
                    "Le lien doit commencer par http."
                )
            else:
                add_custom(
                    [
                        {
                            "name": name.strip(),
                            "url": url.strip(),
                            "logo": logo.strip(),
                            "country": "",
                            "group": group.strip(),
                            "key": norm(name),
                            "official": "",
                            "description": "",
                        }
                    ]
                )

                st.success(
                    "Chaîne ajoutée."
                )

    mine = dedupe(
        [
            extra,
            st.session_state.custom,
        ]
    )

    if mine:
        groups = sorted(
            {
                channel.get("group", "")
                for channel in mine
                if channel.get("group")
            }
        )

        if groups:
            selected_group = st.selectbox(
                "Catégorie",
                ["Toutes", *groups],
            )
        else:
            selected_group = "Toutes"

        view = [
            channel
            for channel in mine
            if selected_group == "Toutes"
            or channel.get("group") == selected_group
        ]

        section_title(
            "Mes chaînes",
            len(view),
        )

        grid(
            view[:200],
            "mine",
        )

        if st.session_state.custom:
            if st.button(
                "🗑️ Vider ma liste",
                key="clear_custom",
            ):
                st.session_state.custom = []
                st.rerun()

    else:
        st.info(
            "Ajoute une playlist M3U ou une chaîne "
            "pour la retrouver ici."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:45px;
        padding:20px 5px;
        text-align:center;
        color:rgba(255,255,255,.42);
        font-size:12px;
    ">
        PAVEL TV · Lecteur de contenus publics et autorisés
        <br>
        Les disponibilités dépendent des serveurs des chaînes.
    </div>
    """,
    unsafe_allow_html=True,
)

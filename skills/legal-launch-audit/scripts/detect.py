#!/usr/bin/env python3
"""legal-launch-kit detector.

Scans a project folder (read-only) for signals that trigger legal or
store-policy obligations: trackers, ad SDKs, consent managers, accounts,
payments, foreign processors, permissions, AI features, legal pages, etc.

Every signal comes with file:line evidence so a reviewer can verify it.
Standard library only. Python 3.9+.

Usage:
    python3 detect.py <project-root> [--format md|json] [--max-hits 5] [--fail-on P0]

The output is a starting point for an audit, not a legal conclusion.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

VERSION = "0.3.1"

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "bower_components", ".next", ".nuxt",
    ".svelte-kit", ".astro", "dist", "build", "out", ".output", ".dart_tool",
    "Pods", ".gradle", ".idea", ".vscode", "vendor", "__pycache__", ".venv",
    "venv", "env", "coverage", ".turbo", ".cache", "DerivedData", ".expo",
    ".parcel-cache", "tmp", ".terraform", "target", "bin", "obj",
}

TEXT_EXT = {
    ".html", ".htm", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".vue",
    ".svelte", ".astro", ".php", ".py", ".rb", ".go", ".java", ".kt", ".kts",
    ".swift", ".m", ".mm", ".dart", ".xml", ".gradle", ".json", ".yaml",
    ".yml", ".toml", ".plist", ".xcprivacy", ".md", ".mdx", ".txt", ".liquid",
    ".twig", ".blade", ".erb", ".ejs", ".hbs", ".njk", ".cs", ".cshtml",
    ".razor", ".properties", ".env", ".ini", ".conf",
}

SPECIAL_NAMES = {
    "Podfile", "Gemfile", "Dockerfile", "Info.plist", "AndroidManifest.xml",
    "pubspec.yaml", "package.json", "build.gradle", "build.gradle.kts",
    "PrivacyInfo.xcprivacy", "Cartfile", "Package.swift", "app.json",
    "capacitor.config.json", "netlify.toml", "vercel.json", "firebase.json",
    ".htaccess", "nginx.conf", "_redirects", "web.config",
}

SKIP_FILE_RE = re.compile(
    r"(\.min\.(js|css)$|\.map$|package-lock\.json$|yarn\.lock$|pnpm-lock\.yaml$|"
    r"pubspec\.lock$|Podfile\.lock$|composer\.lock$|Gemfile\.lock$)",
    re.I,
)

MAX_BYTES = 1_500_000
SNIPPET_LEN = 140


def tr(word: str) -> str:
    """Build a regex fragment that matches a Turkish word with or without
    Turkish characters, in any case (e.g. 'çerez' matches 'cerez', 'Çerez')."""
    table = {
        "i": "[iİıI]", "ı": "[ıIiİ]", "ş": "[şŞsS]", "ç": "[çÇcC]",
        "ö": "[öÖoO]", "ü": "[üÜuU]", "ğ": "[ğĞgG]", "s": "[sSşŞ]",
        "c": "[cCçÇ]", "o": "[oOöÖ]", "u": "[uUüÜ]", "g": "[gGğĞ]",
    }
    out = []
    for ch in word:
        out.append(table.get(ch, re.escape(ch)))
    return "".join(out)


def rx(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.I)


# ---------------------------------------------------------------------------
# Signal catalogue. Each entry: id, category, label, regex.
# Keep labels short; they show up in reports.
# ---------------------------------------------------------------------------
SIGNALS = [
    # Analytics / tracking
    ("google_analytics", "analytics", "Google Analytics / Tag Manager / Firebase Analytics",
     rx(r"googletagmanager\.com|google-analytics\.com|\bgtag\s*\(|\bG-[A-Z0-9]{8,}\b|firebase[_/-]analytics|FirebaseAnalytics|@react-native-firebase/analytics")),
    ("meta_pixel", "analytics", "Meta (Facebook) Pixel / App Events SDK",
     rx(r"connect\.facebook\.net|\bfbq\s*\(|facebook_app_events|FBSDKCoreKit|com\.facebook\.android:facebook")),
    ("tiktok_pixel", "analytics", "TikTok Pixel / SDK",
     rx(r"analytics\.tiktok\.com|\bttq\.(load|page|track)|tiktok-business-sdk")),
    ("yandex_metrica", "analytics", "Yandex Metrica",
     rx(r"mc\.yandex\.ru|\bym\s*\(\s*\d+")),
    ("session_replay", "analytics", "Session replay / heatmap (Hotjar, Clarity, FullStory, Smartlook)",
     rx(r"static\.hotjar\.com|\bhj\s*\(|clarity\.ms|microsoft_clarity|fullstory|smartlook|logrocket|mouseflow")),
    ("product_analytics", "analytics", "Product analytics (Mixpanel, Amplitude, Segment, PostHog)",
     rx(r"mixpanel|amplitude|cdn\.segment\.com|@segment/|posthog")),
    ("cookieless_analytics", "analytics_cookieless", "Cookieless analytics (Plausible, Umami, Simple Analytics, Fathom)",
     rx(r"plausible\.io|umami|simpleanalytics|usefathom")),

    # Ads
    ("admob", "ads", "Google AdMob / Mobile Ads SDK",
     rx(r"google_mobile_ads|play-services-ads|GoogleMobileAds|react-native-google-mobile-ads|com\.google\.android\.gms\.ads|ca-app-pub-\d+")),
    ("adsense", "ads", "Google AdSense",
     rx(r"pagead2\.googlesyndication\.com|adsbygoogle|ca-pub-\d{6,}")),
    ("other_ad_networks", "ads", "Other ad networks (AppLovin, Unity Ads, ironSource, Meta AN, Liftoff, Mintegral)",
     rx(r"applovin|unity-?ads|unityads|ironsource|audience_network|AudienceNetwork|vungle|liftoff|chartboost|mintegral|pangle")),

    # Consent
    ("google_ump", "consent", "Google User Messaging Platform (UMP) consent SDK",
     rx(r"UserMessagingPlatform|ConsentInformation|ConsentRequestParameters|ConsentForm\b|user_messaging_platform|requestConsentInfoUpdate")),
    ("web_cmp", "consent", "Web consent manager (Cookiebot, OneTrust, CookieYes, Klaro, Didomi, Usercentrics, iubenda…)",
     rx(r"cookiebot|onetrust|cookielaw\.org|cookieyes|cookie-script|klaro|osano|iubenda|usercentrics|tarteaucitron|cookieconsent|didomi|complianz|consentmanager|termly")),
    ("consent_mode", "consent", "Google Consent Mode call",
     rx(r"gtag\s*\(\s*['\"]consent['\"]")),

    # Consent anti-patterns
    ("prechecked_checkbox", "consent_antipattern", "Pre-ticked checkbox (must not be used for consent)",
     rx(r"type=[\"']checkbox[\"'][^>]*\bchecked\b|\bchecked\b[^>]*type=[\"']checkbox[\"']|defaultChecked|value:\s*true,\s*//\s*consent")),
    ("implied_consent", "consent_antipattern", "Implied consent wording (\"by continuing you accept\")",
     rx(r"by continuing to (use|browse)|by using this (site|website|app),? you (agree|accept|consent)|" + tr("kullanmaya devam ederek") + r"|" + tr("gezinmeye devam ederek"))),

    # Accounts
    ("auth", "auth", "User accounts / authentication",
     rx(r"firebase_auth|FirebaseAuth|firebase/auth|@react-native-firebase/auth|supabase\.auth|auth\.sign[_]?up|signUp\s*\(|createUserWithEmailAndPassword|next-auth|@auth0|@clerk|aws-amplify|google_sign_in|GoogleSignIn|sign_in_with_apple|ASAuthorizationAppleIDProvider|type=[\"']password[\"']|obscureText:\s*true")),
    ("account_deletion", "account_deletion", "Account deletion path",
     rx(r"deleteUser|delete_user|currentUser\??\.delete\s*\(|deleteAccount|delete_account|account[/_-]delete|delete[/_-]account|data[/_-]deletion|auth\.admin\.deleteUser|" + tr("hesabımı sil") + "|" + tr("hesabı sil") + "|" + tr("hesap silme") + r"|delete\s+(my\s+)?account")),

    # Money
    ("payment_gateway", "payments", "Payment gateway (Stripe, iyzico, PayTR, Paddle, PayPal, Adyen…)",
     rx(r"\bstripe\b|@stripe/|js\.stripe\.com|iyzico|iyzipay|\bpaytr\b|\bpaddle\.(com|js)|@paddle/|lemonsqueezy|braintree|paypal|\badyen\b|\bmollie\b|razorpay|craftgate|\bsipay\b|parampos|shopier|shopify")),
    ("in_app_purchase", "payments", "In-app purchases / store billing",
     rx(r"in_app_purchase|purchases_flutter|RevenueCat|react-native-purchases|react-native-iap|StoreKit|SKPaymentQueue|BillingClient|com\.android\.billingclient")),
    ("subscription", "subscriptions", "Auto-renewing subscription logic",
     rx(r"auto[-_ ]?renew|subscriptionPeriod|SubscriptionPeriod|" + tr("otomatik yenilen") + r"|free[-_ ]?trial|" + tr("deneme süresi"))),
    ("discount_claims", "pricing", "Discount / strike-through price UI",
     rx(r"line-through|old[_-]?price|compare[_-]?at[_-]?price|" + tr("indirim") + r"|discount[_-]?percent|% ?off\b")),
    ("reviews", "reviews", "Customer reviews / ratings UI",
     rx(r"RatingBar|star[_-]?rating|review[_-]?(list|form|count|stars|card)|reviews?Collection|aggregateRating|<Reviews?\b")),

    # Messaging
    ("marketing_email_sms", "marketing_messages", "Email/SMS marketing provider (Mailchimp, Brevo, Klaviyo, SendGrid, Netgsm, İleti Merkezi, Twilio…)",
     rx(r"mailchimp|sendinblue|brevo|klaviyo|sendgrid|mailerlite|convertkit|netgsm|iletimerkezi|twilio|vonage|nexmo|mutlucell|jetsms|verimor")),
    ("newsletter_optin", "marketing_messages", "Newsletter / campaign opt-in UI",
     rx(r"newsletter|" + tr("e-bülten") + r"|" + tr("bültene abone") + r"|" + tr("kampanyalardan") + r"|marketing[_ ]?(emails?|consent)|" + tr("ticari elektronik ileti"))),
    ("push", "push", "Push notifications (FCM, OneSignal, APNs)",
     rx(r"firebase_messaging|FirebaseMessaging|@react-native-firebase/messaging|onesignal|UNUserNotificationCenter|POST_NOTIFICATIONS")),

    # Personal data collection
    ("form", "forms", "Form that collects user input",
     rx(r"<form\b|<Form\b|useForm\s*\(|FormBuilder|TextFormField")),
    ("pii_contact_fields", "forms", "Email / phone fields",
     rx(r"type=[\"'](email|tel)[\"']|TextInputType\.(emailAddress|phone)|keyboardType=[\"'](email-address|phone-pad)")),
    ("pii_national_id", "pii_overcollection", "National ID (TCKN) field",
     rx(r"\btckn\b|tc[_ ]?kimlik|kimlik[_ ]?no|identityNumber|nationalId|national_id")),
    ("pii_birthdate", "pii_overcollection", "Birth date field",
     rx(r"\b(birth_?date|birthDate|date_?of_?birth|dateOfBirth|dob|dogum_?tarihi|dogumTarihi)\b")),
    ("special_category", "special_category", "Possible special-category data (health, biometrics, religion, sexual life)",
     rx(r"HealthKit|health_connect|androidx\.health|health[_-]?data|medical[_-]?record|diagnos(is|e)|blood[_-]?type|kan[_-]?grubu|" + tr("teşhis") + r"|religion|sexual[_-]?orientation|pregnan|menstrua")),

    # Processors that usually mean data leaves the user's country
    ("foreign_processors", "foreign_processors", "Third-party cloud / SaaS processor",
     rx(r"firebase|googleapis\.com|amazonaws\.com|@aws-sdk|aws-sdk|vercel|netlify|supabase|cloudflare|azure|sentry|crashlytics|bugsnag|datadog|algolia|onesignal|intercom|crisp\.chat|tawk\.to|zendesk|hubspot|cloudinary|mongodb\.net|planetscale|neon\.tech|heroku|render\.com|fly\.io|digitaloceanspaces")),

    # Mobile permissions and tracking
    ("android_permission", "permissions", "Android permission",
     rx(r"<uses-permission[^>]*android:name=[\"']android\.permission\.([A-Z_]+)")),
    ("ios_usage_description", "permissions", "iOS usage description",
     rx(r"<key>(NS\w+UsageDescription)</key>")),
    ("ios_att", "tracking", "App Tracking Transparency",
     rx(r"NSUserTrackingUsageDescription|ATTrackingManager|AppTrackingTransparency|app_tracking_transparency")),

    # AI features
    ("ai_api", "ai", "AI / LLM API or SDK",
     rx(r"\bopenai\b|@anthropic-ai|\banthropic\b|generative-?ai|@google/genai|google_generative_ai|firebase_vertexai|vertexai|mistralai|cohere|replicate\.com|huggingface|langchain|ollama|groq|elevenlabs|stability\.ai|dall-?e|\bgpt-[345]")),

    # User-generated content
    ("ugc", "ugc", "User-generated content (posts, comments, uploads, reporting/blocking)",
     rx(r"createPost|uploadPost|addComment|comments?Collection|user[_-]?generated|reportContent|report[_-]?(post|user|comment)|blockUser|block[_-]?user")),

    # Social features (TR under-15 rules, UK Online Safety Act, store UGC rules)
    ("social_features", "social", "Social features (followers, friends, direct messages, chat, live streaming)",
     rx(r"followers?\b|follow[_-]?user|friend[_-]?request|addFriend|direct[_-]?message|chat[_-]?room|ChatScreen|ChatPage|conversations?Collection|live[_-]?stream|LiveStream|" + tr("takipçi") + r"|" + tr("arkadaş ekle"))),

    # Children
    ("children", "children", "Child-directed configuration",
     rx(r"tagForChildDirectedTreatment|tag_for_child_directed|maxAdContentRating|\bCOPPA\b|designed for families|child[-_ ]?directed|kids[-_ ]?category")),

    # Web storage
    ("web_storage", "storage", "Writes cookies / localStorage",
     rx(r"document\.cookie\s*=|localStorage\.setItem|cookies\(\)\.set|setCookie\s*\(|js-cookie")),

    # Security / outdated items
    ("cleartext", "security", "Cleartext HTTP allowed or used",
     rx(r"usesCleartextTraffic=[\"']true|NSAllowsArbitraryLoads</key>\s*<true|[\"']http://(?!localhost|127\.|0\.0\.0\.0|10\.|192\.168\.|www\.w3\.org|schemas|xmlns|ns\.adobe|purl\.org|json-schema)[a-z0-9]")),
    ("https_redirect", "https", "HTTP→HTTPS redirect rule",
     rx(r"RewriteCond\s+%\{HTTPS\}\s+(off|!on)|RewriteCond\s+%\{SERVER_PORT\}\s+80|X-Forwarded-Proto|return\s+301\s+https://|forceHTTPS|force_https|enforce_https")),
    ("odr_link", "outdated", "Link to the closed EU ODR platform",
     rx(r"ec\.europa\.eu/(odr|consumers/odr)|consumer-redress/odr")),
]

# Legal pages: matched against file paths and against content (quoted paths
# or visible titles). Turkish and English variants.
LEGAL_PAGES = {
    "privacy_policy": ("Privacy policy", rx(r"privacy|" + tr("gizlilik") + r"|datenschutz|polityka-prywatnosci")),
    "kvkk_notice": ("KVKK privacy notice (aydınlatma metni)", rx(r"\bkvkk\b|" + tr("aydınlatma"))),
    "cookie_policy": ("Cookie policy", rx(r"cookie[-_ ]?polic|" + tr("çerez"))),
    "terms": ("Terms of use / service", rx(r"terms[-_ ]?(of[-_ ]?)?(use|service)|[\"'/]terms/?[\"']|[\"'/]kosullar/?[\"']|\btos\b|\beula\b|" + tr("kullanım koşulları") + r"|kullanim[-_]kosullari|" + tr("üyelik sözleşmesi"))),
    "distance_sales": ("Distance sales contract (mesafeli satış)", rx(tr("mesafeli")) ),
    "pre_contract": ("Pre-contract information form (ön bilgilendirme)", rx(tr("ön bilgilendirme") + r"|on[-_]?bilgilendirme")),
    "withdrawal_returns": ("Withdrawal / returns / refund policy", rx(r"refund|returns?[-_ ]?polic|withdraw|" + tr("iade") + r"|" + tr("cayma"))),
    "imprint_contact": ("Imprint / company info / contact", rx(r"impressum|imprint|legal[-_ ]?notice|" + tr("künye") + r"|\bcontact(?![a-z])|" + tr("iletişim"))),
    "account_deletion_page": ("Account / data deletion page", rx(r"delete[-_ ]?account|account[-_ ]?deletion|data[-_ ]?deletion|" + tr("hesap silme") + r"|hesap[-_]sil|veri[-_]silme")),
    "accessibility_statement": ("Accessibility statement", rx(r"accessibility|" + tr("erişilebilirlik"))),
}

CONTENT_PAGE_HINT = re.compile(
    r"(href|to|path|route|url|link|name|title)\s*[:=]\s*[\"'{(]|<a\b|<Link\b|<title>|<h1|Navigator|GoRoute|routes|\[\s*[\"'][a-z-]+[\"']\s*,",
    re.I,
)

# Purpose / sector hints: what the product does. Shown to the agent so it can
# ask the right questions; never treated as a conclusion.
SECTOR_HINTS = {
    "health_fitness": rx(r"healthkit|health_connect|workout|fitness|calorie|" + tr("kalori") + r"|heart[_-]?rate|" + tr("nabız") + r"|menstrua|period[_-]?track|pregnan|" + tr("hamile") + r"|\bdiet\b|" + tr("diyet") + r"|therapy|" + tr("terapi") + r"|meditation|symptom"),
    "finance_crypto": rx(r"\bwallet\b|" + tr("cüzdan") + r"|\bloan\b|\bkredi\b|\binvest|" + tr("yatırım") + r"|crypto|kripto|bitcoin|\btrading\b|borsa|insurance|sigorta|\biban\b"),
    "kids_education": rx(r"\bkids?\b|" + tr("çocuk") + r"|preschool|parental[_-]?(gate|control)|homework|" + tr("ödev")),
    "dating": rx(r"\bdating\b|" + tr("flört") + r"|swipe[_-]?(left|right)"),
    "gambling": rx(r"\bbet(ting|s)?\b|bahis|casino|kumar|lottery|piyango|loot[_-]?box|sweepstake|" + tr("çekiliş")),
    "delivery_booking": rx(r"courier|kurye|ride[_-]?(hailing|share)|booking|rezervasyon|reservation|appointment|randevu"),
    "location_tracking": rx(r"ACCESS_BACKGROUND_LOCATION|background[_-]?location|location[_-]?tracking|geofenc|" + tr("konum takibi")),
    "iot_hardware": rx(r"flutter_blue|react-native-ble|CoreBluetooth|BluetoothGatt|\bmqtt\b|esp32|arduino"),
    "restricted_goods": rx(r"alcohol|alkol|\bwine\b|" + tr("şarap") + r"|\bbeer\b|tobacco|" + tr("tütün") + r"|\bvape\b|pharmacy|eczane|\bsupplements?\b|takviye"),
}

SUMMARY_PATTERNS = [
    ("package.json", rx(r'"(name|description)"\s*:\s*"([^"]{1,300})"')),
    ("pubspec.yaml", rx(r"^(name|description):\s*(.{1,300})$")),
    ("app.json", rx(r'"(name|description)"\s*:\s*"([^"]{1,300})"')),
    ("AndroidManifest.xml", rx(r'android:(label)="([^"]{1,120})"')),
    ("Info.plist", rx(r"<key>(CFBundleDisplayName|CFBundleName)</key>\s*<string>([^<]{1,120})</string>")),
    ("*.html", rx(r'<(title)>([^<]{1,200})</title>|<meta\s+name="(description)"\s+content="([^"]{1,300})"')),
]

DOC_SUFFIXES = {".md", ".mdx", ".txt"}


def looks_like_prose(line: str) -> bool:
    """Long natural-language lines (privacy texts, translations) mention
    features without implementing them. Skip them for code signals."""
    if len(line) < 200:
        return False
    if re.search(r"<script|src=[\"'][^\"']+\.js|https?://\S+\.(js|php)\b", line):
        return False
    return line.count(" ") / len(line) > 0.1


PAGE_SUFFIXES = {
    ".html", ".htm", ".php", ".astro", ".vue", ".svelte", ".jsx", ".tsx", ".js",
    ".ts", ".mjs", ".dart", ".md", ".mdx", ".kt", ".swift", ".liquid", ".twig",
    ".blade", ".erb", ".ejs", ".hbs", ".njk", ".cshtml", ".razor",
}

SENSITIVE_ANDROID = {
    "ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION", "ACCESS_BACKGROUND_LOCATION",
    "CAMERA", "RECORD_AUDIO", "READ_CONTACTS", "WRITE_CONTACTS", "READ_SMS",
    "SEND_SMS", "RECEIVE_SMS", "READ_CALL_LOG", "READ_PHONE_STATE",
    "READ_EXTERNAL_STORAGE", "WRITE_EXTERNAL_STORAGE", "READ_MEDIA_IMAGES",
    "READ_MEDIA_VIDEO", "READ_MEDIA_AUDIO", "MANAGE_EXTERNAL_STORAGE",
    "QUERY_ALL_PACKAGES", "BODY_SENSORS", "ACTIVITY_RECOGNITION",
    "SCHEDULE_EXACT_ALARM", "USE_EXACT_ALARM", "BIND_ACCESSIBILITY_SERVICE",
    "AD_ID", "POST_NOTIFICATIONS", "BLUETOOTH_SCAN", "NEARBY_WIFI_DEVICES",
}


def is_text_candidate(path: Path) -> bool:
    if SKIP_FILE_RE.search(path.name):
        return False
    if path.name in SPECIAL_NAMES:
        return True
    return path.suffix.lower() in TEXT_EXT


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and (not d.startswith(".") or d in {".github", ".well-known"})
        ]
        for name in filenames:
            p = Path(dirpath) / name
            try:
                if p.is_symlink() or p.stat().st_size > MAX_BYTES:
                    continue
            except OSError:
                continue
            yield p


def snippet(line: str, m: re.Match) -> str:
    line = line.strip()
    if len(line) <= SNIPPET_LEN:
        return line
    start = max(0, m.start() - 50)
    return ("…" if start else "") + line[start:start + SNIPPET_LEN] + "…"


def detect_platforms(rel_paths: list[str], contents_hint: dict[str, str]) -> list[str]:
    plats = set()
    names = {Path(p).name for p in rel_paths}
    lower = [p.lower() for p in rel_paths]
    if "pubspec.yaml" in names:
        plats.add("flutter")
    if "AndroidManifest.xml" in names or any(p.endswith(("build.gradle", "build.gradle.kts")) for p in lower):
        plats.add("android")
    if "Info.plist" in names or "Podfile" in names or any(".xcodeproj" in p for p in lower) or any(p.endswith(".swift") for p in lower):
        plats.add("ios")
    pkg = contents_hint.get("package.json", "")
    deps: set[str] = set()
    try:
        data = json.loads(pkg) if pkg else {}
        for k in ("dependencies", "devDependencies", "peerDependencies"):
            deps.update((data.get(k) or {}).keys())
    except ValueError:
        pass
    if "react-native" in deps or "expo" in deps:
        plats.add("react-native")
    if any(d.startswith("@capacitor/") for d in deps) or "capacitor.config.json" in names:
        plats.add("capacitor")
    web_markers = {"next", "nuxt", "astro", "vite", "react-dom", "vue", "svelte", "gatsby", "@remix-run/react", "@angular/core"}
    if any(p.endswith((".html", ".htm", ".php", ".astro", ".vue", ".svelte")) for p in lower) or deps & web_markers:
        plats.add("web")
    return sorted(plats)


def scan(root: Path, max_hits: int) -> dict:
    root = root.resolve()
    signals: dict[str, dict] = {}
    pages: dict[str, dict] = {k: {"label": v[0], "files": [], "mentions": []} for k, v in LEGAL_PAGES.items()}
    rel_paths: list[str] = []
    contents_hint: dict[str, str] = {}
    android_perms: dict[str, list] = {}
    ios_usage: dict[str, list] = {}
    has_privacy_manifest = False
    security_contact: list[str] = []
    server_configs: list[str] = []
    summary: list[dict] = []
    sectors: dict[str, dict] = {}
    files_scanned = 0

    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        rel_paths.append(rel)
        if path.name == "PrivacyInfo.xcprivacy":
            has_privacy_manifest = True
        if path.name.lower() in {"security.txt", "security.md"}:
            security_contact.append(rel)

        # Legal pages by file path (only for page-like files)
        if path.suffix.lower() in PAGE_SUFFIXES:
            for key, (_, pat) in LEGAL_PAGES.items():
                if pat.search(rel) and len(pages[key]["files"]) < max_hits:
                    pages[key]["files"].append(rel)

        if not is_text_candidate(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files_scanned += 1
        if path.name == "package.json" and path.parent == root:
            contents_hint["package.json"] = text
        collect_summary(path, rel, root, text, summary)

        is_doc = path.suffix.lower() in DOC_SUFFIXES
        if path.name == ".htaccess" or path.name in {"nginx.conf", "_redirects", "web.config", "netlify.toml", "vercel.json"}:
            server_configs.append(rel)
        for lineno, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            skip_signals = is_doc or looks_like_prose(line)
            for sid, cat, label, pat in SIGNALS:
                if skip_signals:
                    break
                m = pat.search(line)
                if not m:
                    continue
                entry = signals.setdefault(sid, {"category": cat, "label": label, "count": 0, "evidence": []})
                entry["count"] += 1
                if sid == "android_permission":
                    perm = m.group(1)
                    android_perms.setdefault(perm, []).append(f"{rel}:{lineno}")
                if sid == "ios_usage_description":
                    key = m.group(1)
                    ios_usage.setdefault(key, []).append(f"{rel}:{lineno}")
                if len(entry["evidence"]) < max_hits:
                    entry["evidence"].append({"file": rel, "line": lineno, "match": m.group(0)[:80], "text": snippet(line, m)})
            for sector, spat in SECTOR_HINTS.items():
                sm = spat.search(line)
                if sm:
                    sec = sectors.setdefault(sector, {"count": 0, "evidence": []})
                    sec["count"] += 1
                    if len(sec["evidence"]) < 3:
                        sec["evidence"].append({"file": rel, "line": lineno, "text": snippet(line, sm)})
            # Legal page mentions in content (links, routes, titles)
            if path.suffix.lower() in PAGE_SUFFIXES and CONTENT_PAGE_HINT.search(line):
                for key, (_, pat) in LEGAL_PAGES.items():
                    pm = pat.search(line)
                    if pm and len(pages[key]["mentions"]) < max_hits:
                        pages[key]["mentions"].append({"file": rel, "line": lineno, "text": snippet(line, pm)})

    platforms = detect_platforms(rel_paths, contents_hint)
    derived = derive(signals, pages, platforms, android_perms, ios_usage, has_privacy_manifest, security_contact)
    if server_configs and "https_redirect" not in signals:
        derived.append({"id": "no_https_redirect", "suggested_priority": "P2",
                        "text": "Server config found (" + ", ".join(server_configs[:3]) + ") without an HTTP→HTTPS redirect rule. Check whether the host forces HTTPS; otherwise add one.",
                        "matrix_rows": ["3.1"]})

    return {
        "tool": "legal-launch-kit/detect.py",
        "version": VERSION,
        "root": str(root),
        "files_scanned": files_scanned,
        "platforms": platforms,
        "project_summary": summary,
        "sector_hints": dict(sorted(sectors.items(), key=lambda kv: -kv[1]["count"])),
        "security_contact_files": security_contact,
        "signals": signals,
        "legal_pages": pages,
        "android_permissions": android_perms,
        "ios_usage_descriptions": ios_usage,
        "ios_privacy_manifest": has_privacy_manifest,
        "derived_flags": derived,
        "disclaimer": "Heuristic signals only. Confirm every item in the source before reporting. Not legal advice.",
    }


def collect_summary(path: Path, rel: str, root: Path, text: str, summary: list) -> None:
    """Collect name/description lines that tell what the product is for."""
    if len(summary) >= 20:
        return
    name = path.name
    # README at the project root: first heading + first paragraph
    if name.lower().startswith("readme") and path.parent == root:
        skip_heads = {"contents", "table of contents", "içindekiler", "index", "toc"}
        lines = [re.sub(r"<[^>]+>", "", l).strip() for l in text.splitlines()]
        head = next((l.lstrip("# ").strip() for l in lines
                     if l.startswith("#") and l.lstrip("# ").strip().replace("İ", "i").lower() not in skip_heads), "")
        para = next((l for l in lines if len(l) > 20 and not l.startswith(("#", "!", "[", "```", "|", "-", "*", ">"))), "")
        if head or para:
            summary.append({"source": rel, "field": "readme", "value": (head + " — " + para)[:300]})
        return
    # Store listing text (fastlane metadata, Play listing)
    if ("metadata" in rel or "fastlane" in rel) and name in {"short_description.txt", "full_description.txt", "description.txt", "subtitle.txt", "title.txt"}:
        summary.append({"source": rel, "field": name[:-4], "value": " ".join(text.split())[:300]})
        return
    for fname, pat in SUMMARY_PATTERNS:
        if (fname.startswith("*") and name.endswith(fname[1:])) or name == fname:
            if fname == "package.json" and path.parent != root:
                continue
            for m in pat.finditer(text):
                groups = [g for g in m.groups() if g]
                if len(groups) >= 2 and len(summary) < 20:
                    summary.append({"source": rel, "field": groups[0], "value": groups[1].strip()})


def has(signals: dict, *ids: str) -> bool:
    return any(i in signals for i in ids)


def has_cat(signals: dict, cat: str) -> bool:
    return any(v["category"] == cat for v in signals.values())


def page_found(pages: dict, key: str) -> bool:
    return bool(pages[key]["files"] or pages[key]["mentions"])


def derive(signals, pages, platforms, android_perms, ios_usage, has_manifest, security_contact=()) -> list[dict]:
    """Combine raw signals into review flags. Each flag points to matrix rows."""
    flags = []
    mobile = any(p in platforms for p in ("android", "ios", "flutter", "react-native", "capacitor"))
    collects_data = has_cat(signals, "forms") or has_cat(signals, "auth") or has_cat(signals, "analytics") or has_cat(signals, "ads")

    def add(fid, level, text, rows):
        flags.append({"id": fid, "suggested_priority": level, "text": text, "matrix_rows": rows})

    if collects_data and not (page_found(pages, "privacy_policy") or page_found(pages, "kvkk_notice")):
        add("no_privacy_notice", "P0", "Personal data appears to be collected but no privacy policy / KVKK notice page or link was found.", ["1.1"])
    if (has_cat(signals, "analytics") or has_cat(signals, "ads")) and not has_cat(signals, "consent"):
        add("trackers_without_consent_manager", "P0", "Tracking/ads code found but no consent manager. Check whether trackers fire before consent.", ["1.4", "1.5"])
    if has(signals, "admob") and not has(signals, "google_ump"):
        add("admob_without_ump", "P1", "AdMob found without Google UMP / certified CMP. Personalised ads to EEA/UK/CH need a certified TCF CMP.", ["4.7"])
    if has_cat(signals, "auth") and not has(signals, "account_deletion"):
        add("auth_without_deletion", "P0" if mobile else "P1", "Account creation found but no account-deletion path.", ["4.1", "1.3"])
    if mobile and has_cat(signals, "auth") and not page_found(pages, "account_deletion_page"):
        add("no_web_deletion_page", "P1", "Mobile app with accounts: Google Play also needs a web page/link to request account + data deletion.", ["4.1"])
    if has_cat(signals, "foreign_processors"):
        add("foreign_processors", "P1", "Third-party cloud/SaaS processors found. Personal data likely stored abroad: check KVKK Art. 9 / GDPR Chapter V safeguards and disclose them in the notice.", ["1.6"])
    if has_cat(signals, "pii_overcollection"):
        add("pii_overcollection", "P2", "National ID or birth date fields found. Confirm they are strictly necessary (data minimisation).", ["3.6"])
    if has_cat(signals, "special_category"):
        add("special_category", "P0", "Possible special-category (sensitive) data. Needs a specific legal basis, extra security and possibly a DPIA.", ["1.2"])
    if has_cat(signals, "payments") and not page_found(pages, "pre_contract") and not has(signals, "in_app_purchase"):
        add("sales_without_precontract", "P1", "Payment gateway found but no pre-contract information form / distance-sales contract (B2C TR/EU).", ["2.3", "2.4", "2.5"])
    if has(signals, "payment_gateway") and not page_found(pages, "withdrawal_returns"):
        add("sales_without_withdrawal", "P1", "Payments found but no withdrawal/returns/refund policy.", ["2.5", "2.6"])
    if has_cat(signals, "subscriptions") or has(signals, "in_app_purchase"):
        add("subscription_terms", "P1", "Paid plans/subscriptions found: verify price, period, renewal and cancel path are shown before purchase.", ["2.7"])
    if has_cat(signals, "marketing_messages"):
        add("marketing_messages", "P1", "Marketing email/SMS tooling or opt-in UI found: needs separate unticked consent; TR requires İYS registration.", ["2.13", "1.2"])
    if has_cat(signals, "ai"):
        add("ai_features", "P1", "AI API/SDK found: disclose AI interaction / AI-generated content where people see it (EU AI Act Art. 50); TR ads must disclose AI use.", ["5.2"])
    if has_cat(signals, "social") or has_cat(signals, "ugc"):
        add("social_tr_under15", "P0", "Social / user-content features found. If available in Türkiye: under-15 ban, e-Devlet age verification, protected mode for 15–17 and parental controls apply from 1 Nov 2026 (no user threshold). Also check the UK Online Safety Act.", ["5.3", "5.4"])
    if mobile and not security_contact:
        add("cra_security_contact", "P2", "Mobile app on the EU market: the Cyber Resilience Act requires reporting actively exploited vulnerabilities since 11 Sept 2026. Publish a security contact (security.txt / SECURITY.md) and define a 24-hour reporting process.", ["3.7"])
    if "android" in platforms or "flutter" in platforms or "react-native" in platforms:
        add("android_dev_verification", "P3", "Android: developer identity verification + app registration required on certified devices (BR/ID/SG/TH since 30 Sept 2026, global from 2027), also for APKs outside Play.", ["4.9"])
    if has_cat(signals, "ugc"):
        add("ugc", "P1", "User-generated content features found: need report + block + takedown flow and contact.", ["5.1"])
    if has_cat(signals, "children"):
        add("children", "P0", "Child-directed configuration found: COPPA / store kids policies apply.", ["1.10"])
    if has_cat(signals, "reviews"):
        add("reviews", "P2", "Review/rating UI found: TR (since 1 Aug 2026) only verified buyers, publish positive and negative, objective ordering.", ["2.10"])
    if has_cat(signals, "pricing"):
        add("discounts", "P2", "Discount UI found: reference price must follow TR 10-day / EU 30-day lowest price rule.", ["2.9"])
    if has_cat(signals, "consent_antipattern"):
        add("consent_antipatterns", "P1", "Pre-ticked checkbox or implied-consent wording found. Consent must be an active, unticked, separate choice.", ["1.2", "1.4"])
    if has(signals, "odr_link"):
        add("odr_link", "P2", "Link to the EU ODR platform found. The platform closed on 20 July 2025: remove it.", ["2.14"])
    if has(signals, "cleartext"):
        add("cleartext", "P1", "Cleartext HTTP allowed or used: personal data must travel over HTTPS.", ["3.1"])
    if "ios" in platforms and not has_manifest:
        add("no_privacy_manifest", "P1", "iOS target found but no PrivacyInfo.xcprivacy file.", ["4.3"])
    if "ios" in platforms and (has_cat(signals, "ads") or has(signals, "meta_pixel")) and not has(signals, "ios_att"):
        add("ios_tracking_without_att", "P1", "Ad/attribution SDK on iOS without App Tracking Transparency.", ["4.5"])
    sensitive = sorted(p for p in android_perms if p in SENSITIVE_ANDROID)
    if sensitive:
        add("android_sensitive_permissions", "P2", "Sensitive Android permissions declared: " + ", ".join(sensitive) + ". Confirm each is used, disclosed and justified.", ["4.4"])
    if ios_usage:
        add("ios_usage_strings", "P3", "iOS usage descriptions declared: " + ", ".join(sorted(ios_usage)) + ". Confirm texts explain the real purpose.", ["4.4"])
    if mobile:
        add("store_labels", "P1", "Mobile app: store privacy labels (Apple App Privacy / Google Data safety) must list every SDK found above.", ["4.2"])
    if not (page_found(pages, "imprint_contact")):
        add("no_contact_info", "P2", "No contact / imprint page or link found (business identity is required for commercial sites).", ["2.1"])
    return flags


def to_markdown(r: dict) -> str:
    out = []
    out.append(f"# Detector output: `{Path(r['root']).name}`\n")
    out.append(f"Files scanned: {r['files_scanned']} · Platforms: {', '.join(r['platforms']) or 'unknown'} · iOS privacy manifest: {'yes' if r['ios_privacy_manifest'] else 'no'}\n")
    out.append("> Heuristic signals. Open each file to confirm before reporting. Not legal advice.\n")

    out.append("## What the project seems to be (confirm with the user)\n")
    if r["project_summary"]:
        for item in r["project_summary"][:10]:
            out.append(f"- `{item['source']}` {item['field']}: {item['value']}")
    else:
        out.append("- No name/description found. Ask the user what the product does.")
    if r["sector_hints"]:
        out.append("\nSector hints (keyword matches, may be false positives):")
        for sec, d in list(r["sector_hints"].items())[:6]:
            ev = ", ".join(f"`{e['file']}:{e['line']}`" for e in d["evidence"])
            out.append(f"- **{sec}** ({d['count']} hits): {ev}")
    out.append("")

    out.append("## Review flags\n")
    if r["derived_flags"]:
        out.append("| Priority | Flag | Matrix rows |\n|---|---|---|")
        for f in sorted(r["derived_flags"], key=lambda x: x["suggested_priority"]):
            out.append(f"| {f['suggested_priority']} | {f['text']} | {', '.join(f['matrix_rows'])} |")
    else:
        out.append("No flags.")
    out.append("")

    out.append("## Signals\n")
    if r["signals"]:
        by_cat: dict[str, list] = {}
        for sid, s in r["signals"].items():
            by_cat.setdefault(s["category"], []).append((sid, s))
        for cat in sorted(by_cat):
            out.append(f"### {cat}\n")
            for sid, s in by_cat[cat]:
                out.append(f"- **{s['label']}** ({s['count']} hits)")
                for e in s["evidence"]:
                    out.append(f"  - `{e['file']}:{e['line']}` — `{e['text'].replace('`', '´')}`")
            out.append("")
    else:
        out.append("No signals found.\n")

    out.append("## Legal pages / links\n")
    out.append("| Page | Found | Evidence |\n|---|---|---|")
    for key, p in r["legal_pages"].items():
        ev = [f"`{f}`" for f in p["files"][:3]] + [f"`{m['file']}:{m['line']}`" for m in p["mentions"][:3]]
        found = "yes" if ev else "no"
        out.append(f"| {p['label']} | {found} | {'<br>'.join(ev) if ev else '—'} |")
    out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Scan a project for legally relevant signals (read-only).")
    ap.add_argument("root", nargs="?", default=".", help="project root folder")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--max-hits", type=int, default=5, help="evidence lines kept per signal")
    ap.add_argument("--fail-on", choices=["P0", "P1", "P2", "P3"], default=None,
                    help="exit with code 1 if any review flag has this priority or higher (for CI)")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    result = scan(root, max(1, args.max_hits))
    if args.format == "json":
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(to_markdown(result))
    if args.fail_on:
        hits = [f for f in result["derived_flags"] if f["suggested_priority"] <= args.fail_on]
        if hits:
            print(f"\nlegal-launch-kit: {len(hits)} flag(s) at {args.fail_on} or higher: "
                  + ", ".join(f["id"] for f in hits), file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

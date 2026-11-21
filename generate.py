#!/usr/bin/env python3
"""Draw a dense front-page image summing up the world news of Saturday 21 November 2026.

Layout: newspaper masthead, a one-line strap of the day's biggest threads, then
seven region boxes (North America, Latin America, Europe, Middle East, Africa,
Asia-Pacific, Global & Science) with five dated stories each, and a markets strip.
Output: entry.png (1024x1024) beside this file. Python 3 + Pillow only.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W = H = 1024
PAPER = (250, 247, 240)
INK = (18, 16, 14)
MUTED = (70, 66, 60)
RULE = (30, 28, 26)

REGIONS = [
    ("NORTH AMERICA", [
        ("AI sell-off pushes S&P 500 into correction",
         "Chip and AI shares routed worldwide; the S&P 500 fell 3.7% and Japan's Nikkei 5.1%."),
        ("FBI probes breach of national crime database",
         "Hackers reportedly entered the NCIC law-enforcement database and a USDA payment system."),
        ("Man convicted of starting deadly Palisades fire",
         "A Los Angeles jury finds the arsonist guilty over the deadly blaze."),
        ("Trump orders contractors to flag Congress requests",
         "An executive order tells federal contractors to notify the White House of congressional inquiries."),
        ("Judge again blocks Trump's 250-foot triumphal arch",
         "A second federal judge halts construction near Arlington National Cemetery."),
    ]),
    ("LATIN AMERICA", [
        ("Mexico captures cartel boss 'El Chapo Isidro'",
         "The Los Mazatlecos leader was seized in Sinaloa in a joint US-Mexico operation."),
        ("Bolsonaro hospitalized with intestinal obstruction",
         "The jailed ex-president, 71, was taken from house arrest in Brasilia and treated without surgery."),
        ("Magnitude 6.7 earthquake shakes central Peru",
         "A strong quake struck the Jun\u00edn region of Peru."),
        ("Salvadoran troops battle gangs in Haiti",
         "Salvadoran forces fighting gangs in Port-au-Prince lose soldiers."),
        ("Storm destroys thousands of homes in southern Brazil",
         "A severe storm tore roofs off homes in Tupanciret\u00e3, killing at least three people."),
    ]),
    ("EUROPE", [
        ("Russia fires 400+ drones, 110 missiles at Ukraine",
         "At least eight killed in Kyiv; bridges and energy sites hit, power cut in ten regions."),
        ("Russian missiles and drone land in Poland",
         "NATO calls it a grave violation of Polish airspace; Warsaw says a deliberate provocation."),
        ("UK and EU sign three post-Brexit agreements",
         "PM Burnham seals a Brussels reset deal on trade, energy and youth mobility."),
        ("Denmark expels Russian diplomat over rapper plot",
         "Copenhagen arrests two men over an alleged plot to kill US-Ukrainian rapper Kyivstoner."),
        ("EU disburses \u20ac7.9 billion to Ukraine",
         "The largest Ukraine Facility payment yet takes EU support to \u20ac40 billion since mid-2024."),
    ]),
    ("MIDDLE EAST", [
        ("Tankers hit near Hormuz as US-Iran talks stall",
         "Projectiles strike outbound tankers near Oman; no casualties were reported."),
        ("Houthis fire missiles at Riyadh",
         "Saudi Arabia says it intercepted three Houthi missiles targeting the capital."),
        ("Israeli fire kills Palestinians in Gaza",
         "Deaths were reported in Gaza amid rising tensions in the West Bank."),
        ("Trump weighs new strikes on Iran, officials say",
         "Washington considers another round of extensive strikes as Israel presses for action."),
        ("Fire at Basra power station kills four",
         "A blaze at an Iraqi power station leaves four people dead."),
    ]),
    ("AFRICA", [
        ("Phumzile Mlambo-Ngcuka dies aged 71",
         "South Africa's first woman deputy president and former UN Women chief is mourned."),
        ("WHO keeps Congo Ebola outbreak a global emergency",
         "Cases reach 11,613 with 5,678 deaths; children under five die at seven in ten."),
        ("Morocco commits \u20ac366m to defence industry",
         "Rabat funds a national defence industry programme to be built by 2035."),
        ("Uganda restricts gatherings and travel over Ebola",
         "Kampala tightens measures to contain the outbreak."),
        ("Kenya begins onshore crude drilling in Turkana",
         "Kenya starts drilling for oil in the Turkana basin."),
    ]),
    ("ASIA-PACIFIC", [
        ("Trump, Xi and Putin hold trilateral summit in Shenzhen",
         "The first three-way summit on the APEC sidelines; leaders adopt the Shenzhen Outlook."),
        ("Japan core inflation rises to 2.2% in October",
         "Price growth edges up as the Nikkei tumbles 5.1% in the AI sell-off."),
        ("Pilotless air taxi carries a passenger in Japan",
         "An autonomous electric air taxi completes a passenger flight in Yamanashi."),
        ("UN court finds Myanmar responsible for Rohingya genocide",
         "Rohingya in Bangladesh welcome the verdict but say they want to go home."),
        ("Honda and Toyota recall 1.6 million vehicles",
         "The recall was issued over Takata airbag rupture risk."),
    ]),
    ("GLOBAL & SCIENCE", [
        ("COP31 climate talks run past deadline over fossil fuels",
         "The Antalya summit passes its Friday deadline without a deal on phase-out and finance."),
        ("128 countries move toward 'killer robot' rules",
         "Geneva delegates agree to keep working on lethal autonomous weapons rules to 2028."),
        ("Pill shows major progress against pancreatic cancer",
         "Daraxonrasib made cancer undetectable in one in 12 patients in a trial."),
        ("BepiColombo reaches Mercury orbit after eight years",
         "The ESA-JAXA probe arrives at Mercury."),
        ("GTA VI earns $3.8 billion on its first day",
         "Rockstar's launch smashes entertainment records."),
    ]),
]

MARKETS = ("MARKETS  S&P 500 6,910 \u25bc3.7%   Nikkei \u25bc5.1%   Gold \u25bc4.6%   "
           "Bitcoin ~$57,850   Brent $89.95 \u25b20.6%   FTSE 100 10,346 \u25bc1.0%")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_story(draw, x, y, w, headline, summary, fh, fs):
    """Draw one story; return the y just below it."""
    for line in wrap(draw, headline, fh, w):
        draw.text((x, y), line, font=fh, fill=INK)
        y += 15
    for line in wrap(draw, summary, fs, w):
        draw.text((x, y), line, font=fs, fill=MUTED)
        y += 14
    return y + 7


def draw_region(draw, x, y, w, name, stories, fh, fs, fhead):
    draw.rectangle([x, y, x + w, y + 21], fill=INK)
    draw.text((x + 7, y + 4), name, font=fhead, fill=PAPER)
    y += 27
    for headline, summary in stories:
        y = draw_story(draw, x + 2, y, w - 4, headline, summary, fh, fs)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_mast = font(SERIF_BOLD, 46)
    f_date = font(SANS_BOLD, 15)
    f_strap = font(SERIF, 14)
    f_head = font(SANS_BOLD, 12)
    f_hl = font(SERIF_BOLD, 13)
    f_sum = font(SANS, 10)
    f_mkt = font(SANS_BOLD, 11)

    margin = 16
    # Masthead
    d.line([(margin, 12), (W - margin, 12)], fill=RULE, width=3)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 18), title, font=f_mast, fill=INK)
    dateline = "SATURDAY 21 NOVEMBER 2026  \u00b7  35 STORIES  \u00b7  7 REGIONS"
    dw = d.textlength(dateline, font=f_date)
    d.text(((W - dw) / 2, 72), dateline, font=f_date, fill=INK)
    d.line([(margin, 96), (W - margin, 96)], fill=RULE, width=1)
    strap = ("Stocks slide worldwide \u00b7 Russia strikes Ukraine, missiles land in Poland "
             "\u00b7 Tankers hit near Hormuz \u00b7 COP31 deadlocked")
    sw = d.textlength(strap, font=f_strap)
    d.text(((W - sw) / 2, 102), strap, font=f_strap, fill=MUTED)
    d.line([(margin, 124), (W - margin, 124)], fill=RULE, width=2)

    # Region grid: 3 columns, two rows of three, then Global full width in 2 sub-columns
    gutter = 12
    col_w = (W - 2 * margin - 2 * gutter) // 3
    xs = [margin + i * (col_w + gutter) for i in range(3)]
    y = 132
    row1 = [REGIONS[0], REGIONS[2], REGIONS[3]]      # N. America, Europe, Middle East
    row2 = [REGIONS[1], REGIONS[4], REGIONS[5]]      # Latin America, Africa, Asia-Pacific
    bottoms = []
    for i, (name, stories) in enumerate(row1):
        bottoms.append(draw_region(d, xs[i], y, col_w, name, stories, f_hl, f_sum, f_head))
    y = max(bottoms) + 6
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=1)
    y += 8
    bottoms = []
    for i, (name, stories) in enumerate(row2):
        bottoms.append(draw_region(d, xs[i], y, col_w, name, stories, f_hl, f_sum, f_head))
    y = max(bottoms) + 6
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=1)
    y += 8

    # Global & Science, full width, two sub-columns (3 + 2)
    name, stories = REGIONS[6]
    full_w = W - 2 * margin
    d.rectangle([margin, y, margin + full_w, y + 21], fill=INK)
    d.text((margin + 7, y + 4), name, font=f_head, fill=PAPER)
    y += 27
    sub_w = (full_w - gutter) // 2
    y_left = y
    for headline, summary in stories[:3]:
        y_left = draw_story(d, margin + 2, y_left, sub_w - 4, headline, summary, f_hl, f_sum)
    y_right = y
    for headline, summary in stories[3:]:
        y_right = draw_story(d, margin + sub_w + gutter + 2, y_right, sub_w - 4,
                             headline, summary, f_hl, f_sum)
    y = max(y_left, y_right) + 4

    # Markets strip + footer
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=2)
    y += 7
    mw = d.textlength(MARKETS, font=f_mkt)
    d.text(((W - mw) / 2, y), MARKETS, font=f_mkt, fill=INK)
    y += 20
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=1)
    y += 5
    foot = "All stories happened or were first reported on 21 November 2026."
    fw = d.textlength(foot, font=font(SANS, 10))
    d.text(((W - fw) / 2, y), foot, font=font(SANS, 10), fill=MUTED)
    y += 16

    out = HERE / "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} size={out.stat().st_size} bytes, content ends at y={y}")


if __name__ == "__main__":
    main()

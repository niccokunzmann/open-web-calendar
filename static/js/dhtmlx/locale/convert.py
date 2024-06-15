# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only
"""Script to convert the DHTMLX calendar translations for yaml files."""

import os
import re

regex = re.compile(r"\{[^{]*(\{.*\})\}", re.DOTALL | re.MULTILINE)

date = "date"
month_full = "month_full:"

en = {}

M = "jan feb mar apr may jun jul aug sep oct nov dec".split()
D = "sun mon tue wed thu fri sat".split()


def used(s):
    return (
        s.startswith("date_")
        or (
            s.startswith("labels_")
            and not any(
                x in s
                for x in "repeat drag message button icon new confirm section "
                "select recurring labels_year_tab labels_grid_tab"
                "labels_full_day".split()
            )
        )
        or s
        in """
    labels_dhx_cal_today_button
    """
    )


def add(l, v):  # noqa: E741
    global yaml  # noqa: PLW0603
    k = "_".join(l)
    # sanitize
    #    v = v.strip()
    assert '"' not in v
    v = '"' + v.replace("=", ":") + '"'
    if v == "":
        v = '""'
    # check translated
    if lang == "en":
        en[k] = v
    elif en.get(k) == v:
        print(f"skip {k} is english: {v}")
        return
    if not used(k):
        #        print(f"Not used {k}")
        yaml += "#: not used in this project\n"
    yaml += f"{k}: {v}\n"


for file in ["locale_en.js"] + os.listdir("."):
    if not file.endswith(".js"):
        continue
    lang = file[file.index("_") + 1 : file.index(".")]
    print(f" ----- {lang} ----- ")
    with open(file) as f:
        r = regex.findall(f.read())
    assert len(r) == 1, r
    r = r[0].replace("{", "dict(").replace("}", ")").replace(":", "=")
    r = eval(r)
    print(list(r))
    print(r)
    yaml = ""
    for x in ["month_full", "month_short"]:
        for k, v in zip(M, r["date"][x]):
            add(["date", x, k], v)
    for x in ["day_full", "day_short"]:
        for k, v in zip(D, r["date"][x]):
            if x == "day_full" and lang == "el" and k == "sat" and v == "Κυριακή":
                # https://github.com/niccokunzmann/open-web-calendar/commit/670b6a7587a3b6bc730301bf288b31afb760d419
                v = "Σάββατο"
            add(["date", x, k], v)
    for k, v in r["labels"].items():
        if not isinstance(v, str):
            assert k in ["month_for_recurring", "day_for_recurring"], v  # checked below
            continue
        add(["labels", k], v)
    if "month_for_recurring" in r["labels"]:
        for k, v in zip(M, r["labels"]["month_for_recurring"]):
            add(["labels", "month_for_recurring", k], v)
    if "day_for_recurring" in r["labels"]:
        for k, v in zip(D, r["labels"]["day_for_recurring"]):
            add(["labels", "day_for_recurring", k], v)
    print(yaml)
    directory = "../../../../translations/" + lang
    os.makedirs(directory, exist_ok=True)
    with open(directory + "/calendar.yml", "w") as f:
        f.write(yaml)

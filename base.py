import requests
import json

BASE = "https://www.gosuslugi.ru"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
})

student_id=1280590 

def get_applicants(competition_id: int):
    url = f"{BASE}/api/university-applicant-list/v1/public/2026/competition/{competition_id}/applicants"
    r = session.get(url)
    r.raise_for_status()
    return r.json()

def parse_applicant(a):
    return {
        "rating": a.get("rating"),
        "score": a.get("sumMark"),
        "priority": a.get("priority"),
        "status": a.get("statusName"),
        "id": a.get("idApplication"),
    }

def get_all_applicants(competition_ids):
    result = {}

    for cid in competition_ids:
        print(f"Загружаю competition {cid}...")

        try:
            data = get_applicants(cid)
            result[cid] = data.get("applicants", [])

            print(f"  → {len(result[cid])} абитуриентов")

        except Exception as e:
            print(f"  ❌ ошибка {cid}: {e}")

    return result


if True:
    competition_ids = [106611, 106610, 106614, 106612]

    data = get_all_applicants(competition_ids)
    total = sum(len(v) for v in data.values())

    for cid, apps in data.items():

        for a in apps:
            p = parse_applicant(a)

            if p["id"] == student_id:
                print("\nCompetition:", cid)
                print(*list(p.values()))
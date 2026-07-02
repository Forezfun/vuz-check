import requests
import browser_cookie3


STUDENT_ID = 1280590
ORGANIZATION_IDS = [2264,113,1858,20]

BASE_URL = "https://www.gosuslugi.ru"


cookies = browser_cookie3.firefox(domain_name="gosuslugi.ru")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
})
session.cookies.update(cookies)


def get_applicants(competition_id: int) -> dict:
    url = (
        f"{BASE_URL}/api/university-applicant-list/v1/public/2026/"
        f"competition/{competition_id}/applicants"
    )

    response = session.get(url)
    response.raise_for_status()

    return response.json()


def get_all_applicants(competition_ids: list[int]) -> dict:
    applicants_by_competition = {}

    for competition_id in competition_ids:
        try:
            response_data = get_applicants(competition_id)

            applicants_by_competition[competition_id] = (
                response_data.get("applicants", [])
            )

        except Exception as error:
            print(f"❌ Ошибка {competition_id}: {error}")

    return applicants_by_competition


def get_student_competitions(student_id: int) -> list[int]:
    url = (
        f"{BASE_URL}/api/university-applicant-list/v1/"
        f"competition/statuses/applicant-lists-statistics"
        f"?entrantId={student_id}&listType=applicant-list"
    )

    response = session.get(url)
    response.raise_for_status()

    statistics = response.json()

    return [int(item["groupId"]) for item in statistics]


def get_program_info(
    organization_id: int,
    competition_ids: list[int]
) -> dict:

    url = (
        f"{BASE_URL}/api/vuz-navigator/public/v1/2026/"
        f"educational-programs/items"
    )

    payload = {
        "orgId": organization_id,
        "competitionIds": competition_ids
    }

    response = session.post(url, json=payload)
    response.raise_for_status()

    programs = {}

    for program in response.json():

        program_name = None

        if program.get("programs"):
            program_name = program["programs"][0]["name"]

        # print(program)
        type_cost=None 
        place_type_id = program.get("placeTypeId")
        if place_type_id == 1:type_cost='Бюджет'
        if place_type_id == 2:type_cost='Целевое'
        if place_type_id == 3:type_cost='Платное'
        programs[program["id"]] = {
            "university": program.get("humanReadableTitle"),
            "program": program_name,
            "type_cost":type_cost,
            "education_form": program.get("educationFormName"),
            "places": program.get("numberPlaces"),
            "organization_id": program.get("organizationId")
        }

    return programs


def parse_applicant(applicant: dict) -> dict:
    return {
        "rating": applicant.get("rating"),
        "score": int(applicant.get("sumMark")),
        "priority": applicant.get("priority"),
        "status": applicant.get("statusName"),
        "application_id": applicant.get("idApplication"),
    }


def get_admission_indicator(
    rating: int,
    places: int
) -> str:

    if not rating or not places:
        return "⚪"

    if rating <= places * 0.9:
        return "🟢"

    if rating <= places:
        return "🟡"

    return "🔴"


competition_ids = get_student_competitions(STUDENT_ID)

applicants_data = get_all_applicants(competition_ids)

for competition_id, applicants in applicants_data.items():

    program_info = {}

    for organization_id in ORGANIZATION_IDS:
        try:
            program_info = get_program_info(
                organization_id=organization_id,
                competition_ids=[competition_id]
            )

            if competition_id in program_info:
                break

        except Exception:
            pass

    competition_info = program_info.get(competition_id, {})

    for applicant in applicants:

        applicant_info = parse_applicant(applicant)

        if applicant_info["application_id"] != STUDENT_ID:
            continue

        places = competition_info.get("places") or 0
        rating = applicant_info["rating"]

        indicator = get_admission_indicator(
            rating=rating,
            places=places
        )
        print("\n======================")
        print("ВУЗ:", competition_info.get("university"))
        print("Программа:", competition_info.get("program"))
        print("Форма:", competition_info.get("education_form"))
        print("Тип обучения по цене:",competition_info.get("type_cost"))
        print("Мест:", places)
        print("Подано заявлений:",len(applicants))
        print()
        print(f"{indicator} Вероятность поступления")
        print()
        print(
            f"Место: {applicant_info['rating']} | "
            f"Баллы: {applicant_info['score']} | "
            f"Приоритет: {applicant_info['priority']} | "
            f"Статус: {applicant_info['status']}"
        )
        print("----------------------")

        break
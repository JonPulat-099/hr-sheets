from sheets.models import Config, Candidate, Vacancy, Organization
from .get_all_sheets_value import get_all
import re


def extract_org_code(org_string):
    match = re.search(r"\[([a-zA-Z0-9_-]+)\]", org_string)
    if match:
        return match.group(1)
    return None


def save_data():
    vacancies, canditates = get_all()

    # write vacancies
    for vacancy in vacancies:
        org_code = extract_org_code(vacancy[0])
        # print('org_code -> ', org_code)
        if org_code:
            org = Organization.objects.get(org_code=org_code)
            # print('org -> ', org.name, '  vacancy -> ', vacancy[1])
            Vacancy.objects.update_or_create(
                organization=org,
                title=vacancy[1],
                description=vacancy[2],
                salary=vacancy[3],
                count=vacancy[4],
            )

    # write candidates
    for candidate in canditates:
        org_code = extract_org_code(candidate[7])
        # print('org_code -> ', org_code)
        
        if org_code:
            org = Organization.objects.get(org_code=org_code)
            vacancy = Vacancy.objects.get(organization=org, title=candidate[6])
            # print('org -> ', org.name, '  vacancy -> ', vacancy.title)

            if org and vacancy:
                gender = extract_org_code(candidate[2])
                country = extract_org_code(candidate[3])

                Candidate.objects.update_or_create(
                    vacancy=vacancy,
                    full_name=candidate[0],
                    email=candidate[1],
                    gender=gender,
                    country=country,
                    salary=candidate[4],
                    state=candidate[5],
                )

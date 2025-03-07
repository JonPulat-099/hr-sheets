from sheets.models import Application, Config, Candidate, Country, Vacancy, Organization, VacancyCategory
from .get_all_sheets_value import get_all_organization_sheets
import re
from django.core.exceptions import ObjectDoesNotExist
import uuid

def extract_org_code(org_string):
    match = re.search(r"\[([a-zA-Z0-9_-]+)\]", org_string)
    if match:
        return match.group(1)
    return None


def save_data():
    try:
        vacancies, canditates, employees = get_all_organization_sheets()

        # write vacancies
        for vacancy in vacancies:
            try:
                org_code = extract_org_code(vacancy[0])
                #print('org_code -> ', org_code)
                if org_code:
                    org = Organization.objects.get(org_code=org_code)
                    category, created = VacancyCategory.objects.get_or_create(name=vacancy[2] or str(uuid.uuid4())[:15], organization=org)

                    is_top = False
                    if len(vacancy) > 6:
                        is_top = vacancy[6] == "Да"
                        
                    if category:
                        #print('org -> ', org.name, '  vacancy -> ', vacancy[1])
                        Vacancy.objects.update_or_create(
                            organization=org,
                            title=vacancy[1],
                            category=category,
                            salary=vacancy[4],
                            count=vacancy[5],
                            is_top=is_top,
                            description=vacancy[3]
                        )
            except Exception as e:
                print('[ERROR]', e)
                pass

        # write candidates
        for candidate in canditates:
            try:
                org_code = extract_org_code(candidate[7])
                # print('org_code -> ', org_code)

                if org_code:
                    org = Organization.objects.get(org_code=org_code)
                    vacancy = Vacancy.objects.filter(organization=org, title=candidate[6]).first()
                    # print('org -> ', org.name, '  vacancy -> ', vacancy.title)

                    if org and vacancy:
                        gender = extract_org_code(candidate[2])
                        try:
                            country = Country.objects.get(iso_code=extract_org_code(candidate[3]))
                        except ObjectDoesNotExist:
                            #print('Country not found')
                            pass
                        state = extract_org_code(candidate[5])

                        cand, created = Candidate.objects.update_or_create(
                            full_name=candidate[0],
                            email=candidate[1],
                            gender=gender,
                            country=country,
                        )
                        #print(cand)

                        Application.objects.update_or_create(
                            candidate=cand,
                            vacancy=vacancy,
                            organization=org,
                            salary=candidate[4],
                            state=state
                        )

            except Exception as e:
                print('[ERROR]', e)
                pass
        

        for stat in employees:
            try:
                org_code = extract_org_code(stat[0])
                Organization.objects.filter(org_code=org_code).update(
                    employees=stat[1] or 0,
                    male_employees=stat[2] or 0,
                    female_employees=stat[3] or 0,
                    expatriates=stat[4] or 0
                )
            except Exception as e:
                print('[ERROR]', e)
                pass
            
    except Exception as e:
        print('[ERROR]', e)

from django.db import IntegrityError
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from .models import Vacancy, Organization, Candidate, Application, VacancyCategory
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.db import connection

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def custom_404_view(request, exception):
    return redirect("/admin/")


class GetVacancy(View):
    def get(self, request):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        data = {
            "type": "service_account",
            "project_id": "python-sheets-448719",
            "private_key_id": "daeb1a231ea1f327de871e1cef584e5365a3cd9b",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/4vLUkpJ5Bmxy\n7vKE5/JedSSZz1vxRX7Qk/CVA3gN8t24Z/MHuovoj5JZxbSmY8n+um8dLYTPXw2e\nRXjal+qhepRlGSdA21Jn0TfwXWILnn317mnRmtkDtCeerGbUN+CkIz7oOP5gyuLj\nYBtf3yZzolvxOB2XhezyOfq9q85Em/dk+3AmRaBUaT9AVtdluimjhg6b6SNDaQO/\nTzhL45+3qzICad5wF03ZZfJqodS+DlsR7WDocuNjbqxo7rOKt+ycfZIoSMFmPEqX\ncyZl/GCDrGFC2I9KxnHJ9AAAzU7bQcczRwOAIrwN8C1TPkvQzCFycqJRs/oHNAZn\nqEVRPUitAgMBAAECggEALWcC24LZ1vqK3xAEQKfMHIb9s8oRYG9339zdVDjnp29D\ngI5R/g5o68xKzeR+h889PIE66M28Kr/8LiqUe65t5SrmoVw4AjvSzf8+S+igmgy0\nk6QHlEGeHyb5p+z1gLm+9L9lM1fG8rqWwEOdfowDomE0fYkwUUmuRKss1cOo0Oko\nlp7KO6JJxt7hwNlarTDDbwoZfs0LD3OW2bXvXHOq9GK0JODvI3dU+WMVevtsQJh9\n1FxlmARDWEaqRn9HMhbcGBNepaqW6jlGTjFqe+XzK1GXxB8IqwDuoPeXV5PKZfFh\nRK8bKrZ7idkpq7FSUz871vLha+Rxi4SE1MpIZf4rEQKBgQDf7K07GdtYa/TwRmR0\nWhoZzw/DI7mqIow7knpx85jaF/3VAwEiObeU1WIo45n7dyym/v8XCk+qF1uNpg6O\ncUVe5dlz4DZT4HjSVS3/co2wOWUxpRHWMb2OjalOYX0t4T8eFM/9SOzq2rJg9GNZ\nXo6TBj+PjUXmdg+JAoKfW031UQKBgQDbX2/RVfQxpKILYouyXbJArMUZgszQW4lv\nia1FluOt51TmTijbkqFnjpTlDQf8NaFCBCB2znXpP7Fck4bsXU+I+wadfZX/pGBS\nGmW6yIS7KCdligsKXuUPoTUQ7xPwCDDsZm8A3qhuM/XZEXtsAjnwf875NxhVi6s0\njGY5WRL2nQKBgQCiptQd/eYqECDW9wq4yUn0PUeBw011m6qpCvkOFJeOs6aZN5l3\nNt12qpimgsyysBorI0Y/ginjrxu9hEVGiliNWf/d/5r2yjJ49Y534smwm8A5k2Gl\naHP8PEIiwQWgceDbBNsfa/1LipfPfTU9EUYW3Y8FwuRnRpJ6PuyKvFOgQQKBgQCC\nqmn0CnqVRzauCVikOWL/WulbtKlCQgOuyBbJKIMdBnlvZIa5orE4+Zh+hjCHbXpL\n1CFyIq/g6us99TGcgEfrk3nxPOiniMVGoiqOAvnscJJmzL6ewr81fBQbrgv2ISri\n5HCh1/4DBjgdv2gAgaL5OWeS0dpQugyUFDyfVAsTkQKBgH1xggNBF8pWNsSA2ggO\nOBs79wMvSg37yH6p9rcA/TG+tp437opAnchgRw5qOqrR2mTR8jlz5GbnoG6qcX0m\nWXxWGefl8ynnQ8FS+IVdaUI9Ft9jc/F+WcXjNp0j/luwb5VpxqkAO1GrQGEEyq5M\nLmq4V/ogNBoknV27ZoGOfgSm\n-----END PRIVATE KEY-----\n",
            "client_email": "jonpulat@python-sheets-448719.iam.gserviceaccount.com",
            "client_id": "105715684605356850987",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jonpulat%40python-sheets-448719.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com",
        }

        creds = ServiceAccountCredentials.from_json_keyfile_dict(data, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(
            "1AvALes5XGB8ZtOcJwAgLM3kkUj3Ki0oMh5tCq01kJA8"
        ).worksheets()
        print(123, "-> ", sheet)
        for sh in sheet:
            rows = sh.get_all_values()

            for row in rows[1:]:
                try:
                    # TODO: Handle this error, when organization category not exists
                    org = Organization.objects.get(org_code=row[3])
                    Vacancy.objects.create(
                        organization=org,
                        title=row[1],
                        description=row[4],
                        salary=str(row[2]).replace(" ", ""),
                        created_at=timezone.now(),
                    )
                except IntegrityError:
                    # TODO: Handle this error, when organization not exists
                    pass
        return redirect(request.META["HTTP_REFERER"])


class GetCandidate(View):
    def get(self, request):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        data = {
            "type": "service_account",
            "project_id": "python-sheets-448719",
            "private_key_id": "daeb1a231ea1f327de871e1cef584e5365a3cd9b",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/4vLUkpJ5Bmxy\n7vKE5/JedSSZz1vxRX7Qk/CVA3gN8t24Z/MHuovoj5JZxbSmY8n+um8dLYTPXw2e\nRXjal+qhepRlGSdA21Jn0TfwXWILnn317mnRmtkDtCeerGbUN+CkIz7oOP5gyuLj\nYBtf3yZzolvxOB2XhezyOfq9q85Em/dk+3AmRaBUaT9AVtdluimjhg6b6SNDaQO/\nTzhL45+3qzICad5wF03ZZfJqodS+DlsR7WDocuNjbqxo7rOKt+ycfZIoSMFmPEqX\ncyZl/GCDrGFC2I9KxnHJ9AAAzU7bQcczRwOAIrwN8C1TPkvQzCFycqJRs/oHNAZn\nqEVRPUitAgMBAAECggEALWcC24LZ1vqK3xAEQKfMHIb9s8oRYG9339zdVDjnp29D\ngI5R/g5o68xKzeR+h889PIE66M28Kr/8LiqUe65t5SrmoVw4AjvSzf8+S+igmgy0\nk6QHlEGeHyb5p+z1gLm+9L9lM1fG8rqWwEOdfowDomE0fYkwUUmuRKss1cOo0Oko\nlp7KO6JJxt7hwNlarTDDbwoZfs0LD3OW2bXvXHOq9GK0JODvI3dU+WMVevtsQJh9\n1FxlmARDWEaqRn9HMhbcGBNepaqW6jlGTjFqe+XzK1GXxB8IqwDuoPeXV5PKZfFh\nRK8bKrZ7idkpq7FSUz871vLha+Rxi4SE1MpIZf4rEQKBgQDf7K07GdtYa/TwRmR0\nWhoZzw/DI7mqIow7knpx85jaF/3VAwEiObeU1WIo45n7dyym/v8XCk+qF1uNpg6O\ncUVe5dlz4DZT4HjSVS3/co2wOWUxpRHWMb2OjalOYX0t4T8eFM/9SOzq2rJg9GNZ\nXo6TBj+PjUXmdg+JAoKfW031UQKBgQDbX2/RVfQxpKILYouyXbJArMUZgszQW4lv\nia1FluOt51TmTijbkqFnjpTlDQf8NaFCBCB2znXpP7Fck4bsXU+I+wadfZX/pGBS\nGmW6yIS7KCdligsKXuUPoTUQ7xPwCDDsZm8A3qhuM/XZEXtsAjnwf875NxhVi6s0\njGY5WRL2nQKBgQCiptQd/eYqECDW9wq4yUn0PUeBw011m6qpCvkOFJeOs6aZN5l3\nNt12qpimgsyysBorI0Y/ginjrxu9hEVGiliNWf/d/5r2yjJ49Y534smwm8A5k2Gl\naHP8PEIiwQWgceDbBNsfa/1LipfPfTU9EUYW3Y8FwuRnRpJ6PuyKvFOgQQKBgQCC\nqmn0CnqVRzauCVikOWL/WulbtKlCQgOuyBbJKIMdBnlvZIa5orE4+Zh+hjCHbXpL\n1CFyIq/g6us99TGcgEfrk3nxPOiniMVGoiqOAvnscJJmzL6ewr81fBQbrgv2ISri\n5HCh1/4DBjgdv2gAgaL5OWeS0dpQugyUFDyfVAsTkQKBgH1xggNBF8pWNsSA2ggO\nOBs79wMvSg37yH6p9rcA/TG+tp437opAnchgRw5qOqrR2mTR8jlz5GbnoG6qcX0m\nWXxWGefl8ynnQ8FS+IVdaUI9Ft9jc/F+WcXjNp0j/luwb5VpxqkAO1GrQGEEyq5M\nLmq4V/ogNBoknV27ZoGOfgSm\n-----END PRIVATE KEY-----\n",
            "client_email": "jonpulat@python-sheets-448719.iam.gserviceaccount.com",
            "client_id": "105715684605356850987",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jonpulat%40python-sheets-448719.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com",
        }

        creds = ServiceAccountCredentials.from_json_keyfile_dict(data, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(
            "1TaGUjcaf4I5lKVpWgGxC0XxQhfgI9nYgx0sDjoM5zak"
        ).worksheets()

        print(123, "-> ", sheet)
        for sh in sheet:
            rows = sh.get_all_values()

            for row in rows[1:]:
                try:
                    # TODO: Handle this error, when organization category not exists
                    vacan = Vacancy.objects.get(title=row[3])
                    Candidate.objects.create(
                        vacancy=vacan,
                        email=row[1],
                        full_name=row[2],
                        country=row[5],
                        salary=str(row[4]).replace(" ", ""),
                        created_at=timezone.now(),
                    )
                except Vacancy.DoesNotExist:
                    print(row)
                    pass
                except IntegrityError:
                    # TODO: Handle this error, when organization not exists
                    pass
        return redirect(request.META["HTTP_REFERER"])


def mainStats(request):
    try:
        query = """
            SELECT 
                o.country_id AS iso_code, 
                c.name_ru, 
                c.flag,
                COUNT(o.country_id) AS count
            FROM sheets_candidate o
            LEFT JOIN sheets_country c ON o.country_id = c.iso_code
            GROUP BY o.country_id, c.name_ru, c.flag;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]  # Get column names
            countries = [dict(zip(columns, row)) for row in cursor.fetchall()]
            countries = list(
                map(
                    lambda country: {**country, "flag": "/media/" + country["flag"]},
                    countries,
                )
            )

        total_vacancy = Vacancy.objects.aggregate(Sum("count"))["count__sum"] or 0
        total_applications = Application.objects.count() or 0
        organizations = (
            Organization.objects.annotate(count=Sum("vacancy__count"))
            .annotate(candidate=Count("application"))
            .values("count", "name", "logo", "org_code", "candidate")
        )

        data = {
            "total_competition": (
                0 if total_vacancy == 0 else total_applications / total_vacancy
            ),
            "total_vacancy": total_vacancy,
            "total_candidate": total_applications,
            "total_new_position": total_vacancy,
            "totla_country": countries,
            "organizations": list(
                map(
                    lambda org: {
                        "name": org["name"],
                        "org_code": org["org_code"],
                        "competition": (
                            0
                            if org["count"] == None
                            else round(org["candidate"] / org["count"], 1)
                        ),
                        "logo": "" if org["logo"] == "" else "/media/" + org["logo"],
                    },
                    organizations,
                )
            ),
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse(
            {"error": f"An unexpected error occurred: {str(e)}"}, status=500
        )


def orgStats(request, org_code):
    try:
        org = Organization.objects.get(org_code=org_code)
        vacancies = Vacancy.objects.filter(organization=org)
        applications = Application.objects.filter(organization=org)

        total_vacancies = vacancies.aggregate(Sum("count"))["count__sum"] or 0
        total_applications = applications.count()
        byLevel = vacancies.annotate(
            candidate=Count(
                "application",
                filter=~Q(application__state="reject") & ~Q(application__state="hired"),
            )
        ).values(
            "id",
            "title",
            "salary",
            "description",
            "is_top",
            "count",
            "organization__logo",
            "candidate",
            "category__name",
        )

        countries = (
            applications.exclude(candidate__country="uz")
            .values("candidate__country__flag", "candidate__country__name_ru")
            .annotate(application_count=Count("id"))
            .order_by("-application_count")
        )

        data = {
            "name": org.name,
            "orgCode": org_code,
            "logo": org.logo.url if org.logo else "",
            "stats": {
                "averageCompetition": (
                    0
                    if total_vacancies == 0
                    else round(total_applications / total_vacancies, 1)
                ),
                "countInternationals": applications.exclude(
                    candidate__country="uz"
                ).count(),
                "countExpatriates": org.expatriates or 0,
                "totalEmployees": org.employees or 0,
                "genderDistribution": {
                    "male": (
                        0
                        if org.employees == None
                        else round((org.male_employees or 0) / org.employees, 1)
                    ),
                    "female": (
                        0
                        if org.employees == None
                        else round((org.female_employees or 0) / org.employees, 1)
                    ),
                },
            },
            "candidatesByCountry": list(
                map(
                    lambda c: {
                        "name": c["candidate__country__name_ru"],
                        "flag": "/media/" + c["candidate__country__flag"],
                        "candidate": c["application_count"],
                    },
                    countries,
                )
            ),
            "competitionByLevel": list(
                map(
                    lambda item: {
                        "vacancyName": item["title"],
                        "minSalary": item["salary"],
                        "averageCompetitors": (
                            0
                            if item["count"] == None or item["count"] == 0
                            else round(item["candidate"] / item["count"], 1)
                        ),
                        "details": item["description"],
                        "orgCategory": item["category__name"],
                        "orgLogo": org.logo.url if org.logo else "",
                        "candidate": item["candidate"],
                    },
                    byLevel,
                )
            ),
        }

        return JsonResponse(data)
    except Organization.DoesNotExist:
        return JsonResponse(
            {
                "name": "",
                "orgCode": "",
                "logo": "",
                "stats": {},
                "candidatesByCountry": [],
                "competitionByLevel": [],
            }
        )

    except Exception as e:
        # Handle other unexpected errors
        return JsonResponse(
            {"error": f"An unexpected error occurred: {str(e)}"}, status=500
        )


def getCategories(request):
    categories = VacancyCategory.objects.all()[:5]
    payload = []

    for category in categories:
        payload.append(
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "vacancies": list(
                    Vacancy.objects.filter(category=category)
                    .annotate(
                        candidate=Count(
                            "application",
                            filter=~Q(application__state="reject")
                            & ~Q(application__state="hired"),
                        )
                    )
                    .values("title", "candidate")
                ),
            }
        )

    data = {"categories": list(payload)}

    return JsonResponse(data)


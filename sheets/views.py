from django.shortcuts import redirect
from django.views import View
from .models import Vacancy, Organization, Application, VacancyCategory
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.db import connection
from sheets.services.google.save_to_db import save_data


def custom_404_view(request, exception):
    return redirect("/admin/")

class UpdateDatabase(View):
    def get(self, request):
        try:
            save_data()
        except Exception as e:
            pass
            print(e)

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

        topVacancies = (
            Vacancy.objects
            .filter(is_top=True)
            .annotate(
                candidate=Count(
                    "application",
                    filter=~Q(application__state="reject")
                    & ~Q(application__state="hired"),
                )
            )
            .values(
                "id",
                "title",
                "salary",
                "description",
                "organization__logo",
                "candidate",
                "category__name",
            )
        )

        data = {
            "total_competition": (
                0 if total_vacancy == 0 else total_applications / total_vacancy
            ),
            "total_vacancy": total_vacancy,
            "total_candidate": total_applications,
            "total_new_position": total_vacancy,
            "total_country": countries,
            "organizations": list(
                map(
                    lambda org: {
                        "name": org["name"],
                        "href": org["org_code"],
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
            "topVacancies": list(topVacancies)
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
                        "text": "Кандидатов",
                    },
                    countries,
                )
            ),
            "competitionByLevel": list(
                map(
                    lambda item: {
                        "vacancyName": item["title"],
                        "minSalary": round(item["salary"]),
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

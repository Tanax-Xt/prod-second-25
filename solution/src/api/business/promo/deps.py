"""
This code may be based on "prod-hackaton-msk24" by Danila Sedelnikov <sedelnikovdanila@gmail.com> (https://github.com/Tanax-Xt).
Available at: https://github.com/Tanax-Xt/prod-hackaton-msk24

This code may be based on "fusion" by Rapid Integration (https://github.com/rapid-integration).
Available at: https://github.com/rapid-integration/fusion

This code may be based on "api" by Quotepedia (https://github.com/quotepedia).
Available at: https://github.com/quotepedia/api

Modifications made by Danila Sedelnikov on January 2025.
"""

from fastapi import Query, HTTPException, status
from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha2

SEARCH_PARAMS_LIST_SEPARATOR = ","


class Country(BaseModel):
    country: CountryAlpha2


def parse_list_query(country: list[str] | None = Query(None)) -> list[CountryAlpha2]:
    parsed_country = []
    if country:
        for tag in country:
            if tag and SEARCH_PARAMS_LIST_SEPARATOR in tag:
                parsed_country.extend(map(str.strip, tag.split(SEARCH_PARAMS_LIST_SEPARATOR)))
            else:
                parsed_country.append(tag)

    # МДАААА, костыль, но работает
    out = set()
    for i in parsed_country:
        try:
            out.add(Country(country=i).country)
        except Exception:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return list(out)

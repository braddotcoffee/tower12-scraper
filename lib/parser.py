from bs4 import BeautifulSoup, Tag
from typing import List
from lib.apartment import Apartment


def parse_apartments(floorplan_html: str) -> List[Apartment]:
    soup = BeautifulSoup(floorplan_html, "html.parser")
    units = soup.select(".unit-item")
    apartments = [parse_apartment(unit) for unit in units]
    return apartments


def parse_apartment(unit_item: Tag) -> Apartment:
    floor = parse_floor(unit_item)
    floorplan = parse_floorplan(unit_item)
    price = parse_price(unit_item)
    availability = parse_availability(unit_item)
    unit = parse_unit(unit_item)
    return Apartment(
        unit=unit,
        floor=floor,
        floorplan=floorplan,
        price=price,
        availability=availability,
    )


def parse_floorplan(unit_item: Tag) -> str:
    floor_plan_row: Tag = unit_item.select_one(".floor-plan-row")
    floor_plan_td: Tag = floor_plan_row.find_all("td")[1]
    return floor_plan_td.string


def parse_floor(unit_item: Tag) -> int:
    floor_row: Tag = unit_item.select_one(".floor-number-row")
    floor_row_td: Tag = floor_row.find_all("td")[1]
    return int(floor_row_td.string)


def parse_price(unit_item: Tag) -> int:
    price_row: Tag = unit_item.select_one(".unit-price-row")
    price_row_td: Tag = price_row.find_all("td")[1]
    return price_row_td.string


def parse_availability(unit_item: Tag) -> int:
    availability_row: Tag = unit_item.select_one(".availability-row")
    availability_row_td: Tag = availability_row.find_all("td")[1]
    return availability_row_td.string


def parse_unit(unit_item: Tag) -> str:
    unit_tag: Tag = unit_item.select_one(".apartment-name")
    return unit_tag.string.split()[1]

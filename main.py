from lib.grabber import grab_floorplans
from lib.parser import parse_apartments


def main():
    existing_apartments = set()
    count = 0
    while count < 10:
        apartments = parse_apartments(grab_floorplans())
        new_apartments = list(
            filter(lambda apt: apt not in existing_apartments, apartments)
        )
        print(len(new_apartments))
        existing_apartments.update(new_apartments)
        count += 1


if __name__ == "__main__":
    main()

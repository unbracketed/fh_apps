import csv

from apps.music_scene.db_api import list_venues

if __name__ == "__main__":
    with open("api-venues.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id",
                "name",
                "address",
                "city",
                "state",
                "zip_code",
                "website",
                "description",
            ]
        )
        for venue in list_venues():
            writer.writerow(
                [
                    venue.id,
                    venue.name,
                    venue.address,
                    venue.city,
                    venue.state,
                    venue.zip_code,
                    venue.website,
                    venue.description,
                ]
            )

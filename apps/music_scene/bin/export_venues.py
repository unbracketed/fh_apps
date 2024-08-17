import csv

from apps.music_scene.models import events, venues

if __name__ == "__main__":
    with open("venues.csv", "w", newline="") as file:
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
        for venue in venues():
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

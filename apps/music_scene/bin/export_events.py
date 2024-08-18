import csv

from apps.music_scene.db_api import list_events


if __name__ == "__main__":
    with open("api-events.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id",
                "title",
                "artist",
                "date",
                "start_time",
                "venue_id",
                "description",
                "url",
                "is_featured",
            ]
        )
        for event in list_events():
            writer.writerow(
                [
                    event.id,
                    event.title,
                    event.artist,
                    event.date,
                    event.start_time,
                    event.venue_id,
                    event.description,
                    event.url,
                    event.is_featured,
                ]
            )

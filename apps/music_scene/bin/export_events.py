import csv

from apps.music_scene.models import events


if __name__ == "__main__":
    with open("events.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "id",
                "title",
                "artist",
                "date",
                "start_time",
                "venue",
                "description",
                "url",
            ]
        )
        for event in events(order_by="date"):
            writer.writerow(
                [
                    event.id,
                    event.title,
                    event.artist,
                    event.date,
                    event.start_time,
                    event.venue,
                    event.description,
                    event.url,
                ]
            )

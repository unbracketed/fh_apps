from sqlite_utils.utils import rows_from_file

from apps.music_scene.models import events

if __name__ == "__main__":
    rows, format = rows_from_file(open("events.csv", "rb"))
    for row in rows:
        row.pop("id")

        existing = list(
            events.rows_where(
                "title = ? and artist = ? and venue = ? and date = ? and start_time = ?",
                [
                    row["title"],
                    row["artist"],
                    row["venue"],
                    row["date"],
                    row["start_time"],
                ],
            )
        )
        if not existing:
            events.insert(row)
        else:
            print("skipping", row)

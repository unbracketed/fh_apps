from sqlite_utils.utils import rows_from_file

from apps.music_scene.db_api import get_events_table

if __name__ == "__main__":
    events_table = get_events_table()
    rows, format = rows_from_file(open("api-events.csv", "rb"))
    for row in rows:
        row.pop("id")

        existing = list(
            events_table.rows_where(
                "title = ? and artist = ? and venue_id = ? and date = ? and start_time = ?",
                [
                    row["title"],
                    row["artist"],
                    row["venue_id"],
                    row["date"],
                    row["start_time"],
                ],
            )
        )
        if not existing:
            events_table.insert(row)
        else:
            print("skipping", row)

from sqlite_utils.utils import rows_from_file

from apps.music_scene.models import events, venues

if __name__ == "__main__":
    rows, format = rows_from_file(open("venues.csv", "rb"))
    for row in rows:
        row.pop("id")

        existing = list(
            venues.rows_where(
                "name = ? and city = ? and state = ?",
                [
                    row["name"],
                    row["city"],
                    row["state"],
                ],
            )
        )
        if not existing:
            venues.insert(row)
        else:
            print("skipping", row)

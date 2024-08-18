from sqlite_utils.utils import rows_from_file

from apps.music_scene.db_api import get_venues_table

if __name__ == "__main__":
    venues_table = get_venues_table()
    rows, format = rows_from_file(open("api-venues.csv", "rb"))
    for row in rows:
        row.pop("id")

        existing = list(
            venues_table.rows_where(
                "name = ? and city = ? and state = ?",
                [
                    row["name"],
                    row["city"],
                    row["state"],
                ],
            )
        )
        if not existing:
            venues_table.insert(row)
        else:
            print("skipping", row)

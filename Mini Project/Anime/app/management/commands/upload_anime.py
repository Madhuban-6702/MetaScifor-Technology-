import csv
import os
from django.core.management.base import BaseCommand
from app.models import Anime

class Command(BaseCommand):
    help = "Upload anime data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not os.path.exists(csv_file):
            self.stderr.write(f"File '{csv_file}' does not exist.")
            return

        with open(csv_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            # Print column headers from CSV for debugging
            print("CSV Headers:", reader.fieldnames)

            for row in reader:
                try:
                    # Check if anime_id already exists in the database
                    anime_id = int(row["anime_id"])
                    if Anime.objects.filter(anime_id=anime_id).exists():
                        print(f"Skipping duplicate anime_id: {anime_id}")
                        continue  # Skip duplicate entries

                    # Handle 'UNKNOWN' or invalid numeric values for Episodes
                    episodes_value = row["Episodes"].strip() if row["Episodes"] else None
                    episodes = int(float(episodes_value)) if episodes_value and episodes_value.replace('.', '', 1).isdigit() else None

                    Anime.objects.create(
                        anime_id=anime_id,
                        name=row["Name"],
                        english_name=row.get("English name"),
                        other_name=row.get("Other name"),
                        score=float(row["Score"]) if row["Score"].replace('.', '', 1).isdigit() else None,
                        genres=row.get("Genres"),
                        synopsis=row.get("Synopsis"),
                        type=row.get("Type"),
                        episodes=episodes,
                        aired=row.get("Aired"),
                        premiered=row.get("Premiered"),
                        status=row.get("Status"),
                        producers=row.get("Producers"),
                        licensors=row.get("Licensors"),
                        studios=row.get("Studios"),
                        source=row.get("Source"),
                        duration=row.get("Duration"),
                        rating=row.get("Rating"),
                        rank=int(row["Rank"]) if row["Rank"].isdigit() else None,
                        popularity=int(row["Popularity"]) if row["Popularity"].isdigit() else None,
                        favorites=int(row["Favorites"]) if row["Favorites"].isdigit() else None,
                        scored_by=int(row["Scored By"]) if row["Scored By"].isdigit() else None,
                        members=int(row["Members"]) if row["Members"].isdigit() else None,
                        image_url=row.get("Image URL"),
                    )
                except ValueError as e:
                    print(f"Skipping row {reader.line_num} due to conversion error: {e}")
                    continue
                except KeyError as e:
                    print(f"Skipping row {reader.line_num} due to missing column: {e}")
                    continue

        print("Successfully uploaded data!")

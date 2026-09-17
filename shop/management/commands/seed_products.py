import os
from decimal import Decimal

from django.core.files import File
from django.core.management.base import BaseCommand

from shop.models import Category, Product

# folder name -> (display name, order, default price in ETB)
CATEGORY_MAP = {
    "bags": ("Bags", 1, Decimal("4200.00")),
    "sling-bags": ("Sling Bags", 2, Decimal("3200.00")),
    "wallets": ("Wallets", 3, Decimal("1400.00")),
    "belts": ("Belts", 4, Decimal("1600.00")),
    "laptop-skins": ("Laptop Skins", 5, Decimal("950.00")),
    "travel-bag": ("Travel Bags", 6, Decimal("6200.00")),
    "shoes": ("Shoes", 7, Decimal("2800.00")),
}

SEED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "seed_images")


class Command(BaseCommand):
    help = (
        "Creates categories and imports the bundled product photos from "
        "shop/seed_images/ into the database. Safe to re-run — it skips "
        "products that already exist (matched by name)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all existing products and categories before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(self.style.WARNING("Deleting existing products and categories…"))
            Product.objects.all().delete()
            Category.objects.all().delete()

        if not os.path.isdir(SEED_DIR):
            self.stdout.write(self.style.ERROR(f"Seed folder not found: {SEED_DIR}"))
            return

        created_categories = 0
        created_products = 0
        skipped = 0

        for folder_name, (display_name, order, default_price) in CATEGORY_MAP.items():
            folder_path = os.path.join(SEED_DIR, folder_name)
            if not os.path.isdir(folder_path):
                continue

            category, was_created = Category.objects.get_or_create(
                name=display_name,
                defaults={"order": order},
            )
            if was_created:
                created_categories += 1
                self.stdout.write(f"  + Category: {display_name}")

            image_files = sorted(
                f for f in os.listdir(folder_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            )

            singular = display_name[:-1] if display_name.endswith("s") and not display_name.endswith("ss") else display_name

            for i, fname in enumerate(image_files, start=1):
                product_name = f"{singular} {i}" if len(image_files) > 1 else singular

                if Product.objects.filter(name=product_name, category=category).exists():
                    skipped += 1
                    continue

                file_path = os.path.join(folder_path, fname)
                product = Product(
                    name=product_name,
                    category=category,
                    price=default_price,
                    in_stock=True,
                    is_featured=(i == 1),  # first item of each category gets featured
                )
                with open(file_path, "rb") as f:
                    product.image.save(fname, File(f), save=False)
                product.save()
                created_products += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created_categories} categories created, "
            f"{created_products} products created, {skipped} already existed."
        ))
        self.stdout.write(
            "Prices were set to sensible category defaults — edit them for "
            "real pricing in the admin panel at /admin/."
        )

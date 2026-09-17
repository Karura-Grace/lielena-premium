# LIELENA Design — Django Store

A Django rebuild of the site: a real admin panel for managing products,
organized into categories, with your 90 product photos already included
and ready to import.

No payment gateway is wired up (Chapa was fully removed per your request).
This is a catalog/admin system — add checkout/payment back later if and
when you want to.

---

## What's inside

- **`shop/` app** — `Category` and `Product` models, a customized admin
  panel, and the public-facing pages (home, shop listing with category
  filter + search, product detail).
- **`shop/seed_images/`** — your 90 photos, already resized/compressed
  for the web and organized into 7 category folders (bags, sling-bags,
  wallets, belts, laptop-skins, travel-bag, shoes).
- **`shop/management/commands/seed_products.py`** — a one-time command
  that creates the 7 categories and imports all 90 photos as real
  `Product` rows in the database, with sensible starter prices per
  category (you'll want to adjust these to your real prices).

---

## 1. Local setup (do this first to check everything works)

You need Python 3.10+ installed.

```bash
# from inside this folder
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate          # creates the database
python manage.py seed_products    # imports categories + your 90 products
python manage.py createsuperuser  # create your own admin login

python manage.py runserver
```

Visit:
- **http://127.0.0.1:8000/** — the storefront
- **http://127.0.0.1:8000/admin/** — the admin panel (log in with the
  superuser you just created)

In the admin, click into any product to edit its price, description,
stock status, or swap the photo. Click "Add Product" to add a brand new
one — pick a category, set a price, upload a photo, save.

---

## 2. Deploying to HostPinnacle (cPanel)

Most cPanel hosts, including HostPinnacle, support Python apps through
a feature usually called **"Setup Python App"** (under the Software
section of cPanel). This is different from how you deployed the PHP
version — Django needs an actual Python process running, not just PHP
files sitting in a folder.

**Steps:**

1. In cPanel, open **Setup Python App**.
2. Click **Create Application**.
   - **Python version**: pick 3.10 or newer if offered.
   - **Application root**: e.g. `lielena_site` (a folder cPanel creates
     for you outside the public web root).
   - **Application URL**: your domain (or a subdomain/subfolder if you
     prefer, e.g. `shop.yourdomain.com`).
   - **Application startup file**: `passenger_wsgi.py` (already included
     in this project — don't edit it).
   - **Application Entry point**: `application`
3. cPanel will give you a command to "enter the virtual environment" —
   run it, then inside that environment run:
   ```bash
   pip install -r requirements.txt
   ```
4. Upload this whole project folder's contents into the **Application
   root** cPanel created (via File Manager or FTP) — everything except
   the `venv/` folder if you made one locally (cPanel makes its own).
5. Still inside that same cPanel Python environment, run:
   ```bash
   python manage.py migrate
   python manage.py seed_products
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```
6. **Set environment variables** for production (cPanel's Python App
   page has an "Environment variables" section — add these there
   instead of editing settings.py):
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` = `yourdomain.com,www.yourdomain.com`
   - `DJANGO_SECRET_KEY` = *(generate a random 50-character string —
     you can use https://djecrety.ir or run
     `python -c "import secrets; print(secrets.token_urlsafe(50))"`)*
7. Restart the app from the cPanel Python App page.

**If HostPinnacle doesn't offer "Setup Python App":** contact their
support and ask directly — this is the standard way shared hosts run
Django/Python. If they genuinely don't support Python apps at all,
you'd need a host that does (Python-friendly hosts, or a small VPS)
since Django can't run the way plain PHP files did.

**Media files (product photos) in production:** by default Django
serves uploaded photos itself only while `DEBUG=True`. In production
you'll want your web server (Apache, via cPanel) to serve the `/media/`
folder directly for speed — ask HostPinnacle support to confirm the
`MEDIA_ROOT` folder is served as static files, or point them to
Django's docs on deploying static/media files:
https://docs.djangoproject.com/en/stable/howto/static-files/deployment/

---

## 3. Everyday use once it's live

- Add a new product: **Admin → Products → Add Product**
- Add a new category: **Admin → Categories → Add Category**
- Change prices, mark something out of stock, or feature it on the
  homepage: just edit the product in the admin — changes are live
  immediately, no redeploying needed.

---

## Notes on pricing

The `seed_products` command set starting prices per category (e.g. all
bags start at 4200 ETB, all wallets at 1400 ETB, etc.) just so nothing
shows as free. **These are placeholders** — go through the admin panel
and set your real prices per item before launching.

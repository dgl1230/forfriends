from django.contrib.sitemaps import Sitemap


class FrenvuSitemap(Sitemap):
	changefreq = 'never'
	priority = 0.5
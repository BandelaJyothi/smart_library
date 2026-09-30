from django.contrib import admin

from .models import Book, Member, Issue, Reservation


admin.site.register(Book)

admin.site.register(Member)

admin.site.register(Issue)

admin.site.register(Reservation)
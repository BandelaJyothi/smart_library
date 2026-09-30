from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.landing,
        name='landing'
    ),

    path(
        'login/',
        views.login_choice,
        name='login_choice'
    ),

    path(
        'student/login/',
        views.student_login,
        name='student_login'
    ),

    path(
        'librarian/login/',
        views.librarian_login,
        name='librarian_login'
    ),

    path(
        'student/register/',
        views.student_register,
        name='student_register'
    ),

    path(
        'librarian/register/',
        views.librarian_register,
        name='librarian_register'
    ),

    path(
        'student/profile/',
        views.student_profile,
        name='student_profile'
    ),

    path(
        'student/dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'books/',
        views.book_catalog,
        name='book_catalog'
    ),

    path(
        'books/<int:book_id>/',
        views.book_details,
        name='book_details'
    ),

    path(
        'books/<int:book_id>/availability/',
        views.book_availability,
        name='book_availability'
    ),

    path(
        'books/<int:book_id>/reserve/',
        views.reserve_book,
        name='reserve_book'
    ),

    path(
    'librarian/books/add/',
    views.add_book,
    name='add_book'
),

    path(
        'librarian/dashboard/',
        views.librarian_dashboard,
        name='librarian_dashboard'
    ),

    path(
        'logout/',
        views.logout_user,
        name='logout_user'
    ),

    path(
        'return/<int:issue_id>/',
        views.return_book,
        name='return_book'
    ),


    path('librarian/books/add/', views.add_book, name='add_book'),

    path(
    'librarian/books/<int:book_id>/update/',
    views.update_book,
    name='update_book'
),
]



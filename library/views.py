from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Book, Reservation, Member, Issue


def landing(request):
    return render(request, 'library/landing.html')


def login_choice(request):
    return render(request, 'library/login_choice.html')


def student_login(request):
    if request.method == 'POST':
        logout(request)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return render(request, 'library/student_login.html', {
                'message': 'Login successful!'
            })

        return render(request, 'library/student_login.html', {
            'message': 'Invalid username or password.'
        })

    return render(request, 'library/student_login.html')


def librarian_login(request):
    return render(request, 'library/librarian_login.html')


def student_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        return render(request, 'library/student_register.html', {
            'message': 'Registration successful!'
        })

    return render(request, 'library/student_register.html')


def librarian_register(request):
    return render(request, 'library/librarian_register.html')


def student_profile(request):
    return render(request, 'library/student_profile.html')


def student_dashboard(request):
    reservations = Reservation.objects.filter(
        member__email=request.user.email
    )

    return render(request, 'library/student_dashboard.html', {
        'reservations': reservations
    })


def book_catalog(request):
    search = request.GET.get('search', '')

    if search:
        books = Book.objects.filter(
            title__icontains=search
        ) | Book.objects.filter(
            author__icontains=search
        )
    else:
        books = Book.objects.all()

    return render(request, 'library/book_catalog.html', {
        'books': books
    })


def book_details(request, book_id):
    book = Book.objects.get(id=book_id)

    return render(request, 'library/book_details.html', {
        'book': book
    })


def book_availability(request, book_id):
    book = Book.objects.get(id=book_id)

    return render(request, 'library/book_availability.html', {
        'book': book
    })

def reserve_book(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        member, created = Member.objects.get_or_create(
            email=request.user.email,
            defaults={
                'name': request.user.first_name,
                'phone': ''
            }
        )

        Reservation.objects.create(
            book=book,
            member=member
        )

        Issue.objects.create(
            book=book,
            member=member
        )

        return render(request, 'library/book_reservation.html', {
            'book': book,
            'message': 'Book reserved and borrowed successfully!'
        })

    return render(request, 'library/book_reservation.html', {
        'book': book
    })
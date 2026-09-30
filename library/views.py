from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Book, Member, Issue, Reservation


def landing(request):
    return render(request, 'library/landing.html')


def login_choice(request):
    return render(request, 'library/login_choice.html')


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('student_dashboard')

        return render(request, 'library/student_login.html', {
            'message': 'Invalid username or password.'
        })

    return render(request, 'library/student_login.html')


def librarian_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('librarian_dashboard')

        return render(request, 'library/librarian_login.html', {
            'message': 'Invalid librarian username or password.'
        })

    return render(request, 'library/librarian_login.html')


def logout_user(request):
    logout(request)
    return redirect('landing')


def student_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        print("PASSWORD LENGTH:", len(password or ""))
        print("CONFIRM LENGTH:", len(confirm_password or ""))
        print("PASSWORDS MATCH:", password == confirm_password)



        if password != confirm_password:
            return render(request, 'library/student_register.html', {
                'message': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'library/student_register.html', {
                'message': 'Username already exists.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        Member.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': ''
            }
        )

        return render(request, 'library/student_login.html', {
            'message': 'Registration successful. Please login.'
        })

    return render(request, 'library/student_register.html')


def librarian_register(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'library/librarian_register.html', {
                'message': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'library/librarian_register.html', {
                'message': 'Username already exists.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        user.is_staff = True
        user.save()

        return render(request, 'library/librarian_login.html', {
            'message': 'Registration successful. Please login.'
        })

    return render(request, 'library/librarian_register.html')

def student_profile(request):
    return render(request, 'library/student_profile.html')


def student_dashboard(request):
    reservations = Reservation.objects.filter(
        member__email=request.user.email
    )

    issues = Issue.objects.filter(
        member__email=request.user.email
    )

    return render(request, 'library/student_dashboard.html', {
        'reservations': reservations,
        'issues': issues,
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
        'books': books,
        'search': search
    })


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    return render(request, 'library/book_details.html', {
        'book': book
    })


def book_availability(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    return render(request, 'library/book_availability.html', {
        'book': book
    })


def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not request.user.is_authenticated:
        return redirect('student_login')

    member, created = Member.objects.get_or_create(
        email=request.user.email,
        defaults={
            'name': request.user.first_name or request.user.username,
            'phone': ''
        }
    )

    if request.method == 'POST':

        # Check whether the student already borrowed this book
        existing_issue = Issue.objects.filter(
            book=book,
            member=member,
            returned=False
        ).first()

        if existing_issue:
            return render(request, 'library/book_reservation.html', {
                'book': book,
                'message': 'You have already borrowed this book.'
            })

        # Check whether the student already reserved this book
        existing_reservation = Reservation.objects.filter(
            book=book,
            member=member,
            status='Reserved'
        ).first()

        if existing_reservation:
            return render(request, 'library/book_reservation.html', {
                'book': book,
                'message': 'You have already reserved this book.'
            })

        # Check book availability
        if book.available_quantity <= 0:
            return render(request, 'library/book_reservation.html', {
                'book': book,
                'message': 'This book is currently unavailable.'
            })

        # Create reservation
        Reservation.objects.create(
            book=book,
            member=member
        )

        # Create issue/borrow record
        Issue.objects.create(
            book=book,
            member=member
        )

        # Reduce available quantity
        book.available_quantity -= 1
        book.save()

        return render(request, 'library/book_reservation.html', {
            'book': book,
            'message': 'Book reserved and borrowed successfully!'
        })

    return render(request, 'library/book_reservation.html', {
        'book': book
    })

def add_book(request):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('librarian_login')

    if request.method == 'POST':

        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        quantity = request.POST.get('quantity')

        if Book.objects.filter(isbn=isbn).exists():
            return render(request, 'library/add_book.html', {
                'message': 'A book with this ISBN already exists.'
            })

        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity,
            available_quantity=quantity
        )

        return render(request, 'library/add_book.html', {
            'message': 'Book added successfully.'
        })

    return render(request, 'library/add_book.html')

def update_book(request, book_id):

    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('librarian_login')

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':

        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn = request.POST.get('isbn')
        book.quantity = request.POST.get('quantity')
        book.available_quantity = request.POST.get('available_quantity')

        book.save()

        return render(request, 'library/update_book.html', {
            'book': book,
            'message': 'Book updated successfully.'
        })

    return render(request, 'library/update_book.html', {
        'book': book
    })


def return_book(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if not issue.returned:
        from django.utils import timezone

        issue.returned = True
        issue.return_date = timezone.now().date()
        issue.save()

        issue.book.available_quantity += 1
        issue.book.save()

    return redirect('librarian_dashboard')



def librarian_dashboard(request):

    books = Book.objects.all()
    members = Member.objects.all()
    issues = Issue.objects.all()

    total_books = books.count()
    total_members = members.count()
    issued_books = issues.filter(returned=False).count()

    available_books = sum(
        book.available_quantity for book in books
    )

    return render(request, 'library/librarian_dashboard.html', {
        'books': books,
        'members': members,
        'issues': issues,
        'total_books': total_books,
        'total_members': total_members,
        'issued_books': issued_books,
        'available_books': available_books,
    })
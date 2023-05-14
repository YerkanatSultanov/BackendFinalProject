from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Publisher(models.Model):
    name = models.CharField(max_length=50,
                            help_text="The name of the Publisher.")
    website = models.URLField(help_text="The Publisher's website.")
    email = models.EmailField(help_text="The Publisher's email address.")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=70,
                             help_text="The title of the book.")
    publication_date = models.DateField(
        verbose_name="Date the book was published.")
    isbn = models.TextField(help_text="The Review text.")
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor',
                                          through="BookContributor")
    cover = models.ImageField(null=True,
                              blank=True,
                              upload_to="book_covers/")
    price = models.CharField(max_length=50,
                             help_text="The price of the book")
    hasSale = models.BooleanField(help_text="Определяет есть ли скидка или нет")

    saleFromPrice = models.CharField(max_length=50,
                                     help_text="Для определения новой ценны учитывая скидку")
    slug = models.SlugField(unique=True, null=False, max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    first_names = models.CharField(max_length=50,
                                   help_text="The contributor's first name or names.")
    last_names = models.CharField(max_length=50,
                                  help_text="The contributor's last name or names.")
    email = models.EmailField(help_text="The contact email for the contributor.")

    def initialled_name(self):
        initials = ''.join([name[0] for name
                            in self.first_names.split(' ')])
        return "{}, {}".format(self.last_names, initials)

    def __str__(self):
        return self.initialled_name()


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this contributor had in the book.",
                            choices=ContributionRole.choices, max_length=20)


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The the reviewer has given.", null=True)
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True,
                                       help_text='''The date and time the review was last edited.'''
                                       )
    creator = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             help_text="The Book that this review is for.")


class Category(models.Model):
    category = models.CharField(max_length=50,
                                help_text="The category of the book")

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# ==============================
# PLANT TYPE CHOICES
# ==============================
PLANT_TYPES = [
    ("Apple", "Apple"),
    ("Corn", "Corn"),
    ("Grape", "Grape"),
    ("Tomato", "Tomato"),
    ("Cherry", "Cherry"),
    ("Peach", "Peach"),
    ("Pepper", "Pepper"),
    ("Potato", "Potato"),
    ("Strawberry", "Strawberry"),
    ("Orange", "Orange"),
    ("Raspberry", "Raspberry"),
    ("Soybean_healthy", "Soybean Healthy"),
    ("Squash", "Squash"),
]


# ==============================
# TAMILNADU DISTRICTS (reuse if needed)
# ==============================
TAMILNADU_DISTRICTS =  [
    ('Ariyalur', 'Ariyalur'),
    ('Chengalpattu', 'Chengalpattu'),
    ('Chennai', 'Chennai'),
    ('Coimbatore', 'Coimbatore'),
    ('Cuddalore', 'Cuddalore'),
    ('Dharmapuri', 'Dharmapuri'),
    ('Dindigul', 'Dindigul'),
    ('Erode', 'Erode'),
    ('Kallakurichi', 'Kallakurichi'),
    ('Kanchipuram', 'Kanchipuram'),
    ('Kanyakumari', 'Kanyakumari'),
    ('Karur', 'Karur'),
    ('Krishnagiri', 'Krishnagiri'),
    ('Madurai', 'Madurai'),
    ('Mayiladuthurai', 'Mayiladuthurai'),
    ('Nagapattinam', 'Nagapattinam'),
    ('Namakkal', 'Namakkal'),
    ('Nilgiris', 'Nilgiris'),
    ('Perambalur', 'Perambalur'),
    ('Pudukkottai', 'Pudukkottai'),
    ('Ramanathapuram', 'Ramanathapuram'),
    ('Ranipet', 'Ranipet'),
    ('Salem', 'Salem'),
    ('Sivaganga', 'Sivaganga'),
    ('Tenkasi', 'Tenkasi'),
    ('Thanjavur', 'Thanjavur'),
    ('Theni', 'Theni'),
    ('Thoothukudi', 'Thoothukudi'),
    ('Tiruchirappalli', 'Tiruchirappalli'),
    ('Tirunelveli', 'Tirunelveli'),
    ('Tirupathur', 'Tirupathur'),
    ('Tiruppur', 'Tiruppur'),
    ('Tiruvallur', 'Tiruvallur'),
    ('Tiruvannamalai', 'Tiruvannamalai'),
    ('Tiruvarur', 'Tiruvarur'),
    ('Vellore', 'Vellore'),
    ('Viluppuram', 'Viluppuram'),
    ('Virudhunagar', 'Virudhunagar'),
]


# ==============================
# MODEL
# ==============================
class PestClass(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    district = models.CharField(
        max_length=50,
        choices=TAMILNADU_DISTRICTS
    )

    location = models.CharField(max_length=100)

    plant_type = models.CharField(
        max_length=50,
        choices=PLANT_TYPES
    )

    image = models.ImageField(
        upload_to='Pest_Photos/', blank=True, null=True
    )

    predicted_disease = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    confidence = models.FloatField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.plant_type}"
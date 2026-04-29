from django.db import models
from django.contrib.auth.models import User

TAMILNADU_DISTRICTS = [
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

class CropPrediction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=50, default='Unknown')

    # ✅ Better: keep default instead of null
    district = models.CharField(
        max_length=50,
        choices=TAMILNADU_DISTRICTS,
        default='Chennai'
    )

    place = models.CharField(max_length=50)

    # Soil Data
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    # Environment
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()

    # Soil Properties
    soil_moisture = models.FloatField()
    soil_ph = models.FloatField()
    cation_exchange_capacity = models.FloatField()

    # Output
    prediction = models.CharField(max_length=100)
    probability = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.district} | {self.prediction}"
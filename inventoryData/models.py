from django.db import models
from authe.models import User

class Boxes(models.Model):
    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    
    @property
    def area(self):
        return self.length * self.width
    
    @property
    def volume(self):
        return self.length * self.width * self.height


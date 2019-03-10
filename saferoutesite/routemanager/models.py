from django.db import models

class Address(models.Model):
    address_one = models.CharField("Address Line 1", max_length=200)
    address_two = models.CharField("Address Line 2", max_length=200)
    city_name = models.CharField("City", max_length=50)
    state_abbr = models.CharField("State", max_length=3)
    zip_code = models.CharField("Zip", max_length=10)

    
    def __str__(self):
        return (self.address_one, self.address_two, self.city_name, ", ",\
                self.state_abbr, ", ", self.zip_code)

class Route(models.Model):
    steps = models.CharField(max_length=100000)
    safety_score = models.FloatField()

    def __str__(self):
    	return (self.steps, self.safety_score)
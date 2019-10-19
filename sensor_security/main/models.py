from django.db import models

class Transactions (models.Model):
    temp_sensor = models.CharField(max_length=100)
    humidity_sensor = models.CharField(max_length=100)
    vibration_sensor = models.CharField(max_length=100)
    time_stamp = models.CharField(max_length=100)

    def __str__(self):
        return "Temperature : {} Humidity : {} Vibration : {}".format(self.temp_sensor, self.humidity_sensor, self.vibration_sensor) 

class Block (models.Model): #populated after getting chain
    time_stamp = models.CharField(max_length=100)
    previous_hash = models.CharField(max_length=100)
    index = models.IntegerField(primary_key=True)
    hash_num = models.CharField(max_length=500)
    nonce = models.CharField(max_length=10)
    
    def __str__(self):
        return "Index : {}".format(self.index) 

class Chain(models.Model):
    name = models.CharField(max_length=100)
    length = models.CharField(max_length=3)

    def __str__(self):
        return "Name : {}".format(self.name) 
    
class b2t(models.Model):
    transaction = models.ForeignKey(to=Transactions,on_delete=models.CASCADE)
    block = models.ForeignKey(to=Block,on_delete=models.CASCADE)

class b2c(models.Model):
    block = models.ForeignKey(to=Block,on_delete=models.CASCADE)
    chain = models.ForeignKey(to=Chain,on_delete=models.CASCADE)

class Data(models.Model):
    temp_sensor = models.CharField(max_length=100)
    humidity_sensor = models.CharField(max_length=100)
    vibration_sensor = models.CharField(max_length=100)

    def __str__(self):
        return "Temperature : {} Humidity : {} Vibration : {}".format(self.temp_sensor, self.humidity_sensor, self.vibration_sensor) 

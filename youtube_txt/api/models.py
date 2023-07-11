from django.db import models


class Customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.TextField()
    email = models.TextField()
    password = models.TextField()


class Video(models.Model):
    video_id = models.TextField(primary_key=True)
    video_url = models.TextField()
    video_count = models.IntegerField(default=0)
    video_title = models.TextField()

    def __str__(self):
        return self.video_id[:50]


class LaterList(models.Model):
    later_list_id = models.IntegerField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)


class Headline(models.Model):
    video_id = models.TextField()
    timestamp = models.FloatField()
    headline = models.TextField()


   


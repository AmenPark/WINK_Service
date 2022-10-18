from django.db import models

class routine(models.Model):
    routine_id = models.IntegerField(primary_key=True)      #고유 인덱스
    account_id = models.IntegerField()                      #작성자 정보
    title = models.CharField(max_length=20)                 #제목 최대 20자. 제한이 없어서 임의로 정함
    category = (('M', 'MIRACLE'),
                ('H', 'HOMEWORK'),)
    goal = models.TextField()
    is_alarm = models.BooleanField()
    is_deleted = models.BooleanField()
    created_at = models.DateField()
    modified_at = models.DateField()

class routine_result(models.Model):
    routine_result_id = models.IntegerField(primary_key=True)
    routine_id = models.ForeignKey(routine, on_delete=models.CASCADE)
    result = (('N', 'NOT'),
              ('T', 'TRY'),
              ('D', 'DONE'),)
    is_deleted = models.BooleanField()
    created_at = models.DateField()
    modified_at = models.DateField()

class routine_day(models.Model):
    day = models.DateField()
    routine_id = models.ForeignKey(routine, on_delete=models.CASCADE)
    created_at = models.DateField()
    modified_at = models.DateField()
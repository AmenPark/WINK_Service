from django.db import models

class routine(models.Model):
    routine_id = models.AutoField(primary_key=True)      #고유 인덱스
    account_id = models.IntegerField()                      #작성자 정보
    title = models.CharField(max_length=20)                 #제목 최대 20자. 제한이 없어서 임의로 정함
    Category_CHOICE = (('M', 'MIRACLE'),
                ('H', 'HOMEWORK'),)
    Category_var = [i[1] for i in Category_CHOICE]
    category = models.CharField(max_length=1, choices=Category_CHOICE)
    goal = models.TextField()
    is_alarm = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

class routine_result(models.Model):
    routine_result_id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey(routine, on_delete=models.CASCADE)
    result_CHOICE = (('N', 'NOT'),
              ('T', 'TRY'),
              ('D', 'DONE'),)
    result_var = [i[1] for i in result_CHOICE]
    result = models.CharField(max_length=1, choices=result_CHOICE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

class routine_day(models.Model):
    datechoices = (('MON','MON'),
                   ('TUE','TUE'),
                   ('WED','WED'),
                   ('THU','THU'),
                   ('FRI','FRI'),
                   ('SAT','SAT'),
                   ('SUN','SUN')
                   )
    datevar = [i[1] for i in datechoices]
    day = models.CharField(max_length=3, choices=datechoices)
    routine_id = models.ForeignKey(routine, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
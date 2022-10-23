from rest_framework.response import Response
from .models import routine,routine_result,routine_day
from rest_framework.views import APIView
from datetime import datetime

class GetRoutineList(APIView):
    def post(self,request):
        try:
            date = request.data["today"]
        except:
            data = {"message":{"msg" : "today is missing",
                               "status" : "ROUTINE_NOT_EXIST",}}
            return Response(data=data, status=400)
        try:
            today = datetime.strptime(date, '%Y-%m-%d')
        except :
            data = {"message":{"msg":"Incorrect today format, should be YYYY-MM-DD",
                               "status":"INVALID_TODAY"}}
            return Response(data=data, status=400)
        day = routine_day.datevar[today.weekday()]
        userid = request.user.id
        if userid == None:
            data = {"message":{"msg":"Need to login", "status":"NEED_LOGIN"}}
            return Response(data=data, status=401)

        try:
            routineDatas = routine_day.objects.filter(day=day)
            MyDatas = routine.objects.filter(account_id=userid)
            targetRoutineDatas = routineDatas.filter(routine_id__in = MyDatas)
        except:
            data = {"message": {"msg": "Routine is not exist",
                                "status": "ROUTINE_NOT_EXIST", }}
            return Response(data=data, status=404)

        data = {"data": [{
            "goal": d.routine_id.goal,
            "id": userid,
            "result": d.routine_id.routine_result_set.all()[0].result,
            "title": d.routine_id.title,
        } for d in targetRoutineDatas],
            "message": {"msg": "Routine lookup was successful.",
                        "status": "ROUTINE_LIST_OK"}}

        return Response(data=data, status=200)


class RoutineAPI(APIView):
    def get(self, request, id):
        try:
            routineData = routine.objects.get(pk=id)
        except :
            data = {"message":{"msg" : "Routine is not exist",
                               "status" : "ROUTINE_NOT_EXIST",}}
            return Response(data=data, status=404)

        dayDatas = routineData.routine_day_set.all()
        resultData = routineData.routine_result_set.all()
        data = {"data" : {
                    "goal": routineData.goal,
                    "id": id,
                    "result": resultData[0].result,
                    "title": routineData.title,
                    "days": [d.day for d in dayDatas]
                },
                "message" :{"msg": "Routine lookup was successful." ,
                "status" : "ROUTINE_DETAIL_OK"}
        }

        return Response(data=data)

    def delete(self,request,id):
        try:
            routineData = routine.objects.get(pk=id)
        except :
            data = {"message": {"msg": "Routine is not exist",
                                "status": "ROUTINE_NOT_EXIST",}}
            return Response(data=data, status=404)
        if routineData.account_id != request.user.id:
            data = {"message": {"msg": "Not allowed to access", "status": "NOT_ALLOWED"}}
            return Response(data=data, status=401)

        routineData.delete()
        data = {"data" : {
                    "routine_id" : id
                },
                "message" : {"msg":"The routine has been deleted.",
                        "status":"ROUTINE_DELETE_OK"}
        }
        return Response(data=data)

class RoutineSubmit(APIView):
    def put(self,request):      # 아무리 생각해도 id를 바꾸는게 말이 안되는데. id는 고유값 아니었나.
        if request.user.id == None:
            data = {"message":{"msg":"Need to login", "status":"NEED_LOGIN"}}
            return Response(data=data, status=401)
        data = request.data
        routine_id = data.get("routine_id",-1)
        try:
            target_routine = routine.objects.get(pk=routine_id)
        except:
            data = {"message": {"msg": "Routine is not exist",
                                "status": "ROUTINE_NOT_EXIST",}}
            return Response(data=data, status=404)
        if target_routine.account_id != request.user.id:
            data = {"message": {"msg": "Not allowed to access", "status": "NOT_ALLOWED"}}
            return Response(data=data, status=401)
        ct = 0
        if data.get("title",False):
            target_routine.title = data["title"]
            ct+=1
        if data.get("category",False):
            if not(data["category"] in routine.Category_var):
                data = {"message": {"msg": "Category is not defined.", "status": "INVALID_CATEGORY"}}
                return Response(data=data, status=400)
            target_routine.category = data["category"]
            ct+=1
        if data.get("goal",False):
            target_routine.goal = data["goal"]
            ct+=1
        if data.get("is_alarm", None)!=None:
            if not isinstance(data["is_alarm"], bool):
                data = {"message": {"msg": "is_alarm must be boolean", "status": "INVALID_IS_ALARM"}}
                return Response(data=data, status=400)
            target_routine.is_alarm = data["is_alarm"]
            ct+=1
        if data.get("days",None) != None:
            try:
                days = data.getlist("days")
            except:
                days = data["days"]
            for d in days:
                if not(d in routine_day.datevar):
                    data = {"message": {"msg": "the Day of the week is wrong.",
                                        "status": "BAD_DAYOFTHEWEEK"}}
                    return Response(data=data, status=400)
            for dayobj in target_routine.routine_day_set.all():
                dayobj.delete()
            for d in data["days"]:
                dayobj = routine_day(day=d, routine_id=target_routine)
                dayobj.save()
        if ct>0:
            target_routine.save()
            data = {"data":{"routine_id":routine_id},
                "message":{"msg":"The routine has been modified.", "status":"ROUTINE_UPDATE_OK"}}

        return Response(data=data, status=200)

    def post(self,request):         # 생성
        if request.user.id == None:
            data = {"message":{"msg":"Need to login", "status":"NEED_LOGIN"}}
            return Response(data=data, status=401)

        data = request.data
        try:
            key = "title"
            title = data[key]
            key = "category"
            category = data[key]
            key = "goal"
            goal = data[key]
            key = "is_alarm"
            is_alarm = data[key]
            if not(type(is_alarm)==type(True)):
                if type(is_alarm) == type("A"):
                    if is_alarm in ["true", "True", "TRUE"]:
                        is_alarm = True
                    elif is_alarm in ["false", "False", "FALSE"]:
                        is_alarm = False
                    else:
                        data = {"message": {"msg": f"{type(is_alarm)}: is_alarm must be boolean",
                                            "status": "INVALID_IS_ALARM"}}
                        return Response(data=data, status=400)
                else:
                    data = {
                        "message": {"msg": f"{type(is_alarm)}: is_alarm must be boolean", "status": "INVALID_IS_ALARM"}}
                    return Response(data=data, status=400)
            else:
                data = {"message": {"msg": f"{type(is_alarm)}: is_alarm must be boolean",
                                    "status": "INVALID_IS_ALARM"}}
                return Response(data=data, status=400)
            key = "days"
            try:
                days = data.getlist(key)
            except:
                days = data[key]
            account_id = request.user.id
        except:
            data = {"message": {"msg": f"{key} data is missing.", "status": "MISSING_DATA"}}
            return Response(data=data, status=400)
        if not(category in routine.Category_var):
            data = {"message": {"msg": "Category is not defined.", "status": "INVALID_CATEGORY"}}
            return Response(data=data, status=400)

        try:
            objs = []
            routineIns = routine(account_id=account_id, title=title, category=category,
                                 goal=goal, is_alarm=is_alarm)
            routineIns.save()
            objs.append(routineIns)
            routine_resultIns = routine_result(routine_id=routineIns, result="NOT")
            objs.append(routine_resultIns)
            for day in days:
                if not(day in routine_day.datevar):
                    data = {"message": {"msg": f"DAY:{day} is not in {routine_day.datevar}.",
                                        "status": f"BAD_DAYOFTHEWEEK"}}
                    return Response(data=data, status=400)
                routine_dayIns = routine_day(day=day, routine_id=routineIns)
                objs.append(routine_dayIns)
        except:
            data={"message":{"msg":"Invalid datatype", "status":"INVALID_DATA"}}
            return Response(data=data, status=400)


        for obj in objs:
            obj.save()

        data = {
            "data":{
                "routine_id":routineIns.routine_id
            },
            "message":{
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK",
            }
        }
        return Response(data=data, status=201)
from rest_framework import serializers

class ResultObject:
    result_status = True
    error_list = []
    message = ""
    object = None
    return_type = 'object'   #This will be object or message

    def __init__(self):
        self.result_status = True
        self.error_list = []
        self.message = ""
        self.object = None
        self.return_type = 'object'

    def set_object(self,data,result_status):
        self.result_status = result_status
        self.error_list = []
        self.message = ""
        self.object = data
        self.return_type = 'object'

    def set_message(self,message,result_status):
        self.result_status = result_status
        self.error_list = []
        self.message = message
        self.object = None
        self.return_type = 'message'

    

    def set_error_list(self,errors_list,result_status):
        self.result_status = result_status
        self.error_list = errors_list
        self.message = ""
        self.object = None
        self.return_type = 'error_list'


    def set_message_object(self,message,data,result_status):
        self.result_status = result_status
        self.error_list = []
        self.message = message
        self.object = data
        self.return_type = 'message,Object'


#Creating a serializer for ResultObject
class ResultObjectSerializer(serializers.Serializer):
    result_status = serializers.BooleanField()
    object = serializers.CharField()
    error_list = serializers.ListField(child=serializers.CharField(max_length=400))
    message = serializers.CharField(max_length=400)
    return_type = serializers.CharField(max_length=20)
class ChangeUserAgeModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._result = False
        self._detail = ""

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self._result,
                'detail' : self._detail
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    def change_users_age(self):
        today = datetime.datetime.now()
        user_datas = self._database.get_all_data(target="uid")
        if today.month == 1 and today.day == 1:
            for user_data in user_datas:
                user_data['age'] += 1

        # 하나하나 저장 함.
        for user_data in user_datas:
            self._database.modify_data_with_id(target_id="uid", target_data=user_data)

        self._result = True
        self._detail = "Complete Change all users age"

        return
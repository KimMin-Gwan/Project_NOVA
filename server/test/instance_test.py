
class Item():
    def __init__(self, init_data = {"chatting" : 0, "saver":0}):
        self.chatting  = init_data["chatting"]
        self.saver = init_data["saver"]

    def get_dict_form_data(self):
        return {
            "chatting" : self.chatting,
            "saver": self.saver
        }



item = Item(init_data={"chatting": 0, "saver" : 1})

print(item.saver)


attr = getattr(item, "saver")

print(attr)
class ContextManager:

    def __init__(self):

        self.context = {

            "last_object": None,
            "last_action": None,
            "last_site": None,
            "last_program": None,
            "topic": None,

        }

    # -------------------------
    # SET
    # -------------------------

    def set(self, key, value):

        self.context[key] = value

    # -------------------------
    # GET
    # -------------------------

    def get(self, key):

        return self.context.get(key)

    # -------------------------
    # CLEAR
    # -------------------------

    def clear(self):

        for key in self.context:

            self.context[key] = None

    # -------------------------
    # REPLACE
    # -------------------------

    def replace_pronouns(self, text):

        if not text:
            return text

        obj = self.get("last_object")

        if obj:

            pronouns = [

                "его",
                "её",
                "его же",
                "ее",

            ]

            for p in pronouns:

                text = text.replace(
                    p,
                    obj
                )

        return text
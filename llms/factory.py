from traitlets import default


class LLMFactory:

    @staticmethod
    def get_llm(name: str):
        match name:
            case "openai":
                pass
            case _:
                pass
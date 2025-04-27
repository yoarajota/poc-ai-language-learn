from happytransformer import HappyTextToText, TTSettings

class GrammarCorrectionModel:
    def __init__(self):
        print("Loading Grammar Correction model...")

        try:
            self.happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
            self.args = TTSettings(num_beams=5, min_length=1)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.happy_tt = None

    def correct_grammar(self, text):
        if not text or self.happy_tt is None:
            if self.happy_tt is None:
                print("Grammar Correction model is not loaded.")
            return ""

        try:
            input_text = f"grammar: {text}"
            result = self.happy_tt.generate_text(input_text, args=self.args)
            return result.text
        except Exception as e:
            print(f"Error in correct_grammar: {e}")
            return ""
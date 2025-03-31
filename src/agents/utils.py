from langdetect import detect
class Utils:
    def detect_language(question: str) -> str:
        """Detect input language & add translation in the prompt"""
        language = detect(question)
        if language == 'fr':
            question = f"Réponds en français: {question}"
        return question 

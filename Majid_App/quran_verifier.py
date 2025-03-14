from Levenshtein import distance
import arabic_reshaper
import bidi.algorithm

class QuranVerifier:
    def __init__(self, sensitivity=0.8):
        self.sensitivity = sensitivity

    def preprocess_arabic_text(self, text):
        # Remove diacritics and normalize text
        text = text.strip()
        return text

    def calculate_similarity(self, recited_text, expected_text):
        # Preprocess both texts
        recited = self.preprocess_arabic_text(recited_text)
        expected = self.preprocess_arabic_text(expected_text)
        
        # Calculate Levenshtein distance
        max_length = max(len(recited), len(expected))
        if max_length == 0:
            return 1.0
            
        similarity = 1 - (distance(recited, expected) / max_length)
        return similarity

    def verify_recitation(self, recited_text, expected_text):
        similarity = self.calculate_similarity(recited_text, expected_text)
        
        if similarity >= self.sensitivity:
            return True, similarity
        else:
            return False, similarity

    def get_correction_suggestion(self, recited_text, expected_text):
        """
        Returns correction suggestions when recitation differs from expected text
        """
        similarity = self.calculate_similarity(recited_text, expected_text)
        
        if similarity < self.sensitivity:
            # Format the expected text for display
            reshaped_text = arabic_reshaper.reshape(expected_text)
            bidi_text = bidi.algorithm.get_display(reshaped_text)
            return f"Correction needed. The correct verse is: {bidi_text}"
        
        return "Recitation is correct." 
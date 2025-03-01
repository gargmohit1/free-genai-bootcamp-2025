from typing import Dict, List, Optional, Tuple
from ..dao.word_dao import WordDAO
from ..models.word import Word

class WordService:
    def __init__(self, db_path: str):
        self.word_dao = WordDAO(db_path)
    
    def get_words(self, page: int = 1, per_page: int = 10) -> Tuple[List[Dict], int]:
        """Get paginated list of words"""
        return self.word_dao.get_words(page, per_page)
    
    def get_word_by_id(self, word_id: int) -> Optional[Dict]:
        """Get a word by its ID"""
        return self.word_dao.get_word_by_id(word_id)
    
    def create_word(self, word_data: Dict) -> Optional[Dict]:
        """Create a new word"""
        # Create and validate word model
        word = Word(
            kanji=word_data.get('kanji'),
            romaji=word_data.get('romaji'),
            english=word_data.get('english')
        )
        
        # Check for validation errors
        errors = word.validate()
        if errors:
            return None
        
        # Create word in database
        return self.word_dao.create_word(
            kanji=word.kanji,
            romaji=word.romaji,
            english=word.english
        )
    
    def update_word(self, word_id: int, word_data: Dict) -> Optional[Dict]:
        """Update an existing word"""
        # Get existing word
        existing_word = self.get_word_by_id(word_id)
        if not existing_word:
            return None
        
        # Create and validate word model
        word = Word(
            id=word_id,
            kanji=word_data.get('kanji'),
            romaji=word_data.get('romaji'),
            english=word_data.get('english')
        )
        
        # Check for validation errors
        errors = word.validate()
        if errors:
            return None
        
        # Update word in database
        return self.word_dao.update_word(
            word_id=word_id,
            kanji=word.kanji,
            romaji=word.romaji,
            english=word.english
        )
    
    def delete_word(self, word_id: int) -> bool:
        """Delete a word"""
        return self.word_dao.delete_word(word_id)

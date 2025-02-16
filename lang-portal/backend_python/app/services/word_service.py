from typing import Optional, Tuple, List
from ..models.word import Word
from ..dao.word_dao import WordDAO

class WordService:
    def __init__(self, word_dao: WordDAO):
        self.word_dao = word_dao

    def get_words(self, page: int = 1, per_page: int = 10) -> Tuple[List[Word], int]:
        """Get paginated list of words"""
        words_data, total_count = self.word_dao.get_words(page, per_page)
        words = [Word.from_dict(word_data) for word_data in words_data]
        return words, total_count

    def get_word(self, word_id: int) -> Optional[Word]:
        """Get a word by its ID"""
        word_data = self.word_dao.get_word_by_id(word_id)
        return Word.from_dict(word_data) if word_data else None

    def create_word(self, word: Word) -> Tuple[Optional[Word], List[str]]:
        """Create a new word"""
        # Validate word data
        errors = word.validate()
        if errors:
            return None, errors

        # Create word in database
        word_data = self.word_dao.create_word(
            kanji=word.kanji,
            romaji=word.romaji,
            meaning=word.meaning
        )
        return Word.from_dict(word_data), []

    def update_word(self, word_id: int, word: Word) -> Tuple[Optional[Word], List[str]]:
        """Update an existing word"""
        # Validate word data
        errors = word.validate()
        if errors:
            return None, errors

        # Update word in database
        word_data = self.word_dao.update_word(
            word_id=word_id,
            kanji=word.kanji,
            romaji=word.romaji,
            meaning=word.meaning
        )
        return (Word.from_dict(word_data), []) if word_data else (None, ["Word not found"])

    def delete_word(self, word_id: int) -> bool:
        """Delete a word by its ID"""
        return self.word_dao.delete_word(word_id)

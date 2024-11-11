import sys
import json
import random
from pathlib import Path
from typing import List, Dict
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLineEdit, QPushButton, QTextEdit, 
                              QLabel, QMessageBox, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt

from Word import Word
from QuizWindow import QuizWindow
class VocabularyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocabulary Learning App")
        self.setMinimumSize(600, 400)
        
        # Initialize words storage
        self.words_file = Path("learned_words.json")
        self.learned_words: Dict = self.load_words()
        
        # Set up the UI
        self.setup_ui()
    def load_words(self) -> Dict:
        """Load previously learned words from JSON file."""
        if self.words_file.exists():
            try:
                return json.loads(self.words_file.read_text())
            except json.JSONDecodeError:
                return {}
        return {}
    
    def save_words(self):
        """Save learned words to JSON file."""
        self.words_file.write_text(json.dumps(self.learned_words, indent=2))
    
    def add_word(self):
        """Add a new word and display its information."""
        word_text = self.word_input.text().strip().lower()
        if not word_text:
            return
        
        try:
            # Check if word is already learned
            if word_text in self.learned_words:
                self.display_word_info(word_text)
                QMessageBox.information(self, "Word Exists", 
                                      f"The word '{word_text}' is already in your vocabulary list!")
                return
            
            # Fetch word information
            word = Word(word_text)
            
            # Store word information
            self.learned_words[word_text] = {
                "definition": word.main_definition,
                "synonyms": word.all_synonyms,
                "antonyms": word.all_antonyms,
                "phonetic": word.phonetic
            }
            
            # Save to file
            self.save_words()
            
            # Display word information
            self.display_word_info(word_text)
            
            # Clear input
            self.word_input.clear()
            
            # Update word count
            self.update_word_count()
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Could not find word '{word_text}'")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
    
    def display_word_info(self, word: str):
        """Display word information in the text area."""
        word_info = self.learned_words[word]
        
        # Format the information
        display_text = f"Word: {word}\n"
        display_text += f"Phonetic: {word_info['phonetic']}\n\n"
        display_text += f"Definition: {word_info['definition']}\n\n"
        
        if word_info['synonyms']:
            display_text += f"Synonyms: {', '.join(word_info['synonyms'])}\n"
        
        if word_info['antonyms']:
            display_text += f"Antonyms: {', '.join(word_info['antonyms'])}\n"
        
        self.display_area.setText(display_text)
    
    def update_word_count(self):
        """Update the word count label."""
        count = len(self.learned_words)
        self.word_count_label.setText(f"Words learned: {count}")
    def setup_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create input area
        input_layout = QHBoxLayout()
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Enter a word...")
        self.word_input.returnPressed.connect(self.add_word)
        
        add_button = QPushButton("Add Word")
        add_button.clicked.connect(self.add_word)
        
        input_layout.addWidget(self.word_input)
        input_layout.addWidget(add_button)
        
        # Create quiz button
        quiz_button = QPushButton("Start Quiz")
        quiz_button.clicked.connect(self.start_quiz)
        input_layout.addWidget(quiz_button)
        
        # Create display area
        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        
        # Create word count label
        self.word_count_label = QLabel("Words learned: 0")
        
        # Add everything to main layout
        layout.addLayout(input_layout)
        layout.addWidget(QLabel("Word Information:"))
        layout.addWidget(self.display_area)
        layout.addWidget(self.word_count_label)
        
        # Update word count
        self.update_word_count()
    
    def start_quiz(self):
        """Open the quiz window."""
        if len(self.learned_words) < 4:
            QMessageBox.warning(self, "Not Enough Words", 
                              "Please learn at least 4 words before taking the quiz!")
            return
            
        self.quiz_window = QuizWindow(self.learned_words)
        self.quiz_window.show()
    
    # ... (rest of the VocabularyApp class remains the same)

def main():
    app = QApplication(sys.argv)
    window = VocabularyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
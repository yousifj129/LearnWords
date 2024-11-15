import random
from typing import List, Dict
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout , QPushButton, 
                              QLabel, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt

class QuizWindow(QMainWindow):
    def __init__(self, learned_words):
        super().__init__()
        self.setWindowTitle("Vocabulary Quiz")
        self.setMinimumSize(900, 600)  # Made taller for additional info
        self.setMaximumSize(1260,720)
        self.learned_words = learned_words
        self.wordsToLearn = self.learned_words.copy()
        self.current_word = None
        self.correct_answer = None
        
        # Set up the UI
        self.setup_ui()
        
        # Start the first question
        self.next_question()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create score label
        self.score_label = QLabel("Score: 0/0")
        layout.addWidget(self.score_label)
        
        # Create word display
        self.word_label = QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(self.word_label)
        
        # Create result label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 16px; margin: 10px;")
        layout.addWidget(self.result_label)
        
        # Create word info display
        self.word_info = QLabel()
        self.word_info.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.word_info.setWordWrap(True)
        self.word_info.setStyleSheet("margin: 10px; padding: 10px; border-radius: 5px;")
        self.word_info.hide()  # Initially hidden
        layout.addWidget(self.word_info)
        
        # Create options group
        self.options_group = QButtonGroup()
        self.option_buttons = []
        
        for i in range(4):
            radio = QRadioButton()
            self.option_buttons.append(radio)
            self.options_group.addButton(radio, i)
            layout.addWidget(radio)
        
        # Create buttons layout
        buttons_layout = QHBoxLayout()
        
        # Submit button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.check_answer)
        buttons_layout.addWidget(self.submit_button)
        
        # Next button
        self.next_button = QPushButton("Next Question")
        self.next_button.clicked.connect(self.next_question)
        buttons_layout.addWidget(self.next_button)
        
        layout.addLayout(buttons_layout)
        
        # Add some stretching space
        layout.addStretch()
        
        # Initialize score
        self.correct_count = 0
        self.total_questions = 0
    
    def get_random_words(self, exclude_word: str) -> List[str]:
        """Get random words from learned words, excluding the current word."""
        available_words = [word for word in self.wordsToLearn.keys() if word != exclude_word]
        return random.sample(available_words, min(3, len(available_words)))
    
    def next_question(self):
        """Set up the next quiz question."""
        # Clear previous result and word info
        self.result_label.clear()
        self.word_info.hide()
        
        if len(self.wordsToLearn) < 4:
            self.result_label.setText("Please learn at least 4 words before taking the quiz!")
            self.close()
            return
        
        # Select a random word
        self.current_word = random.choice(list(self.wordsToLearn.keys()))
        self.word_label.setText(self.current_word)
        
        # Get the correct definition
        correct_definition = self.learned_words[self.current_word]["definition"][0]
        
        # Get wrong definitions from other random words
        other_words = self.get_random_words(self.current_word)
        wrong_definitions = [self.learned_words[word]["definition"][0] for word in other_words]
        
        # Create all options and shuffle them
        all_options = [correct_definition] + wrong_definitions
        random.shuffle(all_options)
        
        # Store the correct answer index
        self.correct_answer = all_options.index(correct_definition)
        
        self.options_group.setExclusive(False)
        # Set the radio button texts
        for i, option in enumerate(all_options):
            self.option_buttons[i].setText(option)
            self.options_group.buttons()[i].setChecked(False)
            self.option_buttons[i].setChecked(False)
        self.options_group.setExclusive(True)
        # Enable submit button
        self.submit_button.setEnabled(True)
    
    def check_answer(self):
        """Check if the selected answer is correct."""
        selected_answer = self.options_group.checkedId()
        
        if selected_answer == -1:  # No selection made
            self.result_label.setText("Please select an answer!")
            self.result_label.setStyleSheet("color: orange; font-size: 16px; margin: 10px;")
            return
        
        self.total_questions += 1
        word_data = self.learned_words[self.current_word]
        definstr = ""
        for defin in word_data['definition']:
            definstr +=  '- '+defin+'\n'
        # Prepare word information display
        info_text = f"Definition:\n {definstr}\n\n"
        
        if word_data['synonyms']:
            info_text += f"Synonyms: {', '.join(word_data['synonyms'])}\n"
        
        if word_data['antonyms']:
            info_text += f"Antonyms: {', '.join(word_data['antonyms'])}"
        
        self.word_info.setText(info_text)
        self.word_info.show()
        
        if selected_answer == self.correct_answer:
            self.correct_count += 1
            self.result_label.setText("✓ Correct!")
            self.result_label.setStyleSheet("color: green; font-size: 16px; margin: 10px;")
            self.wordsToLearn.pop(self.current_word)
        else:
            self.result_label.setText("✗ Incorrect!")
            self.result_label.setStyleSheet("color: red; font-size: 16px; margin: 10px;")
        
        # Update score
        self.score_label.setText(f"Score: {self.correct_count}/{self.total_questions}")
        
        # Disable submit button until next question
        self.submit_button.setEnabled(False)
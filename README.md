# LearnWords

## Using the App

LearnWords is a vocabulary-building app that helps you learn new words while reading books. Here's how to use it:

1. Run the app and enter a word you'd like to learn.
2. The app will fetch the word's definition, synonyms, antonyms, and examples from a public dictionary API.
3. Review the word's information and add it to your vocabulary list.
4. Take a quiz to test your knowledge of the words you've learned.
5. to inspect and delete words you don't need anymore, click on the `Inspect words` button, and then double click the word you want to delete. Also, you can clear all with one button.
![alt text](https://github.com/yousifj129/LearnWords/blob/aed01cda79d163ff4343ded2f8c2bd4552258306/imgs/mainWindow.png)

## Under the Hood

LearnWords uses the DictionaryAPI to fetch word data. When you add a word to your vocabulary list, the app saves the word's information to a JSON file named `learned_words.json`. This file stores all the words you've learned, along with their definitions, synonyms, antonyms, and examples.

The app uses the following:
* PySide6 for GUI
* requests for making API calls to DictionaryAPI
* json for storing and loading word data

## Features

* Learn new words and their meanings
* Review word definitions, synonyms, antonyms, and examples
* Take a quiz to test your knowledge
* Save learned words to a JSON file for later access (todo: have multiple JSON files for different sets of vocab and prebuilt vocab to make it easier to learn topic specific words (like the SAT, IELTS and others))

## License

LearnWords is licensed under the MIT License. See LICENSE for details.

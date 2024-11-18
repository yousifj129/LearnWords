from dataclasses import dataclass
from typing import List, Optional
import requests
from typing import Dict, Any
from bing_image_downloader import downloader
import os
import threading

@dataclass
class Phonetic:
    text: str
    audio: Optional[str] = None
    source_url: Optional[str] = None
    license: Optional[Dict[str, str]] = None

@dataclass
class Definition:
    definition: str
    example: Optional[str] = None
    synonyms: List[str] = None
    antonyms: List[str] = None

    def __post_init__(self):
        self.synonyms = self.synonyms or []
        self.antonyms = self.antonyms or []

@dataclass
class Meaning:
    part_of_speech: str
    definitions: List[Definition]
    synonyms: List[str] = None
    antonyms: List[str] = None

    def __post_init__(self):
        self.synonyms = self.synonyms or []
        self.antonyms = self.antonyms or []

class Word:
    def __init__(self, word: str):
        self.word = word
        self.phonetic = ""
        self.phonetics: List[Phonetic] = []
        self.origin: Optional[str] = None
        self.meanings: List[Meaning] = []
        self.license: Optional[Dict[str, str]] = None
        self.source_urls: List[str] = []
        self.imageLink = None
        # Convenience properties
        self.main_definition: Optional[str] = None
        self.all_synonyms: List[str] = []
        self.all_antonyms: List[str] = []
        
        self._fetch_data()
        self._process_data()
    
    def _fetch_data(self) -> None:
        """Fetches word data from the dictionary API."""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}"
        response = requests.get(url)
        if response.status_code == 200:
            self._parse_response(response.json()[0])
        else:
            raise ValueError(f"Could not find word '{self.word}'")
        
        self.downloadimages(self.word)
            
    
    def _parse_response(self, data: Dict[str, Any]) -> None:
        """Parses the API response and sets the class attributes."""
        self.phonetic = data.get("phonetic", "")
        
        # Parse phonetics
        for phonetic_data in data.get("phonetics", []):
            phonetic = Phonetic(
                text=phonetic_data.get("text", ""),
                audio=phonetic_data.get("audio"),
                source_url=phonetic_data.get("sourceUrl"),
                license=phonetic_data.get("license")
            )
            self.phonetics.append(phonetic)
        
        self.origin = data.get("origin")
        self.license = data.get("license")
        self.source_urls = data.get("sourceUrls", [])
        
        # Parse meanings
        for meaning_data in data.get("meanings", []):
            definitions = []
            for def_data in meaning_data.get("definitions", []):
                definition = Definition(
                    definition=def_data["definition"],
                    example=def_data.get("example"),
                    synonyms=def_data.get("synonyms", []),
                    antonyms=def_data.get("antonyms", [])
                )
                definitions.append(definition)
            meaning = Meaning(
                part_of_speech=meaning_data["partOfSpeech"],
                definitions=definitions,
                synonyms=meaning_data.get("synonyms", []),  # Get synonyms at meaning level
                antonyms=meaning_data.get("antonyms", [])  # Get antonyms at meaning level
            )
            self.meanings.append(meaning)
    
    def _process_data(self) -> None:
        """Processes the parsed data to set convenience properties."""
        # Set main definition (first definition found)
        if self.meanings and self.meanings[0].definitions:
            self.main_definition = self.meanings[0].definitions[0].definition
        
        # Collect all synonyms and antonyms from both levels
        for meaning in self.meanings:
            # Add synonyms/antonyms from the meaning level
            self.all_synonyms.extend(meaning.synonyms)
            self.all_antonyms.extend(meaning.antonyms)
            
            # Add synonyms/antonyms from each definition
            for definition in meaning.definitions:
                self.all_synonyms.extend(definition.synonyms)
                self.all_antonyms.extend(definition.antonyms)
        
        # Remove duplicates while maintaining order
        self.all_synonyms = list(dict.fromkeys(self.all_synonyms))
        self.all_antonyms = list(dict.fromkeys(self.all_antonyms))
    
    def get_definitions_by_part_of_speech(self, part_of_speech: str) -> List[str]:
        """Returns all definitions for a specific part of speech."""
        for meaning in self.meanings:
            if meaning.part_of_speech.lower() == part_of_speech.lower():
                return [d.definition for d in meaning.definitions]
        return []
    
    def __str__(self) -> str:
        """Returns a string representation of the word with its main definition."""
        return f"{self.word}: {self.main_definition or 'No definition available'}"
    
    def __repr__(self) -> str:
        return f"Word('{self.word}')"
    
    def downloadimages(self, query):
        threading.Thread(target=self._download_images, args=(query,)).start()

    def _download_images(self, query):
        w = downloader.download(query, limit=1,  output_dir='downloads', 
                                adult_filter_off=True, force_replace=False, timeout=60,verbose=False)
        for file in os.listdir("./downloads/" + query):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".gif") or file.endswith(".webp"):
                self.imageLink = "./downloads/" + query + "/" + file
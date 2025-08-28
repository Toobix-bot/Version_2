"""
Toobix Speech Engine
Spracherkennung, Wake-Word Detection und Text-to-Speech
"""
import speech_recognition as sr
import pyttsx3
import threading
import time
import queue
from typing import Callable, Optional

class SpeechEngine:
    """Verwaltet Sprach-Ein- und Ausgabe für Toobix"""
    
    def __init__(self, settings):
        self.settings = settings
        self.speech_config = settings.get_speech_config()
        
        # Speech Recognition Setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-Speech Setup
        self.tts_engine = pyttsx3.init()
        self._setup_tts()
        
        # Threading und Kontrolle
        self.listening = False
        self.wake_word_active = True
        self.audio_queue = queue.Queue()
        
        # Callbacks
        self.on_command_received = None
        self.on_wake_word_detected = None
        
        print("🎤 Speech Engine initialisiert")
        self._calibrate_microphone()
    
    def _setup_tts(self):
        """Konfiguriert Text-to-Speech Engine"""
        try:
            # Stimme einstellen
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if self.speech_config['tts_voice'] in voice.id.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            # Geschwindigkeit und Lautstärke
            self.tts_engine.setProperty('rate', self.speech_config['tts_rate'])
            self.tts_engine.setProperty('volume', 0.8)
            
            print(f"🔊 TTS konfiguriert - Stimme: {self.speech_config['tts_voice']}")
            
        except Exception as e:
            print(f"⚠️ TTS Setup Fehler: {e}")
    
    def _calibrate_microphone(self):
        """Kalibriert Mikrofon für Umgebungsgeräusche"""
        try:
            print("🎯 Kalibriere Mikrofon...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Mikrofon kalibriert")
        except Exception as e:
            print(f"⚠️ Mikrofon-Kalibrierung fehlgeschlagen: {e}")
    
    def start_listening(self):
        """Startet kontinuierliche Spracherkennung"""
        self.listening = True
        print(f"👂 Höre auf Wake-Word: '{self.speech_config['wake_word']}'")
        
        while self.listening:
            try:
                with self.microphone as source:
                    # Kurzes Timeout für responsive UI
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                # Audio in Queue für Verarbeitung
                self.audio_queue.put(audio)
                
                # Audio in separatem Thread verarbeiten
                threading.Thread(
                    target=self._process_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                # Normal - einfach weiter hören
                pass
            except Exception as e:
                print(f"❌ Listening Fehler: {e}")
                time.sleep(1)
    
    def _process_audio(self, audio):
        """Verarbeitet aufgenommenes Audio"""
        try:
            # Sprache zu Text
            text = self.recognizer.recognize_google(
                audio, 
                language=self.speech_config['language']
            ).lower()
            
            print(f"👂 Gehört: '{text}'")
            
            # Wake-Word prüfen
            if self.wake_word_active and self.speech_config['wake_word'] in text:
                self._on_wake_word_detected(text)
            
            # Direkter Command (wenn Wake-Word bereits aktiv)
            elif not self.wake_word_active:
                self._on_command_received(text)
                
        except sr.UnknownValueError:
            # Nichts verstanden - normal
            pass
        except sr.RequestError as e:
            print(f"❌ Speech Recognition Fehler: {e}")
    
    def _on_wake_word_detected(self, text: str):
        """Behandelt Wake-Word Erkennung"""
        print("🚀 Wake-Word erkannt!")
        self.wake_word_active = False
        
        # Beep oder Ton abspielen (optional)
        self.speak("Ja?", wait=False)
        
        # Command aus Text extrahieren
        wake_word = self.speech_config['wake_word']
        if wake_word in text:
            command = text.replace(wake_word, "").strip()
            if command:
                self._on_command_received(command)
        
        # Callback aufrufen
        if self.on_wake_word_detected:
            self.on_wake_word_detected(text)
        
        # Wake-Word nach kurzer Zeit wieder aktivieren
        threading.Timer(10.0, self._reactivate_wake_word).start()
    
    def _on_command_received(self, command: str):
        """Behandelt erkannten Sprachbefehl"""
        print(f"🎯 Command: '{command}'")
        
        if self.on_command_received:
            self.on_command_received(command)
        
        # Wake-Word wieder aktivieren nach Command
        self._reactivate_wake_word()
    
    def _reactivate_wake_word(self):
        """Aktiviert Wake-Word Detection wieder"""
        self.wake_word_active = True
        print(f"👂 Höre wieder auf Wake-Word: '{self.speech_config['wake_word']}'")
    
    def speak(self, text: str, wait: bool = True):
        """Spricht Text aus (Thread-safe optimiert)"""
        try:
            print(f"🔊 Toobix sagt: '{text}'")
            
            if wait:
                # Synchron mit Error-Handling
                self._speak_sync(text)
            else:
                # Asynchron mit Queue
                threading.Thread(
                    target=self._speak_async,
                    args=(text,),
                    daemon=True
                ).start()
                
        except Exception as e:
            print(f"❌ TTS Fehler: {e}")
    
    def _speak_sync(self, text: str):
        """Synchrone TTS mit Runtime-Error-Handling"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except RuntimeError as e:
            if "run loop already started" in str(e):
                # Engine bereits aktiv - stoppe und versuche erneut
                try:
                    self.tts_engine.stop()
                    import time
                    time.sleep(0.1)
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except:
                    print(f"🔇 TTS temporär nicht verfügbar")
            else:
                print(f"🔇 TTS Runtime-Fehler: {e}")
        except Exception as e:
            print(f"🔇 TTS allgemeiner Fehler: {e}")
    
    def _speak_async(self, text: str):
        """Asynchrone TTS mit Error-Handling"""
        try:
            self._speak_sync(text)
        except Exception as e:
            print(f"🔇 TTS-Async Fehler: {e}")
    
    def stop(self):
        """Stoppt Speech Engine"""
        print("🔇 Speech Engine wird gestoppt...")
        self.listening = False
        
        try:
            self.tts_engine.stop()
        except:
            pass
    
    def set_callbacks(self, on_command: Callable = None, on_wake_word: Callable = None):
        """Setzt Callback-Funktionen"""
        self.on_command_received = on_command
        self.on_wake_word_detected = on_wake_word
    
    def manual_listen(self) -> Optional[str]:
        """Einmalige Spracherkennung (für Button-Aktivierung)"""
        try:
            print("🎤 Sprechen Sie jetzt...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(
                audio, 
                language=self.speech_config['language']
            )
            
            print(f"👂 Verstanden: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ Keine Sprache erkannt")
            return None
        except sr.UnknownValueError:
            print("❓ Sprache nicht verstanden")
            return None
        except Exception as e:
            print(f"❌ Sprach-Fehler: {e}")
            return None
    
    def is_listening(self) -> bool:
        """Prüft ob gerade gelauscht wird"""
        return self.listening
    
    def toggle_wake_word(self):
        """Schaltet Wake-Word Detection ein/aus"""
        self.wake_word_active = not self.wake_word_active
        status = "an" if self.wake_word_active else "aus"
        print(f"🎛️ Wake-Word {status}")
        return self.wake_word_active

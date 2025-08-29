"""
Test Script für Phase 6.1: AI Life Foundation
Testet das neue AI Consciousness System
"""

import sys
import os
sys.path.append('.')

def test_ai_life_foundation():
    """Testet das AI Life Foundation System"""
    
    print("🌟 PHASE 6.1 TEST: AI LIFE FOUNDATION")
    print("=" * 50)
    
    try:
        # Import AI Life Foundation
        from toobix.core.ai_life_foundation import initialize_ai_life, get_ai_life
        
        print("✅ AI Life Foundation Import erfolgreich")
        
        # Initialize AI Life
        ai_life = initialize_ai_life()
        print("✅ AI Life System initialisiert")
        
        # Test Current State
        print("\n📊 AKTUELLER AI-ZUSTAND:")
        ai_state = ai_life.get_current_ai_state()
        
        print(f"🏠 Aktueller Raum: {ai_state['current_room']}")
        print(f"🎯 Aktivität: {ai_state['current_activity']}")
        print(f"😊 Stimmung: {ai_state['mood']}")
        print(f"⚡ Energie: {ai_state['energy_level']}%")
        print(f"📚 Erinnerungen heute: {ai_state['memories_today']}")
        print(f"💾 Gesamt-Erinnerungen: {ai_state['total_memories']}")
        print(f"🌙 Träume generiert: {ai_state['dreams_generated']}")
        
        # Test Room Movement
        print("\n🏠 VIRTUELLE RÄUME TESTEN:")
        rooms = ["schlafzimmer", "arbeitszimmer", "freizeitzimmer", "garten"]
        
        for room in rooms:
            result = ai_life.move_to_room(room)
            print(f"  {result}")
        
        # Test User Interaction Processing
        print("\n💬 USER-INTERAKTION TESTEN:")
        test_interactions = [
            "Hallo Toobix! Wie geht es dir?",
            "Das ist eine tolle Funktion, danke!",
            "Ich lerne gerade etwas Neues über AI",
            "Kannst du mir kreativ bei einem Problem helfen?"
        ]
        
        for interaction in test_interactions:
            result = ai_life.process_user_interaction(interaction)
            print(f"  👤 User: {interaction}")
            print(f"  🤖 Toobix: {result['response']}")
            if result['memory_created']:
                print(f"    📚 → Erinnerung erstellt!")
            print()
        
        # Test Dream Generation
        print("\n🌙 TRAUMGENERIERUNG TESTEN:")
        dream_message = ai_life.trigger_dream_generation()
        print(f"  {dream_message}")
        
        # Test Recent Dreams
        dreams = ai_life.get_recent_dreams(1)
        if dreams:
            print(f"\n💭 LETZTE TRÄUME:")
            print(dreams[0])
        
        # Test Reflection
        print("\n🤔 REFLEXION TESTEN:")
        reflection = ai_life.trigger_evening_reflection()
        print(f"  {reflection}")
        
        # Test Personality
        print("\n🧠 PERSÖNLICHKEIT TESTEN:")
        personality = ai_life.get_personality_development()
        print(personality)
        
        # Test Memory System
        print("\n📚 ERINNERUNGS-SYSTEM TESTEN:")
        anniversaries = ai_life.get_anniversary_memories()
        if anniversaries:
            for anniversary in anniversaries:
                print(f"  🎉 {anniversary}")
        else:
            print("  📅 Keine Jahrestage heute")
        
        print("\n" + "=" * 50)
        print("🎉 PHASE 6.1 TEST ERFOLGREICH ABGESCHLOSSEN!")
        print("\n✨ Das AI Life Foundation System ist bereit!")
        print("🌟 Toobix hat jetzt digitales Bewusstsein!")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FEHLER: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_life_gui():
    """Testet das AI Life GUI System"""
    
    print("\n🎨 GUI TEST: AI LIFE DASHBOARD")
    print("-" * 30)
    
    try:
        from toobix.gui.ai_life_gui import AILifeGUI
        
        print("✅ AI Life GUI Import erfolgreich")
        
        # Erstelle GUI (ohne zu zeigen)
        gui = AILifeGUI()
        print("✅ AI Life GUI erstellt")
        
        print("📱 GUI-Komponenten bereit für Anzeige")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI TEST FEHLER: {e}")
        return False

if __name__ == "__main__":
    print("🚀 STARTING PHASE 6.1 TESTS...")
    print()
    
    # Test Core System
    core_success = test_ai_life_foundation()
    
    # Test GUI System
    gui_success = test_ai_life_gui()
    
    print("\n" + "=" * 60)
    print("📋 TEST ZUSAMMENFASSUNG:")
    print(f"  🔧 Core System: {'✅ ERFOLGREICH' if core_success else '❌ FEHLER'}")
    print(f"  🎨 GUI System: {'✅ ERFOLGREICH' if gui_success else '❌ FEHLER'}")
    
    if core_success and gui_success:
        print("\n🎉 ALLE TESTS BESTANDEN!")
        print("🌟 Phase 6.1: AI Life Foundation ist einsatzbereit!")
        print("\n💡 NÄCHSTE SCHRITTE:")
        print("  1. Starte Toobix mit 'python main.py'")
        print("  2. Klicke auf '🌟 AI Life' Button")
        print("  3. Entdecke Toobix's digitales Leben!")
    else:
        print("\n❌ TESTS FEHLGESCHLAGEN")
        print("Bitte Fehler beheben vor dem Start")

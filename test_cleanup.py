#!/usr/bin/env python3
"""
Teste die neuen System-Aufräum-Features von Toobix
"""
import sys
sys.path.append('.')

from toobix.core.system_organizer import SystemOrganizer
from toobix.core.desktop_integration import DesktopIntegration
from toobix.config.settings import Settings

def test_system_organizer():
    print("🧪 Teste Toobix System-Aufräum-Features\n")
    
    # Initialisierung
    settings = Settings()
    desktop = DesktopIntegration()
    
    print("=" * 60)
    print("1️⃣ SYSTEM-ANALYSE:")
    print("=" * 60)
    analysis_result = desktop.analyze_system_cleanliness()
    print(analysis_result)
    
    print("\n" + "=" * 60)
    print("2️⃣ AUFRÄUMPLAN:")
    print("=" * 60)
    plan_result = desktop.create_cleanup_plan()
    print(plan_result)
    
    print("\n" + "=" * 60)
    print("3️⃣ SYSTEM-INFO:")
    print("=" * 60)
    system_info = desktop.get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 60)
    print("🎉 ALLE TESTS ABGESCHLOSSEN!")
    print("=" * 60)
    print("💡 Du kannst jetzt diese Befehle in Toobix verwenden:")
    print("   • 'Analysiere mein System'")
    print("   • 'Erstelle einen Aufräumplan'")
    print("   • 'Erstelle ein Backup'")
    print("   • 'Räume mein System auf bestätigt'")

if __name__ == "__main__":
    test_system_organizer()

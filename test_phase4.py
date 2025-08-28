"""
Toobix Phase 4 Test und Demo
Testet alle Phase 4 Features für System-Transparenz und erweiterte Funktionalität
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import json
from datetime import datetime

def test_system_documentation_engine():
    """Testet System Documentation Engine"""
    print("=" * 60)
    print("🔍 TESTING: System Documentation Engine")
    print("=" * 60)
    
    try:
        from toobix.core.system_documentation_engine import SystemDocumentationEngine
        
        doc_engine = SystemDocumentationEngine()
        
        # Test System Overview
        print("\n📋 System Overview:")
        overview = doc_engine.get_system_overview()
        print(overview[:200] + "..." if len(overview) > 200 else overview)
        
        # Test Component Categories
        print("\n📂 Component Categories:")
        categories = doc_engine.get_component_categories()
        for category in categories:
            print(f"  • {category}")
        
        # Test Function Search
        print("\n🔍 Function Search Test:")
        search_results = doc_engine.search_functions("AI")
        print(f"Found {len(search_results)} functions related to 'AI'")
        for result in search_results[:3]:
            print(f"  • {result['name']}: {result['description'][:50]}...")
        
        # Test Component Documentation
        print("\n📖 Component Documentation Test:")
        ai_components = doc_engine.get_components_by_category("Core AI")
        print(f"Found {len(ai_components)} AI components")
        
        print("✅ System Documentation Engine: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ System Documentation Engine: FAILED - {e}")
        return False

def test_ki_thought_stream_engine():
    """Testet KI Thought Stream Engine"""
    print("=" * 60)
    print("🧠 TESTING: KI Thought Stream Engine")
    print("=" * 60)
    
    try:
        from toobix.core.ki_thought_stream_engine import KIThoughtStreamEngine
        
        thought_engine = KIThoughtStreamEngine()
        
        # Test Gedanken-Injection
        print("\n💭 Testing Thought Injection:")
        thought_engine.inject_thought("Das ist ein Test-Gedanke", "test", "high")
        
        # Test Stream Start
        print("\n🌊 Starting Thought Stream:")
        thought_engine.start_thought_stream()
        
        # Warte kurz für erste Gedanken
        print("⏳ Waiting for thoughts to generate...")
        time.sleep(3)
        
        # Test Gedanken abrufen
        print("\n📝 Recent Thoughts:")
        thoughts = thought_engine.get_thought_stream(3)
        for i, thought in enumerate(thoughts, 1):
            print(f"{i}. [{thought['thought_type']}] {thought['content'][:60]}...")
        
        # Test Actionable Thoughts
        print("\n⚡ Actionable Thoughts:")
        actionable = thought_engine.get_actionable_thoughts(2)
        print(f"Found {len(actionable)} actionable thoughts")
        
        # Test Statistics
        print("\n📊 Thought Stream Statistics:")
        stats = thought_engine.get_thought_statistics()
        print(f"Total thoughts: {stats['total_thoughts']}")
        print(f"Stream active: {stats['stream_active']}")
        
        # Stop Stream
        thought_engine.stop_thought_stream()
        
        print("✅ KI Thought Stream Engine: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ KI Thought Stream Engine: FAILED - {e}")
        return False

def test_extended_settings_engine():
    """Testet Extended Settings Engine"""
    print("=" * 60)
    print("⚙️ TESTING: Extended Settings Engine")
    print("=" * 60)
    
    try:
        from toobix.core.extended_settings_engine import ExtendedSettingsEngine
        
        settings_engine = ExtendedSettingsEngine()
        
        # Test Categories
        print("\n📂 Settings Categories:")
        categories = settings_engine.get_all_categories()
        for category in categories:
            print(f"  • {category}")
        
        # Test Setting Get/Set
        print("\n🔧 Testing Setting Operations:")
        # Test AI Temperature
        old_temp = settings_engine.get_setting('ai_response_temperature')
        print(f"Current AI temperature: {old_temp}")
        
        # Set new value
        success = settings_engine.set_setting('ai_response_temperature', 0.8)
        new_temp = settings_engine.get_setting('ai_response_temperature')
        print(f"Set AI temperature to 0.8: {success}, New value: {new_temp}")
        
        # Test Category Settings
        print("\n🎛️ AI Settings:")
        ai_settings = settings_engine.get_settings_by_category('AI & Intelligenz')
        print(f"Found {len(ai_settings)} AI settings")
        for key, setting in list(ai_settings.items())[:3]:
            print(f"  • {setting.display_name}: {setting.current_value}")
        
        # Test Settings Summary
        print("\n📋 Settings Summary:")
        summary = settings_engine.get_settings_summary()
        print(f"Total settings: {summary['total_settings']}")
        print(f"Categories: {summary['categories']}")
        print(f"Current theme: {summary['current_theme']}")
        
        print("✅ Extended Settings Engine: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Extended Settings Engine: FAILED - {e}")
        return False

def test_interactive_tutorial_system():
    """Testet Interactive Tutorial System"""
    print("=" * 60)
    print("🎓 TESTING: Interactive Tutorial System")
    print("=" * 60)
    
    try:
        from toobix.core.interactive_tutorial_system import InteractiveTutorialSystem
        
        tutorial_system = InteractiveTutorialSystem()
        
        # Test Available Tutorials
        print("\n📚 Available Tutorials:")
        tutorials = tutorial_system.get_available_tutorials()
        for tutorial in tutorials:
            print(f"  • {tutorial['title']} ({tutorial['type']}, {tutorial['estimated_duration']}min)")
        
        # Test Tutorial Start
        print("\n🚀 Starting Basic Tutorial:")
        success = tutorial_system.start_tutorial('basics')
        print(f"Tutorial started: {success}")
        
        if success:
            # Test Tutorial Steps
            print("\n📋 Tutorial Steps:")
            step = tutorial_system.next_step()
            if step:
                print(f"Current step: {step.title}")
                print(f"Description: {step.description[:80]}...")
                
                # Complete step
                tutorial_system.complete_step(step.step_id)
                print("Step completed")
        
        # Test Recommendations
        print("\n💡 Recommended Tutorials:")
        recommendations = tutorial_system.get_recommended_tutorials()
        for rec in recommendations[:3]:
            print(f"  • {rec['title']} (Score: {rec['score']:.1f})")
        
        # Test Search
        print("\n🔍 Tutorial Search:")
        search_results = tutorial_system.search_tutorials("basic")
        print(f"Found {len(search_results)} tutorials for 'basic'")
        
        # Test Statistics
        print("\n📊 User Statistics:")
        stats = tutorial_system.get_user_statistics()
        print(f"Total tutorials: {stats['total_tutorials']}")
        print(f"Completed: {stats['completed_tutorials']}")
        print(f"In progress: {stats['in_progress_tutorials']}")
        
        print("✅ Interactive Tutorial System: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Interactive Tutorial System: FAILED - {e}")
        return False

def test_phase4_integration():
    """Testet Phase 4 Integration"""
    print("=" * 60)
    print("🔗 TESTING: Phase 4 Integration")
    print("=" * 60)
    
    try:
        # Test Import aller Phase 4 Module
        print("\n📦 Testing Module Imports:")
        
        from toobix.core.system_documentation_engine import SystemDocumentationEngine
        from toobix.core.ki_thought_stream_engine import KIThoughtStreamEngine
        from toobix.core.extended_settings_engine import ExtendedSettingsEngine
        from toobix.core.interactive_tutorial_system import InteractiveTutorialSystem
        from toobix.gui.phase4_panels import Phase4TabManager
        
        print("  ✅ All modules imported successfully")
        
        # Test Engine Initialization
        print("\n🏗️ Testing Engine Initialization:")
        doc_engine = SystemDocumentationEngine()
        thought_engine = KIThoughtStreamEngine()
        settings_engine = ExtendedSettingsEngine()
        tutorial_system = InteractiveTutorialSystem()
        
        print("  ✅ All engines initialized successfully")
        
        # Test Cross-Engine Communication
        print("\n🔄 Testing Cross-Engine Communication:")
        
        # Settings -> Thought Stream
        thought_freq = settings_engine.get_setting('thought_frequency')
        print(f"  • Settings provides thought frequency: {thought_freq}")
        
        # Documentation -> Tutorial System
        docs_components = doc_engine.get_component_categories()
        tutorial_categories = [t['type'] for t in tutorial_system.get_available_tutorials()]
        print(f"  • Documentation has {len(docs_components)} categories")
        print(f"  • Tutorials cover {len(set(tutorial_categories))} categories")
        
        # Thought Stream -> Settings integration test
        thought_engine.start_thought_stream()
        time.sleep(2)  # Wait for thoughts
        
        thoughts = thought_engine.get_thought_stream(2)
        if thoughts:
            print(f"  • Thought stream generated {len(thoughts)} thoughts")
        
        thought_engine.stop_thought_stream()
        
        print("✅ Phase 4 Integration: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Phase 4 Integration: FAILED - {e}")
        return False

def demonstrate_phase4_features():
    """Demonstriert Phase 4 Features"""
    print("=" * 60)
    print("🎭 PHASE 4 FEATURE DEMONSTRATION")
    print("=" * 60)
    
    try:
        from toobix.core.system_documentation_engine import SystemDocumentationEngine
        from toobix.core.ki_thought_stream_engine import KIThoughtStreamEngine
        from toobix.core.extended_settings_engine import ExtendedSettingsEngine
        from toobix.core.interactive_tutorial_system import InteractiveTutorialSystem
        
        print("\n🚀 Initializing Phase 4 System...")
        
        # Initialize all engines
        doc_engine = SystemDocumentationEngine()
        thought_engine = KIThoughtStreamEngine()
        settings_engine = ExtendedSettingsEngine()
        tutorial_system = InteractiveTutorialSystem()
        
        print("✅ All Phase 4 components initialized!")
        
        # Demonstrate System Documentation
        print("\n📚 SYSTEM DOCUMENTATION DEMO:")
        print("-" * 40)
        overview = doc_engine.get_system_overview()
        print("System Overview Generated:")
        print(overview[:300] + "..." if len(overview) > 300 else overview)
        
        # Demonstrate KI Thought Stream
        print("\n🧠 KI THOUGHT STREAM DEMO:")
        print("-" * 40)
        thought_engine.start_thought_stream()
        
        # Add some manual thoughts for demo
        thought_engine.inject_thought("Demonstrating the power of continuous AI insights", "insight", "high")
        thought_engine.inject_thought("System transparency allows users to understand what's happening", "observation", "medium")
        
        print("Thought stream started. Recent thoughts:")
        time.sleep(2)
        
        recent_thoughts = thought_engine.get_thought_stream(3)
        for i, thought in enumerate(recent_thoughts, 1):
            print(f"{i}. [{thought['thought_type'].upper()}] {thought['content']}")
        
        # Demonstrate Extended Settings
        print("\n⚙️ EXTENDED SETTINGS DEMO:")
        print("-" * 40)
        print("Available setting categories:")
        categories = settings_engine.get_all_categories()
        for cat in categories[:5]:
            print(f"  • {cat}")
        
        print(f"\nTotal settings: {settings_engine.get_settings_summary()['total_settings']}")
        
        # Demonstrate Tutorial System
        print("\n🎓 TUTORIAL SYSTEM DEMO:")
        print("-" * 40)
        tutorials = tutorial_system.get_available_tutorials()
        print("Available tutorials:")
        for tutorial in tutorials[:3]:
            print(f"  • {tutorial['title']} ({tutorial['difficulty_level']}/5 ⭐)")
        
        recommendations = tutorial_system.get_recommended_tutorials()
        print(f"\nTop recommendation: {recommendations[0]['title']}")
        
        # Clean up
        thought_engine.stop_thought_stream()
        
        print("\n" + "=" * 60)
        print("🎉 PHASE 4 DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("\nPhase 4 Features Summary:")
        print("✅ System Documentation Engine - Complete system transparency")
        print("✅ KI Thought Stream Engine - Continuous AI insights")
        print("✅ Extended Settings Engine - Comprehensive system control")
        print("✅ Interactive Tutorial System - Guided learning experience")
        print("✅ GUI Integration - User-friendly interface panels")
        print("\n🚀 Toobix Phase 4: SYSTEM TRANSPARENCY AND ENHANCED UX - COMPLETE!")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 4 Demonstration: FAILED - {e}")
        return False

def main():
    """Haupttest-Funktion"""
    print("🌟" * 30)
    print("🚀 TOOBIX PHASE 4 TESTING SUITE")
    print("🌟" * 30)
    print("\nTesting System Transparency and Enhanced User Experience Features...")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("System Documentation Engine", test_system_documentation_engine),
        ("KI Thought Stream Engine", test_ki_thought_stream_engine),
        ("Extended Settings Engine", test_extended_settings_engine),
        ("Interactive Tutorial System", test_interactive_tutorial_system),
        ("Phase 4 Integration", test_phase4_integration)
    ]
    
    results = []
    
    print("\n" + "🔬" * 60)
    print("RUNNING COMPONENT TESTS")
    print("🔬" * 60)
    
    for test_name, test_func in tests:
        print(f"\n▶️ Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Brief pause between tests
    
    # Test Summary
    print("\n" + "📊" * 60)
    print("TEST RESULTS SUMMARY")
    print("📊" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    # Run Demonstration if all tests passed
    if failed == 0:
        print(f"\n{'🎉' * 20}")
        print("ALL TESTS PASSED! Running Feature Demonstration...")
        print(f"{'🎉' * 20}")
        time.sleep(2)
        demonstrate_phase4_features()
    else:
        print(f"\n{'⚠️' * 20}")
        print("SOME TESTS FAILED! Please check the errors above.")
        print(f"{'⚠️' * 20}")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()

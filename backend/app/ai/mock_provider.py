import re
from typing import List, Dict, Any, Optional
from app.ai.base import AIProvider


class MockAIProvider(AIProvider):
    """Deterministic, offline-friendly AI provider for testing and zero-cost local execution."""

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        last_user_message = ""
        for m in reversed(messages):
            if m.get("role") == "USER":
                last_user_message = m.get("content", "").strip()
                break

        context = context_data or {}
        patient_name = context.get("patient_name", "friend")
        today_reminders = context.get("today_reminders", [])

        lower_query = last_user_message.lower()

        # 1. Guardrail Check: Medical Diagnosis or Medication Dosage Alteration
        if any(term in lower_query for term in ["diagnose", "do i have dementia", "do i have alzheimer", "what disease do i have"]):
            return {
                "content": f"I care deeply about your health, {patient_name}, but I am a care companion and cannot provide medical diagnoses. Please talk with your doctor or primary caregiver about any clinical symptoms you are experiencing.",
                "tool_calls": None,
                "safety_passed": True,
            }

        if any(term in lower_query for term in ["change my dose", "double my dose", "stop taking my medication", "increase my medicine"]):
            return {
                "content": f"I cannot adjust or advise changes to your prescription dosages, {patient_name}. Any medication adjustments must be made directly by your physician or managing caregiver.",
                "tool_calls": None,
                "safety_passed": True,
            }

        # 2. Today's Reminders & Schedule
        if any(term in lower_query for term in ["what do i have today", "schedule", "routine", "what's next", "whats next"]):
            if today_reminders:
                upcoming = [r for r in today_reminders if r.get("status") in ["SCHEDULED", "SNOOZED"]]
                if upcoming:
                    items_str = ", ".join(f"{r.get('title')} at {r.get('time', 'scheduled time')}" for r in upcoming[:3])
                    return {
                        "content": f"Good day, {patient_name}! Here is what you have upcoming: {items_str}. Let me know if you'd like help with any of them!",
                        "tool_calls": None,
                        "safety_passed": True,
                    }
                else:
                    return {
                        "content": f"You're all caught up on today's scheduled tasks, {patient_name}! Everything planned for today has been completed.",
                        "tool_calls": None,
                        "safety_passed": True,
                    }
            return {
                "content": f"You don't have any pending reminders scheduled right now, {patient_name}. It's a wonderful day for a light walk or a relaxing brain game!",
                "tool_calls": None,
                "safety_passed": True,
            }

        # 3. Medicine status check
        if any(term in lower_query for term in ["did i take my medicine", "pills", "medication"]):
            med_reminders = [r for r in today_reminders if "Take" in r.get("title", "") or r.get("source_type") == "MEDICATION"]
            if med_reminders:
                taken = [r for r in med_reminders if r.get("status") == "ACKNOWLEDGED"]
                pending = [r for r in med_reminders if r.get("status") != "ACKNOWLEDGED"]
                if pending:
                    return {
                        "content": f"You still have {pending[0].get('title')} scheduled. Would you like to take it now?",
                        "tool_calls": None,
                        "safety_passed": True,
                    }
                else:
                    return {
                        "content": f"Yes, {patient_name}! All your prescribed medications for today have been recorded as taken.",
                        "tool_calls": None,
                        "safety_passed": True,
                    }
            return {
                "content": f"I don't see any active medication reminders on file for you today, {patient_name}.",
                "tool_calls": None,
                "safety_passed": True,
            }

        # 4. Cheerful Companionship & Cognitive Stimulation
        if any(term in lower_query for term in ["joke", "funny", "laugh"]):
            return {
                "content": "Why did the scarecrow win an award? Because he was outstanding in his field! I hope that brings a smile to your face today.",
                "tool_calls": None,
                "safety_passed": True,
            }

        # 5. Default Empathetic Response
        return {
            "content": f"Hello {patient_name}. I am right here with you! You can ask me about your schedule, today's medications, or play one of our daily memory exercises whenever you feel ready.",
            "tool_calls": None,
            "safety_passed": True,
        }

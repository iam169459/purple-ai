"""
Personal Assistant - Manage everything like a real assistant
Calendar, Reminders, Notes, Tasks, Files, and more
"""
import os
import json
import subprocess
import platform
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from logger import logger

class PersonalAssistant:
    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.project_root, "assistant_data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Data files
        self.calendar_file = os.path.join(self.data_dir, "calendar.json")
        self.reminders_file = os.path.join(self.data_dir, "reminders.json")
        self.notes_file = os.path.join(self.data_dir, "notes.json")
        self.tasks_file = os.path.join(self.data_dir, "tasks.json")
        self.contacts_file = os.path.join(self.data_dir, "contacts.json")
        self.shopping_file = os.path.join(self.data_dir, "shopping.json")
        self.budget_file = os.path.join(self.data_dir, "budget.json")
        self.habits_file = os.path.join(self.data_dir, "habits.json")
        self.alarms_file = os.path.join(self.data_dir, "alarms.json")
        
        # Load all data
        self.calendar = self._load_data(self.calendar_file, {"events": []})
        self.reminders = self._load_data(self.reminders_file, {"reminders": []})
        self.notes = self._load_data(self.notes_file, {"notes": []})
        self.tasks = self._load_data(self.tasks_file, {"tasks": []})
        self.contacts = self._load_data(self.contacts_file, {"contacts": []})
        self.shopping = self._load_data(self.shopping_file, {"items": []})
        self.budget = self._load_data(self.budget_file, {"transactions": [], "budgets": {}})
        self.habits = self._load_data(self.habits_file, {"habits": []})
        self.alarms = self._load_data(self.alarms_file, {"alarms": []})
        
        logger.info("Personal Assistant initialized")
    
    def _load_data(self, filepath: str, default: Any) -> Any:
        """Load data from JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
        return default
    
    def _save_data(self, filepath: str, data: Any):
        """Save data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving {filepath}: {e}")
    
    # ==================== CALENDAR ====================
    def add_event(self, title: str, date: str, time: str = None, description: str = None) -> Dict:
        """Add calendar event"""
        event = {
            "id": len(self.calendar["events"]) + 1,
            "title": title,
            "date": date,
            "time": time or "All Day",
            "description": description or "",
            "created": datetime.now().isoformat()
        }
        self.calendar["events"].append(event)
        self._save_data(self.calendar_file, self.calendar)
        return {"success": True, "message": f"Event '{title}' added for {date}"}
    
    def get_events(self, date: str = None) -> List[Dict]:
        """Get events for a date"""
        if date:
            return [e for e in self.calendar["events"] if e["date"] == date]
        return self.calendar["events"]
    
    def delete_event(self, event_id: int) -> Dict:
        """Delete event by ID"""
        for i, event in enumerate(self.calendar["events"]):
            if event["id"] == event_id:
                removed = self.calendar["events"].pop(i)
                self._save_data(self.calendar_file, self.calendar)
                return {"success": True, "message": f"Deleted event: {removed['title']}"}
        return {"success": False, "message": "Event not found"}
    
    # ==================== REMINDERS ====================
    def add_reminder(self, text: str, datetime_str: str = None) -> Dict:
        """Add reminder"""
        reminder = {
            "id": len(self.reminders["reminders"]) + 1,
            "text": text,
            "datetime": datetime_str or "When I remember",
            "completed": False,
            "created": datetime.now().isoformat()
        }
        self.reminders["reminders"].append(reminder)
        self._save_data(self.reminders_file, self.reminders)
        return {"success": True, "message": f"Reminder set: {text}"}
    
    def get_reminders(self, include_completed: bool = False) -> List[Dict]:
        """Get all reminders"""
        if include_completed:
            return self.reminders["reminders"]
        return [r for r in self.reminders["reminders"] if not r["completed"]]
    
    def complete_reminder(self, reminder_id: int) -> Dict:
        """Mark reminder as completed"""
        for reminder in self.reminders["reminders"]:
            if reminder["id"] == reminder_id:
                reminder["completed"] = True
                self._save_data(self.reminders_file, self.reminders)
                return {"success": True, "message": f"Completed: {reminder['text']}"}
        return {"success": False, "message": "Reminder not found"}
    
    def delete_reminder(self, reminder_id: int) -> Dict:
        """Delete reminder"""
        for i, reminder in enumerate(self.reminders["reminders"]):
            if reminder["id"] == reminder_id:
                removed = self.reminders["reminders"].pop(i)
                self._save_data(self.reminders_file, self.reminders)
                return {"success": True, "message": f"Deleted: {removed['text']}"}
        return {"success": False, "message": "Reminder not found"}
    
    # ==================== NOTES ====================
    def add_note(self, title: str, content: str, tags: List[str] = None) -> Dict:
        """Add note"""
        note = {
            "id": len(self.notes["notes"]) + 1,
            "title": title,
            "content": content,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
        self.notes["notes"].append(note)
        self._save_data(self.notes_file, self.notes)
        return {"success": True, "message": f"Note '{title}' created"}
    
    def get_notes(self, search: str = None) -> List[Dict]:
        """Get notes, optionally filtered by search"""
        notes = self.notes["notes"]
        if search:
            search_lower = search.lower()
            notes = [n for n in notes if search_lower in n["title"].lower() or search_lower in n["content"].lower()]
        return notes
    
    def update_note(self, note_id: int, title: str = None, content: str = None) -> Dict:
        """Update note"""
        for note in self.notes["notes"]:
            if note["id"] == note_id:
                if title:
                    note["title"] = title
                if content:
                    note["content"] = content
                note["modified"] = datetime.now().isoformat()
                self._save_data(self.notes_file, self.notes)
                return {"success": True, "message": "Note updated"}
        return {"success": False, "message": "Note not found"}
    
    def delete_note(self, note_id: int) -> Dict:
        """Delete note"""
        for i, note in enumerate(self.notes["notes"]):
            if note["id"] == note_id:
                removed = self.notes["notes"].pop(i)
                self._save_data(self.notes_file, self.notes)
                return {"success": True, "message": f"Deleted note: {removed['title']}"}
        return {"success": False, "message": "Note not found"}
    
    # ==================== TASKS ====================
    def add_task(self, title: str, priority: str = "medium", due_date: str = None) -> Dict:
        """Add task"""
        task = {
            "id": len(self.tasks["tasks"]) + 1,
            "title": title,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created": datetime.now().isoformat()
        }
        self.tasks["tasks"].append(task)
        self._save_data(self.tasks_file, self.tasks)
        return {"success": True, "message": f"Task '{title}' added"}
    
    def get_tasks(self, include_completed: bool = False) -> List[Dict]:
        """Get tasks"""
        if include_completed:
            return self.tasks["tasks"]
        return [t for t in self.tasks["tasks"] if not t["completed"]]
    
    def complete_task(self, task_id: int) -> Dict:
        """Complete task"""
        for task in self.tasks["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                self._save_data(self.tasks_file, self.tasks)
                return {"success": True, "message": f"Completed: {task['title']}"}
        return {"success": False, "message": "Task not found"}
    
    def delete_task(self, task_id: int) -> Dict:
        """Delete task"""
        for i, task in enumerate(self.tasks["tasks"]):
            if task["id"] == task_id:
                removed = self.tasks["tasks"].pop(i)
                self._save_data(self.tasks_file, self.tasks)
                return {"success": True, "message": f"Deleted: {removed['title']}"}
        return {"success": False, "message": "Task not found"}
    
    # ==================== CONTACTS ====================
    def add_contact(self, name: str, phone: str = None, email: str = None, notes: str = None) -> Dict:
        """Add contact"""
        contact = {
            "id": len(self.contacts["contacts"]) + 1,
            "name": name,
            "phone": phone,
            "email": email,
            "notes": notes,
            "created": datetime.now().isoformat()
        }
        self.contacts["contacts"].append(contact)
        self._save_data(self.contacts_file, self.contacts)
        return {"success": True, "message": f"Contact '{name}' added"}
    
    def get_contacts(self, search: str = None) -> List[Dict]:
        """Get contacts"""
        contacts = self.contacts["contacts"]
        if search:
            search_lower = search.lower()
            contacts = [c for c in contacts if search_lower in c["name"].lower()]
        return contacts
    
    def delete_contact(self, contact_id: int) -> Dict:
        """Delete contact"""
        for i, contact in enumerate(self.contacts["contacts"]):
            if contact["id"] == contact_id:
                removed = self.contacts["contacts"].pop(i)
                self._save_data(self.contacts_file, self.contacts)
                return {"success": True, "message": f"Deleted contact: {removed['name']}"}
        return {"success": False, "message": "Contact not found"}
    
    # ==================== SHOPPING ====================
    def add_shopping_item(self, item: str, quantity: str = "1") -> Dict:
        """Add shopping item"""
        shopping_item = {
            "id": len(self.shopping["items"]) + 1,
            "item": item,
            "quantity": quantity,
            "purchased": False,
            "added": datetime.now().isoformat()
        }
        self.shopping["items"].append(shopping_item)
        self._save_data(self.shopping_file, self.shopping)
        return {"success": True, "message": f"Added '{item}' to shopping list"}
    
    def get_shopping_list(self, include_purchased: bool = False) -> List[Dict]:
        """Get shopping list"""
        if include_purchased:
            return self.shopping["items"]
        return [i for i in self.shopping["items"] if not i["purchased"]]
    
    def complete_shopping_item(self, item_id: int) -> Dict:
        """Mark shopping item as purchased"""
        for item in self.shopping["items"]:
            if item["id"] == item_id:
                item["purchased"] = True
                self._save_data(self.shopping_file, self.shopping)
                return {"success": True, "message": f"Purchased: {item['item']}"}
        return {"success": False, "message": "Item not found"}
    
    def clear_shopping_list(self) -> Dict:
        """Clear purchased items"""
        self.shopping["items"] = [i for i in self.shopping["items"] if not i["purchased"]]
        self._save_data(self.shopping_file, self.shopping)
        return {"success": True, "message": "Shopping list cleared"}
    
    # ==================== BUDGET ====================
    def add_transaction(self, amount: float, category: str, description: str, transaction_type: str = "expense") -> Dict:
        """Add financial transaction"""
        transaction = {
            "id": len(self.budget["transactions"]) + 1,
            "amount": amount,
            "category": category,
            "description": description,
            "type": transaction_type,
            "date": datetime.now().isoformat()
        }
        self.budget["transactions"].append(transaction)
        self._save_data(self.budget_file, self.budget)
        return {"success": True, "message": f"Added {transaction_type}: ${amount} for {description}"}
    
    def get_transactions(self, category: str = None) -> List[Dict]:
        """Get transactions"""
        if category:
            return [t for t in self.budget["transactions"] if t["category"] == category]
        return self.budget["transactions"]
    
    def get_budget_summary(self) -> Dict:
        """Get budget summary"""
        income = sum(t["amount"] for t in self.budget["transactions"] if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.budget["transactions"] if t["type"] == "expense")
        return {
            "income": income,
            "expenses": expenses,
            "balance": income - expenses
        }
    
    # ==================== HABITS ====================
    def add_habit(self, name: str, frequency: str = "daily") -> Dict:
        """Add habit to track"""
        habit = {
            "id": len(self.habits["habits"]) + 1,
            "name": name,
            "frequency": frequency,
            "streak": 0,
            "last_completed": None,
            "created": datetime.now().isoformat()
        }
        self.habits["habits"].append(habit)
        self._save_data(self.habits_file, self.habits)
        return {"success": True, "message": f"Tracking habit: {name}"}
    
    def get_habits(self) -> List[Dict]:
        """Get all habits"""
        return self.habits["habits"]
    
    def complete_habit(self, habit_id: int) -> Dict:
        """Mark habit as completed today"""
        for habit in self.habits["habits"]:
            if habit["id"] == habit_id:
                habit["streak"] += 1
                habit["last_completed"] = datetime.now().isoformat()
                self._save_data(self.habits_file, self.habits)
                return {"success": True, "message": f"Completed: {habit['name']}. Streak: {habit['streak']}"}
        return {"success": False, "message": "Habit not found"}
    
    # ==================== ALARMS ====================
    def add_alarm(self, time: str, label: str = None) -> Dict:
        """Add alarm"""
        alarm = {
            "id": len(self.alarms["alarms"]) + 1,
            "time": time,
            "label": label or "Alarm",
            "enabled": True,
            "created": datetime.now().isoformat()
        }
        self.alarms["alarms"].append(alarm)
        self._save_data(self.alarms_file, self.alarms)
        return {"success": True, "message": f"Alarm set for {time}"}
    
    def get_alarms(self) -> List[Dict]:
        """Get all alarms"""
        return self.alarms["alarms"]
    
    def delete_alarm(self, alarm_id: int) -> Dict:
        """Delete alarm"""
        for i, alarm in enumerate(self.alarms["alarms"]):
            if alarm["id"] == alarm_id:
                removed = self.alarms["alarms"].pop(i)
                self._save_data(self.alarms_file, self.alarms)
                return {"success": True, "message": f"Deleted alarm: {removed['time']}"}
        return {"success": False, "message": "Alarm not found"}
    
    # ==================== UTILITY ====================
    def calculate(self, expression: str) -> Dict:
        """Calculate mathematical expression"""
        try:
            # Basic math operations
            allowed_chars = set('0123456789+-*/().% ')
            if not all(c in allowed_chars for c in expression):
                return {"success": False, "message": "Invalid characters in expression"}
            
            result = eval(expression)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "message": f"Error calculating: {e}"}
    
    def convert_units(self, value: float, from_unit: str, to_unit: str) -> Dict:
        """Convert between units"""
        conversions = {
            ("km", "miles"): lambda x: x * 0.621371,
            ("miles", "km"): lambda x: x * 1.60934,
            ("kg", "lbs"): lambda x: x * 2.20462,
            ("lbs", "kg"): lambda x: x * 0.453592,
            ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("liters", "gallons"): lambda x: x * 0.264172,
            ("gallons", "liters"): lambda x: x * 3.78541,
            ("cm", "inches"): lambda x: x * 0.393701,
            ("inches", "cm"): lambda x: x * 2.54,
        }
        
        key = (from_unit.lower(), to_unit.lower())
        if key in conversions:
            result = conversions[key](value)
            return {"success": True, "result": result}
        return {"success": False, "message": f"Conversion from {from_unit} to {to_unit} not supported"}
    
    def get_daily_summary(self) -> str:
        """Get daily summary of all activities"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        summary = []
        summary.append(f"Daily Summary for {today}:\n")
        
        # Events
        events = self.get_events(today)
        if events:
            summary.append(f"📅 Events ({len(events)}):")
            for event in events:
                summary.append(f"  - {event['title']} at {event['time']}")
        
        # Reminders
        reminders = self.get_reminders()
        if reminders:
            summary.append(f"\n⏰ Reminders ({len(reminders)}):")
            for reminder in reminders[:3]:
                summary.append(f"  - {reminder['text']}")
        
        # Tasks
        tasks = self.get_tasks()
        if tasks:
            summary.append(f"\n✅ Tasks ({len(tasks)} pending):")
            for task in tasks[:3]:
                summary.append(f"  - {task['title']} ({task['priority']})")
        
        # Habits
        habits = self.get_habits()
        if habits:
            summary.append(f"\n🎯 Habits ({len(habits)}):")
            for habit in habits[:3]:
                summary.append(f"  - {habit['name']}: {habit['streak']} day streak")
        
        # Budget
        budget = self.get_budget_summary()
        if budget['income'] > 0 or budget['expenses'] > 0:
            summary.append(f"\n💰 Budget:")
            summary.append(f"  Income: ${budget['income']:.2f}")
            summary.append(f"  Expenses: ${budget['expenses']:.2f}")
            summary.append(f"  Balance: ${budget['balance']:.2f}")
        
        return '\n'.join(summary) if len(summary) > 1 else "No activities recorded for today."


# Global instance
personal_assistant = PersonalAssistant()

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from pathlib import Path
from config.settings import DEADLINES_DIR


class DeadlineTracker:
    def __init__(self):
        self.deadlines_file = DEADLINES_DIR / "deadlines.json"
        self.deadlines = self._load_deadlines()

    def _load_deadlines(self):
        """Load deadlines from storage"""
        if self.deadlines_file.exists():
            with open(self.deadlines_file, 'r') as f:
                return json.load(f)
        return []

    def _save_deadlines(self):
        """Save deadlines to storage"""
        with open(self.deadlines_file, 'w') as f:
            json.dump(self.deadlines, f, indent=2)

    def render(self):
        """Render the deadline tracker interface"""
        st.subheader("📅 Research Deadlines")

        # Add new deadline
        with st.expander("➕ Add New Deadline"):
            self._render_add_deadline()

        # Display deadlines
        self._render_deadlines_list()

        # Upcoming deadlines alert
        self._render_upcoming_alerts()

    def _render_add_deadline(self):
        """Render add deadline form"""
        with st.form("add_deadline"):
            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Title", placeholder="Conference submission")
                deadline_date = st.date_input("Deadline Date", value=datetime.now() + timedelta(days=30))
                deadline_time = st.time_input("Deadline Time", value=datetime.now().time())

            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                category = st.selectbox("Category", ["Conference", "Journal", "Grant", "Review", "Other"])
                reminder_days = st.number_input("Reminder (days before)", min_value=1, max_value=365, value=7)

            description = st.text_area("Description", placeholder="Additional details about this deadline...")

            if st.form_submit_button("Add Deadline"):
                if title and deadline_date:
                    deadline = {
                        'id': f"deadline_{len(self.deadlines) + 1}",
                        'title': title,
                        'date': deadline_date.isoformat(),
                        'time': deadline_time.isoformat(),
                        'priority': priority,
                        'category': category,
                        'description': description,
                        'reminder_days': reminder_days,
                        'created_at': datetime.now().isoformat(),
                        'completed': False
                    }

                    self.deadlines.append(deadline)
                    self._save_deadlines()
                    st.success("Deadline added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")

    def _render_deadlines_list(self):
        """Render list of deadlines"""
        if not self.deadlines:
            st.info("No deadlines added yet. Click 'Add New Deadline' to get started.")
            return

        # Filter options
        col1, col2, col3 = st.columns(3)

        with col1:
            show_completed = st.checkbox("Show completed", value=False)

        with col2:
            filter_category = st.selectbox("Filter by category",
                                           ["All"] + ["Conference", "Journal", "Grant", "Review", "Other"])

        with col3:
            sort_by = st.selectbox("Sort by", ["Date", "Priority", "Title"])

        # Filter deadlines
        filtered_deadlines = self.deadlines.copy()

        if not show_completed:
            filtered_deadlines = [d for d in filtered_deadlines if not d['completed']]

        if filter_category != "All":
            filtered_deadlines = [d for d in filtered_deadlines if d['category'] == filter_category]

        # Sort deadlines
        if sort_by == "Date":
            filtered_deadlines.sort(key=lambda x: x['date'])
        elif sort_by == "Priority":
            priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
            filtered_deadlines.sort(key=lambda x: priority_order.get(x['priority'], 4))
        else:  # Title
            filtered_deadlines.sort(key=lambda x: x['title'])

        # Display deadlines
        for deadline in filtered_deadlines:
            self._render_deadline_card(deadline)

    def _render_deadline_card(self, deadline):
        """Render individual deadline card"""
        deadline_date = datetime.fromisoformat(deadline['date'])
        days_until = (deadline_date - datetime.now()).days

        # Determine card color based on urgency
        if days_until < 0:
            card_color = "#ffebee"  # Red for overdue
            status_emoji = "🔴"
        elif days_until <= 3:
            card_color = "#fff3e0"  # Orange for urgent
            status_emoji = "🟠"
        elif days_until <= 7:
            card_color = "#f3e5f5"  # Yellow for soon
            status_emoji = "🟡"
        else:
            card_color = "#e8f5e8"  # Green for future
            status_emoji = "🟢"

        with st.container():
            st.markdown(f"""
            <div style="background-color: {card_color}; padding: 1rem; border-radius: 8px; margin: 1rem 0; color: #333;">
                <h4>{status_emoji} {deadline['title']}</h4>
                <p><strong>Date:</strong> {deadline_date.strftime('%B %d, %Y')}</p>
                <p><strong>Priority:</strong> {deadline['priority']} | <strong>Category:</strong> {deadline['category']}</p>
                <p><strong>Days until:</strong> {days_until} days</p>
                {f"<p><strong>Description:</strong> {deadline['description']}</p>" if deadline['description'] else ""}
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("✅ Complete", key=f"complete_{deadline['id']}"):
                    self._complete_deadline(deadline['id'])

            with col2:
                if st.button("✏️ Edit", key=f"edit_{deadline['id']}"):
                    self._edit_deadline(deadline['id'])

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{deadline['id']}"):
                    self._delete_deadline(deadline['id'])

    def _render_upcoming_alerts(self):
        """Render upcoming deadline alerts"""
        upcoming = []
        for deadline in self.deadlines:
            if deadline['completed']:
                continue

            deadline_date = datetime.fromisoformat(deadline['date'])
            days_until = (deadline_date - datetime.now()).days

            if days_until <= deadline['reminder_days']:
                upcoming.append((deadline, days_until))

        if upcoming:
            st.subheader("⚠️ Upcoming Deadlines")

            for deadline, days_until in upcoming:
                if days_until < 0:
                    st.error(f"🔴 OVERDUE: {deadline['title']} was due {abs(days_until)} days ago!")
                elif days_until == 0:
                    st.warning(f"🟠 DUE TODAY: {deadline['title']}")
                else:
                    st.info(f"🟡 {deadline['title']} is due in {days_until} days")

    def _complete_deadline(self, deadline_id):
        """Mark deadline as completed"""
        for deadline in self.deadlines:
            if deadline['id'] == deadline_id:
                deadline['completed'] = True
                deadline['completed_at'] = datetime.now().isoformat()
                break

        self._save_deadlines()
        st.success("Deadline marked as completed!")
        st.rerun()

    def _edit_deadline(self, deadline_id):
        """Edit deadline (placeholder for now)"""
        st.info("Edit functionality coming soon!")

    def _delete_deadline(self, deadline_id):
        """Delete deadline"""
        self.deadlines = [d for d in self.deadlines if d['id'] != deadline_id]
        self._save_deadlines()
        st.success("Deadline deleted successfully!")
        st.rerun()
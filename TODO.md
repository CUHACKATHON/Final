# 1-Minute Anonymous Check-in Feature Implementation

## Step 1: The Hook (Homepage UI)
- [ ] Add check-in section to index.html template
- [ ] Include "Aap abhi kaisa mehsoos kar rahe hain?" heading
- [ ] Add "Start 1-Min Check-in" button with anonymity note
- [ ] Style the section appropriately

## Step 2: Interactive Quiz Module
- [ ] Add URL pattern for check-in quiz in core/urls.py
- [ ] Create checkin_view function in core/views.py
- [ ] Create checkin.html template with quiz interface
- [ ] Implement JavaScript for one-question-at-a-time display
- [ ] Add questions with options and point values

## Step 3: Scoring Logic (Backend)
- [ ] Create checkin_api view for processing quiz responses
- [ ] Implement scoring calculation (sum of points)
- [ ] Add bucketing logic (0-4: Green, 5-9: Yellow, 10-15: Red)
- [ ] Store results in session or database

## Step 4: Dynamic Result Dashboard
- [ ] Create checkin_results.html template
- [ ] Implement conditional display based on score bucket
- [ ] Add appropriate buttons for each bucket:
  - Bucket 1: Resource Hub, Home
  - Bucket 2: AI Chatbot, Peer Support Forum
  - Bucket 3: AI Chatbot (Recommended), Psychiatrist Appointment
- [ ] Add URL patterns for results page

## Additional Tasks
- [ ] Update static files (CSS/JS) if needed
- [ ] Test the complete flow
- [ ] Ensure mobile responsiveness

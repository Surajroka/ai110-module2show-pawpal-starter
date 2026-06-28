# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design lets an owner create an account and add pets to manage. 
Pet stores information about each pet the owner adds along with the health notes.
We have a task section about what the task is done and what is needed to be done along with a scheduler to plan what to do in the future.

I have classes listed as Owner to represent  pet owner and manage their pet, Pet class as it stores information about the pet , Task as parent class for child class as Feeding, Walk, medication, appointment, all related to pet activities and a scheduler.

Owner Class with attributes Owner-id, name, email, pets
Pets Class with attributes pet_id, name, species, breed, age, health_note, tasks
Task class with attributes task_id, title, description of the task, due_time, priority, completed
Feeding	attributes food_type, quantity, feeding_time	
Walk	attributes duration_minutes, location, walk_time	
Medication	attributes medicine_name, dosage, instructions, medication_time
Appointment	attributes appointment_type, vet_name, location, appointment_date	
Scheduler	attributes task_list, priority_queue

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

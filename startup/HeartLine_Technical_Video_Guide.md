# HeartLine Platform - Technical Video Presentation Guide
## 4-5 Minute Demo Based on Real Implementation

---

## **Video Overview**
**Duration:** 4 minutes 45 seconds  
**Format:** Screen recording with professional voice-over  
**Resolution:** 1080p (1920x1080)  
**Target Audience:** Medical professionals, investors, healthcare institutions

**Key Differentiators:**
- Based on actual Flask application code and PostgreSQL database
- Real ONNX-powered ResNet-34 AI model for ECG analysis
- Complete practice management integration
- Algerian pharmaceutical database (7,000+ medications)
- Role-based access control for doctors and assistants

---

## **Scene 1: Login & Authentication (0:00 - 0:30)**

### **Technical Implementation:**
- Flask-Login authentication system
- Role-based access control (Doctor/Assistant)
- PostgreSQL user management
- Session persistence with Flask-Session

### **Visual Elements:**
- Clean login interface at `/login` route
- Username/password authentication form
- "Remember Me" checkbox functionality
- Error handling for invalid credentials

### **Script with Precise Actions:**

**[0:00-0:03]** *"Welcome to HeartLine"*
- **Mouse Action:** Start with browser open, cursor hovering over address bar
- **Action:** Type `localhost:5000/login` and press Enter
- **Visual:** Show page loading animation

**[0:03-0:08]** *"Algeria's first AI-powered cardiac practice management platform"*
- **Mouse Action:** Cursor slowly moves across the login form elements
- **Action:** Highlight the HeartLine logo at top of page
- **Visual:** Clean Bootstrap 4 interface loads completely

**[0:08-0:15]** *"Our system integrates complete practice workflows with advanced ECG clinical decision support"*
- **Mouse Action:** Click on username field
- **Action:** Type `dr.benali@heartline.dz` slowly (visible typing)
- **Visual:** Show form field validation (blue border highlight)

**[0:15-0:22]** *"Let me demonstrate our live production platform"*
- **Mouse Action:** Click on password field
- **Action:** Type password (show asterisks), then hover over "Remember Me" checkbox
- **Visual:** Cursor hovers over login button

**[0:22-0:30]** *(Complete login process)*
- **Mouse Action:** Click "Sign In" button
- **Action:** Show brief loading spinner, flash success message appears
- **Visual:** Smooth redirect animation to dashboard

### **Technical Notes:**
- Show HTTPS connection (security indicator in address bar)
- Display session management (show in Network tab)
- Demonstrate responsive design (briefly resize window)

---

## **Scene 2: Doctor Dashboard - Real-time Analytics (0:30 - 1:15)**

### **Technical Implementation:**
- Real-time dashboard with PostgreSQL queries
- Chart.js visualizations for patient metrics
- AJAX endpoints for live data updates
- Moment.js for time formatting

### **Visual Elements:**
- Gradient sidebar with collapsible navigation
- Statistics cards with Bootstrap 4 styling
- Real-time clock and welcome message
- Quick action buttons with Font Awesome icons

### **Script with Precise Actions:**

**[0:30-0:38]** *"The HeartLine dashboard provides doctors with comprehensive practice insights"*
- **Mouse Action:** Cursor enters from left, moves to welcome header
- **Action:** Highlight "Welcome back, Dr. Benali" section
- **Visual:** Show gradient header with real-time clock updating

**[0:38-0:45]** *"You see real-time statistics pulled directly from our PostgreSQL database"*
- **Mouse Action:** Cursor moves to first statistics card (Total Patients)
- **Action:** Hover over "247" number, show subtle animation
- **Visual:** Number counter animation effect

**[0:45-0:52]** *"total patients, today's visits, ECG analyses completed"*
- **Mouse Action:** Move cursor across statistics cards in sequence
- **Action:** Hover over each card: Patients → Today's Visits → ECG Tests → Avg Time
- **Visual:** Cards have hover effect (slight elevation shadow)

**[0:52-1:00]** *"The interface adapts to your role, showing relevant quick actions"*
- **Mouse Action:** Scroll down smoothly to Quick Actions section
- **Action:** Hover over "New Patient" button
- **Visual:** Button shows hover state with gradient effect

**[1:00-1:08]** *"and performance metrics"*
- **Mouse Action:** Move to sidebar, click sidebar collapse button
- **Action:** Demonstrate sidebar collapse/expand animation
- **Visual:** Sidebar width animates, content area adjusts

**[1:08-1:15]** *(Complete dashboard overview)*
- **Mouse Action:** Scroll down to show Today's Schedule widget
- **Action:** Hover over appointment entries, show calendar view
- **Visual:** Show AJAX loading indicator briefly

### **Technical Notes:**
- Show live database queries in Network tab (F12 briefly)
- Demonstrate AJAX data loading with loading spinners
- Display responsive breakpoints (briefly resize window)

---

## **Scene 3: Patient Management - Advanced Search & Registration (1:15 - 2:00)**

### **Technical Implementation:**
- Advanced patient search with SQLAlchemy ORM
- Auto-complete patient lookup
- Comprehensive registration forms with WTForms
- Real-time form validation

### **Visual Elements:**
- Searchable patient table with DataTables
- Patient registration form with Bootstrap validation
- Patient profile with visit history timeline
- Document attachment system

### **Script with Precise Actions:**

**[1:15-1:23]** *"Patient management in HeartLine leverages advanced search capabilities"*
- **Mouse Action:** Click on "Patients" in sidebar navigation
- **Action:** Navigate to `/patients` route, page loads
- **Visual:** Show patients table loading with pagination

**[1:23-1:30]** *"with our PostgreSQL database. The auto-complete search function"*
- **Mouse Action:** Click on search box at top of patients table
- **Action:** Type "Amira" slowly (letter by letter)
- **Visual:** Show search suggestions dropdown appearing

**[1:30-1:37]** *"instantly finds patients as you type"*
- **Mouse Action:** Hover over "Amira Boumediene" in dropdown
- **Action:** Click on patient name from suggestions
- **Visual:** Table filters immediately to show matching patient

**[1:37-1:44]** *"Our registration system captures comprehensive demographic"*
- **Mouse Action:** Click "New Patient" button in top right
- **Action:** Navigate to `/patient/new` form
- **Visual:** Patient registration form loads with empty fields

**[1:44-1:52]** *"and medical history data with real-time validation"*
- **Mouse Action:** Fill form fields in sequence:
- **Action:** 
  - Click First Name → Type "Ahmed"
  - Click Last Name → Type "Mansouri"  
  - Click DOB field → Select 1978-03-15 from date picker
- **Visual:** Show validation checkmarks appearing as fields are completed

**[1:52-2:00]** *(Complete patient creation)*
- **Mouse Action:** Continue filling form:
- **Action:**
  - Select "Male" from Gender dropdown
  - Type phone "+213 555 123 456"
  - Fill address "Rue Didouche Mourad, Algiers"
  - Click "Save Patient" button
- **Visual:** Show success message and redirect to patient profile

### **Technical Notes:**
- Show form validation in real-time (green borders for valid fields)
- Demonstrate database saves (loading spinner on save button)
- Display file upload capabilities (hover over upload areas)

---

## **Scene 4: AI ECG Analysis - ONNX Model in Action (2:00 - 3:00)**

### **Technical Implementation:**
- ONNX Runtime inference with ResNet-34 model
- Real-time ECG file processing (.mat/.hea)
- WFDB Python library for signal processing
- 9-class cardiac condition detection

### **Visual Elements:**
- ECG file upload interface with drag-and-drop
- Real-time analysis progress indicators
- Detailed results with confidence scores
- ECG waveform visualization with SVG rendering

### **Script with Precise Actions:**

**[2:00-2:08]** *"Here's where HeartLine's AI technology truly shines"*
- **Mouse Action:** Click "New Visit" in sidebar navigation
- **Action:** Navigate to `/visit/new` route
- **Visual:** Visit creation form loads with all sections visible

**[2:08-2:15]** *"Our ONNX-optimized ResNet-34 model analyzes standard ECG files"*
- **Mouse Action:** Click on patient search field
- **Action:** Type "Fatima Khalil" in patient auto-complete
- **Visual:** Patient dropdown appears, select patient

**[2:15-2:22]** *"in under 2 seconds. The system processes 12-lead ECG data"*
- **Mouse Action:** Click on visit date/time field
- **Action:** Select current date and time from datetime picker
- **Visual:** Calendar widget opens and closes

**[2:22-2:30]** *"and provides confidence scores for 9 different cardiac conditions"*
- **Mouse Action:** Scroll down to ECG upload section
- **Action:** Type "Routine cardiac evaluation" in diagnosis field
- **Visual:** Focus on ECG file upload area

**[2:30-2:38]** *"serving as a clinical decision support tool for cardiologists"*
- **Mouse Action:** Drag and drop first file over ECG .mat upload area
- **Action:** Drop `record_001.mat` file, show upload progress bar
- **Visual:** File upload progress animation, file name appears

**[2:38-2:45]** *(Upload second file)*
- **Mouse Action:** Drag and drop second file over ECG .hea upload area  
- **Action:** Drop `record_001.hea` file, show matching basename validation
- **Visual:** Both files show as uploaded with green checkmarks

**[2:45-2:52]** *(AI Analysis begins)*
- **Mouse Action:** Click "Save Visit" button
- **Action:** Form submits, show "Analyzing ECG..." loading spinner
- **Visual:** ONNX model processing indicator with rotating animation

**[2:52-3:00]** *(Results display)*
- **Mouse Action:** Cursor moves to results area as they appear
- **Action:** Results populate automatically:
  - Primary: Atrial Fibrillation (89.7%)
  - Secondary findings with percentages
- **Visual:** Confidence bars animate to show percentages, ECG waveform renders

### **Technical Notes:**
- Show actual ONNX model loading message in console
- Demonstrate file validation (matching basenames required)
- Display processing speed metrics (< 2 seconds timer)
- Show confidence calculation methods in progress bars

---

## **Scene 5: Prescription Management - Algerian Pharmaceutical Database (3:00 - 3:30)**

### **Technical Implementation:**
- 7,000+ Algerian medication database
- Select2 AJAX search with autocomplete
- PostgreSQL full-text search
- Multi-prescription visit support

### **Visual Elements:**
- Smart medication search with autocomplete
- Prescription form with dosage instructions
- Multiple prescriptions per visit
- Printable prescription generation

### **Script with Precise Actions:**

**[3:00-3:06]** *"HeartLine includes Algeria's most comprehensive pharmaceutical database"*
- **Mouse Action:** Scroll down to Prescriptions section within visit form
- **Action:** Click on first prescription medication search field
- **Visual:** Focus on prescription row with medication dropdown

**[3:06-3:12]** *"with over 7,000 local medications. Our intelligent search system"*
- **Mouse Action:** Type "Amlo" in medication search field
- **Action:** Show real-time search suggestions appearing
- **Visual:** Select2 dropdown opens with autocomplete results

**[3:12-3:18]** *"supports both commercial and generic names"*
- **Mouse Action:** Hover over "AMLODIPINE 5MG - Amlodipine - 5mg" option
- **Action:** Click to select medication from dropdown
- **Visual:** Medication populates with full details

**[3:18-3:24]** *"making prescription creation fast and accurate for Algerian medical practice"*
- **Mouse Action:** Click in dosage instructions field
- **Action:** Type "1 comprimé une fois par jour le matin"
- **Visual:** Text appears in bilingual format (French/Arabic support shown)

**[3:24-3:30]** *(Complete prescription)*
- **Mouse Action:** Click quantity field → type "30"
- **Action:** Click "Add Prescription" button to add second medication
- **Visual:** New prescription row appears, fill with Aspirin 100mg

### **Technical Notes:**
- Show AJAX medication lookup with network activity
- Demonstrate database performance (search results < 200ms)
- Display pharmaceutical validation (dosage format checking)

---

## **Scene 6: Complete Workflow Integration (3:30 - 4:15)**

### **Technical Implementation:**
- Integrated document management system
- Appointment scheduling with calendar
- Payment tracking with multiple status
- Visit timeline with relationship mapping

### **Visual Elements:**
- File upload for blood work, MRI, X-rays
- Calendar widget for appointments
- Payment status tracking
- Visit summary with all related data

### **Script with Precise Actions:**

**[3:30-3:37]** *"HeartLine seamlessly integrates every aspect of cardiology practice management"*
- **Mouse Action:** Scroll down to Documents section in visit form
- **Action:** Click on document type dropdown in first document row
- **Visual:** Show document type options (Blood Work, MRI, X-Ray)

**[3:37-3:43]** *"Upload and organize diagnostic documents"*
- **Mouse Action:** Select "Blood Work" from dropdown
- **Action:** Click "Choose File" button for document upload
- **Visual:** File browser opens, select blood_results.pdf

**[3:43-3:50]** *"schedule follow-up appointments with our calendar system"*
- **Mouse Action:** Scroll down to Payment & Follow-up section
- **Action:** Click on follow-up date field
- **Visual:** Calendar widget opens, select date two weeks in future

**[3:50-3:57]** *"track payments in Algerian Dinars"*
- **Mouse Action:** Click on payment total field
- **Action:** Type "15000" in payment total field
- **Visual:** Currency formatter shows "15,000.00 DZD"

**[3:57-4:05]** *"and maintain complete visit histories"*
- **Mouse Action:** Select "Partial" from payment status dropdown
- **Action:** Type "5000" in remaining payment field
- **Visual:** Payment calculation updates automatically

**[4:05-4:15]** *"Everything connects through our relational database architecture"*
- **Mouse Action:** Click "Save Visit" button
- **Action:** Complete form submission with loading animation
- **Visual:** Redirect to visit details page showing all connected information

### **Technical Notes:**
- Show database relationships in visit details view
- Demonstrate file storage system (files saved to uploads directory)
- Display currency formatting (DZD with proper comma separation)

---

## **Scene 7: ECG History & Analytics (4:15 - 4:45)**

### **Technical Implementation:**
- Advanced ECG history table with filtering
- PostgreSQL analytical queries
- Export functionality to CSV
- Statistical analysis of ECG trends

### **Visual Elements:**
- Comprehensive ECG history table
- Filter controls for diagnosis, confidence, dates
- Summary statistics cards
- Export and reporting capabilities

### **Script with Precise Actions:**

**[4:15-4:21]** *"HeartLine provides comprehensive ECG analytics"*
- **Mouse Action:** Click "ECG History" in sidebar navigation
- **Action:** Navigate to `/ecg_history` route
- **Visual:** ECG history table loads with all analyses

**[4:21-4:27]** *"to track practice performance and patient outcomes"*
- **Mouse Action:** Hover over summary statistics cards at top
- **Action:** Highlight total ECGs, normal vs abnormal counts
- **Visual:** Statistics cards show hover effects with animations

**[4:27-4:33]** *"Filter and analyze ECG results by diagnosis type, confidence levels"*
- **Mouse Action:** Click "Toggle Filters" button
- **Action:** Expand filters section, click diagnosis dropdown
- **Visual:** Filter controls expand, show diagnosis options

**[4:33-4:39]** *"and date ranges"*
- **Mouse Action:** Select "Atrial Fibrillation" from diagnosis filter
- **Action:** Set minimum confidence to "≥ 80%"
- **Visual:** Table updates in real-time showing filtered results

**[4:39-4:45]** *"Export data for research and regulatory compliance"*
- **Mouse Action:** Click "Export" button
- **Action:** CSV download begins automatically
- **Visual:** Download progress in browser, file saves to downloads folder

### **Technical Notes:**
- Show database query performance (loading indicators)
- Demonstrate real-time filtering (AJAX updates)
- Display export functionality (actual file download)

---

## **Closing (4:45)**

### **Script with Precise Actions:**

**[4:45-4:50]** *"HeartLine represents the future of cardiac practice management in Algeria"*
- **Mouse Action:** Cursor moves to center of screen
- **Action:** Begin screen fade transition
- **Visual:** Current page content starts to fade out

**[4:50-4:55]** *"combining proven AI technology with comprehensive practice workflows"*
- **Mouse Action:** No mouse movement (stationary)
- **Action:** Contact information overlay begins to appear
- **Visual:** HeartLine logo fades in at center

**[4:55-5:00]** *"Ready to transform your cardiology practice? Contact HeartLine today."*
- **Mouse Action:** Cursor highlights contact details one by one
- **Action:** Contact information fully visible:
  - Website: www.heartline.dz
  - Email: contact@heartline.dz  
  - Phone: +213 XX XXX XXXX
- **Visual:** Professional fade to HeartLine logo with gradient background

### **Visual Elements:**
- Contact information overlay with fade-in animation
- HeartLine logo prominently displayed
- Professional gradient background (matches app theme)
- Clean typography for contact details
- Smooth fade-out to black screen

---

## **Production Guidelines - Technical Specifications**

### **Recording Environment:**
- **Development Server:** Local Flask development server
- **Database:** PostgreSQL with sample data
- **Screen Resolution:** 1920x1080 (1080p)
- **Browser:** Chrome with developer tools available
- **Frame Rate:** 30 fps
- **Audio:** Professional voice-over in clear English

### **Sample Data Requirements:**
**Patients (15-20 realistic Algerian profiles):**
- Ahmed Mansouri, DOB: 1978-03-15, Algiers
- Fatima Khalil, DOB: 1985-09-22, Oran  
- Karim Benali, DOB: 1970-12-08, Constantine
- Amira Boumediene, DOB: 1992-05-17, Annaba
- Omar Zeroual, DOB: 1965-04-30, Tlemcen

**ECG Files (4-5 different conditions):**
- Normal Sinus Rhythm (SNR): record_001.mat/.hea
- Atrial Fibrillation (AF): record_002.mat/.hea
- Left Bundle Branch Block (LBBB): record_003.mat/.hea
- ST Elevation (STE): record_004.mat/.hea

**Medications (Real Algerian pharmaceuticals):**
- AMLODIPINE 5MG - Norvasc generics
- ASPIRIN 100MG - Cardioaspirin
- ATENOLOL 50MG - Beta-blocker
- SIMVASTATINE 20MG - Statin
- LISINOPRIL 10MG - ACE inhibitor

**Currency & Localization:**
- All amounts in DZD (Algerian Dinars)
- Addresses in Algerian cities
- Phone numbers: +213 format
- Interface elements in French/Arabic as appropriate

### **Technical Demonstration Points:**
**Performance Metrics:**
- ECG Analysis Speed: <2 seconds
- Database Query Response: <100ms
- File Upload Speed: Depends on size
- Page Load Times: <1 second
- Search Autocomplete: <200ms

**Security Features:**
- HTTPS connections (show in browser)
- Role-based access control
- Session management
- File upload validation
- SQL injection protection

**Integration Points:**
- PostgreSQL database connectivity
- ONNX Runtime model loading
- File system integration
- AJAX API endpoints
- Real-time form validation

### **Quality Standards:**
**Video Quality:**
- 1080p HD recording
- Smooth transitions between scenes
- Clear text and interface elements
- Professional color correction
- Consistent lighting and contrast

**Audio Quality:**
- Clear narration without background noise
- Professional microphone setup
- Consistent volume levels
- No echo or distortion
- Proper pacing and articulation

**Technical Accuracy:**
- All demonstrated features must work
- Real data processing
- Actual database operations
- Genuine file uploads and analysis
- Authentic user interactions

### **Post-Production Requirements:**
**Editing Standards:**
- Clean cuts between scenes
- Smooth transitions
- Professional title screens
- Consistent branding throughout
- Optimized file compression

**Delivery Formats:**
- Primary: MP4 (H.264, 1080p)
- Web-optimized: MP4 (smaller size)
- Backup: MOV format
- Mobile-optimized: 720p version

**Distribution Preparation:**
- YouTube-ready with metadata
- Vimeo professional version
- Embedded player for website
- Social media preview clips
- Presentation-ready format

---

## **Mouse Movement & Timing Guidelines**

### **General Mouse Behavior:**
- **Cursor Speed:** Medium-slow, deliberate movements (not too fast for viewers to follow)
- **Hover Duration:** 1-2 seconds on interactive elements before clicking
- **Click Animation:** Brief pause (0.5s) after each click to show the action
- **Smooth Transitions:** Use curved mouse paths, not straight lines
- **Visual Feedback:** Always show hover states before clicking

### **Specific Movement Patterns:**

**Login Sequence (0:00-0:30):**
- Start cursor at top-left of screen
- Move diagonally down to address bar (2 seconds)
- After page loads, move to username field (curved path, 1.5 seconds)
- Move vertically down to password field (1 second)
- Move to "Remember Me" checkbox (slight curve, 1 second)
- Move to login button with 2-second hover before click

**Dashboard Navigation (0:30-1:15):**
- Cursor starts from login button position
- Move to welcome header with smooth arc (2 seconds)
- Move across statistics cards in left-to-right pattern (3 seconds)
- Scroll gesture with mouse wheel (visible scroll animation)
- Move to sidebar toggle button (diagonal movement, 1.5 seconds)
- Return to main content area for schedule widget

**Form Interactions (Throughout):**
- Always approach form fields from the left side
- Hover over field for 0.5 seconds before clicking
- After typing, brief pause (0.5s) before moving to next field
- Use tab key occasionally instead of mouse clicks
- Show dropdown interactions with deliberate selection

### **Advanced Interaction Timing:**

**File Upload Demonstrations:**
- Approach drag zone slowly (2 seconds)
- Pause at edge of drop zone (0.5 seconds)
- Drop with visible feedback animation
- Move cursor away to show upload progress

**Search and Autocomplete:**
- Type at moderate speed (2-3 characters per second)
- Pause for autocomplete to appear (0.5 seconds)
- Move cursor to selection with precision
- Click with brief highlight of selected option

**Button and Link Interactions:**
- Approach from natural direction (usually left or top)
- Show hover state change (color/shadow effects)
- Click with slight press-and-release animation
- Move cursor away to show post-click state

### **Screen Recording Settings:**
- **Cursor Highlighting:** Use cursor spotlight effect during complex interactions
- **Click Animation:** Enable click ripple effects in recording software
- **Keyboard Shortcuts:** Show Ctrl+S, Ctrl+Z, Tab key usage occasionally
- **Zoom Effects:** 110% zoom on important form fields or results
- **Smooth Scrolling:** Enable smooth scroll in browser for better visual flow

---

## **Free Video Creation Tools & Software**

### **🎥 Screen Recording Software (100% Free)**

#### **1. OBS Studio (Recommended)**
- **Platform:** Windows, Mac, Linux
- **Cost:** Completely free, open source
- **Features:**
  - Professional-grade screen recording
  - Multiple scene compositions
  - Real-time audio/video mixing
  - Custom overlays and transitions
  - Mouse cursor highlighting
  - Click animation effects
- **Perfect for:** Complete video production workflow
- **Download:** https://obsproject.com/

#### **2. ShareX**
- **Platform:** Windows only
- **Cost:** Free, open source
- **Features:**
  - Screen recording with audio
  - Built-in video editor
  - Automatic cursor highlighting
  - Region selection recording
  - GIF creation
- **Download:** https://getsharex.com/

#### **3. CamStudio**
- **Platform:** Windows
- **Cost:** Free
- **Features:**
  - Simple screen recording
  - AVI/SWF output formats
  - Audio recording
- **Download:** http://camstudio.org/

#### **4. SimpleScreenRecorder**
- **Platform:** Linux
- **Cost:** Free
- **Features:**
  - High-quality screen recording
  - Live preview
  - Hardware acceleration
- **Available:** Through Linux package managers

### **🎬 Video Editing Software (Free)**

#### **1. DaVinci Resolve (Hollywood-grade, Free)**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free version (professional features)
- **Features:**
  - Professional color correction
  - Advanced audio editing
  - Motion graphics
  - Multi-timeline editing
  - 4K export support
- **Perfect for:** Professional-quality final product
- **Download:** https://www.blackmagicdesign.com/products/davinciresolve

#### **2. OpenShot**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free, open source
- **Features:**
  - Easy drag-and-drop interface
  - Transitions and effects
  - Title templates
  - Audio waveform display
- **Download:** https://www.openshot.org/

#### **3. Shotcut**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free, open source
- **Features:**
  - Wide format support
  - Professional filters
  - Color correction
  - Audio editing
- **Download:** https://shotcut.org/

#### **4. VSDC Free Video Editor**
- **Platform:** Windows
- **Cost:** Free version available
- **Features:**
  - Non-linear editing
  - Color correction
  - Visual effects
  - Audio editing
- **Download:** http://www.videosoftdev.com/

### **🎙️ Audio Recording & Editing (Free)**

#### **1. Audacity**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free, open source
- **Features:**
  - Multi-track audio editing
  - Noise reduction
  - Voice enhancement
  - Multiple export formats
- **Download:** https://www.audacityteam.org/

#### **2. Reaper (60-day free trial)**
- **Platform:** Windows, Mac, Linux
- **Cost:** 60-day full trial, then $60 license
- **Features:** Professional audio production

### **🎨 Graphics & Visual Assets (Free)**

#### **1. GIMP**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free
- **Purpose:** Logo creation, image editing
- **Download:** https://www.gimp.org/

#### **2. Canva (Free tier)**
- **Platform:** Web-based
- **Cost:** Free with limitations
- **Purpose:** Title slides, overlays, contact screens
- **Features:** Medical-themed templates

#### **3. Unsplash**
- **Platform:** Web
- **Cost:** Free
- **Purpose:** High-quality stock photos
- **Website:** https://unsplash.com/

### **📱 Voice Recording (Free)**

#### **1. Smartphone Apps:**
- **iOS:** Voice Memos (built-in)
- **Android:** Google Recorder, Easy Voice Recorder
- **Windows:** Windows Voice Recorder

#### **2. Online Voice Recorders:**
- **Vocaroo:** https://vocaroo.com/ (no registration)
- **Online Voice Recorder:** https://online-voice-recorder.com/

---

## **Step-by-Step Video Creation Workflow (Free Tools)**

### **Phase 1: Preparation**
1. **Install OBS Studio** for screen recording
2. **Install DaVinci Resolve** for editing
3. **Install Audacity** for audio processing
4. **Prepare sample data** in HeartLine application
5. **Create title slides** using Canva or GIMP

### **Phase 2: Screen Recording with OBS Studio**

#### **OBS Setup for HeartLine Demo:**
```
Scene Configuration:
1. Display Capture: Full screen (1920x1080)
2. Audio Input: Microphone for voice-over
3. Audio Output: System sounds (for click sounds)

Recording Settings:
- Format: MP4
- Encoder: x264
- Quality: High Quality, Medium File Size
- FPS: 30
- Resolution: 1920x1080
```

#### **Recording Checklist:**
- [ ] Close all unnecessary applications
- [ ] Disable notifications (Windows: Focus Assist, Mac: Do Not Disturb)
- [ ] Set browser to full screen
- [ ] Test microphone levels
- [ ] Record a 10-second test clip
- [ ] Check cursor visibility settings

### **Phase 3: Audio Recording Strategy**

#### **Option A: Live Recording (Simultaneous)**
- Record voice-over while doing screen capture
- More natural timing
- Single-take efficiency
- Requires good microphone discipline

#### **Option B: Post-Production (Recommended)**
- Record screen actions first (silent)
- Record voice-over separately using Audacity
- Better audio quality control
- Easier to edit and refine

#### **Professional Audio Tips:**
```
Microphone Setup:
- Use quiet room (carpet, curtains help)
- Position microphone 6-8 inches from mouth
- Use headphones to monitor recording
- Record in WAV format for best quality

Audacity Settings:
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit minimum, 24-bit preferred
- Mono for voice-over (saves space)
```

### **Phase 4: Video Editing in DaVinci Resolve**

#### **Project Setup:**
1. **Create New Project:** "HeartLine_Demo_Video"
2. **Timeline Settings:** 1920x1080, 30fps
3. **Import Media:** Screen recordings, audio files, graphics

#### **Editing Workflow:**
```
Timeline Structure:
Track 1 (Video): Screen recordings
Track 2 (Video): Title overlays, graphics
Track 3 (Audio): Voice-over narration
Track 4 (Audio): System sounds, music

Edit Sequence:
1. Rough cut - arrange clips in order
2. Audio sync - align voice-over with actions
3. Transitions - add smooth cuts between scenes
4. Graphics - add titles, contact info, logo
5. Color correction - ensure consistent look
6. Audio mixing - balance levels, add music
7. Final review - check timing and quality
```

#### **Essential Keyboard Shortcuts (DaVinci Resolve):**
- **Space:** Play/Pause
- **I/O:** Set In/Out points
- **B:** Blade tool (cut clips)
- **A:** Arrow tool (select)
- **Ctrl+Z:** Undo
- **Ctrl+S:** Save project

### **Phase 5: Export & Distribution**

#### **Export Settings (DaVinci Resolve):**
```
Format: MP4
Codec: H.264
Resolution: 1920x1080
Frame Rate: 30fps
Bitrate: 10 Mbps (high quality)
Audio: AAC, 48kHz, 256 kbps

Quality Presets:
- YouTube: Use "YouTube" preset
- Vimeo: Use "Vimeo" preset
- Web: Custom with lower bitrate (5 Mbps)
```

---

## **Mouse Movement & Timing Guidelines**

### **General Mouse Behavior:**
- **Cursor Speed:** Medium-slow, deliberate movements (not too fast for viewers to follow)
- **Hover Duration:** 1-2 seconds on interactive elements before clicking
- **Click Animation:** Brief pause (0.5s) after each click to show the action
- **Smooth Transitions:** Use curved mouse paths, not straight lines
- **Visual Feedback:** Always show hover states before clicking

### **Specific Movement Patterns:**

**Login Sequence (0:00-0:30):**
- Start cursor at top-left of screen
- Move diagonally down to address bar (2 seconds)
- After page loads, move to username field (curved path, 1.5 seconds)
- Move vertically down to password field (1 second)
- Move to "Remember Me" checkbox (slight curve, 1 second)
- Move to login button with 2-second hover before click

**Dashboard Navigation (0:30-1:15):**
- Cursor starts from login button position
- Move to welcome header with smooth arc (2 seconds)
- Move across statistics cards in left-to-right pattern (3 seconds)
- Scroll gesture with mouse wheel (visible scroll animation)
- Move to sidebar toggle button (diagonal movement, 1.5 seconds)
- Return to main content area for schedule widget

**Form Interactions (Throughout):**
- Always approach form fields from the left side
- Hover over field for 0.5 seconds before clicking
- After typing, brief pause (0.5s) before moving to next field
- Use tab key occasionally instead of mouse clicks
- Show dropdown interactions with deliberate selection

### **Advanced Interaction Timing:**

**File Upload Demonstrations:**
- Approach drag zone slowly (2 seconds)
- Pause at edge of drop zone (0.5 seconds)
- Drop with visible feedback animation
- Move cursor away to show upload progress

**Search and Autocomplete:**
- Type at moderate speed (2-3 characters per second)
- Pause for autocomplete to appear (0.5 seconds)
- Move cursor to selection with precision
- Click with brief highlight of selected option

**Button and Link Interactions:**
- Approach from natural direction (usually left or top)
- Show hover state change (color/shadow effects)
- Click with slight press-and-release animation
- Move cursor away to show post-click state

### **Screen Recording Settings:**
- **Cursor Highlighting:** Use cursor spotlight effect during complex interactions
- **Click Animation:** Enable click ripple effects in recording software
- **Keyboard Shortcuts:** Show Ctrl+S, Ctrl+Z, Tab key usage occasionally
- **Zoom Effects:** 110% zoom on important form fields or results
- **Smooth Scrolling:** Enable smooth scroll in browser for better visual flow

---

## **Free Video Creation Tools & Software**

### **🎥 Screen Recording Software (100% Free)**

#### **1. OBS Studio (Recommended)**
- **Platform:** Windows, Mac, Linux
- **Cost:** Completely free, open source
- **Features:**
  - Professional-grade screen recording
  - Multiple scene compositions
  - Real-time audio/video mixing
  - Custom overlays and transitions
  - Mouse cursor highlighting
  - Click animation effects
- **Perfect for:** Complete video production workflow
- **Download:** https://obsproject.com/

#### **2. ShareX**
- **Platform:** Windows only
- **Cost:** Free, open source
- **Features:**
  - Screen recording with audio
  - Built-in video editor
  - Automatic cursor highlighting
  - Region selection recording
  - GIF creation
- **Download:** https://getsharex.com/

#### **3. CamStudio**
- **Platform:** Windows
- **Cost:** Free
- **Features:**
  - Simple screen recording
  - AVI/SWF output formats
  - Audio recording
- **Download:** http://camstudio.org/

#### **4. SimpleScreenRecorder**
- **Platform:** Linux
- **Cost:** Free
- **Features:**
  - High-quality screen recording
  - Live preview
  - Hardware acceleration
- **Available:** Through Linux package managers

### **🎬 Video Editing Software (Free)**

#### **1. DaVinci Resolve (Hollywood-grade, Free)**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free version (professional features)
- **Features:**
  - Professional color correction
  - Advanced audio editing
  - Motion graphics
  - Multi-timeline editing
  - 4K export support
- **Perfect for:** Professional-quality final product
- **Download:** https://www.blackmagicdesign.com/products/davinciresolve

#### **2. OpenShot**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free, open source
- **Features:**
  - Easy drag-and-drop interface
  - Transitions and effects
  - Title templates
  - Audio waveform display
- **Download:** https://www.openshot.org/

#### **3. Shotcut**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free, open source
- **Features:**
  - Wide format support
  - Professional filters
  - Color correction
  - Audio editing
- **Download:** https://shotcut.org/

#### **4. VSDC Free Video Editor**
- **Platform:** Windows
- **Cost:** Free version available
- **Features:**
  - Non-linear editing
  - Color correction
  - Visual effects
  - Audio editing
- **Download:** http://www.videosoftdev.com/

### **🎙️ Audio Recording & Editing (Free)**

#### **1. Audacity**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free, open source
- **Features:**
  - Multi-track audio editing
  - Noise reduction
  - Voice enhancement
  - Multiple export formats
- **Download:** https://www.audacityteam.org/

#### **2. Reaper (60-day free trial)**
- **Platform:** Windows, Mac, Linux
- **Cost:** 60-day full trial, then $60 license
- **Features:** Professional audio production

### **🎨 Graphics & Visual Assets (Free)**

#### **1. GIMP**
- **Platform:** Windows, Mac, Linux
- **Cost:** Free
- **Purpose:** Logo creation, image editing
- **Download:** https://www.gimp.org/

#### **2. Canva (Free tier)**
- **Platform:** Web-based
- **Cost:** Free with limitations
- **Purpose:** Title slides, overlays, contact screens
- **Features:** Medical-themed templates

#### **3. Unsplash**
- **Platform:** Web
- **Cost:** Free
- **Purpose:** High-quality stock photos
- **Website:** https://unsplash.com/

### **📱 Voice Recording (Free)**

#### **1. Smartphone Apps:**
- **iOS:** Voice Memos (built-in)
- **Android:** Google Recorder, Easy Voice Recorder
- **Windows:** Windows Voice Recorder

#### **2. Online Voice Recorders:**
- **Vocaroo:** https://vocaroo.com/ (no registration)
- **Online Voice Recorder:** https://online-voice-recorder.com/

---

## **Step-by-Step Video Creation Workflow (Free Tools)**

### **Phase 1: Preparation**
1. **Install OBS Studio** for screen recording
2. **Install DaVinci Resolve** for editing
3. **Install Audacity** for audio processing
4. **Prepare sample data** in HeartLine application
5. **Create title slides** using Canva or GIMP

### **Phase 2: Screen Recording with OBS Studio**

#### **OBS Setup for HeartLine Demo:**
```
Scene Configuration:
1. Display Capture: Full screen (1920x1080)
2. Audio Input: Microphone for voice-over
3. Audio Output: System sounds (for click sounds)

Recording Settings:
- Format: MP4
- Encoder: x264
- Quality: High Quality, Medium File Size
- FPS: 30
- Resolution: 1920x1080
```

#### **Recording Checklist:**
- [ ] Close all unnecessary applications
- [ ] Disable notifications (Windows: Focus Assist, Mac: Do Not Disturb)
- [ ] Set browser to full screen
- [ ] Test microphone levels
- [ ] Record a 10-second test clip
- [ ] Check cursor visibility settings

### **Phase 3: Audio Recording Strategy**

#### **Option A: Live Recording (Simultaneous)**
- Record voice-over while doing screen capture
- More natural timing
- Single-take efficiency
- Requires good microphone discipline

#### **Option B: Post-Production (Recommended)**
- Record screen actions first (silent)
- Record voice-over separately using Audacity
- Better audio quality control
- Easier to edit and refine

#### **Professional Audio Tips:**
```
Microphone Setup:
- Use quiet room (carpet, curtains help)
- Position microphone 6-8 inches from mouth
- Use headphones to monitor recording
- Record in WAV format for best quality

Audacity Settings:
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit minimum, 24-bit preferred
- Mono for voice-over (saves space)
```

### **Phase 4: Video Editing in DaVinci Resolve**

#### **Project Setup:**
1. **Create New Project:** "HeartLine_Demo_Video"
2. **Timeline Settings:** 1920x1080, 30fps
3. **Import Media:** Screen recordings, audio files, graphics

#### **Editing Workflow:**
```
Timeline Structure:
Track 1 (Video): Screen recordings
Track 2 (Video): Title overlays, graphics
Track 3 (Audio): Voice-over narration
Track 4 (Audio): System sounds, music

Edit Sequence:
1. Rough cut - arrange clips in order
2. Audio sync - align voice-over with actions
3. Transitions - add smooth cuts between scenes
4. Graphics - add titles, contact info, logo
5. Color correction - ensure consistent look
6. Audio mixing - balance levels, add music
7. Final review - check timing and quality
```

#### **Essential Keyboard Shortcuts (DaVinci Resolve):**
- **Space:** Play/Pause
- **I/O:** Set In/Out points
- **B:** Blade tool (cut clips)
- **A:** Arrow tool (select)
- **Ctrl+Z:** Undo
- **Ctrl+S:** Save project

### **Phase 5: Export & Distribution**

#### **Export Settings (DaVinci Resolve):**
```
Format: MP4
Codec: H.264
Resolution: 1920x1080
Frame Rate: 30fps
Bitrate: 10 Mbps (high quality)
Audio: AAC, 48kHz, 256 kbps

Quality Presets:
- YouTube: Use "YouTube" preset
- Vimeo: Use "Vimeo" preset
- Web: Custom with lower bitrate (5 Mbps)
```

---

## **🚀 Quick Professional Video Solutions (12-Hour Deadline)**

### **AI-Powered Video Creation Tools (No Experience Needed)**

#### **1. Synthesia (AI Avatar + Screen Recording)**
- **Platform:** Web-based
- **Cost:** Free trial (10 minutes), then paid plans
- **Perfect for:** Professional presenter + screen demo combination
- **Features:**
  - AI avatar narration (multiple languages including Arabic/French)
  - Screen recording integration
  - Professional backgrounds
  - No voice recording needed
- **Time to create:** 2-3 hours
- **Website:** https://www.synthesia.io/

#### **2. Loom (Screen Recording + AI Enhancement)**
- **Platform:** Web-based + Desktop app
- **Cost:** Free tier (5 minutes), paid for longer videos
- **Features:**
  - One-click screen recording
  - Automatic transcription
  - AI-powered editing suggestions
  - Professional templates
  - Instant sharing
- **Time to create:** 1-2 hours
- **Website:** https://www.loom.com/

#### **3. Riverside.fm (AI Video Editor)**
- **Platform:** Web-based
- **Cost:** Free trial, then subscription
- **Features:**
  - AI-powered video editing
  - Automatic scene detection
  - Professional transitions
  - Real-time collaboration
- **Time to create:** 2-3 hours
- **Website:** https://riverside.fm/

### **Interactive Demo Creation Tools**

#### **1. Storylane (Interactive Product Demos)**
- **Platform:** Web-based
- **Cost:** Free trial, then paid
- **Perfect for:** Interactive software demonstrations
- **Features:**
  - Click-through demos
  - Hotspot interactions
  - Professional templates
  - Analytics tracking
- **Time to create:** 3-4 hours
- **Website:** https://www.storylane.io/

#### **2. Arcade (Interactive Screen Recordings)**
- **Platform:** Web-based
- **Cost:** Free tier available
- **Features:**
  - Interactive screen captures
  - Click-through functionality
  - Professional styling
  - Easy embedding
- **Time to create:** 2-3 hours
- **Website:** https://www.arcade.software/

#### **3. Supademo (Quick Interactive Demos)**
- **Platform:** Web-based
- **Cost:** Free tier available
- **Features:**
  - Auto-generated interactive demos
  - Professional animations
  - No video editing required
- **Time to create:** 1-2 hours
- **Website:** https://supademo.com/

### **🎯 Recommended Fast Track Solution for HeartLine**

#### **Option A: Loom + CapCut (Fastest - 3 hours total)**

**Step 1: Record with Loom (30 minutes)**
```
Setup:
1. Sign up for Loom (free trial)
2. Install browser extension
3. Start screen recording
4. Follow your guide script while recording
5. Loom automatically adds professional touches

Benefits:
- Automatic cursor highlighting
- Clean audio processing
- Instant cloud upload
- Professional quality without setup
```

**Step 2: Enhance in CapCut (2 hours)**
```
CapCut Enhancements:
1. Import Loom video
2. Add professional titles (use templates)
3. Add background music (built-in library)
4. Apply smooth transitions between sections
5. Add contact info overlay at end
6. Export in 1080p

CapCut Templates to Use:
- "Corporate Presentation"
- "Tech Demo"
- "Business Showcase"
```

#### **Option B: Synthesia + Screen Recording (4 hours total)**

**Perfect for professional avatar presentation:**
```
Step 1: Create AI Avatar Introduction (1 hour)
- Professional AI presenter introduces HeartLine
- Explains key benefits and features
- Multiple language options available

Step 2: Screen Recording (1 hour)
- Record silent HeartLine demo following your guide
- Focus on smooth mouse movements and actions

Step 3: Combine in CapCut (2 hours)
- Merge avatar intro with screen demo
- Add transitions and professional graphics
- Export final video
```

#### **Option C: Interactive Demo with Arcade (3 hours total)**

**For interactive presentations:**
```
Perfect for:
- Investor meetings
- Live demonstrations
- Self-guided product tours

Process:
1. Record HeartLine workflow with Arcade
2. Add interactive hotspots and explanations
3. Create click-through experience
4. Embed on website or present live

Benefits:
- Viewers can interact with actual workflow
- Professional animations included
- No video editing skills needed
```

### **⚡ Emergency 6-Hour Solution (Minimal Experience)**

#### **Ultra-Fast Professional Video Creation:**

**Tools Needed:**
- Loom (free trial)
- CapCut (free mobile/desktop app)
- Canva (free account)

**Timeline:**
```
Hour 1: Preparation
- Set up Loom account
- Prepare HeartLine application with sample data
- Create title slide in Canva

Hour 2-3: Recording
- Record complete HeartLine demo with Loom
- One-take recording following your script
- Loom handles audio/video quality automatically

Hour 4-5: Editing in CapCut
- Import Loom video
- Add title slide at beginning
- Insert professional transitions between sections
- Add background music from CapCut library
- Create contact information slide

Hour 6: Final Polish
- Review and trim any issues
- Export in 1080p
- Upload to preferred platform
```

### **🎯 No-Code Interactive Demo (2 hours)**

#### **Using Supademo (Simplest Option):**
```
Process:
1. Navigate through HeartLine application
2. Supademo automatically captures your workflow
3. AI generates interactive hotspots
4. Add text explanations for each step
5. Publish interactive demo

Result:
- Professional interactive presentation
- No video editing required
- Works on any device
- Trackable analytics
```

### **📱 Mobile-First Quick Solution**

#### **CapCut Mobile App (Phone Recording):**
```
If time is extremely limited:
1. Use phone to record computer screen
2. Add professional CapCut mobile templates
3. Use built-in AI features for enhancement
4. Export and share immediately

Benefits:
- Familiar mobile interface
- AI-powered editing suggestions
- Professional templates included
- Fast export and sharing
```

---

## **Decision Matrix for Your Situation**

| Solution | Time | Experience Needed | Professional Quality | Cost |
|----------|------|-------------------|---------------------|------|
| Loom + CapCut | 3 hours | Minimal | High | Free trial |
| Synthesia + CapCut | 4 hours | Minimal | Very High | $30 trial |
| Interactive Arcade | 3 hours | None | High | Free tier |
| Supademo | 2 hours | None | Medium-High | Free tier |
| CapCut Only | 4 hours | Basic | Medium | Free |
| Emergency Mobile | 2 hours | Minimal | Medium | Free |

### **🏆 Recommended for Your Deadline: Loom + CapCut**

**Why this combination works best:**
- ✅ **Fastest professional result** (3 hours total)
- ✅ **Builds on your CapCut experience**
- ✅ **No new software learning curve**
- ✅ **Professional quality guaranteed**
- ✅ **Free trial covers your needs**
- ✅ **One-click recording with Loom**
- ✅ **Professional enhancement in familiar CapCut**

**Quick Start Instructions:**
1. **Sign up for Loom** (5 minutes)
2. **Install browser extension** (2 minutes)
3. **Start recording + follow your script** (45 minutes)
4. **Download video from Loom** (5 minutes)
5. **Import to CapCut + apply professional template** (1 hour)
6. **Add music, transitions, title/end slides** (1 hour)
7. **Export and review** (30 minutes)

**Total: 3 hours 27 minutes for professional result**

---

This technical video guide is based on the actual HeartLine codebase implementation, ensuring every demonstrated feature accurately reflects the real system capabilities, user interface elements, and technical architecture. The guide emphasizes the genuine clinical workflow, AI integration, and comprehensive practice management features that distinguish HeartLine in the Algerian healthcare market.

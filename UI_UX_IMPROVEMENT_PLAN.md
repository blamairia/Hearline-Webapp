# UI/UX Improvement Plan: "Gold Standard" Refactor

## Objective
Standardize the entire application's UI to use a consistent, modern, and professional design system based on Bootstrap 5. Eliminate inline styles, legacy CSS, and inconsistent layouts. Ensure all pages follow the `.page-container` > `.page-header` > `.card` hierarchy.

## Design Standards
- **Layout**: All main content wrapped in `.page-container`.
- **Headers**: Use `.page-header` with `.page-title` (icon + text) and `.page-actions` (buttons).
- **Cards**: Use standard Bootstrap `.card` with `.card-header` and `.card-body`.
- **Tables**: Use `.table .table-hover .align-middle`.
- **Forms**: Use standard `.form-label`, `.form-control`, `.form-select`.
- **Icons**: FontAwesome 5 (`fas fa-*`).
- **Colors**: Use semantic variables (`var(--primary)`, `var(--success)`, etc.) or Bootstrap utility classes (`text-primary`, `bg-light`).

## Progress Tracker

### ✅ Completed (Refactored & Standardized)
- **Dashboards**
    - `templates/dashboard/doctor_dashboard.html`
    - `templates/dashboard/assistant_dashboard.html`
- **Patient Module**
    - `templates/forms/patient_form.html`
    - `templates/tables/patients_table.html`
    - `templates/patient_details.html`
- **Visit Module**
    - `templates/forms/visit_form.html`
    - `templates/forms/visit_edit_form.html`
    - `templates/tables/visits_table.html`
    - `templates/visit_details.html`
- **Appointment Module**
    - `templates/forms/appointment_form.html`
    - `templates/tables/appointments_table.html`
- **ECG Module**
    - `templates/tables/ecg_history_table.html`
- **Authentication & User Management**
    - `templates/auth/register.html`
    - `templates/auth/login.html`
    - `templates/auth/user_management.html`
    - `templates/auth/profile.html`
    - `templates/auth/edit_profile.html`
    - `templates/auth/change_password.html`
- **Settings**
    - `templates/pages/settings.html`
- **Cleanup**
    - Deleted `templates/tables/appointments_table_new.html` (Legacy)
    - Deleted `templates/index.html` (Unused)

### 🚧 In Progress / To Do
- **Print Views**
    - [ ] `templates/print/visit_print.html` (Review for print styling consistency)
- **Root Templates**
    - [ ] `templates/base.html` (Final review of global structure)

## Detailed Change Log

### Recent Updates (Session: Dec 4, 2025)
1.  **`ecg_history_table.html`**: Converted to standard table layout. Added `.stats-grid` for metrics. Removed inline gradients.
2.  **`register.html`**: Standardized form layout. Wrapped in `.page-container`. Added proper header.
3.  **`user_management.html`**: Refactored table. Added stats cards. Removed custom `<style>` block for badges/avatars and used Bootstrap utilities.
4.  **`profile.html`**: Redesigned into a 2-column layout (Profile Card + Activity Card). Standardized badges and icons.
5.  **`edit_profile.html`**: Cleaned up form structure. Added "Current Info" side card.
6.  **`change_password.html`**: Standardized form layout. Added security tips section.
7.  **`settings.html`**: Converted to vertical tab layout. Standardized form inputs and headers.
8.  **`login.html`**: Refactored to remove custom "glassmorphism" CSS and use standard Bootstrap 5 card layout.
9.  **`patient_details.html`**: Polished badge classes (`bg-*`) and standardized avatar styling.
10. **`visit_details.html`**: Polished badge classes (`bg-*`) and standardized avatar styling.
11. **`index.html`**: Deleted unused file.

## Next Steps
1.  Review `templates/print/visit_print.html`.
2.  Final review of `templates/base.html`.

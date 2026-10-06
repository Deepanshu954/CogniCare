export type UserRole = "ELDERLY" | "CAREGIVER" | "REVIEWER" | "ADMIN";

export interface Profile {
  id: string;
  display_name: string;
  phone_number?: string;
  preferred_language: string;
  timezone: string;
  avatar_url?: string;
}

export interface PatientProfileSummary {
  id: string;
  emergency_notes?: string;
  accessibility_preferences: Record<string, any>;
  care_preferences: Record<string, any>;
}

export interface User {
  id: string;
  email: string;
  role: UserRole;
  status: string;
  profile?: Profile;
  patient_profile?: PatientProfileSummary;
  created_at: string;
}

export interface EmergencyContact {
  id: string;
  name: string;
  relationship_type: string;
  phone: string;
  email?: string;
  priority: number;
  is_active: boolean;
}

export interface Consent {
  id: string;
  purpose: string;
  policy_version: string;
  granted: boolean;
  granted_at: string;
  revoked_at?: string;
}

export interface CaregiverLink {
  id: string;
  caregiver_user_id: string;
  caregiver_email?: string;
  caregiver_name?: string;
  relationship_type: string;
  permissions: string[];
  status: string;
  created_at: string;
}

export interface PatientDetail {
  id: string;
  user_id: string;
  display_name: string;
  email: string;
  phone_number?: string;
  emergency_notes?: string;
  accessibility_preferences: Record<string, any>;
  care_preferences: Record<string, any>;
  emergency_contacts: EmergencyContact[];
  consents: Consent[];
  caregivers: CaregiverLink[];
  created_at: string;
}

export interface PatientSummary {
  id: string;
  display_name: string;
  total_medications: number;
  today_reminders_count: number;
  today_completed_reminders: number;
  adherence_percentage: number;
  open_alerts_count: number;
  status: "EXCELLENT" | "ATTENTION_NEEDED" | "CRITICAL_ALERT";
}

export interface MedicationSchedule {
  id: string;
  schedule_type: string;
  time_of_day: string;
  days_of_week: string[];
  criticality: "NORMAL" | "HIGH" | "CRITICAL";
  active: boolean;
}

export interface Medication {
  id: string;
  patient_id: string;
  name: string;
  dosage_text: string;
  instructions?: string;
  active: boolean;
  start_date?: string;
  end_date?: string;
  schedules: MedicationSchedule[];
  created_at: string;
}

export interface Routine {
  id: string;
  patient_id: string;
  routine_type: string;
  title: string;
  description?: string;
  scheduled_time: string;
  recurrence_pattern: string;
  active: boolean;
  created_at: string;
}

export interface Reminder {
  id: string;
  patient_id: string;
  source_type: string;
  source_id?: string;
  title: string;
  description?: string;
  scheduled_for: string;
  status: "SCHEDULED" | "DELIVERED" | "ACKNOWLEDGED" | "SKIPPED" | "SNOOZED" | "MISSED" | "ESCALATED";
  priority: "LOW" | "NORMAL" | "HIGH" | "CRITICAL";
  snooze_until?: string;
  acknowledged_at?: string;
  created_at: string;
}

export interface CognitiveActivityVersion {
  id: string;
  version_number: number;
  difficulty: number;
  content_data: Record<string, any>;
  scoring_config: Record<string, any>;
}

export interface CognitiveActivity {
  id: string;
  activity_type: "MEMORY_RECALL" | "WORD_SEQUENCE" | "ATTENTION_STROOP" | "ORIENTATION_MATCH";
  title: string;
  category: string;
  description: string;
  is_active: boolean;
  current_version?: CognitiveActivityVersion;
}

export interface ActivitySession {
  id: string;
  patient_id: string;
  activity_id: string;
  activity_title?: string;
  status: "IN_PROGRESS" | "COMPLETED" | "ABANDONED";
  difficulty: number;
  total_score: number;
  accuracy_rate: number;
  avg_response_time_ms: number;
  started_at: string;
  completed_at?: string;
  answers_count: number;
  feedback_message?: string;
}

export interface CognitiveOverview {
  current_composite_score: number;
  baseline_score: number;
  total_sessions_completed: number;
  recent_accuracy_rate: number;
  recent_avg_latency_ms: number;
  trend_direction: "STABLE" | "IMPROVING" | "VARIABLE" | "DECLINING";
  category_scores: Record<string, number>;
}

export interface CognitiveTrendPoint {
  date: string;
  score: number;
  accuracy: number;
  avg_latency_ms: number;
  baseline_score: number;
}

export interface SupportSignal {
  id: string;
  signal_type: string;
  severity: "INFO" | "ATTENTION" | "CONCERN";
  description: string;
  evidence: Record<string, any>;
  status: string;
  created_at: string;
}

export interface AlertEvent {
  id: string;
  event_type: string;
  actor_id?: string;
  note?: string;
  created_at: string;
}

export interface Alert {
  id: string;
  patient_id: string;
  alert_type: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  status: "OPEN" | "ACKNOWLEDGED" | "ESCALATED" | "RESOLVED" | "FALSE_POSITIVE";
  summary: string;
  details: Record<string, any>;
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
  events: AlertEvent[];
}

export interface NotificationItem {
  id: string;
  title: string;
  body: string;
  channel: string;
  priority: string;
  read_at?: string;
  created_at: string;
}

export interface Report {
  id: string;
  patient_id: string;
  period_start: string;
  period_end: string;
  metrics_snapshot: Record<string, any>;
  ai_narrative_summary: string;
  status: string;
  created_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: "USER" | "ASSISTANT" | "SYSTEM";
  content: string;
  active_model?: string;
  thinking_trace?: string;
  tool_calls?: any;
  created_at: string;
}

export interface Conversation {
  id: string;
  patient_id: string;
  title: string;
  status: string;
  messages: Message[];
  created_at: string;
}

import { z } from 'zod'

// Authentication schemas
export const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  remember: z.boolean().optional()
})

export const registerSchema = z.object({
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one uppercase letter, one lowercase letter, and one number'),
  confirmPassword: z.string(),
  organization: z.string().optional(),
  position: z.string().optional(),
  phone: z.string().optional(),
  terms: z.boolean().refine(val => val === true, 'You must accept the terms and conditions')
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"]
})

export const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address')
})

export const resetPasswordSchema = z.object({
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one uppercase letter, one lowercase letter, and one number'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"]
})

// Contact form schema
export const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  phone: z.string().optional(),
  organization: z.string().optional(),
  subject: z.string().min(5, 'Subject must be at least 5 characters'),
  message: z.string().min(20, 'Message must be at least 20 characters'),
  type: z.enum(['GENERAL', 'DEMO_REQUEST', 'SALES', 'SUPPORT', 'PARTNERSHIP'])
})

// Newsletter subscription schema
export const newsletterSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  preferences: z.object({
    productUpdates: z.boolean().optional(),
    marketing: z.boolean().optional(),
    newsletter: z.boolean().optional()
  }).optional()
})

// User profile schema
export const profileSchema = z.object({
  firstName: z.string().min(2, 'First name must be at least 2 characters'),
  lastName: z.string().min(2, 'Last name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  phone: z.string().optional(),
  organization: z.string().optional(),
  position: z.string().optional(),
  city: z.string().optional(),
  wilaya: z.string().optional(),
  address: z.string().optional()
})

// Subscription schemas
export const subscriptionSchema = z.object({
  planId: z.string().min(1, 'Please select a plan'),
  billingCycle: z.enum(['MONTHLY', 'ANNUAL']),
  autoRenew: z.boolean().optional().default(true)
})

// Demo request schema
export const demoRequestSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  phone: z.string().min(10, 'Please enter a valid phone number'),
  organization: z.string().min(2, 'Organization name is required'),
  position: z.string().min(2, 'Position is required'),
  numberOfDoctors: z.number().min(1, 'Number of doctors must be at least 1'),
  patientsPerMonth: z.number().min(1, 'Expected patients per month is required'),
  currentSoftware: z.string().optional(),
  challenges: z.string().min(20, 'Please describe your current challenges'),
  preferredDate: z.string().optional(),
  preferredTime: z.string().optional(),
  message: z.string().optional()
})

// Type exports
export type LoginFormData = z.infer<typeof loginSchema>
export type RegisterFormData = z.infer<typeof registerSchema>
export type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>
export type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>
export type ContactFormData = z.infer<typeof contactSchema>
export type NewsletterFormData = z.infer<typeof newsletterSchema>
export type ProfileFormData = z.infer<typeof profileSchema>
export type SubscriptionFormData = z.infer<typeof subscriptionSchema>
export type DemoRequestFormData = z.infer<typeof demoRequestSchema>
